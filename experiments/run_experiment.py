"""Run Clean / Leaky / Audited pilot experiments."""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
import traceback
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

from config import DEFAULT_CASES_PATH, MODELS, RESULTS_DIR, ModelConfig
from finleakaudit import audit_prediction, temporal_availability_check
from prompts import SYSTEM_PROMPT, build_prediction_prompt


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    records = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def append_jsonl(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def completed_case_ids(path: Path) -> set[str]:
    """Return case IDs already present in a result file for resume support."""
    completed = set()
    for record in read_jsonl(path):
        case_id = record.get("case_id")
        if case_id:
            completed.add(case_id)
    return completed


def default_run_name(cases_path: Path) -> str:
    """Derive a stable run name from the cases file name."""
    stem = cases_path.stem
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", stem).strip("_") or "cases"


def extract_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`")
        text = text.removeprefix("json").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start : end + 1])
        raise


def call_chat(config: ModelConfig, user_prompt: str) -> dict:
    payload = {
        "model": config.model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
    }
    request = urllib.request.Request(
        f"{config.base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.api_key}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=config.timeout_seconds) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Model call failed: {exc}") from exc

    body = json.loads(raw)
    content = body["choices"][0]["message"]["content"]
    parsed = extract_json(content)
    parsed["_raw_content"] = content
    parsed["_usage"] = body.get("usage", {})
    return parsed


def normalize_prediction(output: dict) -> dict:
    prediction = str(output.get("prediction", "NEUTRAL")).upper()
    if prediction not in {"UP", "DOWN", "NEUTRAL"}:
        prediction = "NEUTRAL"
    try:
        confidence = float(output.get("confidence", 0.0))
    except (TypeError, ValueError):
        confidence = 0.0
    confidence = max(0.0, min(1.0, confidence))
    rationale = output.get("rationale")
    if not isinstance(rationale, list):
        rationale = []
    return {
        **output,
        "prediction": prediction,
        "confidence": confidence,
        "rationale": rationale,
    }


def shuffled(evidence: list[dict], seed: int) -> list[dict]:
    items = list(evidence)
    random.Random(seed).shuffle(items)
    return items


def insert_leaked_evidence(clean_evidence: list[dict], leaked_evidence: list[dict], seed: int) -> list[dict]:
    """Insert leaked evidence without changing clean evidence order."""
    result = list(clean_evidence)
    rng = random.Random(seed)
    for ev in shuffled(leaked_evidence, seed + 1000):
        result.insert(rng.randint(0, len(result)), ev)
    return result


def is_future_evidence(evidence: dict, case: dict) -> bool:
    prediction_cutoff = case.get("prediction_cutoff") or case.get("prediction_date")
    result = temporal_availability_check(
        [evidence],
        prediction_cutoff=prediction_cutoff,
    )[0]
    return result["temporal_status"] == "future_leakage"


def run_evidence_ablation(
    case: dict,
    model_config: ModelConfig,
    full_evidence: list[dict],
    full_prediction: dict,
) -> list[dict]:
    """Leave-one-evidence-out ablation against the leaky prediction."""
    ablations = []
    for removed in full_evidence:
        remaining = [ev for ev in full_evidence if ev["id"] != removed["id"]]
        prediction = normalize_prediction(
            call_chat(model_config, build_prediction_prompt(case, remaining))
        )
        direction_changed = prediction["prediction"] != full_prediction["prediction"]
        confidence_delta = prediction["confidence"] - full_prediction["confidence"]
        ablations.append(
            {
                "evidence_id": removed["id"],
                "time": removed.get("time"),
                "sentiment": removed.get("sentiment"),
                "is_future_leakage": is_future_evidence(removed, case),
                "full_prediction": full_prediction["prediction"],
                "full_confidence": full_prediction["confidence"],
                "removed_prediction": prediction["prediction"],
                "removed_confidence": prediction["confidence"],
                "direction_changed": direction_changed,
                "confidence_delta_removed_minus_full": confidence_delta,
                "abs_confidence_delta": abs(confidence_delta),
                "is_flip_driver": direction_changed,
                "remaining_evidence_order": [ev["id"] for ev in remaining],
                "prediction_output": prediction,
            }
        )
    return ablations


def summarize_ablation(ablation: list[dict]) -> dict:
    future_items = [item for item in ablation if item["is_future_leakage"]]
    flip_drivers = [item for item in ablation if item["is_flip_driver"]]
    future_flip_drivers = [
        item for item in future_items if item["is_flip_driver"]
    ]
    return {
        "ablation_items": len(ablation),
        "future_ablation_items": len(future_items),
        "ablation_flip_driver_count": len(flip_drivers),
        "future_ablation_flip_driver_count": len(future_flip_drivers),
        "has_future_flip_driver": bool(future_flip_drivers),
    }


def run_case(
    case: dict,
    model_config: ModelConfig,
    seed: int,
    with_ablation: bool = False,
) -> dict:
    clean_evidence = shuffled(case["clean_evidence"], seed)
    leaky_evidence = insert_leaked_evidence(
        clean_evidence,
        case["leaked_evidence"],
        seed + 2000,
    )

    clean = normalize_prediction(
        call_chat(model_config, build_prediction_prompt(case, clean_evidence))
    )
    leaky = normalize_prediction(
        call_chat(model_config, build_prediction_prompt(case, leaky_evidence))
    )
    audit = audit_prediction(case, leaky)
    # Revision must start from the evidence the leaky forecast actually saw.
    audited_evidence = [
        ev
        for ev in leaky_evidence
        if ev["id"] not in audit["removed_evidence_ids"]
    ]
    audited = normalize_prediction(
        call_chat(model_config, build_prediction_prompt(case, audited_evidence))
    )

    result = {
        "case_id": case["case_id"],
        "schema_version": case.get("schema_version"),
        "case_type": case.get("case_type"),
        "dataset_tier": case.get("dataset_tier"),
        "label": case.get("label"),
        "outcome_label": case.get("outcome_label") or case.get("label"),
        "prediction_date": case.get("prediction_date"),
        "outcome_time": case.get("outcome_time"),
        "cutoff_price": case.get("cutoff_price"),
        "outcome_price": case.get("outcome_price"),
        "outcome_return": case.get("outcome_return"),
        "model": model_config.name,
        "model_id": model_config.model,
        "seed": seed,
        "clean": clean,
        "leaky": leaky,
        "audit": audit,
        "audited_evidence_order": [ev["id"] for ev in audited_evidence],
        "audited": audited,
        "metrics": {
            "leaky_cited_future": audit["leakage_detected"],
            "prediction_flipped_clean_to_leaky": clean["prediction"]
            != leaky["prediction"],
            "audited_recovered_clean_direction": audited["prediction"]
            == clean["prediction"],
            "confidence_delta_leaky_minus_clean": leaky["confidence"]
            - clean["confidence"],
        },
    }
    if with_ablation:
        ablation = run_evidence_ablation(
            case,
            model_config,
            full_evidence=leaky_evidence,
            full_prediction=leaky,
        )
        result["ablation"] = ablation
        result["metrics"].update(summarize_ablation(ablation))
    return result


def run_case_with_retry(
    case: dict,
    model_config: ModelConfig,
    seed: int,
    retries: int,
    retry_delay: float,
    with_ablation: bool,
) -> tuple[Optional[dict], list[dict]]:
    """Run one case, retrying transient API and parsing failures."""
    errors = []
    total_attempts = retries + 1
    for attempt in range(1, total_attempts + 1):
        try:
            result = run_case(
                case,
                model_config,
                seed=seed,
                with_ablation=with_ablation,
            )
            result["attempt"] = attempt
            return result, errors
        except Exception as exc:  # noqa: BLE001 - record experiment failures.
            error = {
                "case_id": case.get("case_id"),
                "model": model_config.name,
                "attempt": attempt,
                "max_attempts": total_attempts,
                "error_type": type(exc).__name__,
                "error": str(exc),
                "traceback": traceback.format_exc(limit=3),
            }
            errors.append(error)
            if attempt < total_attempts:
                sleep_seconds = retry_delay * attempt
                print(
                    f"  attempt {attempt}/{total_attempts} failed: {exc}; "
                    f"retrying in {sleep_seconds:.1f}s",
                    flush=True,
                )
                time.sleep(sleep_seconds)
            else:
                print(
                    f"  failed after {total_attempts} attempts: {exc}",
                    flush=True,
                )
    return None, errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen", choices=sorted(MODELS))
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES_PATH)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--retry-delay", type=float, default=3.0)
    parser.add_argument(
        "--with-ablation",
        action="store_true",
        help="Run leave-one-evidence-out ablation for each case.",
    )
    parser.add_argument(
        "--run-name",
        default=None,
        help="Name used in result files. Defaults to the cases file stem.",
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--errors", type=Path, default=None)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)

    model_config = MODELS[args.model]
    cases = read_jsonl(args.cases)
    if args.limit is not None:
        cases = cases[: args.limit]

    run_name = args.run_name or default_run_name(args.cases)
    result_kind = "ablation_results" if args.with_ablation else "results"
    error_kind = "ablation_errors" if args.with_ablation else "errors"
    output_path = (
        args.output or RESULTS_DIR / f"{args.model}_{run_name}_{result_kind}.jsonl"
    )
    error_path = (
        args.errors or RESULTS_DIR / f"{args.model}_{run_name}_{error_kind}.jsonl"
    )
    if args.overwrite and output_path.exists():
        output_path.unlink()
    if args.overwrite and error_path.exists():
        error_path.unlink()

    print(f"results: {output_path}")
    print(f"errors:  {error_path}")

    completed = completed_case_ids(output_path)
    if completed:
        print(f"resume: found {len(completed)} completed case(s) in {output_path}")

    failures = 0
    skipped = 0
    for idx, case in enumerate(cases, start=1):
        if case["case_id"] in completed:
            skipped += 1
            print(
                f"[{idx}/{len(cases)}] skipping {case['case_id']} "
                f"(already completed)",
                flush=True,
            )
            continue

        started = time.time()
        print(f"[{idx}/{len(cases)}] running {case['case_id']} with {args.model}", flush=True)
        result, errors = run_case_with_retry(
            case,
            model_config,
            seed=args.seed + idx,
            retries=args.retries,
            retry_delay=args.retry_delay,
            with_ablation=args.with_ablation,
        )
        for error in errors:
            error["elapsed_seconds"] = round(time.time() - started, 3)
            append_jsonl(error_path, error)

        if result is None:
            failures += 1
            continue

        result["elapsed_seconds"] = round(time.time() - started, 3)
        append_jsonl(output_path, result)
        print(
            "  clean={clean} leaky={leaky} audited={audited} leakage={leakage}".format(
                clean=result["clean"]["prediction"],
                leaky=result["leaky"]["prediction"],
                audited=result["audited"]["prediction"],
                leakage=result["metrics"]["leaky_cited_future"],
            ),
            flush=True,
        )

    print(
        f"wrote {output_path}; errors={failures}; skipped={skipped}; "
        f"error_log={error_path if error_path.exists() else 'none'}"
    )
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

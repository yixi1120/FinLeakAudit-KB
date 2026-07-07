"""Run Clean / Leaky / Audited pilot experiments."""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from config import DEFAULT_CASES_PATH, MODELS, RESULTS_DIR, ModelConfig
from finleakaudit import audit_prediction
from prompts import SYSTEM_PROMPT, build_prediction_prompt


def read_jsonl(path: Path) -> list[dict]:
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


def run_case(case: dict, model_config: ModelConfig, seed: int) -> dict:
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
    audited_evidence = [
        ev for ev in clean_evidence if ev["id"] not in audit["removed_evidence_ids"]
    ]
    audited = normalize_prediction(
        call_chat(model_config, build_prediction_prompt(case, audited_evidence))
    )

    return {
        "case_id": case["case_id"],
        "case_type": case.get("case_type"),
        "label": case.get("label"),
        "model": model_config.name,
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


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen", choices=sorted(MODELS))
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES_PATH)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args(argv)

    model_config = MODELS[args.model]
    cases = read_jsonl(args.cases)
    if args.limit is not None:
        cases = cases[: args.limit]

    output_path = RESULTS_DIR / f"{args.model}_pilot_results.jsonl"
    if args.overwrite and output_path.exists():
        output_path.unlink()

    for idx, case in enumerate(cases, start=1):
        started = time.time()
        print(f"[{idx}/{len(cases)}] running {case['case_id']} with {args.model}", flush=True)
        result = run_case(case, model_config, seed=args.seed + idx)
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

    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

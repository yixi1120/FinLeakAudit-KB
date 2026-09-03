#!/usr/bin/env python3
"""Run the rank-preserving backfill baseline for natural replay revisions."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from config import MODELS, RESULTS_DIR, ModelConfig
from run_experiment import append_jsonl, completed_case_ids
from run_natural_experiment import (
    evidence_log,
    is_correct,
    predict,
    prepare_event,
    resolve_events,
    validate_citations,
    validate_model_config,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE_RESULTS = {
    "deepseek": RESULTS_DIR / "deepseek_natural_pit_5event_v1_results.jsonl",
    "zhipu": RESULTS_DIR / "zhipu_natural_pit_5event_v1_results.jsonl",
    "qwen": RESULTS_DIR / "qwen_natural_pit_5event_v1_results.jsonl",
}
POLICY = "remove_post_cutoff_then_rank_preserving_backfill_from_cutoff_top_k"


def read_source_results(path: Path) -> dict[str, dict]:
    if not path.exists():
        raise FileNotFoundError(path)
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    by_event = {str(row["event_id"]): row for row in rows}
    if len(by_event) != len(rows):
        raise ValueError(f"Duplicate event result in {path}")
    return by_event


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_refilled_evidence(prepared: dict, top_k: int) -> tuple[list[dict], list[str]]:
    """Keep surviving unfiltered order, then append cutoff-safe ranked evidence."""
    refilled = list(prepared["audited_evidence"])
    existing_ids = {str(item["id"]) for item in refilled}
    added_ids = []
    for evidence in prepared["clean_evidence"]:
        evidence_id = str(evidence["id"])
        if len(refilled) >= top_k:
            break
        if evidence_id in existing_ids:
            continue
        refilled.append(evidence)
        existing_ids.add(evidence_id)
        added_ids.append(evidence_id)

    future_ids = set(prepared["removed_evidence_ids"])
    if existing_ids & future_ids:
        raise ValueError("Refilled context contains post-cutoff evidence")
    if len(existing_ids) != len(refilled):
        raise ValueError("Refilled context contains duplicate evidence IDs")
    if len(refilled) != min(top_k, len(prepared["clean_evidence"])):
        raise ValueError("Unable to refill revised context to the requested safe size")
    return refilled, added_ids


def source_predictions(source: dict) -> dict:
    return {
        condition: {
            "prediction": source[condition]["prediction"],
            "confidence": source[condition]["confidence"],
        }
        for condition in ("clean", "unfiltered", "audited")
    }


def run_refill_event(
    event_id: str,
    model_config: ModelConfig,
    source: dict,
    source_path: Path,
    top_k: int,
) -> dict:
    if str(source["model"]) != model_config.name:
        raise ValueError(
            f"{event_id}: source model {source['model']} != requested {model_config.name}"
        )
    if int(source["top_k"]) != top_k:
        raise ValueError(f"{event_id}: source top_k differs from refill top_k")

    prepared = prepare_event(event_id, top_k=top_k)
    refilled, added_ids = build_refilled_evidence(prepared, top_k)
    refilled_prediction = predict(model_config, prepared["manifest"], refilled)
    citation_check = validate_citations(refilled_prediction, refilled)
    refilled_ids = [str(item["id"]) for item in refilled]
    clean_ids = [str(item["id"]) for item in prepared["clean_evidence"]]
    original = source_predictions(source)
    initial_flip = original["clean"]["prediction"] != original["unfiltered"]["prediction"]
    sparse_drift = original["audited"]["prediction"] != original["clean"]["prediction"]
    refill_drift = refilled_prediction["prediction"] != original["clean"]["prediction"]

    return {
        "schema_version": "finleakaudit_natural_refill_result_v1",
        "event_id": event_id,
        "case_id": event_id,
        "company": source["company"],
        "ticker": source["ticker"],
        "model": source["model"],
        "model_id": source["model_id"],
        "temperature": source["temperature"],
        "prediction_cutoff": source["prediction_cutoff"],
        "forecast_horizon": source["forecast_horizon"],
        "outcome_label": source["outcome_label"],
        "top_k": top_k,
        "policy": POLICY,
        "source_result": {
            "path": source_path.resolve().relative_to(ROOT).as_posix(),
            "sha256": file_sha256(source_path),
        },
        "source_predictions": original,
        "revision_context": {
            "unfiltered_count": len(prepared["unfiltered_evidence"]),
            "removed_evidence_ids": prepared["removed_evidence_ids"],
            "sparse_audited_count": len(prepared["audited_evidence"]),
            "backfilled_count": len(refilled),
            "backfilled_evidence_ids": refilled_ids,
            "added_evidence_ids": added_ids,
            "backfilled_matches_clean_sequence": refilled_ids == clean_ids,
            "backfilled_evidence": evidence_log(refilled),
        },
        "audited_refill": refilled_prediction,
        "citation_validation": citation_check,
        "metrics": {
            "initial_clean_to_unfiltered_flip": initial_flip,
            "sparse_audited_matches_clean": not sparse_drift,
            "backfilled_audited_matches_clean": not refill_drift,
            "sparse_revision_drift_without_initial_flip": not initial_flip
            and sparse_drift,
            "backfilled_revision_drift_without_initial_flip": not initial_flip
            and refill_drift,
            "backfill_changed_sparse_audited_direction": refilled_prediction[
                "prediction"
            ]
            != original["audited"]["prediction"],
            "backfilled_correct": is_correct(
                refilled_prediction, str(source["outcome_label"])
            ),
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def run_with_retry(
    event_id: str,
    model_config: ModelConfig,
    source: dict,
    source_path: Path,
    top_k: int,
    retries: int,
    retry_delay: float,
) -> tuple[Optional[dict], list[dict]]:
    errors = []
    for attempt in range(1, retries + 2):
        try:
            result = run_refill_event(
                event_id, model_config, source, source_path, top_k
            )
            result["attempt"] = attempt
            return result, errors
        except Exception as exc:  # noqa: BLE001 - experiment errors must be logged.
            errors.append(
                {
                    "event_id": event_id,
                    "model": model_config.name,
                    "attempt": attempt,
                    "max_attempts": retries + 1,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "traceback": traceback.format_exc(limit=3),
                }
            )
            if attempt <= retries:
                delay = retry_delay * attempt
                print(f"  attempt {attempt} failed: {exc}; retrying in {delay:.1f}s")
                time.sleep(delay)
    return None, errors


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen", choices=sorted(MODELS))
    parser.add_argument("--event", action="append", dest="events")
    parser.add_argument("--minimal", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--source", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--errors", type=Path)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--retry-delay", type=float, default=3.0)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    events = resolve_events(args.events, args.minimal, args.limit)
    source_path = (args.source or SOURCE_RESULTS[args.model]).resolve()
    sources = read_source_results(source_path)
    missing = sorted(set(events) - set(sources))
    if missing:
        raise ValueError(f"Source results are missing events: {missing}")

    if args.dry_run:
        for event_id in events:
            prepared = prepare_event(event_id, top_k=args.top_k)
            refilled, added = build_refilled_evidence(prepared, args.top_k)
            clean_ids = [item["id"] for item in prepared["clean_evidence"]]
            print(
                f"{event_id}: sparse={len(prepared['audited_evidence'])} "
                f"backfilled={len(refilled)} added={len(added)} "
                f"matches_clean_sequence={clean_ids == [item['id'] for item in refilled]}"
            )
        return 0

    model_config = MODELS[args.model]
    validate_model_config(args.model, model_config)
    output_path = args.output or RESULTS_DIR / (
        f"{args.model}_natural_refill_5event_v1_results.jsonl"
    )
    error_path = args.errors or RESULTS_DIR / (
        f"{args.model}_natural_refill_5event_v1_errors.jsonl"
    )
    if args.overwrite and output_path.exists():
        output_path.unlink()
    if args.overwrite and error_path.exists():
        error_path.unlink()

    completed = completed_case_ids(output_path)
    failures = 0
    for index, event_id in enumerate(events, start=1):
        if event_id in completed:
            print(f"[{index}/{len(events)}] skipping {event_id} (already completed)")
            continue
        started = time.time()
        print(f"[{index}/{len(events)}] backfilling {event_id} with {args.model}")
        result, errors = run_with_retry(
            event_id,
            model_config,
            sources[event_id],
            source_path,
            args.top_k,
            args.retries,
            args.retry_delay,
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
            "  clean={clean} sparse={sparse} backfilled={backfilled} "
            "matches_clean={matches}".format(
                clean=result["source_predictions"]["clean"]["prediction"],
                sparse=result["source_predictions"]["audited"]["prediction"],
                backfilled=result["audited_refill"]["prediction"],
                matches=result["metrics"]["backfilled_audited_matches_clean"],
            )
        )
    print(f"wrote {output_path}; errors={failures}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

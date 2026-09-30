#!/usr/bin/env python3
"""Run the rank-preserving backfill baseline for natural replay revisions."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import traceback
from dataclasses import replace
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
    retrieve_condition,
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
STANDARD_POLICY = "remove_post_cutoff_then_rank_preserving_backfill_from_cutoff_top_k"
NOVEL_SAFE_POLICY = (
    "remove_post_cutoff_then_rank_preserving_backfill_excluding_clean_top_k"
)
POLICIES = {
    "standard": STANDARD_POLICY,
    "novel_safe": NOVEL_SAFE_POLICY,
}
POLICY = STANDARD_POLICY


class InvalidCitationError(ValueError):
    """Raised when a prediction still cites IDs outside the supplied evidence."""


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


def build_novel_safe_refilled_evidence(
    prepared: dict, top_k: int
) -> tuple[list[dict], list[str], dict]:
    """Backfill with ranked cutoff-safe evidence outside the Clean top-k."""
    refilled = list(prepared["audited_evidence"])
    existing_ids = {str(item["id"]) for item in refilled}
    clean_ids = {str(item["id"]) for item in prepared["clean_evidence"]}
    manifest = prepared["manifest"]
    cutoff_safe_pool = retrieve_condition(
        manifest,
        as_of=manifest["prediction_cutoff"],
        top_k=1_000_000,
    )
    eligible = [
        evidence
        for evidence in cutoff_safe_pool
        if str(evidence["id"]) not in clean_ids
        and str(evidence["id"]) not in existing_ids
    ]
    added_ids = []
    for evidence in eligible:
        if len(refilled) >= top_k:
            break
        evidence_id = str(evidence["id"])
        refilled.append(evidence)
        existing_ids.add(evidence_id)
        added_ids.append(evidence_id)

    future_ids = set(prepared["removed_evidence_ids"])
    if existing_ids & future_ids:
        raise ValueError("Novel-safe context contains post-cutoff evidence")
    if len(existing_ids) != len(refilled):
        raise ValueError("Novel-safe context contains duplicate evidence IDs")
    if set(added_ids) & clean_ids:
        raise ValueError("Novel-safe additions overlap the Clean top-k")

    needed = max(0, top_k - len(prepared["audited_evidence"]))
    metadata = {
        "novel_safe_backfill_complete": len(refilled) == top_k,
        "novel_safe_backfill_needed": needed,
        "novel_safe_eligible_candidate_count": len(eligible),
        "novel_safe_backfill_count": len(added_ids),
        "novel_safe_clean_id_overlap": len(existing_ids & clean_ids),
        "cutoff_safe_pool_count": len(cutoff_safe_pool),
    }
    return refilled, added_ids, metadata


def build_policy_evidence(
    prepared: dict, top_k: int, policy_key: str
) -> tuple[list[dict], list[str], dict]:
    if policy_key == "standard":
        refilled, added_ids = build_refilled_evidence(prepared, top_k)
        return refilled, added_ids, {
            "novel_safe_backfill_complete": None,
            "novel_safe_backfill_needed": None,
            "novel_safe_eligible_candidate_count": None,
            "novel_safe_backfill_count": None,
            "novel_safe_clean_id_overlap": None,
            "cutoff_safe_pool_count": None,
        }
    if policy_key == "novel_safe":
        return build_novel_safe_refilled_evidence(prepared, top_k)
    raise ValueError(f"Unknown backfill policy: {policy_key}")


def source_predictions(source: dict) -> dict:
    return {
        condition: {
            "prediction": source[condition]["prediction"],
            "confidence": source[condition]["confidence"],
        }
        for condition in ("clean", "unfiltered", "audited")
    }


def predict_with_citation_guard(
    model_config: ModelConfig,
    manifest: dict,
    evidence: list[dict],
    citation_retries: int = 2,
) -> tuple[dict, dict, dict]:
    """Retry only invalid citations and reject outputs that never pass the whitelist."""
    if citation_retries < 0:
        raise ValueError("citation_retries must be non-negative")

    allowed_ids = [str(item["id"]) for item in evidence]
    invalid_attempts = []
    correction = None
    for attempt in range(1, citation_retries + 2):
        prediction = predict(
            model_config,
            manifest,
            evidence,
            citation_correction=correction,
        )
        validation = validate_citations(prediction, evidence)
        if validation["all_citations_valid"]:
            return prediction, validation, {
                "citation_attempts": attempt,
                "citation_retry_count": attempt - 1,
                "invalid_citation_attempts": invalid_attempts,
            }

        invalid_ids = validation["invalid_citation_ids"]
        invalid_attempts.append(
            {
                "attempt": attempt,
                "invalid_citation_ids": invalid_ids,
            }
        )
        correction = (
            "Citation validation correction: regenerate the entire JSON response. "
            f"The previous response used invalid evidence IDs: {invalid_ids}. "
            "Every evidence_ids value must exactly match one of these allowed IDs: "
            f"{allowed_ids}. Do not shorten, alter, or invent IDs."
        )

    raise InvalidCitationError(
        "Citation whitelist validation failed after "
        f"{citation_retries + 1} attempts: {invalid_attempts}"
    )


def run_refill_event(
    event_id: str,
    model_config: ModelConfig,
    source: dict,
    source_path: Path,
    top_k: int,
    policy_key: str = "standard",
    citation_retries: int = 2,
) -> dict:
    if str(source["model"]) != model_config.name:
        raise ValueError(
            f"{event_id}: source model {source['model']} != requested {model_config.name}"
        )
    if int(source["top_k"]) != top_k:
        raise ValueError(f"{event_id}: source top_k differs from refill top_k")

    prepared = prepare_event(event_id, top_k=top_k)
    refilled, added_ids, policy_metadata = build_policy_evidence(
        prepared, top_k, policy_key
    )
    if policy_key == "novel_safe" and not policy_metadata[
        "novel_safe_backfill_complete"
    ]:
        raise ValueError(
            f"{event_id}: novel-safe candidates cannot refill to top_k={top_k}; "
            f"needed={policy_metadata['novel_safe_backfill_needed']} "
            f"eligible={policy_metadata['novel_safe_eligible_candidate_count']}"
        )
    refilled_prediction, citation_check, citation_retry = predict_with_citation_guard(
        model_config,
        prepared["manifest"],
        refilled,
        citation_retries=citation_retries,
    )
    refilled_ids = [str(item["id"]) for item in refilled]
    clean_ids = [str(item["id"]) for item in prepared["clean_evidence"]]
    original = source_predictions(source)
    initial_flip = original["clean"]["prediction"] != original["unfiltered"]["prediction"]
    sparse_drift = original["audited"]["prediction"] != original["clean"]["prediction"]
    refill_drift = refilled_prediction["prediction"] != original["clean"]["prediction"]

    return {
        "schema_version": (
            "finleakaudit_natural_refill_result_v1"
            if policy_key == "standard"
            else "finleakaudit_natural_novel_safe_refill_result_v1"
        ),
        "event_id": event_id,
        "case_id": event_id,
        "company": source["company"],
        "ticker": source["ticker"],
        "model": source["model"],
        "model_id": source["model_id"],
        "temperature": source["temperature"],
        "max_tokens": model_config.max_tokens,
        "prediction_cutoff": source["prediction_cutoff"],
        "forecast_horizon": source["forecast_horizon"],
        "outcome_label": source["outcome_label"],
        "top_k": top_k,
        "policy": POLICIES[policy_key],
        "policy_key": policy_key,
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
            **policy_metadata,
        },
        "audited_refill": refilled_prediction,
        "citation_validation": citation_check,
        "citation_retry": citation_retry,
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
    policy_key: str,
    citation_retries: int,
    retries: int,
    retry_delay: float,
) -> tuple[Optional[dict], list[dict]]:
    errors = []
    for attempt in range(1, retries + 2):
        try:
            result = run_refill_event(
                event_id,
                model_config,
                source,
                source_path,
                top_k,
                policy_key=policy_key,
                citation_retries=citation_retries,
            )
            result["attempt"] = attempt
            return result, errors
        except Exception as exc:  # noqa: BLE001 - experiment errors must be logged.
            citation_failure = isinstance(exc, InvalidCitationError)
            errors.append(
                {
                    "event_id": event_id,
                    "model": model_config.name,
                    "attempt": attempt,
                    "max_attempts": retries + 1,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "retryable": not citation_failure,
                    "traceback": traceback.format_exc(limit=3),
                }
            )
            if citation_failure:
                break
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
    parser.add_argument("--max-tokens", type=int)
    parser.add_argument("--policy", choices=sorted(POLICIES), default="standard")
    parser.add_argument("--source", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--errors", type=Path)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--citation-retries", type=int, default=2)
    parser.add_argument("--retry-delay", type=float, default=3.0)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    events = resolve_events(args.events, args.minimal, args.limit)
    if args.citation_retries < 0:
        parser.error("--citation-retries must be non-negative")
    if args.dry_run:
        for event_id in events:
            prepared = prepare_event(event_id, top_k=args.top_k)
            refilled, added, metadata = build_policy_evidence(
                prepared, args.top_k, args.policy
            )
            clean_ids = [item["id"] for item in prepared["clean_evidence"]]
            print(
                f"{event_id}: sparse={len(prepared['audited_evidence'])} "
                f"backfilled={len(refilled)} added={len(added)} "
                f"matches_clean_sequence={clean_ids == [item['id'] for item in refilled]} "
                f"novel_complete={metadata['novel_safe_backfill_complete']} "
                f"novel_eligible={metadata['novel_safe_eligible_candidate_count']}"
            )
        return 0

    source_path = (args.source or SOURCE_RESULTS[args.model]).resolve()
    sources = read_source_results(source_path)
    missing = sorted(set(events) - set(sources))
    if missing:
        raise ValueError(f"Source results are missing events: {missing}")

    model_config = MODELS[args.model]
    validate_model_config(args.model, model_config)
    if args.max_tokens is not None:
        if args.max_tokens <= 0:
            raise ValueError("--max-tokens must be positive")
        model_config = replace(model_config, max_tokens=args.max_tokens)
    output_stem = (
        "natural_refill_5event_v1"
        if args.policy == "standard"
        else "natural_novel_safe_refill_5event_v1"
    )
    output_path = args.output or RESULTS_DIR / (
        f"{args.model}_{output_stem}_results.jsonl"
    )
    error_path = args.errors or RESULTS_DIR / (
        f"{args.model}_{output_stem}_errors.jsonl"
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
        print(
            f"[{index}/{len(events)}] {args.policy} backfilling "
            f"{event_id} with {args.model}"
        )
        result, errors = run_with_retry(
            event_id,
            model_config,
            sources[event_id],
            source_path,
            args.top_k,
            args.policy,
            args.citation_retries,
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

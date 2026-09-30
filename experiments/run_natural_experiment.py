#!/usr/bin/env python3
"""Run a point-in-time replay over the natural primary-source corpus."""

from __future__ import annotations

import argparse
import json
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from config import MODELS, RESULTS_DIR, ModelConfig
from finleakaudit import detect_rationale_leakage, temporal_availability_check
from prompts import build_natural_prediction_prompt
from run_experiment import (
    append_jsonl,
    call_chat,
    completed_case_ids,
    normalize_prediction,
)


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "数据线"
sys.path.insert(0, str(ROOT))

from tools.natural_event_registry import EVENT_SPECS  # noqa: E402
from tools.natural_retrieval import load_candidate_chunks, rank_lexical  # noqa: E402


MINIMAL_EVENT_IDS = [
    "natural_001",
    "natural_002",
    "natural_004",
    "natural_007",
    "natural_010",
]
AUDIT_POLICY = "timestamp_only_remove_all_post_cutoff_from_unfiltered_top_k"


def load_manifest(event_id: str) -> dict:
    path = DATA / f"{event_id}.json"
    if not path.exists():
        raise FileNotFoundError(path)
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if manifest.get("event_id") != event_id:
        raise ValueError(f"{path}: event_id does not match filename")
    return manifest


def internal_evidence(chunk: dict[str, object], rank: int) -> dict:
    """Retain audit metadata while exposing only id/text to the prompt builder."""
    return {
        "id": str(chunk["chunk_id"]),
        "text": str(chunk["text"]),
        "retrieval_rank": rank,
        "retrieval_score": float(chunk["retrieval_score"]),
        "retrieval_unit_id": str(chunk["retrieval_unit_id"]),
        "parent_document_id": str(chunk["parent_document_id"]),
        "title": str(chunk["title"]),
        "source_type": str(chunk["source_type"]),
        "canonical_url": str(chunk["canonical_url"]),
        "available_at": str(chunk["available_at"]),
    }


def retrieve_condition(manifest: dict, as_of: str, top_k: int) -> list[dict]:
    chunks = load_candidate_chunks(manifest["event_id"], as_of=as_of)
    ranked = rank_lexical(manifest["retrieval_query"], chunks, top_k=top_k)
    return [internal_evidence(chunk, rank) for rank, chunk in enumerate(ranked, start=1)]


def prepare_event(event_id: str, top_k: int = 8) -> dict:
    """Build clean, unfiltered, and audited inputs without calling a model."""
    manifest = load_manifest(event_id)
    clean_evidence = retrieve_condition(
        manifest, as_of=manifest["prediction_cutoff"], top_k=top_k
    )
    unfiltered_evidence = retrieve_condition(
        manifest, as_of=manifest["outcome_time"], top_k=top_k
    )
    temporal_check = temporal_availability_check(
        unfiltered_evidence,
        prediction_cutoff=manifest["prediction_cutoff"],
    )
    future_ids = {
        row["evidence_id"]
        for row in temporal_check
        if row["temporal_status"] == "future_leakage"
    }
    audited_evidence = [
        evidence for evidence in unfiltered_evidence if evidence["id"] not in future_ids
    ]
    return {
        "manifest": manifest,
        "clean_evidence": clean_evidence,
        "unfiltered_evidence": unfiltered_evidence,
        "audited_evidence": audited_evidence,
        "temporal_check": temporal_check,
        "removed_evidence_ids": sorted(future_ids),
    }


def prediction_case(manifest: dict) -> dict:
    """Return only metadata that is appropriate for the prediction prompt."""
    return {
        "company": manifest["company"],
        "ticker": manifest["ticker"],
        "prediction_cutoff": manifest["prediction_cutoff"],
        "forecast_horizon": manifest["forecast_horizon"],
    }


def predict(
    model_config: ModelConfig,
    manifest: dict,
    evidence: list[dict],
    citation_correction: str | None = None,
) -> dict:
    prompt = build_natural_prediction_prompt(prediction_case(manifest), evidence)
    if citation_correction:
        prompt = f"{prompt}\n\n{citation_correction}"
    return normalize_prediction(call_chat(model_config, prompt))


def cited_future_report(prediction: dict, temporal_check: list[dict]) -> dict:
    return detect_rationale_leakage(prediction.get("rationale") or [], temporal_check)


def validate_citations(prediction: dict, evidence: list[dict]) -> dict:
    available_ids = {item["id"] for item in evidence}
    cited_ids = sorted(
        {
            str(evidence_id)
            for claim in prediction.get("rationale") or []
            for evidence_id in claim.get("evidence_ids") or []
        }
    )
    invalid_ids = sorted(set(cited_ids) - available_ids)
    return {
        "cited_evidence_ids": cited_ids,
        "invalid_citation_ids": invalid_ids,
        "all_citations_valid": not invalid_ids,
    }


def evidence_log(evidence: list[dict]) -> list[dict]:
    """Store provenance and short previews without duplicating full raw documents."""
    fields = (
        "id",
        "retrieval_rank",
        "retrieval_score",
        "retrieval_unit_id",
        "parent_document_id",
        "title",
        "source_type",
        "canonical_url",
        "available_at",
    )
    return [
        {
            **{field: item[field] for field in fields},
            "text_preview": item["text"][:500],
        }
        for item in evidence
    ]


def is_correct(prediction: dict, outcome_label: str) -> bool:
    return prediction["prediction"] == outcome_label


def run_event(
    event_id: str,
    model_config: ModelConfig,
    top_k: int = 8,
) -> dict:
    prepared = prepare_event(event_id, top_k=top_k)
    manifest = prepared["manifest"]
    clean = predict(model_config, manifest, prepared["clean_evidence"])
    unfiltered = predict(model_config, manifest, prepared["unfiltered_evidence"])
    leakage_report = cited_future_report(unfiltered, prepared["temporal_check"])
    audited = predict(model_config, manifest, prepared["audited_evidence"])
    citation_validation = {
        "clean": validate_citations(clean, prepared["clean_evidence"]),
        "unfiltered": validate_citations(unfiltered, prepared["unfiltered_evidence"]),
        "audited": validate_citations(audited, prepared["audited_evidence"]),
    }
    outcome_label = manifest["outcome_label"]

    return {
        "schema_version": "finleakaudit_natural_replay_result_v1",
        "case_id": event_id,
        "event_id": event_id,
        "company": manifest["company"],
        "ticker": manifest["ticker"],
        "prediction_cutoff": manifest["prediction_cutoff"],
        "forecast_horizon": manifest["forecast_horizon"],
        "outcome_time": manifest["outcome_time"],
        "outcome_label": outcome_label,
        "outcome_return": manifest["outcome_return"],
        "model": model_config.name,
        "model_id": model_config.model,
        "temperature": model_config.temperature,
        "retrieval_order": "deterministic_lexical_rank",
        "top_k": top_k,
        "audit_policy": AUDIT_POLICY,
        "retrieval": {
            "query": manifest["retrieval_query"],
            "clean_as_of": manifest["prediction_cutoff"],
            "unfiltered_as_of": manifest["outcome_time"],
            "clean_evidence": evidence_log(prepared["clean_evidence"]),
            "unfiltered_evidence": evidence_log(prepared["unfiltered_evidence"]),
            "audited_evidence": evidence_log(prepared["audited_evidence"]),
        },
        "clean": clean,
        "unfiltered": unfiltered,
        "audit": {
            "policy": AUDIT_POLICY,
            "temporal_check": prepared["temporal_check"],
            "removed_evidence_ids": prepared["removed_evidence_ids"],
            "citation_leakage_report": leakage_report,
            "citation_validation": citation_validation,
        },
        "audited": audited,
        "metrics": {
            "future_evidence_retrieved": bool(prepared["removed_evidence_ids"]),
            "future_evidence_retrieved_count": len(prepared["removed_evidence_ids"]),
            "future_evidence_cited": leakage_report["has_leakage"],
            "future_evidence_cited_claim_count": leakage_report["leakage_count"],
            "prediction_changed_clean_to_unfiltered": clean["prediction"]
            != unfiltered["prediction"],
            "audited_recovered_clean_direction": audited["prediction"]
            == clean["prediction"],
            "confidence_delta_unfiltered_minus_clean": unfiltered["confidence"]
            - clean["confidence"],
            "clean_correct": is_correct(clean, outcome_label),
            "unfiltered_correct": is_correct(unfiltered, outcome_label),
            "audited_correct": is_correct(audited, outcome_label),
            "all_condition_citations_valid": all(
                item["all_citations_valid"] for item in citation_validation.values()
            ),
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
    }


def run_event_with_retry(
    event_id: str,
    model_config: ModelConfig,
    top_k: int,
    retries: int,
    retry_delay: float,
) -> tuple[Optional[dict], list[dict]]:
    errors = []
    total_attempts = retries + 1
    for attempt in range(1, total_attempts + 1):
        try:
            result = run_event(event_id, model_config, top_k=top_k)
            result["attempt"] = attempt
            return result, errors
        except Exception as exc:  # noqa: BLE001 - experiment failures are logged.
            errors.append(
                {
                    "case_id": event_id,
                    "event_id": event_id,
                    "model": model_config.name,
                    "attempt": attempt,
                    "max_attempts": total_attempts,
                    "error_type": type(exc).__name__,
                    "error": str(exc),
                    "traceback": traceback.format_exc(limit=3),
                }
            )
            if attempt < total_attempts:
                sleep_seconds = retry_delay * attempt
                print(
                    f"  attempt {attempt}/{total_attempts} failed: {exc}; "
                    f"retrying in {sleep_seconds:.1f}s",
                    flush=True,
                )
                time.sleep(sleep_seconds)
            else:
                print(f"  failed after {total_attempts} attempts: {exc}", flush=True)
    return None, errors


def resolve_events(requested: list[str] | None, minimal: bool, limit: int | None) -> list[str]:
    events = list(requested or (MINIMAL_EVENT_IDS if minimal else EVENT_SPECS))
    unknown = sorted(set(events) - set(EVENT_SPECS))
    if unknown:
        raise ValueError(f"Unknown event IDs: {unknown}")
    if len(events) != len(set(events)):
        raise ValueError("Event IDs must be unique")
    return events[:limit] if limit is not None else events


def validate_model_config(model_key: str, config: ModelConfig) -> None:
    if model_key != "qwen" and config.api_key.startswith("missing-"):
        env_name = "DEEPSEEK_API_KEY" if model_key == "deepseek" else "ZHIPU_API_KEY"
        raise RuntimeError(f"Missing {env_name}; export it before running {model_key}")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="deepseek", choices=sorted(MODELS))
    parser.add_argument("--event", action="append", dest="events")
    parser.add_argument("--minimal", action="store_true", help="Use the frozen five-event set")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--retry-delay", type=float, default=3.0)
    parser.add_argument("--run-name", default="natural_pit_replay_v1")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--errors", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    events = resolve_events(args.events, minimal=args.minimal, limit=args.limit)
    if args.top_k <= 0:
        parser.error("--top-k must be positive")

    if args.dry_run:
        for event_id in events:
            prepared = prepare_event(event_id, top_k=args.top_k)
            print(
                f"{event_id}: clean={len(prepared['clean_evidence'])} "
                f"unfiltered={len(prepared['unfiltered_evidence'])} "
                f"future_removed={len(prepared['removed_evidence_ids'])} "
                f"audited={len(prepared['audited_evidence'])}"
            )
        return 0

    model_config = MODELS[args.model]
    validate_model_config(args.model, model_config)
    output_path = args.output or RESULTS_DIR / f"{args.model}_{args.run_name}_results.jsonl"
    error_path = args.errors or RESULTS_DIR / f"{args.model}_{args.run_name}_errors.jsonl"
    if args.overwrite and output_path.exists():
        output_path.unlink()
    if args.overwrite and error_path.exists():
        error_path.unlink()

    print(f"results: {output_path}")
    print(f"errors:  {error_path}")
    completed = completed_case_ids(output_path)
    failures = 0
    skipped = 0
    for index, event_id in enumerate(events, start=1):
        if event_id in completed:
            skipped += 1
            print(f"[{index}/{len(events)}] skipping {event_id} (already completed)")
            continue
        started = time.time()
        print(f"[{index}/{len(events)}] running {event_id} with {args.model}", flush=True)
        result, errors = run_event_with_retry(
            event_id,
            model_config,
            top_k=args.top_k,
            retries=args.retries,
            retry_delay=args.retry_delay,
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
            "  clean={clean} unfiltered={unfiltered} audited={audited} "
            "future_retrieved={retrieved} future_cited={cited}".format(
                clean=result["clean"]["prediction"],
                unfiltered=result["unfiltered"]["prediction"],
                audited=result["audited"]["prediction"],
                retrieved=result["metrics"]["future_evidence_retrieved"],
                cited=result["metrics"]["future_evidence_cited"],
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

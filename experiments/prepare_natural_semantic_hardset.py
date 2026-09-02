#!/usr/bin/env python3
"""Build a frozen natural claim-evidence hard set from replay outputs."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
from pathlib import Path
from typing import Iterable

from run_natural_experiment import prepare_event


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = ROOT / "experiments" / "analysis"
DEFAULT_INPUTS = [
    ROOT / "experiments" / "results" / "deepseek_natural_pit_5event_v1_results.jsonl",
    ROOT / "experiments" / "results" / "zhipu_natural_pit_5event_v1_results.jsonl",
]
DEFAULT_DEV_OUTPUT = ANALYSIS_DIR / "natural_semantic_hard_dev_blind_v1.csv"
DEFAULT_TEST_OUTPUT = ANALYSIS_DIR / "natural_semantic_hard_test_blind_v1.csv"
DEFAULT_KEY_OUTPUT = ANALYSIS_DIR / "natural_semantic_hard_key_v1.csv"
DEFAULT_MANIFEST_OUTPUT = ANALYSIS_DIR / "natural_semantic_hard_manifest_v1.json"
SPLIT_SEED = 29
DEV_EVENT_COUNT = 2
FREEZE_DATE = "2026-09-02"

BLIND_FIELDS = [
    "sample_id",
    "claim_text",
    "claim_direction",
    "pre_cutoff_evidence",
    "post_cutoff_evidence_text",
    "label_semantic_dependency",
    "label_relation",
    "label_exclusive_to_post_cutoff",
    "matched_claim_span",
    "confidence_1_to_5",
    "annotator_id",
    "notes",
]

KEY_FIELDS = [
    "sample_id",
    "split",
    "event_id",
    "case_id",
    "company",
    "model",
    "model_id",
    "claim_index",
    "post_cutoff_evidence_id",
    "explicit_future_citation",
    "prediction_cutoff",
    "candidate_available_at",
    "retrieval_rank",
    "parent_document_id",
    "canonical_url",
    "source_type",
    "split_seed",
    "shuffle_seed",
    "pair_sha256",
]


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Missing natural replay result: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def sha256_bytes(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def stable_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def evidence_text_view(items: Iterable[dict]) -> str:
    """Expose only model-visible text, without IDs or temporal metadata."""
    return json.dumps(
        [{"text": str(item["text"])} for item in items],
        ensure_ascii=False,
        separators=(",", ":"),
    )


def split_events(
    event_ids: Iterable[str], seed: int = SPLIT_SEED, dev_event_count: int = DEV_EVENT_COUNT
) -> tuple[list[str], list[str]]:
    ordered = sorted(set(event_ids))
    if not 0 < dev_event_count < len(ordered):
        raise ValueError("dev_event_count must leave at least one event in each split")
    random.Random(seed).shuffle(ordered)
    return ordered[:dev_event_count], ordered[dev_event_count:]


def validate_and_reconstruct_result(result: dict, cache: dict[str, dict]) -> dict:
    event_id = str(result["event_id"])
    top_k = int(result["top_k"])
    if event_id not in cache:
        cache[event_id] = prepare_event(event_id, top_k=top_k)
    prepared = cache[event_id]
    if len(prepared["unfiltered_evidence"]) != top_k:
        raise ValueError(f"{event_id}: reconstructed unfiltered evidence is not top_k={top_k}")

    logged = result["retrieval"]["unfiltered_evidence"]
    current = prepared["unfiltered_evidence"]
    logged_ids = [str(item["id"]) for item in logged]
    current_ids = [str(item["id"]) for item in current]
    if logged_ids != current_ids:
        raise ValueError(f"{event_id}: reconstructed evidence order differs from replay log")

    for current_item, logged_item in zip(current, logged):
        if not str(current_item["text"]).startswith(str(logged_item["text_preview"])):
            raise ValueError(
                f"{event_id}/{current_item['id']}: archived text differs from replay preview"
            )

    logged_future_ids = sorted(result["audit"]["removed_evidence_ids"])
    current_future_ids = sorted(prepared["removed_evidence_ids"])
    if logged_future_ids != current_future_ids:
        raise ValueError(f"{event_id}: post-cutoff membership changed since replay")

    temporal_by_id = {
        str(row["evidence_id"]): str(row["temporal_status"])
        for row in prepared["temporal_check"]
    }
    valid_evidence = [
        item for item in current if temporal_by_id[item["id"]] != "future_leakage"
    ]
    future_evidence = [
        item for item in current if temporal_by_id[item["id"]] == "future_leakage"
    ]
    if [item["id"] for item in future_evidence] != [
        item["id"] for item in current if item["id"] in set(logged_future_ids)
    ]:
        raise ValueError(f"{event_id}: temporal reconstruction is internally inconsistent")
    return {
        "valid_evidence": valid_evidence,
        "future_evidence": future_evidence,
        "manifest": prepared["manifest"],
    }


def build_pairs(results: list[dict]) -> list[dict]:
    pairs: list[dict] = []
    cache: dict[str, dict] = {}
    seen_runs: set[tuple[str, str]] = set()
    seen_pairs: set[tuple[str, str, int, str]] = set()

    for result in results:
        event_id = str(result["event_id"])
        model = str(result["model"])
        run_key = (event_id, model)
        if run_key in seen_runs:
            raise ValueError(f"Duplicate natural replay run: {event_id}/{model}")
        seen_runs.add(run_key)

        reconstructed = validate_and_reconstruct_result(result, cache)
        pre_cutoff_view = evidence_text_view(reconstructed["valid_evidence"])
        claims = (result.get("unfiltered") or {}).get("rationale") or []
        if not claims:
            raise ValueError(f"{event_id}/{model}: unfiltered rationale is empty")

        for claim_index, claim in enumerate(claims):
            cited_ids = {str(item) for item in claim.get("evidence_ids") or []}
            for candidate in reconstructed["future_evidence"]:
                candidate_id = str(candidate["id"])
                pair_key = (event_id, model, claim_index, candidate_id)
                if pair_key in seen_pairs:
                    raise ValueError(f"Duplicate claim-evidence pair: {pair_key}")
                seen_pairs.add(pair_key)
                pair_content = {
                    "event_id": event_id,
                    "model": model,
                    "claim_index": claim_index,
                    "claim_text": str(claim.get("claim", "")),
                    "pre_cutoff_evidence": pre_cutoff_view,
                    "post_cutoff_evidence_id": candidate_id,
                    "post_cutoff_evidence_text": str(candidate["text"]),
                }
                pairs.append(
                    {
                        **pair_content,
                        "case_id": str(result["case_id"]),
                        "company": str(result["company"]),
                        "model_id": str(result["model_id"]),
                        "claim_direction": str(claim.get("direction", "")),
                        "explicit_future_citation": candidate_id in cited_ids,
                        "prediction_cutoff": str(result["prediction_cutoff"]),
                        "candidate_available_at": str(candidate["available_at"]),
                        "retrieval_rank": int(candidate["retrieval_rank"]),
                        "parent_document_id": str(candidate["parent_document_id"]),
                        "canonical_url": str(candidate["canonical_url"]),
                        "source_type": str(candidate["source_type"]),
                        "pair_sha256": sha256_bytes(stable_json(pair_content).encode("utf-8")),
                    }
                )
    return pairs


def blind_split(
    pairs: list[dict], split: str, split_seed: int = SPLIT_SEED
) -> tuple[list[dict], list[dict], int]:
    if split not in {"dev", "test"}:
        raise ValueError("split must be dev or test")
    shuffle_seed = split_seed * 1000 + (1 if split == "dev" else 2)
    ordered = list(pairs)
    random.Random(shuffle_seed).shuffle(ordered)
    blind_rows: list[dict] = []
    key_rows: list[dict] = []

    for index, pair in enumerate(ordered, start=1):
        sample_id = f"natural_hard_v1_{split}_{index:03d}"
        blind_rows.append(
            {
                "sample_id": sample_id,
                "claim_text": pair["claim_text"],
                "claim_direction": pair["claim_direction"],
                "pre_cutoff_evidence": pair["pre_cutoff_evidence"],
                "post_cutoff_evidence_text": pair["post_cutoff_evidence_text"],
                "label_semantic_dependency": "",
                "label_relation": "",
                "label_exclusive_to_post_cutoff": "",
                "matched_claim_span": "",
                "confidence_1_to_5": "",
                "annotator_id": "",
                "notes": "",
            }
        )
        key_rows.append(
            {
                "sample_id": sample_id,
                "split": split,
                "event_id": pair["event_id"],
                "case_id": pair["case_id"],
                "company": pair["company"],
                "model": pair["model"],
                "model_id": pair["model_id"],
                "claim_index": pair["claim_index"],
                "post_cutoff_evidence_id": pair["post_cutoff_evidence_id"],
                "explicit_future_citation": str(pair["explicit_future_citation"]).lower(),
                "prediction_cutoff": pair["prediction_cutoff"],
                "candidate_available_at": pair["candidate_available_at"],
                "retrieval_rank": pair["retrieval_rank"],
                "parent_document_id": pair["parent_document_id"],
                "canonical_url": pair["canonical_url"],
                "source_type": pair["source_type"],
                "split_seed": split_seed,
                "shuffle_seed": shuffle_seed,
                "pair_sha256": pair["pair_sha256"],
            }
        )
    return blind_rows, key_rows, shuffle_seed


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_hardset(
    input_paths: list[Path], split_seed: int = SPLIT_SEED, dev_event_count: int = DEV_EVENT_COUNT
) -> dict:
    results = [row for path in input_paths for row in read_jsonl(path)]
    pairs = build_pairs(results)
    dev_events, test_events = split_events(
        (pair["event_id"] for pair in pairs), split_seed, dev_event_count
    )
    dev_event_set = set(dev_events)
    test_event_set = set(test_events)
    if dev_event_set & test_event_set:
        raise ValueError("Event leakage detected between dev and test")

    dev_pairs = [pair for pair in pairs if pair["event_id"] in dev_event_set]
    test_pairs = [pair for pair in pairs if pair["event_id"] in test_event_set]
    dev_blind, dev_key, dev_shuffle_seed = blind_split(dev_pairs, "dev", split_seed)
    test_blind, test_key, test_shuffle_seed = blind_split(test_pairs, "test", split_seed)
    return {
        "pairs": pairs,
        "dev_events": dev_events,
        "test_events": test_events,
        "dev_blind": dev_blind,
        "test_blind": test_blind,
        "key": dev_key + test_key,
        "dev_shuffle_seed": dev_shuffle_seed,
        "test_shuffle_seed": test_shuffle_seed,
    }


def count_explicit(rows: list[dict]) -> int:
    return sum(row["explicit_future_citation"] == "true" for row in rows)


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT).as_posix()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", type=Path, dest="inputs")
    parser.add_argument("--dev-output", type=Path, default=DEFAULT_DEV_OUTPUT)
    parser.add_argument("--test-output", type=Path, default=DEFAULT_TEST_OUTPUT)
    parser.add_argument("--key-output", type=Path, default=DEFAULT_KEY_OUTPUT)
    parser.add_argument("--manifest-output", type=Path, default=DEFAULT_MANIFEST_OUTPUT)
    parser.add_argument("--split-seed", type=int, default=SPLIT_SEED)
    parser.add_argument("--dev-event-count", type=int, default=DEV_EVENT_COUNT)
    args = parser.parse_args()

    input_paths = [path.resolve() for path in (args.inputs or DEFAULT_INPUTS)]
    built = build_hardset(input_paths, args.split_seed, args.dev_event_count)
    write_csv(args.dev_output, built["dev_blind"], BLIND_FIELDS)
    write_csv(args.test_output, built["test_blind"], BLIND_FIELDS)
    write_csv(args.key_output, built["key"], KEY_FIELDS)

    manifest = {
        "schema_version": "finleakaudit_natural_semantic_hardset_manifest_v1",
        "freeze_date": FREEZE_DATE,
        "purpose": "blinded semantic dependency evaluation on natural replay rationales",
        "source_results": [
            {"path": relative(path), "sha256": sha256_file(path)}
            for path in input_paths
        ],
        "split_policy": "event-level random split before semantic labeling",
        "split_seed": args.split_seed,
        "dev_event_count": args.dev_event_count,
        "dev_events": built["dev_events"],
        "test_events": built["test_events"],
        "shuffle_seeds": {
            "dev": built["dev_shuffle_seed"],
            "test": built["test_shuffle_seed"],
        },
        "counts": {
            "events": len(built["dev_events"]) + len(built["test_events"]),
            "model_event_runs": len(
                {(pair["event_id"], pair["model"]) for pair in built["pairs"]}
            ),
            "claims": len(
                {
                    (pair["event_id"], pair["model"], pair["claim_index"])
                    for pair in built["pairs"]
                }
            ),
            "pairs_total": len(built["pairs"]),
            "pairs_dev": len(built["dev_blind"]),
            "pairs_test": len(built["test_blind"]),
            "explicit_future_citations_dev": count_explicit(
                built["key"][: len(built["dev_blind"])]
            ),
            "explicit_future_citations_test": count_explicit(
                built["key"][len(built["dev_blind"]) :]
            ),
        },
        "blinding": {
            "hidden_from_annotators": [
                "event_id",
                "model",
                "model_id",
                "evidence_id",
                "timestamps",
                "explicit citation flag",
                "market outcome",
                "forecast correctness",
            ],
            "coordinator_key_ignored_until_gold_freeze": True,
        },
        "outputs": {},
    }
    for name, path in (
        ("dev_blind", args.dev_output),
        ("test_blind", args.test_output),
        ("coordinator_key", args.key_output),
    ):
        manifest["outputs"][name] = {
            "path": relative(path),
            "sha256": sha256_file(path),
        }
    args.manifest_output.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_output.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(
        f"wrote {args.dev_output} ({len(built['dev_blind'])} dev pairs; "
        f"events={','.join(built['dev_events'])})"
    )
    print(
        f"wrote {args.test_output} ({len(built['test_blind'])} test pairs; "
        f"events={','.join(built['test_events'])})"
    )
    print(f"wrote {args.key_output} ({len(built['key'])} blinded key rows; keep local)")
    print(f"wrote {args.manifest_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

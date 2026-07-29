"""Build a blinded claim-evidence annotation batch from completed v4 runs."""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path

from config import RESULTS_DIR


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES = ROOT / "数据线" / "cases_pilot_v4_mixed10_candidate.jsonl"
DEFAULT_INPUTS = [
    RESULTS_DIR / "deepseek_v4_mixed10_abs_time_20260726_ablation_results.jsonl",
    RESULTS_DIR / "zhipu_v4_mixed10_abs_time_20260726_ablation_results.jsonl",
    RESULTS_DIR / "qwen_v4_mixed10_abs_time_20260726_ablation_results.jsonl",
]
DEFAULT_OUTPUT = ROOT / "experiments" / "analysis" / "semantic_annotation_batch_v1.csv"
DEFAULT_KEY_OUTPUT = (
    ROOT / "experiments" / "analysis" / "semantic_annotation_key_v1.csv"
)


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Missing JSONL file: {path}")
    with path.open("r", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def evidence_view(items: list[dict]) -> str:
    return json.dumps(
        [{"id": item.get("id"), "text": item.get("text")} for item in items],
        ensure_ascii=False,
        separators=(",", ":"),
    )


def build_pairs(cases: list[dict], results: list[dict]) -> list[dict]:
    cases_by_id = {case["case_id"]: case for case in cases}
    pairs = []
    for result in results:
        case_id = result["case_id"]
        if case_id not in cases_by_id:
            raise ValueError(f"Result references unknown case: {case_id}")
        case = cases_by_id[case_id]
        clean_evidence = case.get("clean_evidence") or []
        future_evidence = case.get("leaked_evidence") or []
        for claim_index, claim in enumerate(
            (result.get("leaky") or {}).get("rationale") or []
        ):
            cited_ids = set(claim.get("evidence_ids") or [])
            for evidence in future_evidence:
                evidence_id = evidence["id"]
                pairs.append(
                    {
                        "case_id": case_id,
                        "dataset_tier": result.get("dataset_tier"),
                        "model": result.get("model"),
                        "model_id": result.get("model_id"),
                        "claim_index": claim_index,
                        "forecast_prediction": (result.get("leaky") or {}).get(
                            "prediction"
                        ),
                        "claim_text": claim.get("claim", ""),
                        "claim_direction": claim.get("direction", ""),
                        "pre_cutoff_evidence": evidence_view(clean_evidence),
                        "post_cutoff_evidence_id": evidence_id,
                        "post_cutoff_evidence_text": evidence.get("text", ""),
                        "explicit_future_citation": evidence_id in cited_ids,
                    }
                )
    return pairs


def blind_pairs(pairs: list[dict], seed: int) -> tuple[list[dict], list[dict]]:
    ordered = list(pairs)
    random.Random(seed).shuffle(ordered)
    batch = []
    key = []
    for index, pair in enumerate(ordered, start=1):
        sample_id = f"semantic_v1_{index:03d}"
        batch.append(
            {
                "sample_id": sample_id,
                "forecast_prediction": pair["forecast_prediction"],
                "claim_text": pair["claim_text"],
                "claim_direction": pair["claim_direction"],
                "pre_cutoff_evidence": pair["pre_cutoff_evidence"],
                "post_cutoff_evidence_id": pair["post_cutoff_evidence_id"],
                "post_cutoff_evidence_text": pair["post_cutoff_evidence_text"],
                "label_semantic_dependency": "",
                "label_relation": "",
                "label_exclusive_to_post_cutoff": "",
                "label_should_remove": "",
                "matched_claim_span": "",
                "confidence_1_to_5": "",
                "annotator_id": "",
                "notes": "",
            }
        )
        key.append(
            {
                "sample_id": sample_id,
                "case_id": pair["case_id"],
                "dataset_tier": pair["dataset_tier"],
                "model": pair["model"],
                "model_id": pair["model_id"],
                "claim_index": pair["claim_index"],
                "post_cutoff_evidence_id": pair["post_cutoff_evidence_id"],
                "explicit_future_citation": pair["explicit_future_citation"],
                "shuffle_seed": seed,
            }
        )
    return batch, key


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError("Refusing to write an empty annotation file")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=list(rows[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--input", action="append", type=Path, dest="inputs")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--key-output", type=Path, default=DEFAULT_KEY_OUTPUT)
    parser.add_argument("--seed", type=int, default=17)
    args = parser.parse_args()

    cases = read_jsonl(args.cases)
    results = []
    for path in args.inputs or DEFAULT_INPUTS:
        results.extend(read_jsonl(path))
    pairs = build_pairs(cases, results)
    batch, key = blind_pairs(pairs, args.seed)
    write_csv(args.output, batch)
    write_csv(args.key_output, key)
    print(f"wrote {args.output} ({len(batch)} blinded claim-evidence pairs)")
    print(f"wrote {args.key_output} ({len(key)} coordinator key rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

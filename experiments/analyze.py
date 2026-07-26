"""Summarize FinLeakAudit pilot outputs."""

from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

from config import RESULTS_DIR


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def rate(successes: int, total: int) -> float:
    return successes / total if total else 0.0


def outcome_label(row: dict) -> str:
    return str(row.get("outcome_label") or row.get("label") or "").upper()


def prediction_matches_outcome(row: dict, condition: str) -> bool:
    prediction = str((row.get(condition) or {}).get("prediction") or "").upper()
    gold = outcome_label(row)
    return bool(gold) and prediction == gold


def cited_evidence_ids(prediction: dict) -> set[str]:
    return {
        evidence_id
        for claim in (prediction or {}).get("rationale") or []
        for evidence_id in claim.get("evidence_ids") or []
    }


def response_objects(row: dict) -> list[dict]:
    responses = [
        row.get("clean") or {},
        row.get("leaky") or {},
        row.get("audited") or {},
    ]
    responses.extend(
        item.get("prediction_output") or {} for item in row.get("ablation") or []
    )
    return responses


def usage_value(response: dict, *names: str) -> int:
    usage = response.get("_usage") or {}
    for name in names:
        value = usage.get(name)
        if isinstance(value, (int, float)):
            return int(value)
    return 0


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float, float]:
    if total == 0:
        return (0.0, 0.0)
    p = successes / total
    denom = 1 + z * z / total
    center = (p + z * z / (2 * total)) / denom
    margin = z * math.sqrt((p * (1 - p) + z * z / (4 * total)) / total) / denom
    return (center - margin, center + margin)


def summarize(rows: list[dict]) -> dict:
    n = len(rows)
    leakage = sum(1 for row in rows if row["metrics"]["leaky_cited_future"])
    flips = sum(
        1 for row in rows if row["metrics"]["prediction_flipped_clean_to_leaky"]
    )
    clean_agreements = sum(
        1 for row in rows if row["metrics"]["audited_recovered_clean_direction"]
    )
    recovered_flips = sum(
        1
        for row in rows
        if row["metrics"]["prediction_flipped_clean_to_leaky"]
        and row["metrics"]["audited_recovered_clean_direction"]
    )
    clean_correct = sum(prediction_matches_outcome(row, "clean") for row in rows)
    leaky_correct = sum(prediction_matches_outcome(row, "leaky") for row in rows)
    audited_correct = sum(prediction_matches_outcome(row, "audited") for row in rows)
    deltas = [row["metrics"]["confidence_delta_leaky_minus_clean"] for row in rows]
    future_items = 0
    removed_items = 0
    correctly_removed_items = 0
    unknown_temporal_items = 0
    pure_audited_rationales = 0
    responses = []
    elapsed = []
    for row in rows:
        temporal_check = (row.get("audit") or {}).get("temporal_check") or []
        future_ids = {
            item["evidence_id"]
            for item in temporal_check
            if item.get("temporal_status") == "future_leakage"
        }
        unknown_temporal_items += sum(
            item.get("temporal_status") == "unknown" for item in temporal_check
        )
        removed_ids = set((row.get("audit") or {}).get("removed_evidence_ids") or [])
        future_items += len(future_ids)
        removed_items += len(removed_ids)
        correctly_removed_items += len(future_ids & removed_ids)
        if not (cited_evidence_ids(row.get("audited") or {}) & future_ids):
            pure_audited_rationales += 1
        responses.extend(response_objects(row))
        if isinstance(row.get("elapsed_seconds"), (int, float)):
            elapsed.append(float(row["elapsed_seconds"]))

    prompt_tokens = sum(
        usage_value(response, "prompt_tokens", "input_tokens") for response in responses
    )
    completion_tokens = sum(
        usage_value(response, "completion_tokens", "output_tokens")
        for response in responses
    )
    total_tokens = sum(
        usage_value(response, "total_tokens") for response in responses
    )
    if not total_tokens:
        total_tokens = prompt_tokens + completion_tokens

    flip_low, flip_high = wilson_interval(flips, n)
    recovery_low, recovery_high = wilson_interval(recovered_flips, flips)
    summary = {
        "n_cases": n,
        "rationale_leakage_rate": rate(leakage, n),
        "prediction_flips": flips,
        "prediction_flip_rate": rate(flips, n),
        "prediction_flip_wilson_low": flip_low,
        "prediction_flip_wilson_high": flip_high,
        "revision_recovered_flips": recovered_flips,
        "audited_recovery_rate": rate(recovered_flips, flips),
        "audited_recovery_wilson_low": recovery_low,
        "audited_recovery_wilson_high": recovery_high,
        "audited_clean_agreement_rate": rate(clean_agreements, n),
        "clean_accuracy": rate(clean_correct, n),
        "leaky_accuracy": rate(leaky_correct, n),
        "audited_accuracy": rate(audited_correct, n),
        "future_removal_precision": rate(correctly_removed_items, removed_items),
        "future_removal_recall": rate(correctly_removed_items, future_items),
        "audited_rationale_purity_rate": rate(pure_audited_rationales, n),
        "unknown_temporal_items": unknown_temporal_items,
        "mean_confidence_delta": mean(deltas),
        "api_calls": len(responses),
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "total_elapsed_seconds": sum(elapsed),
        "mean_elapsed_seconds": mean(elapsed),
    }
    ablation_items = [
        item
        for row in rows
        for item in row.get("ablation", [])
    ]
    if ablation_items:
        future_ablation_items = [
            item for item in ablation_items if item.get("is_future_leakage")
        ]
        clean_ablation_items = [
            item for item in ablation_items if not item.get("is_future_leakage")
        ]
        flip_drivers = [
            item for item in ablation_items if item.get("is_flip_driver")
        ]
        future_flip_drivers = [
            item
            for item in future_ablation_items
            if item.get("is_flip_driver")
        ]
        future_confidence_deltas = [
            item["confidence_delta_removed_minus_full"]
            for item in future_ablation_items
        ]
        clean_confidence_deltas = [
            item["confidence_delta_removed_minus_full"]
            for item in clean_ablation_items
        ]
        summary.update(
            {
                "ablation_case_rate": sum(
                    1 for row in rows if row.get("ablation")
                )
                / n
                if n
                else 0.0,
                "ablation_items": len(ablation_items),
                "ablation_flip_driver_rate": len(flip_drivers)
                / len(ablation_items),
                "future_ablation_items": len(future_ablation_items),
                "future_evidence_flip_driver_rate": len(future_flip_drivers)
                / len(future_ablation_items)
                if future_ablation_items
                else 0.0,
                "mean_future_confidence_delta_removed_minus_full": mean(
                    future_confidence_deltas
                ),
                "mean_clean_confidence_delta_removed_minus_full": mean(
                    clean_confidence_deltas
                ),
            }
        )
    return summary


def write_summary(path: Path, summary: dict) -> None:
    write_summaries(path, [summary])


def write_summaries(path: Path, summaries: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(dict.fromkeys(key for row in summaries for key in row))
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(summaries)


def default_summary_path(input_path: Path) -> Path:
    stem = input_path.stem
    if stem.endswith("_results"):
        stem = stem[: -len("_results")]
    return input_path.with_name(f"{stem}_summary.csv")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", type=Path, default=RESULTS_DIR / "qwen_cases_pilot_results.jsonl"
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--group-by",
        default=None,
        help="Optional result field used to produce one summary row per group.",
    )
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    output_path = args.output or default_summary_path(args.input)
    if args.group_by:
        group_values = sorted({str(row.get(args.group_by) or "missing") for row in rows})
        summaries = []
        for value in group_values:
            group_rows = [
                row for row in rows if str(row.get(args.group_by) or "missing") == value
            ]
            summaries.append({args.group_by: value, **summarize(group_rows)})
        write_summaries(output_path, summaries)
        print(json.dumps(summaries, indent=2, ensure_ascii=False))
    else:
        summary = summarize(rows)
        write_summary(output_path, summary)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

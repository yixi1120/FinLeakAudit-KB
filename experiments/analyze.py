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
    recovered = sum(
        1 for row in rows if row["metrics"]["audited_recovered_clean_direction"]
    )
    deltas = [row["metrics"]["confidence_delta_leaky_minus_clean"] for row in rows]
    flip_low, flip_high = wilson_interval(flips, n)
    summary = {
        "n_cases": n,
        "rationale_leakage_rate": leakage / n if n else 0.0,
        "prediction_flip_rate": flips / n if n else 0.0,
        "prediction_flip_wilson_low": flip_low,
        "prediction_flip_wilson_high": flip_high,
        "audited_recovery_rate": recovered / n if n else 0.0,
        "mean_confidence_delta": mean(deltas),
    }
    ablation_items = [
        item
        for row in rows
        for item in row.get("ablation", [])
    ]
    if ablation_items:
        future_items = [
            item for item in ablation_items if item.get("is_future_leakage")
        ]
        clean_items = [
            item for item in ablation_items if not item.get("is_future_leakage")
        ]
        flip_drivers = [
            item for item in ablation_items if item.get("is_flip_driver")
        ]
        future_flip_drivers = [
            item for item in future_items if item.get("is_flip_driver")
        ]
        future_confidence_deltas = [
            item["confidence_delta_removed_minus_full"]
            for item in future_items
        ]
        clean_confidence_deltas = [
            item["confidence_delta_removed_minus_full"]
            for item in clean_items
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
                "future_ablation_items": len(future_items),
                "future_evidence_flip_driver_rate": len(future_flip_drivers)
                / len(future_items)
                if future_items
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
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary), lineterminator="\n")
        writer.writeheader()
        writer.writerow(summary)


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
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    summary = summarize(rows)
    output_path = args.output or default_summary_path(args.input)
    write_summary(output_path, summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

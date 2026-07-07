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
    return {
        "n_cases": n,
        "rationale_leakage_rate": leakage / n if n else 0.0,
        "prediction_flip_rate": flips / n if n else 0.0,
        "prediction_flip_wilson_low": flip_low,
        "prediction_flip_wilson_high": flip_high,
        "audited_recovery_rate": recovered / n if n else 0.0,
        "mean_confidence_delta": mean(deltas),
    }


def write_summary(path: Path, summary: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(summary))
        writer.writeheader()
        writer.writerow(summary)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input", type=Path, default=RESULTS_DIR / "qwen_pilot_results.jsonl"
    )
    parser.add_argument("--output", type=Path, default=RESULTS_DIR / "summary.csv")
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    summary = summarize(rows)
    write_summary(args.output, summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


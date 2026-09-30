#!/usr/bin/env python3
"""Freeze offline eligibility for the Novel-safe Backfill ablation."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from run_natural_experiment import prepare_event
from run_natural_refill_baseline import build_novel_safe_refilled_evidence


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS = ROOT / "experiments" / "analysis"
WIKI = ROOT / "wiki" / "experiments"
DEFAULT_CSV = ANALYSIS / "novel_safe_backfill_eligibility_v1.csv"
DEFAULT_REPORT = WIKI / "novel_safe_backfill_eligibility_2026_09_30.md"


def eligibility_rows(top_k: int = 8) -> list[dict]:
    rows = []
    for index in range(1, 11):
        event_id = f"natural_{index:03d}"
        prepared = prepare_event(event_id, top_k=top_k)
        refilled, added, metadata = build_novel_safe_refilled_evidence(
            prepared, top_k
        )
        rows.append(
            {
                "event_id": event_id,
                "ticker": prepared["manifest"]["ticker"],
                "top_k": top_k,
                "sparse_count": len(prepared["audited_evidence"]),
                "backfill_needed": metadata["novel_safe_backfill_needed"],
                "cutoff_safe_pool_count": metadata["cutoff_safe_pool_count"],
                "novel_eligible_candidate_count": metadata[
                    "novel_safe_eligible_candidate_count"
                ],
                "novel_added_count": len(added),
                "novel_refilled_count": len(refilled),
                "novel_safe_backfill_complete": metadata[
                    "novel_safe_backfill_complete"
                ],
                "added_evidence_ids": "|".join(added),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def write_report(path: Path, rows: list[dict]) -> None:
    complete = [row for row in rows if row["novel_safe_backfill_complete"]]
    incomplete = [row for row in rows if not row["novel_safe_backfill_complete"]]
    lines = [
        "---",
        "title: Novel-safe Backfill offline eligibility",
        "date: 2026-09-30",
        "status: frozen-before-model-calls",
        "---",
        "",
        "# Scope",
        "",
        "This check excludes the Clean top-k only for newly added evidence. Safe",
        "survivors from the actual Unfiltered context are retained. Candidates are",
        "ranked using the frozen cutoff-time lexical retrieval and parent-document cap.",
        "No outcome label or model prediction is used.",
        "",
        "# Eligibility result",
        "",
        f"{len(complete)}/10 events can be refilled to top-k using cutoff-safe evidence",
        "outside the Clean top-k. The remaining events are frozen as incomplete and",
        "must not be silently included in a complete-case model comparison.",
        "",
        "| Event | Ticker | Sparse | Needed | Safe pool | Novel candidates | Added | Complete |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in rows:
        lines.append(
            f"| {row['event_id']} | {row['ticker']} | {row['sparse_count']} | "
            f"{row['backfill_needed']} | {row['cutoff_safe_pool_count']} | "
            f"{row['novel_eligible_candidate_count']} | {row['novel_added_count']} | "
            f"{'yes' if row['novel_safe_backfill_complete'] else 'no'} |"
        )
    lines.extend(
        [
            "",
            "# Frozen complete-case set",
            "",
            ", ".join(row["event_id"] for row in complete),
            "",
            "# Frozen incomplete set",
            "",
            ", ".join(row["event_id"] for row in incomplete),
            "",
            "# Interpretation boundary",
            "",
            "- This is an input-eligibility result, not a model-performance result.",
            "- Complete-case model results will be conditional on this six-event subset.",
            "- Expanding the four incomplete candidate pools requires a separately frozen",
            "  source-collection protocol; sources must not be chosen using outcomes.",
            "- The workshop paper remains unchanged until model calls and analysis finish.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--top-k", type=int, default=8)
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    rows = eligibility_rows(args.top_k)
    write_csv(args.csv, rows)
    write_report(args.report, rows)
    print(f"wrote {args.csv}")
    print(f"wrote {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

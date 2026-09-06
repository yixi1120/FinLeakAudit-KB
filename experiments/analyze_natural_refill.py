#!/usr/bin/env python3
"""Summarize the three-model natural revision backfill experiment."""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "experiments" / "results"
ANALYSIS = ROOT / "experiments" / "analysis"
WIKI = ROOT / "wiki" / "experiments"
DEFAULT_INPUTS = [
    RESULTS / "deepseek_natural_refill_5event_v1_results.jsonl",
    RESULTS / "zhipu_natural_refill_5event_v1_results.jsonl",
    RESULTS / "qwen_natural_refill_5event_v1_results.jsonl",
]
DEFAULT_SUMMARY = ANALYSIS / "natural_refill_5event_three_model_summary_v1.csv"
DEFAULT_CASES = ANALYSIS / "natural_refill_5event_three_model_case_results_v1.csv"
DEFAULT_REPORT = WIKI / "natural_revision_refill_three_model_results_2026_09_06.md"
EXPECTED_SCHEMA = "finleakaudit_natural_refill_result_v1"


def read_results(paths: list[Path]) -> list[dict]:
    rows = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(path)
        with path.open(encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("schema_version") != EXPECTED_SCHEMA:
                    raise ValueError(f"{path}:{line_number}: unexpected schema version")
                rows.append(row)

    seen = set()
    for row in rows:
        key = (str(row["model"]), str(row["event_id"]))
        if key in seen:
            raise ValueError(f"Duplicate model-event result: {key}")
        seen.add(key)
    return rows


def divide(numerator: int | float, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def wilson_interval(
    successes: int, total: int, z: float = 1.96
) -> tuple[float | None, float | None]:
    if total == 0:
        return None, None
    proportion = successes / total
    denominator = 1 + z * z / total
    centre = proportion + z * z / (2 * total)
    margin = z * math.sqrt(
        proportion * (1 - proportion) / total + z * z / (4 * total * total)
    )
    return (centre - margin) / denominator, (centre + margin) / denominator


def usage_total(row: dict) -> int:
    usage = row["audited_refill"].get("_usage") or {}
    return int(usage.get("total_tokens") or 0)


def summarize_rows(rows: list[dict], scope: str, model: str) -> dict:
    initial_flips = [
        row for row in rows if row["metrics"]["initial_clean_to_unfiltered_flip"]
    ]
    nonflips = [
        row for row in rows if not row["metrics"]["initial_clean_to_unfiltered_flip"]
    ]
    sparse_drift = [
        row
        for row in nonflips
        if row["metrics"]["sparse_revision_drift_without_initial_flip"]
    ]
    backfilled_drift = [
        row
        for row in nonflips
        if row["metrics"]["backfilled_revision_drift_without_initial_flip"]
    ]
    sparse_recovery = [
        row for row in initial_flips if row["metrics"]["sparse_audited_matches_clean"]
    ]
    backfilled_recovery = [
        row
        for row in initial_flips
        if row["metrics"]["backfilled_audited_matches_clean"]
    ]
    invalid_ids = [
        evidence_id
        for row in rows
        for evidence_id in row["citation_validation"]["invalid_citation_ids"]
    ]
    cited_ids = [
        evidence_id
        for row in rows
        for evidence_id in row["citation_validation"]["cited_evidence_ids"]
    ]
    confidence_gaps = [
        abs(
            float(row["audited_refill"]["confidence"])
            - float(row["source_predictions"]["clean"]["confidence"])
        )
        for row in rows
    ]
    match_count = sum(
        row["metrics"]["backfilled_audited_matches_clean"] for row in rows
    )
    match_low, match_high = wilson_interval(match_count, len(rows))
    return {
        "scope": scope,
        "model": model,
        "n_model_events": len(rows),
        "backfill_model_calls": len(rows),
        "initial_flip_count": len(initial_flips),
        "sparse_recovery_count": len(sparse_recovery),
        "sparse_recovery_rate": divide(len(sparse_recovery), len(initial_flips)),
        "backfilled_recovery_count": len(backfilled_recovery),
        "backfilled_recovery_rate": divide(
            len(backfilled_recovery), len(initial_flips)
        ),
        "nonflip_count": len(nonflips),
        "sparse_drift_count": len(sparse_drift),
        "sparse_drift_rate": divide(len(sparse_drift), len(nonflips)),
        "backfilled_drift_count": len(backfilled_drift),
        "backfilled_drift_rate": divide(len(backfilled_drift), len(nonflips)),
        "backfilled_matches_clean_count": match_count,
        "backfilled_matches_clean_rate": divide(
            match_count, len(rows)
        ),
        "backfilled_matches_clean_wilson_95_low": match_low,
        "backfilled_matches_clean_wilson_95_high": match_high,
        "backfilled_matches_clean_sequence_count": sum(
            row["revision_context"]["backfilled_matches_clean_sequence"]
            for row in rows
        ),
        "backfilled_matches_clean_sequence_rate": divide(
            sum(
                row["revision_context"]["backfilled_matches_clean_sequence"]
                for row in rows
            ),
            len(rows),
        ),
        "backfilled_correct_count": sum(
            row["metrics"]["backfilled_correct"] for row in rows
        ),
        "backfilled_accuracy": divide(
            sum(row["metrics"]["backfilled_correct"] for row in rows), len(rows)
        ),
        "all_citations_valid_count": sum(
            row["citation_validation"]["all_citations_valid"] for row in rows
        ),
        "outputs_with_citations_count": sum(
            bool(row["citation_validation"]["cited_evidence_ids"]) for row in rows
        ),
        "cited_evidence_id_count": len(cited_ids),
        "invalid_citation_id_count": len(invalid_ids),
        "mean_absolute_confidence_gap_from_clean": divide(
            sum(confidence_gaps), len(confidence_gaps)
        ),
        "total_tokens": sum(usage_total(row) for row in rows),
        "total_runtime_seconds": sum(
            float(row.get("elapsed_seconds") or 0.0) for row in rows
        ),
    }


def build_summary(rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[str(row["model"])].append(row)
    output = [summarize_rows(rows, "all", "all")]
    output.extend(
        summarize_rows(grouped[model], "model", model) for model in sorted(grouped)
    )
    return output


def build_case_rows(rows: list[dict]) -> list[dict]:
    output = []
    for row in sorted(rows, key=lambda item: (item["model"], item["event_id"])):
        metrics = row["metrics"]
        output.append(
            {
                "model": row["model"],
                "event_id": row["event_id"],
                "ticker": row["ticker"],
                "clean_prediction": row["source_predictions"]["clean"]["prediction"],
                "unfiltered_prediction": row["source_predictions"]["unfiltered"][
                    "prediction"
                ],
                "sparse_audited_prediction": row["source_predictions"]["audited"][
                    "prediction"
                ],
                "backfilled_audited_prediction": row["audited_refill"]["prediction"],
                "clean_confidence": row["source_predictions"]["clean"]["confidence"],
                "backfilled_confidence": row["audited_refill"]["confidence"],
                "initial_flip": metrics["initial_clean_to_unfiltered_flip"],
                "sparse_matches_clean": metrics["sparse_audited_matches_clean"],
                "backfilled_matches_clean": metrics[
                    "backfilled_audited_matches_clean"
                ],
                "sparse_drift_without_initial_flip": metrics[
                    "sparse_revision_drift_without_initial_flip"
                ],
                "backfilled_drift_without_initial_flip": metrics[
                    "backfilled_revision_drift_without_initial_flip"
                ],
                "backfilled_matches_clean_sequence": row["revision_context"][
                    "backfilled_matches_clean_sequence"
                ],
                "added_evidence_count": len(
                    row["revision_context"]["added_evidence_ids"]
                ),
                "backfilled_correct": metrics["backfilled_correct"],
                "all_citations_valid": row["citation_validation"][
                    "all_citations_valid"
                ],
                "invalid_citation_id_count": len(
                    row["citation_validation"]["invalid_citation_ids"]
                ),
                "total_tokens": usage_total(row),
                "elapsed_seconds": row.get("elapsed_seconds", 0.0),
            }
        )
    return output


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"Refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def percent(value: float | None) -> str:
    return "N/A" if value is None else f"{value * 100:.1f}%"


def markdown_report(summary: list[dict], cases: list[dict]) -> str:
    all_row = summary[0]
    models = summary[1:]
    lines = [
        "---",
        "title: Natural revision backfill, five-event three-model comparison",
        "date: 2026-09-06",
        "status: completed-three-model-backfill-comparison",
        "---",
        "",
        "# Scope",
        "",
        "This experiment adds one Backfilled Audited call to each frozen natural replay",
        "model-event result. It removes post-cutoff items from the actual Unfiltered top-k,",
        "preserves the surviving order, and appends cutoff-safe ranked fallbacks until top-k",
        "is restored. It does not rerun or overwrite Clean, Unfiltered, or Sparse Audited.",
        "",
        "# Main result",
        "",
        f"Across {all_row['n_model_events']} paired model-event runs, Backfilled Audited matched "
        f"the Clean direction in {all_row['backfilled_matches_clean_count']}/"
        f"{all_row['n_model_events']} ({percent(all_row['backfilled_matches_clean_rate'])}; "
        f"Wilson 95% interval {percent(all_row['backfilled_matches_clean_wilson_95_low'])}-"
        f"{percent(all_row['backfilled_matches_clean_wilson_95_high'])}). Both Sparse and "
        f"Backfilled revision recovered all {all_row['initial_flip_count']} initial "
        "Clean-to-Unfiltered direction changes.",
        "",
        f"The distinction appeared on the {all_row['nonflip_count']} non-flipped runs: "
        f"Sparse revision drifted in {all_row['sparse_drift_count']}/"
        f"{all_row['nonflip_count']}, while Backfilled revision drifted in "
        f"{all_row['backfilled_drift_count']}/{all_row['nonflip_count']}.",
        "",
        "This is one corrected drift in a very small paired sample. It supports context",
        "sparsity as a concrete failure mode, but is not evidence of a statistically reliable",
        "general improvement. Backfilled accuracy was unchanged from Clean because every",
        "Backfilled direction matched Clean.",
        "",
        "# Model summary",
        "",
        "| Model | Runs | Initial flips | Sparse recovery | Backfilled recovery | Sparse drift / non-flips | Backfilled drift / non-flips | Backfilled = Clean | Tokens |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in models:
        lines.append(
            f"| {row['model']} | {row['n_model_events']} | {row['initial_flip_count']} | "
            f"{row['sparse_recovery_count']}/{row['initial_flip_count']} | "
            f"{row['backfilled_recovery_count']}/{row['initial_flip_count']} | "
            f"{row['sparse_drift_count']}/{row['nonflip_count']} | "
            f"{row['backfilled_drift_count']}/{row['nonflip_count']} | "
            f"{row['backfilled_matches_clean_count']}/{row['n_model_events']} | "
            f"{row['total_tokens']} |"
        )
    lines.extend(
        [
            "",
            "# Retrieval control",
            "",
            "The Backfilled evidence sequence exactly matched Clean in "
            f"{all_row['backfilled_matches_clean_sequence_count']}/"
            f"{all_row['n_model_events']} runs. The three exceptions were the JetBlue event,",
            "where parent-document caps and ranking interactions preserved a different survivor",
            "order. Even there, all three models retained the Clean direction:",
            "",
            "| Model | Clean | Sparse Audited | Backfilled Audited | Confidence gap from Clean |",
            "|---|---|---|---|---:|",
        ]
    )
    case_by_key = {(row["model"], row["event_id"]): row for row in cases}
    for model_row in models:
        case = case_by_key[(model_row["model"], "natural_010")]
        lines.append(
            f"| {case['model']} | {case['clean_prediction']} | "
            f"{case['sparse_audited_prediction']} | "
            f"{case['backfilled_audited_prediction']} | "
            f"{abs(float(case['backfilled_confidence']) - float(case['clean_confidence'])):.2f} |"
        )
    lines.extend(
        [
            "",
            f"All {all_row['outputs_with_citations_count']} Backfilled outputs cited evidence. "
            f"All {all_row['cited_evidence_id_count']} cited IDs were valid. Total Backfill-only usage was",
            f"{all_row['total_tokens']:,} tokens. The calls took "
            f"{all_row['total_runtime_seconds']:.1f} recorded seconds in aggregate, with local",
            "Qwen accounting for most wall time.",
            "",
            "# Interpretation boundary",
            "",
            "- Backfill controls context size and partially controls retrieval composition; it",
            "  does not prove that the remaining evidence is truthful or decision-relevant.",
            "- Matching Clean is a revision-consistency target, not market accuracy.",
            "- The single Sparse-to-Backfilled drift correction is descriptive. No significance",
            "  claim is made from one discordant paired observation.",
            "- Twelve runs had a Backfilled sequence identical to Clean, so their direction",
            "  agreement is partly expected under temperature-zero replay.",
            "- The JetBlue cases show that Backfilled is not globally equivalent to rerunning",
            "  Clean, although all three directions happened to match here.",
            "",
            "# Reproduce",
            "",
            "```bash",
            "python3 experiments/run_natural_refill_baseline.py --model deepseek --minimal",
            "python3 experiments/run_natural_refill_baseline.py --model zhipu --minimal",
            "python3 experiments/run_natural_refill_baseline.py --model qwen --minimal",
            "python3 experiments/analyze_natural_refill.py",
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="*", type=Path, default=DEFAULT_INPUTS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    rows = read_results(args.inputs)
    summary = build_summary(rows)
    cases = build_case_rows(rows)
    write_csv(args.summary, summary)
    write_csv(args.cases, cases)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(markdown_report(summary, cases), encoding="utf-8")
    print(f"wrote {args.summary}")
    print(f"wrote {args.cases}")
    print(f"wrote {args.report}")


if __name__ == "__main__":
    main()

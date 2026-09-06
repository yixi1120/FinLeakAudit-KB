#!/usr/bin/env python3
"""Join the two frozen five-event batches into the 10-event paper analysis."""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

from analyze_natural_experiment import (
    citation_validation,
    read_results as read_base_results,
    wilson_interval,
)
from analyze_natural_refill import read_results as read_refill_results
from build_paper_results_snapshot import svg_bar_chart


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "experiments" / "results"
ANALYSIS = ROOT / "experiments" / "analysis"
WIKI = ROOT / "wiki" / "experiments"
MODELS = ("deepseek", "zhipu", "qwen")
BASE_INPUTS = [
    RESULTS / f"{model}_{batch}_results.jsonl"
    for model in MODELS
    for batch in ("natural_pit_5event_v1", "natural_pit_remaining5_v1")
]
REFILL_INPUTS = [
    RESULTS / f"{model}_{batch}_results.jsonl"
    for model in MODELS
    for batch in ("natural_refill_5event_v1", "natural_refill_remaining5_v1")
]
DEFAULT_SUMMARY = ANALYSIS / "natural_pit_10event_three_model_summary_v1.csv"
DEFAULT_CASES = ANALYSIS / "natural_pit_10event_three_model_case_results_v1.csv"
DEFAULT_REPORT = WIKI / "natural_pit_10event_three_model_results_2026_09_06.md"
DEFAULT_FIGURE = WIKI / "figures" / "natural_10event_revision_comparison.svg"
CONDITIONS = ("clean", "unfiltered", "audited")


def divide(numerator: int | float, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def usage_total(prediction: dict) -> int:
    usage = prediction.get("_usage") or {}
    return int(usage.get("total_tokens") or 0)


def exact_mcnemar_p(sparse_only: int, backfill_only: int) -> float | None:
    discordant = sparse_only + backfill_only
    if discordant == 0:
        return None
    tail = min(sparse_only, backfill_only)
    probability = sum(
        math.comb(discordant, index) * 0.5**discordant
        for index in range(tail + 1)
    )
    return min(1.0, 2 * probability)


def join_results(base_rows: list[dict], refill_rows: list[dict]) -> list[tuple[dict, dict]]:
    base = {(row["model"], row["event_id"]): row for row in base_rows}
    refill = {(row["model"], row["event_id"]): row for row in refill_rows}
    if set(base) != set(refill):
        missing_refill = sorted(set(base) - set(refill))
        missing_base = sorted(set(refill) - set(base))
        raise ValueError(
            f"Base/refill keys differ; missing_refill={missing_refill}; "
            f"missing_base={missing_base}"
        )
    joined = [(base[key], refill[key]) for key in sorted(base)]
    for base_row, refill_row in joined:
        expected = {
            condition: base_row[condition]["prediction"]
            for condition in CONDITIONS
        }
        stored = {
            condition: refill_row["source_predictions"][condition]["prediction"]
            for condition in CONDITIONS
        }
        if expected != stored:
            raise ValueError(
                f"{base_row['model']}/{base_row['event_id']}: source predictions drifted"
            )
    return joined


def summarize(rows: list[tuple[dict, dict]], scope: str, model: str) -> dict:
    flips = [
        pair
        for pair in rows
        if pair[0]["clean"]["prediction"] != pair[0]["unfiltered"]["prediction"]
    ]
    nonflips = [pair for pair in rows if pair not in flips]
    sparse_matches = [
        pair
        for pair in rows
        if pair[0]["audited"]["prediction"] == pair[0]["clean"]["prediction"]
    ]
    backfill_matches = [
        pair
        for pair in rows
        if pair[1]["audited_refill"]["prediction"]
        == pair[0]["clean"]["prediction"]
    ]
    sparse_recovery = [pair for pair in flips if pair in sparse_matches]
    backfill_recovery = [pair for pair in flips if pair in backfill_matches]
    sparse_drift = [pair for pair in nonflips if pair not in sparse_matches]
    backfill_drift = [pair for pair in nonflips if pair not in backfill_matches]
    sparse_only = sum(
        pair in sparse_matches and pair not in backfill_matches for pair in rows
    )
    backfill_only = sum(
        pair in backfill_matches and pair not in sparse_matches for pair in rows
    )
    base_checks = [
        citation_validation(base, condition)
        for base, _ in rows
        for condition in CONDITIONS
    ]
    refill_checks = [refill["citation_validation"] for _, refill in rows]
    match_low, match_high = wilson_interval(len(backfill_matches), len(rows))
    recovery_low, recovery_high = wilson_interval(
        len(backfill_recovery), len(flips)
    )
    return {
        "scope": scope,
        "model": model,
        "n_events": len({base["event_id"] for base, _ in rows}),
        "n_model_events": len(rows),
        "retained_prediction_calls": len(rows) * 4,
        "future_cited_count": sum(
            base["metrics"]["future_evidence_cited"] for base, _ in rows
        ),
        "future_cited_rate": divide(
            sum(base["metrics"]["future_evidence_cited"] for base, _ in rows),
            len(rows),
        ),
        "initial_flip_count": len(flips),
        "initial_flip_rate": divide(len(flips), len(rows)),
        "sparse_recovery_count": len(sparse_recovery),
        "sparse_recovery_rate": divide(len(sparse_recovery), len(flips)),
        "backfill_recovery_count": len(backfill_recovery),
        "backfill_recovery_rate": divide(len(backfill_recovery), len(flips)),
        "backfill_recovery_wilson_95_low": recovery_low,
        "backfill_recovery_wilson_95_high": recovery_high,
        "nonflip_count": len(nonflips),
        "sparse_drift_count": len(sparse_drift),
        "sparse_drift_rate": divide(len(sparse_drift), len(nonflips)),
        "backfill_drift_count": len(backfill_drift),
        "backfill_drift_rate": divide(len(backfill_drift), len(nonflips)),
        "sparse_matches_clean_count": len(sparse_matches),
        "sparse_matches_clean_rate": divide(len(sparse_matches), len(rows)),
        "backfill_matches_clean_count": len(backfill_matches),
        "backfill_matches_clean_rate": divide(len(backfill_matches), len(rows)),
        "backfill_matches_clean_wilson_95_low": match_low,
        "backfill_matches_clean_wilson_95_high": match_high,
        "backfill_only_match_count": backfill_only,
        "sparse_only_match_count": sparse_only,
        "paired_exact_mcnemar_p": exact_mcnemar_p(sparse_only, backfill_only),
        "backfill_matches_clean_sequence_count": sum(
            refill["revision_context"]["backfilled_matches_clean_sequence"]
            for _, refill in rows
        ),
        "clean_accuracy": divide(
            sum(base["clean"]["prediction"] == base["outcome_label"] for base, _ in rows),
            len(rows),
        ),
        "unfiltered_accuracy": divide(
            sum(
                base["unfiltered"]["prediction"] == base["outcome_label"]
                for base, _ in rows
            ),
            len(rows),
        ),
        "sparse_accuracy": divide(
            sum(
                base["audited"]["prediction"] == base["outcome_label"]
                for base, _ in rows
            ),
            len(rows),
        ),
        "backfill_accuracy": divide(
            sum(
                refill["audited_refill"]["prediction"] == base["outcome_label"]
                for base, refill in rows
            ),
            len(rows),
        ),
        "base_invalid_citation_output_count": sum(
            not check["all_citations_valid"] for check in base_checks
        ),
        "base_invalid_citation_id_count": sum(
            len(check["invalid_citation_ids"]) for check in base_checks
        ),
        "refill_invalid_citation_output_count": sum(
            not check["all_citations_valid"] for check in refill_checks
        ),
        "refill_invalid_citation_id_count": sum(
            len(check["invalid_citation_ids"]) for check in refill_checks
        ),
        "retry_event_count": sum(int(base.get("attempt") or 1) > 1 for base, _ in rows)
        + sum(int(refill.get("attempt") or 1) > 1 for _, refill in rows),
        "total_tokens": sum(
            usage_total(base[condition])
            for base, _ in rows
            for condition in CONDITIONS
        )
        + sum(usage_total(refill["audited_refill"]) for _, refill in rows),
    }


def build_summary(joined: list[tuple[dict, dict]]) -> list[dict]:
    grouped: dict[str, list[tuple[dict, dict]]] = defaultdict(list)
    for pair in joined:
        grouped[pair[0]["model"]].append(pair)
    output = [summarize(joined, "all", "all")]
    output.extend(
        summarize(grouped[model], "model", model) for model in sorted(grouped)
    )
    return output


def build_cases(joined: list[tuple[dict, dict]]) -> list[dict]:
    output = []
    for base, refill in joined:
        base_invalid = sum(
            len(citation_validation(base, condition)["invalid_citation_ids"])
            for condition in CONDITIONS
        )
        output.append(
            {
                "model": base["model"],
                "event_id": base["event_id"],
                "ticker": base["ticker"],
                "outcome_label": base["outcome_label"],
                "clean": base["clean"]["prediction"],
                "unfiltered": base["unfiltered"]["prediction"],
                "sparse_audited": base["audited"]["prediction"],
                "backfilled_audited": refill["audited_refill"]["prediction"],
                "initial_flip": base["clean"]["prediction"]
                != base["unfiltered"]["prediction"],
                "sparse_matches_clean": base["audited"]["prediction"]
                == base["clean"]["prediction"],
                "backfill_matches_clean": refill["audited_refill"]["prediction"]
                == base["clean"]["prediction"],
                "backfill_matches_clean_sequence": refill["revision_context"][
                    "backfilled_matches_clean_sequence"
                ],
                "base_invalid_citation_ids": base_invalid,
                "refill_invalid_citation_ids": len(
                    refill["citation_validation"]["invalid_citation_ids"]
                ),
                "base_attempt": int(base.get("attempt") or 1),
                "refill_attempt": int(refill.get("attempt") or 1),
            }
        )
    return output


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def percent(value: float | None) -> str:
    return "N/A" if value is None else f"{value * 100:.1f}%"


def markdown_report(summary: list[dict], cases: list[dict]) -> str:
    all_row = summary[0]
    corrected = [
        row
        for row in cases
        if not row["sparse_matches_clean"] and row["backfill_matches_clean"]
    ]
    lines = [
        "---",
        "title: Natural point-in-time replay, 10-event three-model result",
        "date: 2026-09-06",
        "status: completed-10-event-controlled-natural-replay",
        "---",
        "",
        "# Scope",
        "",
        "This analysis joins two frozen five-event batches without rewriting their raw",
        "results. Ten events were evaluated with DeepSeek, Zhipu, and local Qwen under",
        "Clean, outcome-bounded Unfiltered, Sparse Audited, and rank-preserving Backfilled",
        "Audited conditions. This remains a constructed primary-source candidate-feed stress",
        "test, not a production retrieval trace or a leakage-prevalence estimate.",
        "",
        "# Main result",
        "",
        f"Across {all_row['n_model_events']} model-event runs and "
        f"{all_row['retained_prediction_calls']} retained predictions, future evidence was",
        f"explicitly cited in {all_row['future_cited_count']}/"
        f"{all_row['n_model_events']} Unfiltered runs and changed direction in "
        f"{all_row['initial_flip_count']}/{all_row['n_model_events']}.",
        "",
        f"Sparse deletion recovered {all_row['sparse_recovery_count']}/"
        f"{all_row['initial_flip_count']} flips. Backfilled revision recovered "
        f"{all_row['backfill_recovery_count']}/{all_row['initial_flip_count']} "
        f"({percent(all_row['backfill_recovery_rate'])}; Wilson 95% interval "
        f"{percent(all_row['backfill_recovery_wilson_95_low'])}-"
        f"{percent(all_row['backfill_recovery_wilson_95_high'])}). On "
        f"{all_row['nonflip_count']} non-flipped runs, Sparse drifted in "
        f"{all_row['sparse_drift_count']}/{all_row['nonflip_count']} and Backfilled in "
        f"{all_row['backfill_drift_count']}/{all_row['nonflip_count']}.",
        "",
        f"Overall, Sparse matched Clean in {all_row['sparse_matches_clean_count']}/"
        f"{all_row['n_model_events']}, while Backfilled matched Clean in "
        f"{all_row['backfill_matches_clean_count']}/{all_row['n_model_events']} "
        f"(Wilson 95% interval {percent(all_row['backfill_matches_clean_wilson_95_low'])}-"
        f"{percent(all_row['backfill_matches_clean_wilson_95_high'])}). The exact paired",
        f"McNemar p-value is {all_row['paired_exact_mcnemar_p']:.3f}; this sample therefore",
        "does not establish a statistically reliable general advantage.",
        "",
        "![Sparse and backfilled revision comparison](figures/natural_10event_revision_comparison.svg)",
        "",
        "# Model summary",
        "",
        "| Model | Runs | Future cited | Flips | Sparse recovery | Backfill recovery | Sparse drift / non-flips | Backfill drift / non-flips | Backfill = Clean |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary[1:]:
        lines.append(
            f"| {row['model']} | {row['n_model_events']} | "
            f"{row['future_cited_count']}/{row['n_model_events']} | "
            f"{row['initial_flip_count']} | "
            f"{row['sparse_recovery_count']}/{row['initial_flip_count']} | "
            f"{row['backfill_recovery_count']}/{row['initial_flip_count']} | "
            f"{row['sparse_drift_count']}/{row['nonflip_count']} | "
            f"{row['backfill_drift_count']}/{row['nonflip_count']} | "
            f"{row['backfill_matches_clean_count']}/{row['n_model_events']} |"
        )
    lines.extend(
        [
            "",
            "# Cases corrected by Backfill",
            "",
            "| Model | Event | Clean | Unfiltered | Sparse | Backfilled | Type |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for row in corrected:
        failure_type = "recovery failure" if row["initial_flip"] else "non-flip drift"
        lines.append(
            f"| {row['model']} | {row['event_id']} ({row['ticker']}) | "
            f"{row['clean']} | {row['unfiltered']} | {row['sparse_audited']} | "
            f"{row['backfilled_audited']} | {failure_type} |"
        )
    lines.extend(
        [
            "",
            "# Accuracy and citation integrity",
            "",
            f"Outcome accuracy was {percent(all_row['clean_accuracy'])} Clean, "
            f"{percent(all_row['unfiltered_accuracy'])} Unfiltered, "
            f"{percent(all_row['sparse_accuracy'])} Sparse, and "
            f"{percent(all_row['backfill_accuracy'])} Backfilled. The Unfiltered increase is",
            "hindsight inflation and is not valid forecasting performance. Backfilled returns",
            "to Clean accuracy because all Backfilled directions match Clean.",
            "",
            f"Citation validation found {all_row['base_invalid_citation_id_count']} invalid IDs",
            f"across {all_row['base_invalid_citation_output_count']}/"
            f"{all_row['n_model_events'] * 3} base-condition outputs and "
            f"{all_row['refill_invalid_citation_id_count']} invalid IDs across "
            f"{all_row['refill_invalid_citation_output_count']}/"
            f"{all_row['n_model_events']} Backfilled outputs. Errors were preserved rather than",
            "silently normalized. They include shortened document IDs, fabricated IDs, headings",
            "used as IDs, and valid IDs concatenated with filenames.",
            "",
            f"Backfilled evidence order exactly matched Clean in "
            f"{all_row['backfill_matches_clean_sequence_count']}/"
            f"{all_row['n_model_events']} runs. One Qwen event required a recorded event-level",
            "retry after a transient timeout. Total retained-output usage was "
            f"{all_row['total_tokens']:,} tokens.",
            "",
            "# Interpretation boundary",
            "",
            "- The main result is revision consistency, not improved market accuracy.",
            "- Backfill corrected three observed Sparse mismatches, but 24/30 Backfilled inputs",
            "  were identical to Clean and the exact paired test is not significant.",
            "- Timestamp validity does not guarantee evidence truthfulness or relevance.",
            "- Invalid model-generated citation IDs remain an interface and attribution failure.",
            "- The event set is purposive and too small for prevalence claims.",
            "",
            "# Reproduce",
            "",
            "```bash",
            "python3 experiments/analyze_natural_10event.py",
            "python3 -m unittest tests.test_analyze_natural_10event -v",
            "```",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--figure", type=Path, default=DEFAULT_FIGURE)
    args = parser.parse_args()

    joined = join_results(
        read_base_results(BASE_INPUTS), read_refill_results(REFILL_INPUTS)
    )
    summary = build_summary(joined)
    cases = build_cases(joined)
    write_csv(args.summary, summary)
    write_csv(args.cases, cases)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(markdown_report(summary, cases), encoding="utf-8")
    overall = summary[0]
    svg_bar_chart(
        args.figure,
        "Natural Replay Revision Comparison",
        "Ten events x three models; exact counts are retained in the report",
        [
            "Sparse recovery",
            "Backfill recovery",
            "Sparse Clean match",
            "Backfill Clean match",
            "Sparse stability",
            "Backfill stability",
        ],
        [
            overall["sparse_recovery_rate"],
            overall["backfill_recovery_rate"],
            overall["sparse_matches_clean_rate"],
            overall["backfill_matches_clean_rate"],
            1 - overall["sparse_drift_rate"],
            1 - overall["backfill_drift_rate"],
        ],
        ["#6b7280", "#2f855a", "#6b7280", "#2f855a", "#6b7280", "#2f855a"],
        "Rate (%)",
    )
    print(f"wrote {args.summary}")
    print(f"wrote {args.cases}")
    print(f"wrote {args.report}")
    print(f"wrote {args.figure}")


if __name__ == "__main__":
    main()

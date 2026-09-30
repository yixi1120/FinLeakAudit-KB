#!/usr/bin/env python3
"""Analyze the frozen six-event Novel-safe Backfill ablation."""

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
MODELS = ("deepseek", "zhipu", "qwen")
ELIGIBLE_EVENTS = {
    "natural_002",
    "natural_005",
    "natural_006",
    "natural_007",
    "natural_009",
    "natural_010",
}
BATCHES = (
    (
        "natural_pit_5event_v1",
        "natural_refill_5event_v1",
        "natural_novel_safe_refill_5event_v1",
    ),
    (
        "natural_pit_remaining5_v1",
        "natural_refill_remaining5_v1",
        "natural_novel_safe_refill_remaining5_v1",
    ),
)
DEFAULT_SUMMARY = ANALYSIS / "novel_safe_backfill_three_model_summary_v1.csv"
DEFAULT_CASES = ANALYSIS / "novel_safe_backfill_three_model_cases_v1.csv"
DEFAULT_REPORT = WIKI / "novel_safe_backfill_three_model_results_2026_09_30.md"


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(path)
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def index_rows(rows: list[dict], name: str) -> dict[tuple[str, str], dict]:
    indexed = {}
    for row in rows:
        key = (str(row["model"]), str(row["event_id"]))
        if key in indexed:
            raise ValueError(f"Duplicate {name} row: {key}")
        indexed[key] = row
    return indexed


def load_rows() -> list[dict]:
    base_rows = []
    standard_rows = []
    novel_rows = []
    for model in MODELS:
        for base_stem, standard_stem, novel_stem in BATCHES:
            base_rows.extend(read_jsonl(RESULTS / f"{model}_{base_stem}_results.jsonl"))
            standard_rows.extend(
                read_jsonl(RESULTS / f"{model}_{standard_stem}_results.jsonl")
            )
            novel_rows.extend(read_jsonl(RESULTS / f"{model}_{novel_stem}_results.jsonl"))

    base = index_rows(base_rows, "base")
    standard = index_rows(standard_rows, "standard")
    novel = index_rows(novel_rows, "novel")
    expected = {(model, event) for model in MODELS for event in ELIGIBLE_EVENTS}
    if set(novel) != expected:
        raise ValueError(
            f"Novel-safe keys differ; missing={sorted(expected - set(novel))}; "
            f"extra={sorted(set(novel) - expected)}"
        )

    output = []
    for key in sorted(expected):
        base_row = base[key]
        standard_row = standard[key]
        novel_row = novel[key]
        source = novel_row["source_predictions"]
        expected_source = {
            condition: base_row[condition]["prediction"]
            for condition in ("clean", "unfiltered", "audited")
        }
        stored_source = {
            condition: source[condition]["prediction"]
            for condition in ("clean", "unfiltered", "audited")
        }
        if expected_source != stored_source:
            raise ValueError(f"Source predictions drifted for {key}")
        if not novel_row["revision_context"]["novel_safe_backfill_complete"]:
            raise ValueError(f"Incomplete Novel-safe row entered analysis: {key}")
        if novel_row["revision_context"]["backfilled_matches_clean_sequence"]:
            raise ValueError(f"Novel-safe sequence unexpectedly equals Clean: {key}")

        clean = base_row["clean"]["prediction"]
        unfiltered = base_row["unfiltered"]["prediction"]
        sparse = base_row["audited"]["prediction"]
        standard_prediction = standard_row["audited_refill"]["prediction"]
        novel_prediction = novel_row["audited_refill"]["prediction"]
        output.append(
            {
                "model": key[0],
                "event_id": key[1],
                "ticker": base_row["ticker"],
                "clean": clean,
                "unfiltered": unfiltered,
                "sparse": sparse,
                "standard_backfill": standard_prediction,
                "novel_safe_backfill": novel_prediction,
                "initial_flip": clean != unfiltered,
                "sparse_matches_clean": sparse == clean,
                "standard_matches_clean": standard_prediction == clean,
                "novel_matches_clean": novel_prediction == clean,
                "novel_changed_sparse_direction": novel_prediction != sparse,
                "novel_matches_standard_direction": (
                    novel_prediction == standard_prediction
                ),
                "novel_clean_sequence_match": False,
                "novel_added_count": novel_row["revision_context"][
                    "novel_safe_backfill_count"
                ],
                "novel_clean_id_overlap": novel_row["revision_context"][
                    "novel_safe_clean_id_overlap"
                ],
                "all_citations_valid": novel_row["citation_validation"][
                    "all_citations_valid"
                ],
                "invalid_citation_id_count": len(
                    novel_row["citation_validation"]["invalid_citation_ids"]
                ),
                "total_tokens": int(
                    (novel_row["audited_refill"].get("_usage") or {}).get(
                        "total_tokens"
                    )
                    or 0
                ),
                "elapsed_seconds": float(novel_row.get("elapsed_seconds") or 0),
            }
        )
    return output


def divide(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def exact_mcnemar_p(first_only: int, second_only: int) -> float | None:
    discordant = first_only + second_only
    if discordant == 0:
        return None
    tail = min(first_only, second_only)
    probability = sum(
        math.comb(discordant, index) * 0.5**discordant
        for index in range(tail + 1)
    )
    return min(1.0, 2 * probability)


def summarize(rows: list[dict], scope: str, model: str) -> dict:
    flips = [row for row in rows if row["initial_flip"]]
    nonflips = [row for row in rows if not row["initial_flip"]]
    standard_only = sum(
        row["standard_matches_clean"] and not row["novel_matches_clean"]
        for row in rows
    )
    novel_only = sum(
        row["novel_matches_clean"] and not row["standard_matches_clean"]
        for row in rows
    )
    return {
        "scope": scope,
        "model": model,
        "n_model_events": len(rows),
        "initial_flip_count": len(flips),
        "nonflip_count": len(nonflips),
        "sparse_recovery_count": sum(row["sparse_matches_clean"] for row in flips),
        "standard_recovery_count": sum(
            row["standard_matches_clean"] for row in flips
        ),
        "novel_recovery_count": sum(row["novel_matches_clean"] for row in flips),
        "novel_recovery_rate": divide(
            sum(row["novel_matches_clean"] for row in flips), len(flips)
        ),
        "sparse_drift_count": sum(
            not row["sparse_matches_clean"] for row in nonflips
        ),
        "standard_drift_count": sum(
            not row["standard_matches_clean"] for row in nonflips
        ),
        "novel_drift_count": sum(
            not row["novel_matches_clean"] for row in nonflips
        ),
        "sparse_matches_clean_count": sum(row["sparse_matches_clean"] for row in rows),
        "standard_matches_clean_count": sum(
            row["standard_matches_clean"] for row in rows
        ),
        "novel_matches_clean_count": sum(row["novel_matches_clean"] for row in rows),
        "novel_matches_clean_rate": divide(
            sum(row["novel_matches_clean"] for row in rows), len(rows)
        ),
        "standard_only_match_count": standard_only,
        "novel_only_match_count": novel_only,
        "standard_vs_novel_exact_mcnemar_p": exact_mcnemar_p(
            standard_only, novel_only
        ),
        "novel_matches_standard_direction_count": sum(
            row["novel_matches_standard_direction"] for row in rows
        ),
        "novel_changed_sparse_direction_count": sum(
            row["novel_changed_sparse_direction"] for row in rows
        ),
        "novel_clean_sequence_match_count": sum(
            row["novel_clean_sequence_match"] for row in rows
        ),
        "invalid_citation_output_count": sum(
            not row["all_citations_valid"] for row in rows
        ),
        "invalid_citation_id_count": sum(
            row["invalid_citation_id_count"] for row in rows
        ),
        "successful_output_tokens": sum(row["total_tokens"] for row in rows),
        "successful_runtime_seconds": sum(row["elapsed_seconds"] for row in rows),
    }


def summary_rows(rows: list[dict]) -> list[dict]:
    output = [summarize(rows, "all", "all")]
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["model"]].append(row)
    output.extend(
        summarize(grouped[model], "model", model) for model in MODELS
    )
    return output


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=list(rows[0]), lineterminator="\n"
        )
        writer.writeheader()
        writer.writerows(rows)


def fraction(numerator: int, denominator: int) -> str:
    return f"{numerator}/{denominator}"


def write_report(path: Path, cases: list[dict], summaries: list[dict]) -> None:
    overall = summaries[0]
    mismatches = [row for row in cases if not row["novel_matches_clean"]]
    lines = [
        "---",
        "title: Novel-safe Backfill, six-event three-model ablation",
        "date: 2026-09-30",
        "status: completed-eligible-subset",
        "---",
        "",
        "# Scope",
        "",
        "This ablation evaluates only the six events frozen as eligible before model",
        "calls. Newly added evidence is cutoff-safe and excluded from the Clean top-k;",
        "safe survivors from the actual Unfiltered context are retained. Four events",
        "were ineligible because their candidate pools could not restore top-k.",
        "",
        "# Main result",
        "",
        f"Across {overall['n_model_events']} model-event runs, Sparse matched Clean in "
        f"{fraction(overall['sparse_matches_clean_count'], overall['n_model_events'])}, "
        f"Standard Backfill in {fraction(overall['standard_matches_clean_count'], overall['n_model_events'])}, "
        f"and Novel-safe Backfill in "
        f"{fraction(overall['novel_matches_clean_count'], overall['n_model_events'])}.",
        "",
        f"On {overall['initial_flip_count']} initial flips, recovery was "
        f"{overall['sparse_recovery_count']}/{overall['initial_flip_count']} Sparse, "
        f"{overall['standard_recovery_count']}/{overall['initial_flip_count']} Standard, "
        f"and {overall['novel_recovery_count']}/{overall['initial_flip_count']} Novel-safe. "
        f"On {overall['nonflip_count']} non-flips, drift was "
        f"{overall['sparse_drift_count']}/{overall['nonflip_count']}, "
        f"{overall['standard_drift_count']}/{overall['nonflip_count']}, and "
        f"{overall['novel_drift_count']}/{overall['nonflip_count']}, respectively.",
        "",
        f"Standard was the only method matching Clean in "
        f"{overall['standard_only_match_count']} paired runs; Novel-safe was uniquely "
        f"correct in {overall['novel_only_match_count']}. The exact paired McNemar "
        f"p-value is {overall['standard_vs_novel_exact_mcnemar_p']:.2f}; the eligible "
        "subset does not establish a statistically reliable general advantage.",
        "",
        "# Model summary",
        "",
        "| Model | Runs | Flips | Sparse recovery | Standard recovery | Novel recovery | Sparse / Standard / Novel match Clean |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summaries[1:]:
        lines.append(
            f"| {row['model']} | {row['n_model_events']} | {row['initial_flip_count']} | "
            f"{row['sparse_recovery_count']}/{row['initial_flip_count']} | "
            f"{row['standard_recovery_count']}/{row['initial_flip_count']} | "
            f"{row['novel_recovery_count']}/{row['initial_flip_count']} | "
            f"{row['sparse_matches_clean_count']} / {row['standard_matches_clean_count']} / "
            f"{row['novel_matches_clean_count']} |"
        )
    lines.extend(
        [
            "",
            "# Novel-safe mismatches",
            "",
            "| Model | Event | Clean | Unfiltered | Sparse | Standard | Novel-safe |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for row in mismatches:
        lines.append(
            f"| {row['model']} | {row['event_id']} ({row['ticker']}) | "
            f"{row['clean']} | {row['unfiltered']} | {row['sparse']} | "
            f"{row['standard_backfill']} | {row['novel_safe_backfill']} |"
        )
    lines.extend(
        [
            "",
            "# Input and runtime checks",
            "",
            f"- Novel-safe input exactly matched Clean in {overall['novel_clean_sequence_match_count']}/{overall['n_model_events']} runs.",
            f"- Novel-safe changed the Sparse direction in {overall['novel_changed_sparse_direction_count']}/{overall['n_model_events']} runs.",
            f"- Novel-safe and Standard predictions matched in {overall['novel_matches_standard_direction_count']}/{overall['n_model_events']} runs.",
            f"- Citation validation found {overall['invalid_citation_id_count']} invalid IDs across {overall['invalid_citation_output_count']}/{overall['n_model_events']} outputs.",
            f"- Successful outputs used {overall['successful_output_tokens']} recorded tokens and {overall['successful_runtime_seconds']:.1f} recorded seconds.",
            "- Qwen natural_007 initially produced seven retained truncated-JSON errors",
            "  because the 8,102-token prompt exhausted an 8,192-token server context.",
            "  The final call used the same model, prompt, temperature, and 700-token output",
            "  cap after restarting llama.cpp with a 16,384-token context.",
            "",
            "# Interpretation",
            "",
            "Novel-safe did not reproduce the three corrections observed under Standard",
            "Backfill. It matched Sparse on Clean-direction consistency, although DeepSeek",
            "Intel moved from DOWN under Sparse to NEUTRAL under Novel-safe. This supports",
            "the claim that revision behavior depends on the content and ranking of the",
            "replacement evidence, not context count alone. It does not prove that Standard",
            "Backfill is generally superior: the comparison is conditional on a purposively",
            "eligible six-event subset, has only three discordant pairs, and is not significant.",
            "",
            "# Paper status",
            "",
            "The workshop draft remains unchanged. These results are an experimental",
            "follow-up and require author review before any manuscript revision.",
            "",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    cases = load_rows()
    summaries = summary_rows(cases)
    write_csv(args.cases, cases)
    write_csv(args.summary, summaries)
    write_report(args.report, cases, summaries)
    print(f"wrote {args.cases}")
    print(f"wrote {args.summary}")
    print(f"wrote {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

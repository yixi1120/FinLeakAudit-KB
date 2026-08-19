#!/usr/bin/env python3
"""Summarize the minimal natural point-in-time replay."""

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
    RESULTS / "deepseek_natural_pit_5event_v1_results.jsonl",
    RESULTS / "zhipu_natural_pit_5event_v1_results.jsonl",
]
DEFAULT_SUMMARY = ANALYSIS / "natural_pit_5event_summary_v1.csv"
DEFAULT_CASES = ANALYSIS / "natural_pit_5event_case_results_v1.csv"
DEFAULT_REPORT = WIKI / "natural_pit_5event_results_2026_08_19.md"
CONDITIONS = ("clean", "unfiltered", "audited")


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
                if row.get("schema_version") != "finleakaudit_natural_replay_result_v1":
                    raise ValueError(f"{path}:{line_number}: unexpected schema version")
                rows.append(row)
    seen = set()
    for row in rows:
        key = (row["model"], row["event_id"])
        if key in seen:
            raise ValueError(f"Duplicate model-event result: {key}")
        seen.add(key)
    return rows


def divide(numerator: int | float, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def wilson_interval(successes: int, total: int, z: float = 1.96) -> tuple[float | None, float | None]:
    if total == 0:
        return None, None
    proportion = successes / total
    denominator = 1 + z * z / total
    centre = proportion + z * z / (2 * total)
    margin = z * math.sqrt(
        proportion * (1 - proportion) / total + z * z / (4 * total * total)
    )
    return (centre - margin) / denominator, (centre + margin) / denominator


def usage_total(row: dict, field: str) -> int:
    usage = row[field].get("_usage") or {}
    return int(usage.get("total_tokens") or 0)


def citation_validation(row: dict, condition: str) -> dict:
    stored = row.get("audit", {}).get("citation_validation", {}).get(condition)
    if stored is not None:
        return stored
    evidence_key = f"{condition}_evidence"
    available_ids = {
        item["id"] for item in row.get("retrieval", {}).get(evidence_key, [])
    }
    cited_ids = sorted(
        {
            str(evidence_id)
            for claim in row[condition].get("rationale") or []
            for evidence_id in claim.get("evidence_ids") or []
        }
    )
    invalid_ids = sorted(set(cited_ids) - available_ids)
    return {
        "cited_evidence_ids": cited_ids,
        "invalid_citation_ids": invalid_ids,
        "all_citations_valid": not invalid_ids,
    }


def summarize_rows(rows: list[dict], scope: str, model: str) -> dict:
    n = len(rows)
    flipped = [
        row for row in rows if row["metrics"]["prediction_changed_clean_to_unfiltered"]
    ]
    recovered_flips = [
        row for row in flipped if row["metrics"]["audited_recovered_clean_direction"]
    ]
    recovery_low, recovery_high = wilson_interval(len(recovered_flips), len(flipped))
    citation_checks = [
        citation_validation(row, condition) for row in rows for condition in CONDITIONS
    ]
    output = {
        "scope": scope,
        "model": model,
        "n_model_events": n,
        "model_calls": n * len(CONDITIONS),
        "future_retrieval_rate": divide(
            sum(row["metrics"]["future_evidence_retrieved"] for row in rows), n
        ),
        "explicit_future_citation_rate": divide(
            sum(row["metrics"]["future_evidence_cited"] for row in rows), n
        ),
        "direction_flip_rate": divide(len(flipped), n),
        "direction_flip_count": len(flipped),
        "audited_matches_clean_rate": divide(
            sum(row["metrics"]["audited_recovered_clean_direction"] for row in rows), n
        ),
        "recovery_rate_among_flips": divide(len(recovered_flips), len(flipped)),
        "recovery_count_among_flips": len(recovered_flips),
        "recovery_wilson_95_low": recovery_low,
        "recovery_wilson_95_high": recovery_high,
        "clean_accuracy": divide(sum(row["metrics"]["clean_correct"] for row in rows), n),
        "unfiltered_accuracy": divide(
            sum(row["metrics"]["unfiltered_correct"] for row in rows), n
        ),
        "audited_accuracy": divide(
            sum(row["metrics"]["audited_correct"] for row in rows), n
        ),
        "mean_confidence_delta_unfiltered_minus_clean": divide(
            sum(
                row["metrics"]["confidence_delta_unfiltered_minus_clean"]
                for row in rows
            ),
            n,
        ),
        "total_tokens": sum(
            usage_total(row, condition) for row in rows for condition in CONDITIONS
        ),
        "predictions_with_invalid_citations": sum(
            not check["all_citations_valid"] for check in citation_checks
        ),
        "invalid_citation_id_count": sum(
            len(check["invalid_citation_ids"]) for check in citation_checks
        ),
    }
    return output


def build_summary(rows: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row["model"]].append(row)
    output = [summarize_rows(rows, "all", "all")]
    output.extend(
        summarize_rows(grouped[model], "model", model) for model in sorted(grouped)
    )
    return output


def build_case_rows(rows: list[dict]) -> list[dict]:
    output = []
    for row in sorted(rows, key=lambda item: (item["model"], item["event_id"])):
        metrics = row["metrics"]
        invalid_citations = sum(
            len(citation_validation(row, condition)["invalid_citation_ids"])
            for condition in CONDITIONS
        )
        output.append(
            {
                "model": row["model"],
                "model_id": row["model_id"],
                "event_id": row["event_id"],
                "ticker": row["ticker"],
                "outcome_label": row["outcome_label"],
                "outcome_return": row["outcome_return"],
                "clean_prediction": row["clean"]["prediction"],
                "unfiltered_prediction": row["unfiltered"]["prediction"],
                "audited_prediction": row["audited"]["prediction"],
                "future_evidence_retrieved_count": metrics[
                    "future_evidence_retrieved_count"
                ],
                "future_evidence_cited": metrics["future_evidence_cited"],
                "direction_flipped": metrics[
                    "prediction_changed_clean_to_unfiltered"
                ],
                "audited_recovered_clean_direction": metrics[
                    "audited_recovered_clean_direction"
                ],
                "clean_correct": metrics["clean_correct"],
                "unfiltered_correct": metrics["unfiltered_correct"],
                "audited_correct": metrics["audited_correct"],
                "total_tokens": sum(usage_total(row, condition) for condition in CONDITIONS),
                "invalid_citation_id_count": invalid_citations,
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
    return "N/A" if value is None else f"{value * 100:.0f}%"


def markdown_report(summary: list[dict], cases: list[dict]) -> str:
    all_row = summary[0]
    model_rows = summary[1:]
    crowdstrike = [row for row in cases if row["event_id"] == "natural_001"]
    lines = [
        "---",
        "title: Natural point-in-time replay — five-event pilot",
        "date: 2026-08-19",
        "status: controlled-natural-source-replay-pilot",
        "---",
        "",
        "# Scope",
        "",
        "This pilot replays a frozen query over a directly assembled primary-source candidate",
        "corpus. It compares cutoff-safe retrieval, outcome-bounded unfiltered retrieval, and",
        "timestamp-audited revision. It is not a preserved production RAG trace and does not",
        "estimate the prevalence of leakage in deployed systems.",
        "",
        "# Main result",
        "",
        f"Across {all_row['n_model_events']} model-event runs and "
        f"{all_row['model_calls']} prediction calls, cutoff-postdating evidence appeared in "
        f"{percent(all_row['future_retrieval_rate'])} of unfiltered top-k contexts and was "
        f"explicitly cited in {percent(all_row['explicit_future_citation_rate'])}. Direction "
        f"changed in {percent(all_row['direction_flip_rate'])} of runs. Among changed runs, "
        f"timestamp removal restored the Clean direction in "
        f"{percent(all_row['recovery_rate_among_flips'])} "
        f"({all_row['recovery_count_among_flips']}/{all_row['direction_flip_count']}; "
        f"Wilson 95% interval {percent(all_row['recovery_wilson_95_low'])}-"
        f"{percent(all_row['recovery_wilson_95_high'])}).",
        "",
        f"Unfiltered outcome accuracy was {percent(all_row['unfiltered_accuracy'])}, versus "
        f"{percent(all_row['clean_accuracy'])} for Clean and "
        f"{percent(all_row['audited_accuracy'])} after audit. The apparent unfiltered gain is",
        "hindsight inflation in this replay, not evidence of a better forecasting system.",
        "",
        f"Citation-format validation found {all_row['invalid_citation_id_count']} invalid IDs "
        f"in {all_row['predictions_with_invalid_citations']}/{all_row['model_calls']} "
        "predictions: one output invented unavailable chunk suffixes and another shortened "
        "chunk IDs to document IDs.",
        "",
        "# Model summary",
        "",
        "| Model | Runs | Future cited | Direction flip | Recovery on flips | Clean acc. | Unfiltered acc. | Audited acc. | Tokens |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in model_rows:
        lines.append(
            f"| {row['model']} | {row['n_model_events']} | "
            f"{percent(row['explicit_future_citation_rate'])} | "
            f"{percent(row['direction_flip_rate'])} | "
            f"{percent(row['recovery_rate_among_flips'])} | "
            f"{percent(row['clean_accuracy'])} | "
            f"{percent(row['unfiltered_accuracy'])} | "
            f"{percent(row['audited_accuracy'])} | {row['total_tokens']} |"
        )
    lines.extend(
        [
            "",
            "# CrowdStrike case study",
            "",
            "The same outcome-bounded event source changed both model forecasts toward DOWN.",
            "Removing all post-cutoff chunks returned each model to its own cutoff-safe",
            "direction:",
            "",
            "| Model | Clean | Unfiltered | Audited | Outcome | Future cited |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in crowdstrike:
        lines.append(
            f"| {row['model']} | {row['clean_prediction']} | "
            f"{row['unfiltered_prediction']} | {row['audited_prediction']} | "
            f"{row['outcome_label']} | {str(row['future_evidence_cited']).lower()} |"
        )
    lines.extend(
        [
            "",
            "# Interpretation boundary",
            "",
            "- The five events were selected for heterogeneity, not sampled from production traffic.",
            "- The unfiltered condition is deliberately bounded by outcome time and therefore serves",
            "  as a point-in-time replay stress test.",
            "- Explicit citation is not complete semantic attribution; Annotator B and adjudication",
            "  remain pending.",
            "- Two outputs contained invalid evidence IDs, so citation validity must be checked",
            "  rather than assumed.",
            "- Timestamp filtering is a strong deterministic baseline, not the complete planned",
            "  FinLeakAudit semantic operator stack.",
            "- Ten model-event observations are adequate for an RA portfolio pilot, not a paper-level",
            "  general claim.",
            "",
            "# Reproduce",
            "",
            "```bash",
            "python3 experiments/run_natural_experiment.py --model deepseek --minimal --run-name natural_pit_5event_v1",
            "python3 experiments/run_natural_experiment.py --model zhipu --minimal --run-name natural_pit_5event_v1",
            "python3 experiments/analyze_natural_experiment.py",
            "```",
            "",
            "# RA-safe wording",
            "",
            "Built a point-in-time replay for five natural financial events and evaluated",
            "two LLMs across 30 prediction calls. Post-cutoff evidence was explicitly cited",
            "in 9/10 model-event runs and changed the forecast direction in 4/10; timestamp",
            "removal restored the corresponding cutoff-safe direction in all four changed",
            "runs. This is a small outcome-bounded stress test, not an estimate of leakage",
            "prevalence in deployed systems.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", type=Path, dest="inputs")
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--case-output", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    rows = read_results(args.inputs or DEFAULT_INPUTS)
    summary = build_summary(rows)
    cases = build_case_rows(rows)
    write_csv(args.summary, summary)
    write_csv(args.case_output, cases)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(markdown_report(summary, cases), encoding="utf-8")
    print(f"wrote {args.summary}")
    print(f"wrote {args.case_output}")
    print(f"wrote {args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Build policy-baseline and compact case summaries from experiment results."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from config import RESULTS_DIR


DEFAULT_INPUTS = [
    RESULTS_DIR / "deepseek_v4_mixed10_abs_time_20260726_ablation_results.jsonl",
    RESULTS_DIR / "zhipu_v4_mixed10_abs_time_20260726_ablation_results.jsonl",
    RESULTS_DIR / "qwen_v4_mixed10_abs_time_20260726_ablation_results.jsonl",
]

POLICIES = {
    "no_audit": {
        "condition": "leaky",
        "note": "Use the prediction made with all retrieved evidence.",
    },
    "timestamp_only": {
        "condition": "clean",
        "note": "Remove every item available after cutoff before prediction.",
    },
    "citation_only": {
        "condition": "audited",
        "note": "Remove future items explicitly cited in the rationale.",
    },
    "delete_all_future": {
        "condition": "clean",
        "note": "Oracle deletion; identical to timestamp_only in this controlled dataset.",
    },
}


def read_results(paths: list[Path]) -> list[dict]:
    rows = []
    for path in paths:
        if not path.exists():
            raise FileNotFoundError(f"Missing result file: {path}")
        with path.open("r", encoding="utf-8") as fh:
            rows.extend(json.loads(line) for line in fh if line.strip())
    return rows


def rate(successes: int, total: int) -> float:
    return successes / total if total else 0.0


def outcome_label(row: dict) -> str:
    return str(row.get("outcome_label") or row.get("label") or "").upper()


def prediction(row: dict, condition: str) -> str:
    return str((row.get(condition) or {}).get("prediction") or "").upper()


def future_evidence_ids(row: dict) -> set[str]:
    return {
        item["evidence_id"]
        for item in (row.get("audit") or {}).get("temporal_check") or []
        if item.get("temporal_status") == "future_leakage"
    }


def retained_future_count(row: dict, baseline: str) -> int:
    future_ids = future_evidence_ids(row)
    if baseline == "no_audit":
        return len(future_ids)
    if baseline in {"timestamp_only", "delete_all_future"}:
        return 0
    removed_ids = set((row.get("audit") or {}).get("removed_evidence_ids") or [])
    return len(future_ids - removed_ids)


def summarize_policy(rows: list[dict], baseline: str) -> dict:
    condition = POLICIES[baseline]["condition"]
    n = len(rows)
    future_items = sum(len(future_evidence_ids(row)) for row in rows)
    retained_items = sum(retained_future_count(row, baseline) for row in rows)
    correct = sum(
        prediction(row, condition) == outcome_label(row)
        for row in rows
    )
    changes = sum(
        prediction(row, condition) != prediction(row, "leaky")
        for row in rows
    )
    clean_agreements = sum(
        prediction(row, condition) == prediction(row, "clean")
        for row in rows
    )
    return {
        "baseline": baseline,
        "n_model_cases": n,
        "correct_predictions": correct,
        "accuracy": rate(correct, n),
        "changes_vs_no_audit": changes,
        "change_rate_vs_no_audit": rate(changes, n),
        "clean_direction_agreements": clean_agreements,
        "clean_direction_agreement_rate": rate(clean_agreements, n),
        "future_evidence_items": future_items,
        "retained_future_items": retained_items,
        "future_retained_rate": rate(retained_items, future_items),
        "note": POLICIES[baseline]["note"],
    }


def grouped_rows(rows: list[dict]) -> list[tuple[dict, list[dict]]]:
    groups = [
        (
            {"scope": "all", "model": "all", "dataset_tier": "all"},
            rows,
        )
    ]
    models = sorted({str(row.get("model") or "missing") for row in rows})
    tiers = sorted({str(row.get("dataset_tier") or "missing") for row in rows})
    for model in models:
        groups.append(
            (
                {"scope": "model", "model": model, "dataset_tier": "all"},
                [row for row in rows if str(row.get("model") or "missing") == model],
            )
        )
    for tier in tiers:
        groups.append(
            (
                {"scope": "dataset_tier", "model": "all", "dataset_tier": tier},
                [
                    row
                    for row in rows
                    if str(row.get("dataset_tier") or "missing") == tier
                ],
            )
        )
    for model in models:
        for tier in tiers:
            selected = [
                row
                for row in rows
                if str(row.get("model") or "missing") == model
                and str(row.get("dataset_tier") or "missing") == tier
            ]
            if selected:
                groups.append(
                    (
                        {
                            "scope": "model_dataset_tier",
                            "model": model,
                            "dataset_tier": tier,
                        },
                        selected,
                    )
                )
    return groups


def build_policy_rows(rows: list[dict]) -> list[dict]:
    summaries = []
    for group, selected in grouped_rows(rows):
        for baseline in POLICIES:
            summaries.append({**group, **summarize_policy(selected, baseline)})
    return summaries


def build_case_rows(rows: list[dict]) -> list[dict]:
    case_rows = []
    for row in rows:
        future_ids = future_evidence_ids(row)
        removed_ids = set((row.get("audit") or {}).get("removed_evidence_ids") or [])
        future_ablation = [
            item
            for item in row.get("ablation") or []
            if item.get("is_future_leakage")
        ]
        case_rows.append(
            {
                "model": row.get("model"),
                "model_id": row.get("model_id"),
                "case_id": row.get("case_id"),
                "dataset_tier": row.get("dataset_tier"),
                "outcome_label": outcome_label(row),
                "clean_prediction": prediction(row, "clean"),
                "no_audit_prediction": prediction(row, "leaky"),
                "citation_only_prediction": prediction(row, "audited"),
                "clean_to_no_audit_changed": prediction(row, "clean")
                != prediction(row, "leaky"),
                "citation_revision_changed": prediction(row, "audited")
                != prediction(row, "leaky"),
                "explicit_future_citation": bool(
                    (row.get("metrics") or {}).get("leaky_cited_future")
                ),
                "future_evidence_items": len(future_ids),
                "removed_future_items": len(future_ids & removed_ids),
                "future_flip_driver": any(
                    item.get("is_flip_driver") for item in future_ablation
                ),
            }
        )
    return case_rows


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(dict.fromkeys(key for row in rows for key in row))
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        action="append",
        type=Path,
        dest="inputs",
        help="Result JSONL; repeat for multiple models.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=RESULTS_DIR / "v4_baseline_summary.csv",
    )
    parser.add_argument("--case-output", type=Path, default=None)
    args = parser.parse_args()

    rows = read_results(args.inputs or DEFAULT_INPUTS)
    policy_rows = build_policy_rows(rows)
    write_csv(args.output, policy_rows)
    print(f"wrote {args.output} ({len(policy_rows)} policy rows)")
    if args.case_output:
        case_rows = build_case_rows(rows)
        write_csv(args.case_output, case_rows)
        print(f"wrote {args.case_output} ({len(case_rows)} case rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Validate two independent annotation files and measure agreement."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_A = ROOT / "experiments" / "analysis" / "semantic_annotations_annotator_a_v1.csv"
DEFAULT_B = ROOT / "experiments" / "analysis" / "semantic_annotations_annotator_b_v1.csv"
DEFAULT_SUMMARY = ROOT / "experiments" / "analysis" / "semantic_annotation_agreement_v1.json"
DEFAULT_DISAGREEMENTS = (
    ROOT / "experiments" / "analysis" / "semantic_annotation_disagreements_v1.csv"
)
DEFAULT_ADJUDICATION = (
    ROOT / "experiments" / "analysis" / "semantic_annotation_adjudication_template_v1.csv"
)

LABEL_FIELDS = {
    "label_semantic_dependency": {"yes", "no", "uncertain"},
    "label_relation": {"support", "contradict", "irrelevant", "uncertain"},
    "label_exclusive_to_post_cutoff": {"yes", "no", "uncertain"},
    "label_should_remove": {"yes", "no", "uncertain"},
}
ANNOTATION_FIELDS = [
    *LABEL_FIELDS,
    "matched_claim_span",
    "confidence_1_to_5",
    "annotator_id",
    "notes",
]
PAIR_FIELDS = [
    "forecast_prediction",
    "claim_text",
    "claim_direction",
    "pre_cutoff_evidence",
    "post_cutoff_evidence_id",
    "post_cutoff_evidence_text",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing annotation file: {path}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def validate_annotations(rows: list[dict[str, str]], source: str) -> None:
    if not rows:
        raise ValueError(f"{source}: annotation file is empty")
    required = {"sample_id", *PAIR_FIELDS, *ANNOTATION_FIELDS}
    missing_columns = required - set(rows[0])
    if missing_columns:
        raise ValueError(f"{source}: missing columns: {sorted(missing_columns)}")

    seen: set[str] = set()
    for row_number, row in enumerate(rows, start=2):
        sample_id = row["sample_id"].strip()
        location = f"{source}:{row_number} ({sample_id or 'missing sample_id'})"
        if not sample_id:
            raise ValueError(f"{location}: sample_id is required")
        if sample_id in seen:
            raise ValueError(f"{location}: duplicate sample_id")
        seen.add(sample_id)

        for field, allowed in LABEL_FIELDS.items():
            value = row[field].strip().lower()
            if value not in allowed:
                raise ValueError(
                    f"{location}: {field} must be one of {sorted(allowed)}, got {value!r}"
                )

        confidence = row["confidence_1_to_5"].strip()
        if confidence not in {"1", "2", "3", "4", "5"}:
            raise ValueError(f"{location}: confidence_1_to_5 must be an integer 1-5")
        if not row["annotator_id"].strip():
            raise ValueError(f"{location}: annotator_id is required")

        span = row["matched_claim_span"].strip()
        if row["label_semantic_dependency"].strip().lower() == "yes" and not span:
            raise ValueError(f"{location}: semantic dependency 'yes' requires a span")
        if span and span not in row["claim_text"]:
            raise ValueError(f"{location}: matched_claim_span is not an exact claim substring")


def align_annotations(
    rows_a: list[dict[str, str]], rows_b: list[dict[str, str]]
) -> list[tuple[dict[str, str], dict[str, str]]]:
    by_id_a = {row["sample_id"]: row for row in rows_a}
    by_id_b = {row["sample_id"]: row for row in rows_b}
    if set(by_id_a) != set(by_id_b):
        only_a = sorted(set(by_id_a) - set(by_id_b))
        only_b = sorted(set(by_id_b) - set(by_id_a))
        raise ValueError(f"A/B sample IDs differ; only A={only_a}, only B={only_b}")

    aligned = []
    for sample_id in sorted(by_id_a):
        row_a = by_id_a[sample_id]
        row_b = by_id_b[sample_id]
        for field in PAIR_FIELDS:
            if row_a[field] != row_b[field]:
                raise ValueError(f"{sample_id}: A/B source content differs in {field}")
        aligned.append((row_a, row_b))
    return aligned


def cohens_kappa(labels_a: list[str], labels_b: list[str]) -> float | None:
    if len(labels_a) != len(labels_b) or not labels_a:
        raise ValueError("Kappa requires two non-empty label lists of equal length")
    count_a = Counter(labels_a)
    count_b = Counter(labels_b)
    total = len(labels_a)
    observed = sum(a == b for a, b in zip(labels_a, labels_b)) / total
    expected = sum(
        (count_a[label] / total) * (count_b[label] / total)
        for label in set(count_a) | set(count_b)
    )
    if expected == 1.0:
        return 1.0 if observed == 1.0 else None
    return (observed - expected) / (1.0 - expected)


def field_metrics(
    aligned: list[tuple[dict[str, str], dict[str, str]]], field: str
) -> dict[str, object]:
    labels_a = [row_a[field].strip().lower() for row_a, _ in aligned]
    labels_b = [row_b[field].strip().lower() for _, row_b in aligned]
    agreements = sum(a == b for a, b in zip(labels_a, labels_b))
    return {
        "agreement_count": agreements,
        "agreement_rate": agreements / len(aligned),
        "cohens_kappa": cohens_kappa(labels_a, labels_b),
        "annotator_a_distribution": dict(sorted(Counter(labels_a).items())),
        "annotator_b_distribution": dict(sorted(Counter(labels_b).items())),
    }


def summarize_agreement(
    aligned: list[tuple[dict[str, str], dict[str, str]]]
) -> dict[str, object]:
    summary: dict[str, object] = {
        "n_pairs": len(aligned),
        "field_metrics": {
            field: field_metrics(aligned, field) for field in LABEL_FIELDS
        },
    }
    dependency_a = [
        "yes" if row_a["label_semantic_dependency"].strip().lower() == "yes" else "other"
        for row_a, _ in aligned
    ]
    dependency_b = [
        "yes" if row_b["label_semantic_dependency"].strip().lower() == "yes" else "other"
        for _, row_b in aligned
    ]
    binary_agreements = sum(a == b for a, b in zip(dependency_a, dependency_b))
    summary["semantic_dependency_yes_vs_other"] = {
        "agreement_count": binary_agreements,
        "agreement_rate": binary_agreements / len(aligned),
        "cohens_kappa": cohens_kappa(dependency_a, dependency_b),
    }
    summary["semantic_dependency_disagreement_count"] = len(aligned) - int(
        summary["field_metrics"]["label_semantic_dependency"]["agreement_count"]
    )
    return summary


def build_disagreements(
    aligned: list[tuple[dict[str, str], dict[str, str]]]
) -> list[dict[str, str]]:
    rows = []
    for row_a, row_b in aligned:
        if all(row_a[field] == row_b[field] for field in LABEL_FIELDS):
            continue
        output = {"sample_id": row_a["sample_id"]}
        output.update({field: row_a[field] for field in PAIR_FIELDS})
        output.update({f"a_{field}": row_a[field] for field in ANNOTATION_FIELDS})
        output.update({f"b_{field}": row_b[field] for field in ANNOTATION_FIELDS})
        for field in LABEL_FIELDS:
            output[f"adjudicated_{field}"] = ""
        output["adjudicated_matched_claim_span"] = ""
        output["adjudicator_id"] = ""
        output["adjudication_notes"] = ""
        rows.append(output)
    return rows


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--annotator-a", type=Path, default=DEFAULT_A)
    parser.add_argument("--annotator-b", type=Path, default=DEFAULT_B)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--disagreements", type=Path, default=DEFAULT_DISAGREEMENTS)
    parser.add_argument("--adjudication-template", type=Path, default=DEFAULT_ADJUDICATION)
    args = parser.parse_args()

    rows_a = read_csv(args.annotator_a)
    validate_annotations(rows_a, str(args.annotator_a))
    print(f"validated {args.annotator_a} ({len(rows_a)} annotations)")
    if not args.annotator_b.exists():
        print(
            f"waiting for independent Annotator B file: {args.annotator_b}; "
            "agreement outputs were not generated"
        )
        return 0

    rows_b = read_csv(args.annotator_b)
    validate_annotations(rows_b, str(args.annotator_b))
    aligned = align_annotations(rows_a, rows_b)
    summary = summarize_agreement(aligned)
    disagreements = build_disagreements(aligned)

    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    disagreement_fields = list(disagreements[0]) if disagreements else [
        "sample_id",
        *PAIR_FIELDS,
        *(f"a_{field}" for field in ANNOTATION_FIELDS),
        *(f"b_{field}" for field in ANNOTATION_FIELDS),
        *(f"adjudicated_{field}" for field in LABEL_FIELDS),
        "adjudicated_matched_claim_span",
        "adjudicator_id",
        "adjudication_notes",
    ]
    write_csv(args.disagreements, disagreements, disagreement_fields)
    write_csv(args.adjudication_template, disagreements, disagreement_fields)
    print(f"wrote {args.summary}")
    print(f"wrote {args.disagreements} ({len(disagreements)} disagreements)")
    print(f"wrote {args.adjudication_template}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

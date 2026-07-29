"""Deterministic lexical proxy for claim-evidence attribution.

This is an offline baseline, not a semantic entailment model. It scores a
claim against post-cutoff evidence and discounts overlap already explained by
pre-cutoff evidence.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

from config import RESULTS_DIR


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = (
    ROOT / "experiments" / "analysis" / "semantic_annotation_batch_v1.csv"
)
DEFAULT_OUTPUT = RESULTS_DIR / "semantic_lexical_baseline_v1.csv"

TOKEN_RE = re.compile(r"[a-z]+(?:'[a-z]+)?|\d+(?:\.\d+)?%?")
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "because",
    "been",
    "being",
    "by",
    "for",
    "from",
    "had",
    "has",
    "have",
    "in",
    "into",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "there",
    "this",
    "to",
    "was",
    "were",
    "which",
    "with",
    "would",
}


def tokens(text: str) -> list[str]:
    return [
        token
        for token in TOKEN_RE.findall(str(text).lower())
        if token not in STOPWORDS and len(token) > 1
    ]


def bigrams(items: list[str]) -> set[tuple[str, str]]:
    return set(zip(items, items[1:]))


def safe_ratio(numerator: int, denominator: int) -> float:
    return numerator / denominator if denominator else 0.0


def pair_features(claim: str, evidence: str) -> dict:
    claim_tokens = tokens(claim)
    evidence_tokens = tokens(evidence)
    claim_set = set(claim_tokens)
    evidence_set = set(evidence_tokens)
    shared = claim_set & evidence_set
    union = claim_set | evidence_set
    claim_bigrams = bigrams(claim_tokens)
    evidence_bigrams = bigrams(evidence_tokens)
    shared_bigrams = claim_bigrams & evidence_bigrams
    number_overlap = {token for token in shared if token[0].isdigit()}

    claim_coverage = safe_ratio(len(shared), len(claim_set))
    evidence_coverage = safe_ratio(len(shared), len(evidence_set))
    jaccard = safe_ratio(len(shared), len(union))
    bigram_coverage = safe_ratio(
        len(shared_bigrams),
        min(len(claim_bigrams), len(evidence_bigrams)),
    )
    numeric_bonus = min(0.15, 0.05 * len(number_overlap))
    score = min(
        1.0,
        0.45 * claim_coverage
        + 0.20 * evidence_coverage
        + 0.15 * jaccard
        + 0.20 * bigram_coverage
        + numeric_bonus,
    )
    return {
        "score": score,
        "claim_coverage": claim_coverage,
        "evidence_coverage": evidence_coverage,
        "jaccard": jaccard,
        "bigram_coverage": bigram_coverage,
        "numeric_overlap_count": len(number_overlap),
        "shared_tokens": sorted(shared),
    }


def parse_pre_cutoff_evidence(value: str) -> list[dict]:
    try:
        parsed = json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return []
    return parsed if isinstance(parsed, list) else []


def score_annotation_row(
    row: dict,
    threshold: float,
    margin_threshold: float,
) -> dict:
    future = pair_features(
        row.get("claim_text", ""),
        row.get("post_cutoff_evidence_text", ""),
    )
    pre_scores = [
        pair_features(row.get("claim_text", ""), item.get("text", ""))["score"]
        for item in parse_pre_cutoff_evidence(row.get("pre_cutoff_evidence", ""))
    ]
    max_pre_score = max(pre_scores, default=0.0)
    margin = future["score"] - max_pre_score
    candidate = (
        future["score"] >= threshold
        and margin >= margin_threshold
    )
    return {
        "sample_id": row.get("sample_id"),
        "future_lexical_score": round(future["score"], 6),
        "max_pre_cutoff_lexical_score": round(max_pre_score, 6),
        "future_minus_pre_margin": round(margin, 6),
        "provisional_candidate": candidate,
        "claim_coverage": round(future["claim_coverage"], 6),
        "evidence_coverage": round(future["evidence_coverage"], 6),
        "jaccard": round(future["jaccard"], 6),
        "bigram_coverage": round(future["bigram_coverage"], 6),
        "numeric_overlap_count": future["numeric_overlap_count"],
        "shared_tokens": "|".join(future["shared_tokens"]),
        "threshold": threshold,
        "margin_threshold": margin_threshold,
    }


def score_rows(
    rows: list[dict],
    threshold: float,
    margin_threshold: float,
) -> list[dict]:
    return [
        score_annotation_row(row, threshold, margin_threshold)
        for row in rows
    ]


def binary_metrics(scored_rows: list[dict], annotations: list[dict]) -> dict:
    labels = {
        row.get("sample_id"): str(
            row.get("label_semantic_dependency") or ""
        ).strip().lower()
        for row in annotations
    }
    tp = fp = fn = tn = excluded = 0
    for row in scored_rows:
        label = labels.get(row.get("sample_id"), "")
        if label not in {"yes", "no"}:
            excluded += 1
            continue
        predicted = bool(row.get("provisional_candidate"))
        actual = label == "yes"
        if predicted and actual:
            tp += 1
        elif predicted and not actual:
            fp += 1
        elif not predicted and actual:
            fn += 1
        else:
            tn += 1
    precision = safe_ratio(tp, tp + fp)
    recall = safe_ratio(tp, tp + fn)
    f1 = safe_ratio(2 * precision * recall, precision + recall)
    return {
        "evaluated": tp + fp + fn + tn,
        "excluded_blank_or_uncertain": excluded,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    }


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError("Refusing to write an empty score file")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=list(rows[0]),
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--annotations", type=Path, default=None)
    parser.add_argument("--threshold", type=float, default=0.35)
    parser.add_argument("--margin-threshold", type=float, default=0.08)
    args = parser.parse_args()

    rows = read_csv(args.input)
    scored = score_rows(rows, args.threshold, args.margin_threshold)
    write_csv(args.output, scored)
    candidates = sum(bool(row["provisional_candidate"]) for row in scored)
    print(
        f"wrote {args.output} ({len(scored)} rows; "
        f"{candidates} provisional candidates)"
    )
    if args.annotations:
        metrics = binary_metrics(scored, read_csv(args.annotations))
        print(json.dumps(metrics, sort_keys=True))
    else:
        print("gold labels not supplied; precision/recall/F1 not computed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

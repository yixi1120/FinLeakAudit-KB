"""Evaluate reproducible claim-evidence attribution baselines.

The annotation batch was blinded during human labeling. After adjudication is
frozen, the coordinator key can be joined by sample_id to evaluate whether an
explicit future-evidence citation is a sufficient proxy for semantic reliance.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path

from lexical_attribution_baseline import score_rows


ROOT = Path(__file__).resolve().parents[1]
ANALYSIS_DIR = ROOT / "experiments" / "analysis"
DEFAULT_BATCH = ANALYSIS_DIR / "semantic_annotation_batch_v1.csv"
DEFAULT_KEY = ANALYSIS_DIR / "semantic_annotation_key_v1.csv"
DEFAULT_GOLD = ANALYSIS_DIR / "semantic_annotation_adjudicated_v1.csv"
DEFAULT_PREDICTIONS = ANALYSIS_DIR / "semantic_baseline_predictions_v1.csv"
DEFAULT_SUMMARY = ANALYSIS_DIR / "semantic_baseline_results_v1.json"


def read_csv(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def read_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def parse_bool(value: object) -> bool:
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no"}:
        return False
    raise ValueError(f"Invalid boolean value: {value!r}")


def wilson_interval(successes: int, total: int, z: float = 1.959964) -> list[float]:
    if not total:
        return [0.0, 0.0]
    proportion = successes / total
    denominator = 1 + z * z / total
    centre = proportion + z * z / (2 * total)
    margin = z * math.sqrt(
        proportion * (1 - proportion) / total
        + z * z / (4 * total * total)
    )
    return [
        (centre - margin) / denominator,
        (centre + margin) / denominator,
    ]


def index_unique(rows: list[dict], label: str) -> dict[str, dict]:
    indexed: dict[str, dict] = {}
    for row in rows:
        sample_id = str(row.get("sample_id") or "").strip()
        if not sample_id:
            raise ValueError(f"{label} contains a blank sample_id")
        if sample_id in indexed:
            raise ValueError(f"{label} contains duplicate sample_id {sample_id}")
        indexed[sample_id] = row
    return indexed


def binary_metrics(rows: list[dict], prediction_field: str) -> dict:
    tp = fp = fn = tn = excluded = 0
    for row in rows:
        gold = str(row["gold_semantic_dependency"]).strip().lower()
        if gold not in {"yes", "no"}:
            excluded += 1
            continue
        predicted = parse_bool(row[prediction_field])
        actual = gold == "yes"
        if predicted and actual:
            tp += 1
        elif predicted:
            fp += 1
        elif actual:
            fn += 1
        else:
            tn += 1

    def ratio(numerator: int, denominator: int) -> float:
        return numerator / denominator if denominator else 0.0

    precision = ratio(tp, tp + fp)
    recall = ratio(tp, tp + fn)
    specificity = ratio(tn, tn + fp)
    return {
        "evaluated": tp + fp + fn + tn,
        "excluded_uncertain": excluded,
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "accuracy": ratio(tp + tn, tp + fp + fn + tn),
        "accuracy_wilson_95": wilson_interval(
            tp + tn, tp + fp + fn + tn
        ),
        "precision": precision,
        "precision_wilson_95": wilson_interval(tp, tp + fp),
        "recall": recall,
        "recall_wilson_95": wilson_interval(tp, tp + fn),
        "specificity": specificity,
        "f1": ratio(2 * precision * recall, precision + recall),
    }


def join_predictions(
    batch: list[dict],
    key: list[dict],
    gold: list[dict],
    threshold: float,
    margin_threshold: float,
    llm_judge: list[dict] | None = None,
    embedding: list[dict] | None = None,
) -> list[dict]:
    key_by_id = index_unique(key, "coordinator key")
    gold_by_id = index_unique(gold, "gold labels")
    lexical_by_id = index_unique(
        score_rows(batch, threshold, margin_threshold),
        "lexical scores",
    )
    batch_ids = set(index_unique(batch, "annotation batch"))
    if batch_ids != set(key_by_id) or batch_ids != set(gold_by_id):
        raise ValueError("Batch, key, and gold sample_id sets do not match")
    judge_by_id = index_unique(llm_judge, "LLM judge") if llm_judge else {}
    if judge_by_id and batch_ids != set(judge_by_id):
        raise ValueError("LLM judge and batch sample_id sets do not match")
    embedding_by_id = index_unique(embedding, "embedding baseline") if embedding else {}
    if embedding_by_id and batch_ids != set(embedding_by_id):
        raise ValueError("Embedding baseline and batch sample_id sets do not match")

    joined = []
    for sample_id in sorted(batch_ids):
        key_row = key_by_id[sample_id]
        gold_row = gold_by_id[sample_id]
        lexical_row = lexical_by_id[sample_id]
        output = {
                "sample_id": sample_id,
                "case_id": key_row["case_id"],
                "model": key_row["model"],
                "post_cutoff_evidence_id": key_row["post_cutoff_evidence_id"],
                "gold_semantic_dependency": gold_row[
                    "label_semantic_dependency"
                ].strip().lower(),
                "citation_only_prediction": parse_bool(
                    key_row["explicit_future_citation"]
                ),
                "lexical_prediction": bool(
                    lexical_row["provisional_candidate"]
                ),
                "future_lexical_score": lexical_row[
                    "future_lexical_score"
                ],
                "max_pre_cutoff_lexical_score": lexical_row[
                    "max_pre_cutoff_lexical_score"
                ],
                "future_minus_pre_margin": lexical_row[
                    "future_minus_pre_margin"
                ],
            }
        if judge_by_id:
            judge_label = str(
                judge_by_id[sample_id].get("semantic_dependency", "uncertain")
            ).strip().lower()
            if judge_label not in {"yes", "no", "uncertain"}:
                raise ValueError(
                    f"Invalid LLM judge label for {sample_id}: {judge_label}"
                )
            output["llm_judge_label"] = judge_label
            output["llm_judge_prediction"] = judge_label == "yes"
        if embedding_by_id:
            embedding_row = embedding_by_id[sample_id]
            output["embedding_prediction"] = parse_bool(
                embedding_row["embedding_prediction"]
            )
            output["future_embedding_score"] = embedding_row[
                "future_embedding_score"
            ]
            output["max_pre_cutoff_embedding_score"] = embedding_row[
                "max_pre_cutoff_embedding_score"
            ]
            output["future_minus_pre_embedding_margin"] = embedding_row[
                "future_minus_pre_embedding_margin"
            ]
        joined.append(output)
    return joined


def evaluate(joined: list[dict], threshold: float, margin_threshold: float) -> dict:
    baselines = {
        "citation_only": "citation_only_prediction",
        "lexical_overlap": "lexical_prediction",
    }
    if joined and "llm_judge_prediction" in joined[0]:
        baselines["llm_judge"] = "llm_judge_prediction"
    if joined and "embedding_prediction" in joined[0]:
        baselines["embedding_similarity"] = "embedding_prediction"
    summary = {
        "schema_version": "finleakaudit_semantic_baselines_v1",
        "task": "binary claim-to-post-cutoff-evidence semantic dependency",
        "gold_uncertain_policy": "exclude from binary metrics",
        "prediction_policy": "yes is positive; no/uncertain are other",
        "sample_count": len(joined),
        "gold_distribution": dict(
            sorted(
                {
                    label: sum(
                        row["gold_semantic_dependency"] == label
                        for row in joined
                    )
                    for label in {row["gold_semantic_dependency"] for row in joined}
                }.items()
            )
        ),
        "lexical_parameters": {
            "threshold": threshold,
            "margin_threshold": margin_threshold,
            "selection": "pre-specified defaults; not tuned on gold labels",
        },
        "overall": {},
        "by_model": {},
        "error_sample_ids": {},
    }
    for baseline, field in baselines.items():
        summary["overall"][baseline] = binary_metrics(joined, field)
        summary["error_sample_ids"][baseline] = {
            "false_positive": [
                row["sample_id"]
                for row in joined
                if row["gold_semantic_dependency"] == "no"
                and parse_bool(row[field])
            ],
            "false_negative": [
                row["sample_id"]
                for row in joined
                if row["gold_semantic_dependency"] == "yes"
                and not parse_bool(row[field])
            ],
        }

    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in joined:
        grouped[row["model"]].append(row)
    for model, rows in sorted(grouped.items()):
        summary["by_model"][model] = {
            baseline: binary_metrics(rows, field)
            for baseline, field in baselines.items()
        }
    return summary


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=Path, default=DEFAULT_BATCH)
    parser.add_argument("--key", type=Path, default=DEFAULT_KEY)
    parser.add_argument("--gold", type=Path, default=DEFAULT_GOLD)
    parser.add_argument("--predictions", type=Path, default=DEFAULT_PREDICTIONS)
    parser.add_argument("--summary", type=Path, default=DEFAULT_SUMMARY)
    parser.add_argument("--threshold", type=float, default=0.35)
    parser.add_argument("--margin-threshold", type=float, default=0.08)
    parser.add_argument("--llm-judge", type=Path, default=None)
    parser.add_argument("--embedding", type=Path, default=None)
    args = parser.parse_args()

    joined = join_predictions(
        read_csv(args.batch),
        read_csv(args.key),
        read_csv(args.gold),
        args.threshold,
        args.margin_threshold,
        read_jsonl(args.llm_judge) if args.llm_judge else None,
        read_csv(args.embedding) if args.embedding else None,
    )
    summary = evaluate(joined, args.threshold, args.margin_threshold)
    write_csv(args.predictions, joined)
    args.summary.parent.mkdir(parents=True, exist_ok=True)
    args.summary.write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.predictions} ({len(joined)} rows)")
    print(f"wrote {args.summary}")
    for name, metrics in summary["overall"].items():
        print(
            f"{name}: precision={metrics['precision']:.3f} "
            f"recall={metrics['recall']:.3f} f1={metrics['f1']:.3f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

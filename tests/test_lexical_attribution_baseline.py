import sys
import unittest
from pathlib import Path


EXPERIMENTS_DIR = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS_DIR))

from lexical_attribution_baseline import (  # noqa: E402
    binary_metrics,
    pair_features,
    score_annotation_row,
)


def annotation_row(claim: str, pre: str, future: str) -> dict:
    return {
        "sample_id": "sample_1",
        "claim_text": claim,
        "pre_cutoff_evidence": (
            f'[{{"id":"e1","text":"{pre}"}}]'
        ),
        "post_cutoff_evidence_text": future,
    }


class LexicalAttributionBaselineTests(unittest.TestCase):
    def test_exact_number_and_fact_produce_high_score(self):
        features = pair_features(
            "Q4 revenue reached 302.6 million dollars.",
            "The company reported Q4 revenue of 302.6 million dollars.",
        )

        self.assertGreater(features["score"], 0.5)
        self.assertEqual(features["numeric_overlap_count"], 1)

    def test_pre_cutoff_overlap_blocks_false_candidate(self):
        row = annotation_row(
            claim="The company faces a severe inventory glut.",
            pre="Analysts warned of a severe inventory glut.",
            future="The company later reduced shipments because of inventory.",
        )
        scored = score_annotation_row(
            row,
            threshold=0.20,
            margin_threshold=0.05,
        )

        self.assertFalse(scored["provisional_candidate"])
        self.assertLess(scored["future_minus_pre_margin"], 0)

    def test_unrelated_text_is_not_candidate(self):
        row = annotation_row(
            claim="Demand weakened in Europe.",
            pre="Analysts discussed demand in Europe.",
            future="The board appointed a new chief legal officer.",
        )
        scored = score_annotation_row(
            row,
            threshold=0.35,
            margin_threshold=0.08,
        )

        self.assertFalse(scored["provisional_candidate"])

    def test_binary_metrics_exclude_uncertain_and_blank(self):
        scored = [
            {"sample_id": "a", "provisional_candidate": True},
            {"sample_id": "b", "provisional_candidate": True},
            {"sample_id": "c", "provisional_candidate": False},
            {"sample_id": "d", "provisional_candidate": False},
        ]
        annotations = [
            {"sample_id": "a", "label_semantic_dependency": "yes"},
            {"sample_id": "b", "label_semantic_dependency": "no"},
            {"sample_id": "c", "label_semantic_dependency": "yes"},
            {"sample_id": "d", "label_semantic_dependency": "uncertain"},
        ]

        metrics = binary_metrics(scored, annotations)

        self.assertEqual(metrics["tp"], 1)
        self.assertEqual(metrics["fp"], 1)
        self.assertEqual(metrics["fn"], 1)
        self.assertEqual(metrics["excluded_blank_or_uncertain"], 1)
        self.assertAlmostEqual(metrics["f1"], 0.5)


if __name__ == "__main__":
    unittest.main()

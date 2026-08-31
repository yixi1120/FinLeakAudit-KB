import sys
import unittest
from pathlib import Path


EXPERIMENTS_DIR = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS_DIR))

from evaluate_semantic_baselines import (  # noqa: E402
    binary_metrics,
    index_unique,
    join_predictions,
    parse_bool,
    wilson_interval,
)


class SemanticBaselineTests(unittest.TestCase):
    def test_parse_bool_accepts_serialized_csv_values(self):
        self.assertTrue(parse_bool("True"))
        self.assertFalse(parse_bool("false"))
        with self.assertRaises(ValueError):
            parse_bool("maybe")

    def test_binary_metrics_excludes_uncertain(self):
        rows = [
            {"gold_semantic_dependency": "yes", "prediction": True},
            {"gold_semantic_dependency": "no", "prediction": True},
            {"gold_semantic_dependency": "yes", "prediction": False},
            {"gold_semantic_dependency": "uncertain", "prediction": True},
        ]
        metrics = binary_metrics(rows, "prediction")

        self.assertEqual(metrics["evaluated"], 3)
        self.assertEqual(metrics["excluded_uncertain"], 1)
        self.assertEqual(metrics["tp"], 1)
        self.assertEqual(metrics["fp"], 1)
        self.assertEqual(metrics["fn"], 1)
        self.assertAlmostEqual(metrics["f1"], 0.5)

    def test_wilson_interval_contains_observed_proportion(self):
        lower, upper = wilson_interval(40, 44)
        self.assertLess(lower, 40 / 44)
        self.assertGreater(upper, 40 / 44)

    def test_index_unique_rejects_duplicate_sample_ids(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            index_unique([{"sample_id": "a"}, {"sample_id": "a"}], "test")

    def test_join_rejects_misaligned_inputs(self):
        batch = [{"sample_id": "a", "claim_text": "", "pre_cutoff_evidence": "[]", "post_cutoff_evidence_text": ""}]
        key = [{"sample_id": "b"}]
        gold = [{"sample_id": "a"}]
        with self.assertRaisesRegex(ValueError, "do not match"):
            join_predictions(batch, key, gold, 0.35, 0.08)


if __name__ == "__main__":
    unittest.main()

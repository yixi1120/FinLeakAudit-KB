import sys
import unittest
from pathlib import Path


EXPERIMENTS_DIR = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS_DIR))

from analyze import summarize  # noqa: E402


class AnalysisSummaryTests(unittest.TestCase):
    def test_accuracy_removal_and_usage_metrics(self):
        row = {
            "label": "UP",
            "outcome_label": "UP",
            "clean": {
                "prediction": "DOWN",
                "_usage": {"prompt_tokens": 10, "completion_tokens": 2},
            },
            "leaky": {
                "prediction": "UP",
                "_usage": {"prompt_tokens": 12, "completion_tokens": 3},
            },
            "audited": {
                "prediction": "DOWN",
                "rationale": [{"evidence_ids": ["e1"]}],
                "_usage": {"prompt_tokens": 10, "completion_tokens": 2},
            },
            "audit": {
                "removed_evidence_ids": ["e4"],
                "temporal_check": [
                    {"evidence_id": "e1", "temporal_status": "valid"},
                    {"evidence_id": "e4", "temporal_status": "future_leakage"},
                ],
            },
            "metrics": {
                "leaky_cited_future": True,
                "prediction_flipped_clean_to_leaky": True,
                "audited_recovered_clean_direction": True,
                "confidence_delta_leaky_minus_clean": 0.1,
            },
            "elapsed_seconds": 5.0,
        }

        summary = summarize([row])

        self.assertEqual(summary["prediction_flips"], 1)
        self.assertEqual(summary["revision_recovered_flips"], 1)
        self.assertEqual(summary["audited_recovery_rate"], 1.0)
        self.assertEqual(summary["audited_clean_agreement_rate"], 1.0)
        self.assertEqual(summary["clean_accuracy"], 0.0)
        self.assertEqual(summary["leaky_accuracy"], 1.0)
        self.assertEqual(summary["audited_accuracy"], 0.0)
        self.assertEqual(summary["future_removal_precision"], 1.0)
        self.assertEqual(summary["future_removal_recall"], 1.0)
        self.assertEqual(summary["audited_rationale_purity_rate"], 1.0)
        self.assertEqual(summary["api_calls"], 3)
        self.assertEqual(summary["total_tokens"], 39)


if __name__ == "__main__":
    unittest.main()

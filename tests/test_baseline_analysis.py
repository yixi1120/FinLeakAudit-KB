import sys
import unittest
from pathlib import Path


EXPERIMENTS_DIR = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS_DIR))

from analyze_baselines import build_case_rows, summarize_policy  # noqa: E402


def result_row(
    *,
    case_id: str,
    outcome: str,
    clean: str,
    leaky: str,
    audited: str,
    cited: bool,
    removed: bool,
) -> dict:
    return {
        "case_id": case_id,
        "model": "test-model",
        "model_id": "test-model-v1",
        "dataset_tier": "test-tier",
        "outcome_label": outcome,
        "clean": {"prediction": clean},
        "leaky": {"prediction": leaky},
        "audited": {"prediction": audited},
        "audit": {
            "removed_evidence_ids": ["e4"] if removed else [],
            "temporal_check": [
                {"evidence_id": "e1", "temporal_status": "valid"},
                {"evidence_id": "e4", "temporal_status": "future_leakage"},
            ],
        },
        "metrics": {"leaky_cited_future": cited},
        "ablation": [
            {
                "evidence_id": "e4",
                "is_future_leakage": True,
                "is_flip_driver": clean != leaky,
            }
        ],
    }


class BaselineAnalysisTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            result_row(
                case_id="case_1",
                outcome="UP",
                clean="DOWN",
                leaky="UP",
                audited="DOWN",
                cited=True,
                removed=True,
            ),
            result_row(
                case_id="case_2",
                outcome="DOWN",
                clean="DOWN",
                leaky="DOWN",
                audited="DOWN",
                cited=False,
                removed=False,
            ),
        ]

    def test_policy_accuracy_and_retention(self):
        no_audit = summarize_policy(self.rows, "no_audit")
        timestamp = summarize_policy(self.rows, "timestamp_only")
        citation = summarize_policy(self.rows, "citation_only")

        self.assertEqual(no_audit["correct_predictions"], 2)
        self.assertEqual(no_audit["retained_future_items"], 2)
        self.assertEqual(timestamp["correct_predictions"], 1)
        self.assertEqual(timestamp["retained_future_items"], 0)
        self.assertEqual(citation["correct_predictions"], 1)
        self.assertEqual(citation["retained_future_items"], 1)
        self.assertEqual(citation["changes_vs_no_audit"], 1)

    def test_compact_case_rows_preserve_audit_signals(self):
        rows = build_case_rows(self.rows)

        self.assertEqual(len(rows), 2)
        self.assertTrue(rows[0]["explicit_future_citation"])
        self.assertEqual(rows[0]["removed_future_items"], 1)
        self.assertTrue(rows[0]["future_flip_driver"])
        self.assertFalse(rows[1]["explicit_future_citation"])
        self.assertEqual(rows[1]["removed_future_items"], 0)


if __name__ == "__main__":
    unittest.main()

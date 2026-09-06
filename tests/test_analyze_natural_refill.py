import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "experiments"
sys.path.insert(0, str(EXPERIMENTS))

from analyze_natural_refill import (  # noqa: E402
    build_case_rows,
    build_summary,
    read_results,
)


class NaturalRefillAnalysisTests(unittest.TestCase):
    def setUp(self):
        self.rows = read_results(
            [
                ROOT
                / "experiments"
                / "results"
                / f"{model}_natural_refill_5event_v1_results.jsonl"
                for model in ("deepseek", "zhipu", "qwen")
            ]
        )

    def test_frozen_three_model_totals(self):
        overall = build_summary(self.rows)[0]

        self.assertEqual(overall["n_model_events"], 15)
        self.assertEqual(overall["initial_flip_count"], 6)
        self.assertEqual(overall["sparse_recovery_count"], 6)
        self.assertEqual(overall["backfilled_recovery_count"], 6)
        self.assertEqual(overall["nonflip_count"], 9)
        self.assertEqual(overall["sparse_drift_count"], 1)
        self.assertEqual(overall["backfilled_drift_count"], 0)
        self.assertEqual(overall["backfilled_matches_clean_count"], 15)
        self.assertEqual(overall["backfilled_matches_clean_sequence_count"], 12)
        self.assertEqual(overall["outputs_with_citations_count"], 15)
        self.assertEqual(overall["cited_evidence_id_count"], 53)
        self.assertEqual(overall["invalid_citation_id_count"], 0)
        self.assertLess(overall["backfilled_matches_clean_wilson_95_low"], 1.0)
        self.assertEqual(overall["backfilled_matches_clean_wilson_95_high"], 1.0)

    def test_only_qwen_capital_one_changes_sparse_direction(self):
        changed = [
            row
            for row in build_case_rows(self.rows)
            if row["sparse_audited_prediction"]
            != row["backfilled_audited_prediction"]
        ]

        self.assertEqual(len(changed), 1)
        self.assertEqual(changed[0]["model"], "qwen")
        self.assertEqual(changed[0]["event_id"], "natural_007")
        self.assertEqual(changed[0]["backfilled_audited_prediction"], "UP")

    def test_duplicate_model_event_is_rejected(self):
        row = self.rows[0]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.jsonl"
            path.write_text(
                json.dumps(row) + "\n" + json.dumps(row) + "\n",
                encoding="utf-8",
            )
            with self.assertRaisesRegex(ValueError, "Duplicate model-event"):
                read_results([path])


if __name__ == "__main__":
    unittest.main()

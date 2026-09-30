import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "experiments"
sys.path.insert(0, str(EXPERIMENTS))

from analyze_novel_safe_backfill import load_rows, summary_rows  # noqa: E402


class NovelSafeBackfillAnalysisTests(unittest.TestCase):
    def test_frozen_three_model_complete_case_result(self):
        cases = load_rows()
        overall = summary_rows(cases)[0]

        self.assertEqual(len(cases), 18)
        self.assertEqual(overall["initial_flip_count"], 6)
        self.assertEqual(overall["sparse_recovery_count"], 4)
        self.assertEqual(overall["standard_recovery_count"], 6)
        self.assertEqual(overall["novel_recovery_count"], 4)
        self.assertEqual(overall["sparse_drift_count"], 1)
        self.assertEqual(overall["standard_drift_count"], 0)
        self.assertEqual(overall["novel_drift_count"], 1)
        self.assertEqual(overall["sparse_matches_clean_count"], 15)
        self.assertEqual(overall["standard_matches_clean_count"], 18)
        self.assertEqual(overall["novel_matches_clean_count"], 15)
        self.assertEqual(overall["standard_only_match_count"], 3)
        self.assertEqual(overall["novel_only_match_count"], 0)
        self.assertEqual(overall["standard_vs_novel_exact_mcnemar_p"], 0.25)
        self.assertEqual(overall["novel_clean_sequence_match_count"], 0)

    def test_three_novel_safe_mismatches_are_preserved(self):
        mismatches = {
            (row["model"], row["event_id"])
            for row in load_rows()
            if not row["novel_matches_clean"]
        }
        self.assertEqual(
            mismatches,
            {
                ("deepseek", "natural_005"),
                ("qwen", "natural_006"),
                ("qwen", "natural_007"),
            },
        )


if __name__ == "__main__":
    unittest.main()

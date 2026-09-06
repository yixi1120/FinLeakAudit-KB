import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "experiments"
sys.path.insert(0, str(EXPERIMENTS))

from analyze_natural_10event import (  # noqa: E402
    BASE_INPUTS,
    REFILL_INPUTS,
    build_cases,
    build_summary,
    exact_mcnemar_p,
    join_results,
)
from analyze_natural_experiment import read_results as read_base_results  # noqa: E402
from analyze_natural_refill import read_results as read_refill_results  # noqa: E402


class NaturalTenEventAnalysisTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.joined = join_results(
            read_base_results(BASE_INPUTS), read_refill_results(REFILL_INPUTS)
        )

    def test_frozen_totals_and_paired_revision_metrics(self):
        overall = build_summary(self.joined)[0]

        self.assertEqual(overall["n_events"], 10)
        self.assertEqual(overall["n_model_events"], 30)
        self.assertEqual(overall["retained_prediction_calls"], 120)
        self.assertEqual(overall["future_cited_count"], 27)
        self.assertEqual(overall["initial_flip_count"], 13)
        self.assertEqual(overall["sparse_recovery_count"], 11)
        self.assertEqual(overall["backfill_recovery_count"], 13)
        self.assertEqual(overall["sparse_drift_count"], 1)
        self.assertEqual(overall["backfill_drift_count"], 0)
        self.assertEqual(overall["sparse_matches_clean_count"], 27)
        self.assertEqual(overall["backfill_matches_clean_count"], 30)
        self.assertEqual(overall["backfill_matches_clean_sequence_count"], 24)
        self.assertAlmostEqual(overall["paired_exact_mcnemar_p"], 0.25)

    def test_accuracy_and_citation_failures_are_preserved(self):
        overall = build_summary(self.joined)[0]

        self.assertEqual(overall["clean_accuracy"], 11 / 30)
        self.assertEqual(overall["unfiltered_accuracy"], 16 / 30)
        self.assertEqual(overall["sparse_accuracy"], 11 / 30)
        self.assertEqual(overall["backfill_accuracy"], 11 / 30)
        self.assertEqual(overall["base_invalid_citation_id_count"], 30)
        self.assertEqual(overall["refill_invalid_citation_id_count"], 8)
        self.assertEqual(overall["retry_event_count"], 1)

    def test_three_sparse_failures_are_corrected_by_backfill(self):
        corrected = [
            row
            for row in build_cases(self.joined)
            if not row["sparse_matches_clean"] and row["backfill_matches_clean"]
        ]
        self.assertEqual(
            {(row["model"], row["event_id"]) for row in corrected},
            {
                ("deepseek", "natural_005"),
                ("qwen", "natural_006"),
                ("qwen", "natural_007"),
            },
        )

    def test_exact_mcnemar_handles_no_discordance(self):
        self.assertIsNone(exact_mcnemar_p(0, 0))
        self.assertEqual(exact_mcnemar_p(0, 3), 0.25)


if __name__ == "__main__":
    unittest.main()

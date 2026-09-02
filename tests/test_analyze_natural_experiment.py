import sys
import unittest
from pathlib import Path


EXPERIMENTS = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS))

from analyze_natural_experiment import build_summary, wilson_interval  # noqa: E402


def result(model: str, flipped: bool, cited: bool, correct=(False, True, False)) -> dict:
    clean_direction = "UP"
    unfiltered_direction = "DOWN" if flipped else clean_direction
    return {
        "model": model,
        "event_id": f"event_{model}_{flipped}_{cited}",
        "clean": {"prediction": clean_direction, "_usage": {"total_tokens": 10}},
        "unfiltered": {
            "prediction": unfiltered_direction,
            "_usage": {"total_tokens": 20},
        },
        "audited": {"prediction": clean_direction, "_usage": {"total_tokens": 10}},
        "retrieval": {
            "clean_evidence": [],
            "unfiltered_evidence": [],
            "audited_evidence": [],
        },
        "metrics": {
            "future_evidence_retrieved": True,
            "future_evidence_cited": cited,
            "prediction_changed_clean_to_unfiltered": flipped,
            "audited_recovered_clean_direction": True,
            "clean_correct": correct[0],
            "unfiltered_correct": correct[1],
            "audited_correct": correct[2],
            "confidence_delta_unfiltered_minus_clean": 0.1,
        },
    }


class AnalyzeNaturalExperimentTests(unittest.TestCase):
    def test_summary_separates_flip_recovery_and_overall_match(self):
        rows = [
            result("a", flipped=True, cited=True),
            result("a", flipped=False, cited=False),
        ]

        overall = build_summary(rows)[0]

        self.assertEqual(overall["n_model_events"], 2)
        self.assertEqual(overall["model_calls"], 6)
        self.assertEqual(overall["direction_flip_rate"], 0.5)
        self.assertEqual(overall["recovery_rate_among_flips"], 1.0)
        self.assertEqual(overall["audited_matches_clean_rate"], 1.0)
        self.assertEqual(overall["explicit_future_citation_rate"], 0.5)
        self.assertEqual(overall["audited_drift_without_initial_flip_count"], 0)
        self.assertEqual(overall["total_tokens"], 80)
        self.assertEqual(overall["invalid_citation_id_count"], 0)

    def test_wilson_interval_reflects_small_all_success_sample(self):
        low, high = wilson_interval(4, 4)

        self.assertAlmostEqual(low, 0.5101, places=3)
        self.assertAlmostEqual(high, 1.0, places=6)

    def test_reports_audited_drift_when_no_initial_flip_occurred(self):
        row = result("a", flipped=False, cited=True)
        row["audited"]["prediction"] = "NEUTRAL"
        row["metrics"]["audited_recovered_clean_direction"] = False

        overall = build_summary([row])[0]

        self.assertEqual(overall["direction_flip_count"], 0)
        self.assertEqual(overall["audited_drift_without_initial_flip_count"], 1)
        self.assertEqual(overall["audited_drift_without_initial_flip_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()

import sys
import unittest
from pathlib import Path
from unittest.mock import patch


EXPERIMENTS_DIR = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS_DIR))

import run_experiment  # noqa: E402
from config import ModelConfig  # noqa: E402
from finleakaudit import temporal_availability_check  # noqa: E402
from prompts import build_prediction_prompt  # noqa: E402


class AuditedEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.case = {
            "case_id": "logic_test",
            "prediction_date": "Day T",
            "clean_evidence": [
                {"id": "e1", "time": "T-1", "text": "negative context"}
            ],
            "leaked_evidence": [
                {"id": "e4", "time": "T+1", "text": "future context"}
            ],
        }
        self.model = ModelConfig(
            name="fake",
            base_url="http://unused",
            api_key="unused",
            model="fake",
        )

    @staticmethod
    def prediction_for_prompt(prompt):
        if "e4" in prompt:
            return {
                "prediction": "UP",
                "confidence": 0.8,
                "rationale": [],
            }
        return {
            "prediction": "DOWN",
            "confidence": 0.6,
            "rationale": [],
        }

    def test_missed_leakage_stays_in_audited_context(self):
        with patch.object(
            run_experiment,
            "call_chat",
            side_effect=lambda config, prompt: self.prediction_for_prompt(prompt),
        ):
            result = run_experiment.run_case(self.case, self.model, seed=18)

        self.assertFalse(result["audit"]["leakage_detected"])
        self.assertEqual(result["audit"]["removed_evidence_ids"], [])
        self.assertEqual(set(result["audited_evidence_order"]), {"e1", "e4"})
        self.assertEqual(result["audited"]["prediction"], "UP")
        self.assertFalse(result["metrics"]["audited_recovered_clean_direction"])

    def test_detected_future_evidence_is_removed(self):
        def cited_prediction(config, prompt):
            prediction = self.prediction_for_prompt(prompt)
            if "e4" in prompt:
                prediction["rationale"] = [{"evidence_ids": ["e4"]}]
            return prediction

        with patch.object(run_experiment, "call_chat", side_effect=cited_prediction):
            result = run_experiment.run_case(self.case, self.model, seed=18)

        self.assertTrue(result["audit"]["leakage_detected"])
        self.assertEqual(result["audit"]["removed_evidence_ids"], ["e4"])
        self.assertEqual(result["audited_evidence_order"], ["e1"])
        self.assertEqual(result["audited"]["prediction"], "DOWN")
        self.assertTrue(result["metrics"]["audited_recovered_clean_direction"])


class TemporalAvailabilityTests(unittest.TestCase):
    def test_absolute_timestamp_overrides_misleading_relative_label(self):
        cutoff = "2024-06-13T16:00:00-04:00"
        evidence = {
            "id": "e4",
            "time": "T-1",
            "available_at": "2024-06-13T20:06:10Z",
        }

        result = temporal_availability_check([evidence], cutoff)[0]

        self.assertEqual(result["temporal_status"], "future_leakage")
        self.assertEqual(result["availability_basis"], "absolute_timestamp")

    def test_absolute_timestamp_prevents_false_positive_from_t_plus_label(self):
        cutoff = "2024-10-15T13:30:00-04:00"
        evidence = {
            "id": "e4",
            "time": "T+1",
            "available_at": "2024-10-15T12:17:00-04:00",
        }

        result = temporal_availability_check([evidence], cutoff)[0]

        self.assertEqual(result["temporal_status"], "valid")
        self.assertEqual(result["availability_basis"], "absolute_timestamp")

    def test_evidence_available_at_cutoff_is_valid(self):
        cutoff = "2024-05-01T16:00:00-04:00"
        evidence = {"id": "e1", "available_at": cutoff}

        result = temporal_availability_check([evidence], cutoff)[0]

        self.assertEqual(result["temporal_status"], "valid")


class PredictorVisibilityTests(unittest.TestCase):
    def test_prompt_hides_audit_and_evaluator_metadata(self):
        case = {"prediction_date": "2024-06-13T16:00:00-04:00"}
        evidence = [
            {
                "id": "e4",
                "time": "T+1",
                "sentiment": "positive",
                "available_at": "2024-06-13T20:06:10Z",
                "text": "Revenue increased year over year.",
            }
        ]

        prompt = build_prediction_prompt(case, evidence)

        self.assertIn("- e4 | Revenue increased year over year.", prompt)
        self.assertNotIn("T+1", prompt)
        self.assertNotIn("sentiment", prompt)
        self.assertNotIn("available_at", prompt)


if __name__ == "__main__":
    unittest.main()

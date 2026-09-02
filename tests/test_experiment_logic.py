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

    def test_semantic_policy_closes_citation_free_revision_loop(self):
        def uncited_prediction(config, prompt):
            prediction = self.prediction_for_prompt(prompt)
            if "e4" in prompt:
                prediction["rationale"] = [
                    {
                        "claim": "The latest result is strongly positive.",
                        "evidence_ids": ["e1"],
                    }
                ]
            return prediction

        judge = ModelConfig(
            name="judge",
            base_url="http://unused",
            api_key="unused",
            model="judge-v1",
        )
        judgment = {
            "semantic_dependency": "yes",
            "relation": "support",
            "confidence": 0.95,
            "reason": "The latest result appears only in future evidence.",
            "judge_model": "judge",
            "judge_model_id": "judge-v1",
            "usage": {},
            "raw_content": "{}",
        }
        with (
            patch.object(
                run_experiment,
                "call_chat",
                side_effect=uncited_prediction,
            ),
            patch.object(
                run_experiment,
                "call_semantic_judge",
                return_value=judgment,
            ) as semantic_call,
        ):
            result = run_experiment.run_case(
                self.case,
                self.model,
                seed=18,
                audit_policy="semantic_llm",
                judge_config=judge,
            )

        semantic_call.assert_called_once()
        self.assertFalse(result["metrics"]["leaky_cited_future"])
        self.assertTrue(result["metrics"]["leaky_semantic_future"])
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


class CaseSelectionTests(unittest.TestCase):
    def setUp(self):
        self.cases = [
            {"case_id": "case_1"},
            {"case_id": "case_2"},
            {"case_id": "case_3"},
        ]

    def test_select_specific_case_preserves_dataset_order(self):
        selected = run_experiment.select_cases(
            self.cases, ["case_3", "case_1"], None
        )
        self.assertEqual(
            [case["case_id"] for case in selected], ["case_1", "case_3"]
        )

    def test_unknown_case_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "case_9"):
            run_experiment.select_cases(self.cases, ["case_9"], None)


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

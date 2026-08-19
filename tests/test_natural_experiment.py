import sys
import unittest
from pathlib import Path
from unittest.mock import patch


EXPERIMENTS = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS))

from config import ModelConfig  # noqa: E402
from prompts import build_natural_prediction_prompt  # noqa: E402
from run_natural_experiment import (  # noqa: E402
    MINIMAL_EVENT_IDS,
    prepare_event,
    resolve_events,
    run_event,
    validate_citations,
)


class NaturalExperimentTests(unittest.TestCase):
    def test_audited_input_is_unfiltered_minus_future_ids(self):
        prepared = prepare_event("natural_002", top_k=8)
        unfiltered_ids = {item["id"] for item in prepared["unfiltered_evidence"]}
        removed_ids = set(prepared["removed_evidence_ids"])
        audited_ids = {item["id"] for item in prepared["audited_evidence"]}

        self.assertTrue(removed_ids)
        self.assertEqual(audited_ids, unfiltered_ids - removed_ids)
        self.assertTrue(audited_ids.isdisjoint(removed_ids))

    def test_prompt_hides_evidence_audit_and_evaluator_metadata(self):
        case = {
            "company": "Example Corp",
            "ticker": "EXM",
            "prediction_cutoff": "2024-01-02T16:00:00-05:00",
            "forecast_horizon": "next trading day close",
        }
        evidence = [
            {
                "id": "doc::chunk_001",
                "text": "Revenue guidance was raised.",
                "available_at": "2024-01-03T09:00:00-05:00",
                "canonical_url": "https://future.example/report",
                "outcome_label": "UP",
            }
        ]

        prompt = build_natural_prediction_prompt(case, evidence)

        self.assertIn("Revenue guidance was raised.", prompt)
        self.assertIn("2024-01-02T16:00:00-05:00", prompt)
        self.assertNotIn("2024-01-03T09:00:00-05:00", prompt)
        self.assertNotIn("https://future.example/report", prompt)
        self.assertNotIn("outcome_label", prompt)

    def test_run_event_calls_exactly_three_prediction_conditions(self):
        output = {
            "prediction": "UP",
            "confidence": 0.7,
            "rationale": [],
        }
        model = ModelConfig(
            name="test",
            base_url="https://example.invalid",
            api_key="test",
            model="test-model",
        )

        with patch("run_natural_experiment.call_chat", side_effect=[output] * 3) as call:
            result = run_event("natural_002", model, top_k=8)

        self.assertEqual(call.call_count, 3)
        self.assertEqual(result["audit"]["removed_evidence_ids"], [
            row["evidence_id"]
            for row in result["audit"]["temporal_check"]
            if row["temporal_status"] == "future_leakage"
        ])
        self.assertEqual(result["audit_policy"], result["audit"]["policy"])

    def test_minimal_event_set_is_frozen_and_unique(self):
        self.assertEqual(resolve_events(None, minimal=True, limit=None), MINIMAL_EVENT_IDS)
        with self.assertRaisesRegex(ValueError, "must be unique"):
            resolve_events(["natural_001", "natural_001"], minimal=False, limit=None)

    def test_citation_validation_rejects_shortened_document_id(self):
        prediction = {
            "rationale": [{"evidence_ids": ["doc_001", "doc_002::chunk_001"]}]
        }
        evidence = [
            {"id": "doc_001::chunk_001"},
            {"id": "doc_002::chunk_001"},
        ]

        report = validate_citations(prediction, evidence)

        self.assertEqual(report["invalid_citation_ids"], ["doc_001"])
        self.assertFalse(report["all_citations_valid"])


if __name__ == "__main__":
    unittest.main()

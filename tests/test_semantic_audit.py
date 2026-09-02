import sys
import unittest
from pathlib import Path


EXPERIMENTS_DIR = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS_DIR))

from finleakaudit import audit_prediction  # noqa: E402
from semantic_attribution import build_semantic_prompt  # noqa: E402


class SemanticAuditOperatorTests(unittest.TestCase):
    def setUp(self):
        self.case = {
            "prediction_date": "Day T",
            "clean_evidence": [
                {"id": "e1", "time": "T-1", "text": "Historical context."}
            ],
            "leaked_evidence": [
                {"id": "e4", "time": "T+1", "text": "Future result."}
            ],
        }

    def judgment(self, dependency: str, confidence: float) -> dict:
        return {
            "claim_index": 0,
            "claim": "Current results are mixed.",
            "evidence_id": "e4",
            "semantic_dependency": dependency,
            "relation": "support",
            "confidence": confidence,
        }

    def test_citation_free_semantic_dependency_is_removed(self):
        prediction = {
            "rationale": [
                {"claim": "Current results are mixed.", "evidence_ids": ["e1"]}
            ]
        }

        audit = audit_prediction(
            self.case,
            prediction,
            policy="semantic_llm",
            semantic_judgments=[self.judgment("yes", 0.9)],
        )

        self.assertFalse(audit["citation_report"]["has_leakage"])
        self.assertTrue(audit["semantic_report"]["has_leakage"])
        self.assertEqual(audit["removed_evidence_ids"], ["e4"])
        self.assertTrue(audit["audit_complete"])

    def test_redundant_explicit_citation_is_retained_by_semantic_policy(self):
        prediction = {
            "rationale": [
                {"claim": "Historical context remains relevant.", "evidence_ids": ["e4"]}
            ]
        }

        audit = audit_prediction(
            self.case,
            prediction,
            policy="semantic_llm",
            semantic_judgments=[self.judgment("no", 0.95)],
        )

        self.assertTrue(audit["citation_report"]["has_leakage"])
        self.assertFalse(audit["semantic_report"]["has_leakage"])
        self.assertEqual(audit["removed_evidence_ids"], [])

    def test_low_confidence_yes_does_not_trigger_removal(self):
        prediction = {"rationale": [{"claim": "Current results are mixed."}]}

        audit = audit_prediction(
            self.case,
            prediction,
            policy="semantic_llm",
            semantic_judgments=[self.judgment("yes", 0.69)],
            semantic_confidence_threshold=0.7,
        )

        self.assertFalse(audit["leakage_detected"])
        self.assertEqual(audit["removed_evidence_ids"], [])

    def test_timestamp_policy_removes_all_known_future_evidence(self):
        prediction = {"rationale": []}

        audit = audit_prediction(
            self.case,
            prediction,
            policy="timestamp_only",
        )

        self.assertEqual(audit["removed_evidence_ids"], ["e4"])
        self.assertEqual(
            audit["removal_decisions"][0]["removal_basis"],
            "post_cutoff_timestamp",
        )

    def test_full_semantic_keeps_compliance_separate_from_attribution(self):
        prediction = {
            "rationale": [
                {"claim": "Historical context remains relevant.", "evidence_ids": ["e4"]}
            ]
        }

        audit = audit_prediction(
            self.case,
            prediction,
            policy="full_semantic",
            semantic_judgments=[self.judgment("no", 0.95)],
        )

        self.assertFalse(audit["semantic_report"]["has_leakage"])
        self.assertEqual(audit["removed_evidence_ids"], ["e4"])
        self.assertEqual(
            audit["removal_decisions"][0]["removal_basis"],
            "post_cutoff_timestamp",
        )

    def test_semantic_prompt_hides_ids_and_time_metadata(self):
        prompt = build_semantic_prompt(
            "Current results are mixed.",
            [{"id": "e1", "time": "T-1", "text": "Historical context."}],
            {"id": "e4", "time": "T+1", "text": "Future result."},
        )

        self.assertIn("Historical context.", prompt)
        self.assertIn("Future result.", prompt)
        self.assertNotIn("e1", prompt)
        self.assertNotIn("e4", prompt)
        self.assertNotIn("T-1", prompt)
        self.assertNotIn("T+1", prompt)


if __name__ == "__main__":
    unittest.main()

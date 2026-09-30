import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "experiments"
sys.path.insert(0, str(EXPERIMENTS))

from config import ModelConfig  # noqa: E402
from run_natural_experiment import prepare_event  # noqa: E402
from run_natural_refill_baseline import (  # noqa: E402
    SOURCE_RESULTS,
    build_novel_safe_refilled_evidence,
    build_refilled_evidence,
    read_source_results,
    run_refill_event,
)


class NaturalRefillBaselineTests(unittest.TestCase):
    def test_backfill_is_safe_unique_and_full_size(self):
        prepared = prepare_event("natural_007", top_k=8)
        refilled, added = build_refilled_evidence(prepared, top_k=8)
        ids = [item["id"] for item in refilled]

        self.assertEqual(len(ids), 8)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(set(added).isdisjoint(prepared["removed_evidence_ids"]))
        self.assertTrue(
            set(item["id"] for item in prepared["audited_evidence"]).issubset(ids)
        )

    def test_backfill_preserves_survivors_then_uses_clean_rank_order(self):
        prepared = prepare_event("natural_007", top_k=8)
        refilled, added = build_refilled_evidence(prepared, top_k=8)
        sparse_ids = [item["id"] for item in prepared["audited_evidence"]]
        clean_fallback = [
            item["id"]
            for item in prepared["clean_evidence"]
            if item["id"] not in set(sparse_ids)
        ]

        self.assertEqual([item["id"] for item in refilled[: len(sparse_ids)]], sparse_ids)
        self.assertEqual(added, clean_fallback[: len(added)])
        self.assertEqual(
            [item["id"] for item in refilled],
            [item["id"] for item in prepared["clean_evidence"]],
        )

    def test_jetblue_backfill_is_not_assumed_to_equal_clean_ranking(self):
        prepared = prepare_event("natural_010", top_k=8)
        refilled, _ = build_refilled_evidence(prepared, top_k=8)

        self.assertNotEqual(
            [item["id"] for item in refilled],
            [item["id"] for item in prepared["clean_evidence"]],
        )

    def test_novel_safe_backfill_excludes_clean_additions(self):
        prepared = prepare_event("natural_007", top_k=8)
        refilled, added, metadata = build_novel_safe_refilled_evidence(
            prepared, top_k=8
        )
        clean_ids = {item["id"] for item in prepared["clean_evidence"]}
        sparse_ids = [item["id"] for item in prepared["audited_evidence"]]

        self.assertTrue(metadata["novel_safe_backfill_complete"])
        self.assertEqual(len(refilled), 8)
        self.assertTrue(set(added).isdisjoint(clean_ids))
        self.assertEqual(
            [item["id"] for item in refilled[: len(sparse_ids)]], sparse_ids
        )

    def test_novel_safe_backfill_freezes_incomplete_event(self):
        prepared = prepare_event("natural_001", top_k=8)
        refilled, added, metadata = build_novel_safe_refilled_evidence(
            prepared, top_k=8
        )

        self.assertFalse(metadata["novel_safe_backfill_complete"])
        self.assertEqual(len(refilled), 5)
        self.assertEqual(added, [])
        self.assertEqual(metadata["novel_safe_eligible_candidate_count"], 0)

    def test_refill_event_adds_only_one_new_model_call(self):
        source_path = SOURCE_RESULTS["qwen"]
        source = read_source_results(source_path)["natural_007"]
        model = ModelConfig(
            name="qwen",
            base_url="http://example.invalid/v1",
            api_key="none",
            model="test-model",
        )
        output = {
            "prediction": "UP",
            "confidence": 0.7,
            "rationale": [],
        }

        with patch("run_natural_refill_baseline.predict", return_value=output) as call:
            result = run_refill_event(
                "natural_007", model, source, source_path, top_k=8
            )

        self.assertEqual(call.call_count, 1)
        self.assertTrue(result["revision_context"]["backfilled_matches_clean_sequence"])
        self.assertTrue(result["metrics"]["backfilled_audited_matches_clean"])
        self.assertFalse(
            result["metrics"]["backfilled_revision_drift_without_initial_flip"]
        )
        json.dumps(result)

    def test_novel_safe_refill_event_adds_only_one_new_model_call(self):
        source_path = SOURCE_RESULTS["qwen"]
        source = read_source_results(source_path)["natural_007"]
        model = ModelConfig(
            name="qwen",
            base_url="http://example.invalid/v1",
            api_key="none",
            model="test-model",
        )
        output = {
            "prediction": "UP",
            "confidence": 0.7,
            "rationale": [],
        }

        with patch("run_natural_refill_baseline.predict", return_value=output) as call:
            result = run_refill_event(
                "natural_007",
                model,
                source,
                source_path,
                top_k=8,
                policy_key="novel_safe",
            )

        self.assertEqual(call.call_count, 1)
        self.assertEqual(result["policy_key"], "novel_safe")
        self.assertTrue(
            result["revision_context"]["novel_safe_backfill_complete"]
        )
        self.assertFalse(result["revision_context"]["backfilled_matches_clean_sequence"])
        json.dumps(result)


if __name__ == "__main__":
    unittest.main()

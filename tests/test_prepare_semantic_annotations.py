import sys
import unittest
from pathlib import Path


EXPERIMENTS_DIR = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS_DIR))

from prepare_semantic_annotations import blind_pairs, build_pairs  # noqa: E402


class SemanticAnnotationPreparationTests(unittest.TestCase):
    def setUp(self):
        self.cases = [
            {
                "case_id": "case_1",
                "clean_evidence": [
                    {"id": "e1", "text": "Demand was weak before cutoff."}
                ],
                "leaked_evidence": [
                    {"id": "e2", "text": "Revenue later reached $20 million."}
                ],
            }
        ]
        self.results = [
            {
                "case_id": "case_1",
                "dataset_tier": "controlled",
                "model": "test-model",
                "model_id": "test-model-v1",
                "leaky": {
                    "prediction": "UP",
                    "rationale": [
                        {
                            "claim": "Revenue reached $20 million.",
                            "evidence_ids": ["e2"],
                            "direction": "supports UP",
                        },
                        {
                            "claim": "Demand was weak.",
                            "evidence_ids": ["e1"],
                            "direction": "supports DOWN",
                        },
                    ],
                },
            }
        ]

    def test_builds_one_pair_per_claim_and_future_item(self):
        pairs = build_pairs(self.cases, self.results)

        self.assertEqual(len(pairs), 2)
        self.assertTrue(pairs[0]["explicit_future_citation"])
        self.assertFalse(pairs[1]["explicit_future_citation"])
        self.assertIn("Demand was weak", pairs[0]["pre_cutoff_evidence"])

    def test_blinded_batch_hides_model_case_and_auto_label(self):
        pairs = build_pairs(self.cases, self.results)
        batch, key = blind_pairs(pairs, seed=17)

        self.assertEqual(len(batch), len(key))
        self.assertNotIn("model", batch[0])
        self.assertNotIn("case_id", batch[0])
        self.assertNotIn("explicit_future_citation", batch[0])
        self.assertIn("model", key[0])
        self.assertIn("explicit_future_citation", key[0])
        self.assertEqual(batch[0]["sample_id"], key[0]["sample_id"])


if __name__ == "__main__":
    unittest.main()

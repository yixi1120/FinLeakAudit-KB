import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "experiments"
sys.path.insert(0, str(EXPERIMENTS))

from prepare_natural_semantic_hardset import (  # noqa: E402
    BLIND_FIELDS,
    DEFAULT_INPUTS,
    build_hardset,
    split_events,
)


class NaturalSemanticHardsetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.built = build_hardset(DEFAULT_INPUTS)

    def test_frozen_event_split_is_deterministic_and_disjoint(self):
        first = split_events(
            ["natural_001", "natural_002", "natural_004", "natural_007", "natural_010"]
        )
        second = split_events(
            ["natural_010", "natural_004", "natural_001", "natural_007", "natural_002"]
        )

        self.assertEqual(first, second)
        self.assertEqual(first[0], ["natural_007", "natural_004"])
        self.assertEqual(first[1], ["natural_002", "natural_001", "natural_010"])
        self.assertTrue(set(first[0]).isdisjoint(first[1]))

    def test_reconstructed_hardset_has_expected_frozen_counts(self):
        self.assertEqual(len(self.built["pairs"]), 82)
        self.assertEqual(len(self.built["dev_blind"]), 32)
        self.assertEqual(len(self.built["test_blind"]), 50)
        self.assertEqual(len(self.built["key"]), 82)
        self.assertEqual(
            len(
                {
                    (pair["event_id"], pair["model"], pair["claim_index"])
                    for pair in self.built["pairs"]
                }
            ),
            38,
        )

    def test_blind_rows_hide_provenance_and_automatic_hints(self):
        forbidden = {
            "event_id",
            "case_id",
            "company",
            "model",
            "model_id",
            "post_cutoff_evidence_id",
            "explicit_future_citation",
            "prediction_cutoff",
            "candidate_available_at",
            "outcome_label",
        }
        all_blind = self.built["dev_blind"] + self.built["test_blind"]

        self.assertEqual(list(all_blind[0]), BLIND_FIELDS)
        for row in all_blind:
            self.assertTrue(forbidden.isdisjoint(row))
            self.assertTrue(row["pre_cutoff_evidence"].startswith('[{"text":'))
            self.assertNotIn('"id":', row["pre_cutoff_evidence"])

    def test_every_pair_is_unique_and_maps_to_one_blind_sample(self):
        pair_hashes = {pair["pair_sha256"] for pair in self.built["pairs"]}
        sample_ids = {row["sample_id"] for row in self.built["key"]}

        self.assertEqual(len(pair_hashes), 82)
        self.assertEqual(len(sample_ids), 82)
        self.assertEqual(
            sample_ids,
            {
                row["sample_id"]
                for row in self.built["dev_blind"] + self.built["test_blind"]
            },
        )

    def test_dev_and_test_are_balanced_across_source_models(self):
        dev_key = [row for row in self.built["key"] if row["split"] == "dev"]
        test_key = [row for row in self.built["key"] if row["split"] == "test"]

        self.assertEqual(sum(row["model"] == "deepseek" for row in dev_key), 16)
        self.assertEqual(sum(row["model"] == "zhipu" for row in dev_key), 16)
        self.assertEqual(sum(row["explicit_future_citation"] == "true" for row in dev_key), 15)
        self.assertEqual(sum(row["explicit_future_citation"] == "true" for row in test_key), 23)


if __name__ == "__main__":
    unittest.main()

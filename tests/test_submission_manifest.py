import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "paper" / "submission_manifest_ai4f_2026.json"


class SubmissionManifestTests(unittest.TestCase):
    def test_frozen_input_hashes_and_sizes(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual(manifest["release_tag"], "ai4f-2026-submission-v1")
        for item in manifest["frozen_inputs"]:
            path = ROOT / item["path"]
            payload = path.read_bytes()
            self.assertEqual(len(payload), item["bytes"], item["path"])
            self.assertEqual(
                hashlib.sha256(payload).hexdigest(),
                item["sha256"],
                item["path"],
            )

    def test_headline_counts_are_frozen(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        expected = manifest["expected_results"]

        self.assertEqual(expected["controlled_initial_flips"], 12)
        self.assertEqual(expected["controlled_sparse_recoveries"], 12)
        self.assertEqual(expected["natural_initial_flips"], 13)
        self.assertEqual(expected["natural_sparse_recoveries"], 11)
        self.assertEqual(expected["natural_backfill_recoveries"], 13)
        self.assertEqual(expected["attribution_decisive_pairs"], 78)


if __name__ == "__main__":
    unittest.main()

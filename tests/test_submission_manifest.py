import hashlib
import json
import csv
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "paper" / "submission_manifest_ai4f_2026.json"


class SubmissionManifestTests(unittest.TestCase):
    def test_frozen_input_hashes_and_sizes(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))

        self.assertEqual(manifest["release_tag"], "ai4f-2026-submission-v2")
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

    def test_natural_corpus_counts_are_frozen(self):
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        expected = manifest["expected_natural_corpus"]
        data = ROOT / "数据线"

        documents = 0
        retrieval_units = []
        for index in range(1, expected["event_manifests"] + 1):
            event_id = f"natural_{index:03d}"
            event = json.loads((data / f"{event_id}.json").read_text(encoding="utf-8"))
            documents += len(event["documents"])
            with (data / f"{event_id}_retrieval_units_v1.csv").open(
                encoding="utf-8", newline=""
            ) as handle:
                retrieval_units.extend(csv.DictReader(handle))

        status_counts = {
            status: sum(row["ingest_status"] == status for row in retrieval_units)
            for status in {row["ingest_status"] for row in retrieval_units}
        }
        self.assertEqual(documents, expected["candidate_documents"])
        self.assertEqual(len(retrieval_units), expected["retrieval_units_total"])
        self.assertEqual(status_counts["active"], expected["active_retrieval_units"])
        self.assertEqual(
            status_counts["blocked_historical_snapshot_required"],
            expected["blocked_retrieval_units"],
        )

        with (data / "natural_second_verification_batch_v1.csv").open(
            encoding="utf-8", newline=""
        ) as handle:
            verification = list(csv.DictReader(handle))
        self.assertEqual(len(verification), expected["second_verification_records"])
        for decision in ("accept", "reject", "needs_adjudication"):
            self.assertEqual(
                sum(row["decision"] == decision for row in verification),
                expected[f"second_verification_{decision}ed"]
                if decision != "needs_adjudication"
                else expected["second_verification_needs_adjudication"],
            )


if __name__ == "__main__":
    unittest.main()

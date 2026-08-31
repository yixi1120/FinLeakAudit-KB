import csv
import json
import unittest
from datetime import datetime
from pathlib import Path


from tools.natural_event_registry import EVENT_SPECS
from tools.prepare_natural_second_verification import build_batch


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "数据线"


class NaturalEventMetadataTests(unittest.TestCase):
    def test_manifests_match_registry_and_have_valid_timeline(self):
        for event_id, spec in EVENT_SPECS.items():
            manifest = json.loads((DATA / f"{event_id}.json").read_text(encoding="utf-8"))
            for field in (
                "exchange",
                "trading_calendar",
                "prediction_cutoff",
                "forecast_horizon",
                "event_available_at",
                "event_parent_document_id",
                "outcome_time",
                "outcome_label",
            ):
                self.assertEqual(manifest[field], spec[field], f"{event_id}:{field}")
            cutoff = datetime.fromisoformat(manifest["prediction_cutoff"])
            event = datetime.fromisoformat(manifest["event_available_at"])
            outcome = datetime.fromisoformat(manifest["outcome_time"])
            self.assertLess(cutoff, event)
            self.assertLess(event, outcome)
            self.assertLess(cutoff.weekday(), 5)
            calculated = manifest["outcome_price"] / manifest["cutoff_price"] - 1
            self.assertAlmostEqual(calculated, manifest["outcome_return"], places=6)
            secondary = manifest["secondary_price_verification"]
            self.assertEqual(secondary["provider"], "StatMuse Money")
            self.assertTrue(secondary["direction_match"], event_id)

    def test_event_source_is_an_active_retrieval_unit(self):
        for event_id in EVENT_SPECS:
            manifest = json.loads((DATA / f"{event_id}.json").read_text(encoding="utf-8"))
            with (DATA / f"{event_id}_retrieval_units_v1.csv").open(
                encoding="utf-8", newline=""
            ) as handle:
                units = list(csv.DictReader(handle))
            source_matches = [
                unit
                for unit in units
                if unit["ingest_status"] == "active"
                and manifest["event_source"]
                in {unit["canonical_url"], unit["timestamp_source_url"]}
            ]
            self.assertTrue(source_matches, event_id)
            self.assertTrue(
                any(
                    unit["ingest_status"] == "active"
                    and unit["parent_document_id"] == manifest["event_parent_document_id"]
                    for unit in units
                ),
                event_id,
            )

    def test_second_verifier_batch_includes_all_post_cutoff_documents(self):
        manifests = [
            json.loads((DATA / f"{event_id}.json").read_text(encoding="utf-8"))
            for event_id in EVENT_SPECS
        ]
        batch = build_batch(manifests)
        selected = {(row["event_id"], row["document_id"]) for row in batch}
        for manifest in manifests:
            cutoff = datetime.fromisoformat(manifest["prediction_cutoff"])
            for document in manifest["documents"]:
                if not document["available_at"] or datetime.fromisoformat(
                    document["available_at"]
                ) > cutoff:
                    self.assertIn(
                        (manifest["event_id"], document["document_id"]), selected
                    )

    def test_completed_second_verification_is_valid(self):
        with (DATA / "natural_second_verification_batch_v1.csv").open(
            encoding="utf-8", newline=""
        ) as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 139)
        allowed = {
            "url_content_match": {"yes", "no", "uncertain"},
            "timestamp_evidence_match": {"yes", "no", "uncertain"},
            "archive_hash_match": {"yes", "no"},
            "decision": {"accept", "reject", "needs_adjudication"},
        }
        review_fields = [
            "second_verifier_id",
            *allowed,
            "verification_notes",
            "verified_at",
        ]
        for row in rows:
            self.assertTrue(all(row[field].strip() for field in review_fields))
            for field, values in allowed.items():
                self.assertIn(row[field], values)
            datetime.fromisoformat(row["verified_at"])
            if row["decision"] == "accept":
                self.assertEqual(
                    (
                        row["url_content_match"],
                        row["timestamp_evidence_match"],
                        row["archive_hash_match"],
                    ),
                    ("yes", "yes", "yes"),
                )

    def test_second_verification_exceptions_are_adjudicated(self):
        with (DATA / "natural_second_verification_batch_v1.csv").open(
            encoding="utf-8", newline=""
        ) as handle:
            verification = list(csv.DictReader(handle))
        expected = {
            row["document_id"]
            for row in verification
            if row["decision"] in {"reject", "needs_adjudication"}
        }
        with (DATA / "natural_second_verification_adjudication_v1.csv").open(
            encoding="utf-8", newline=""
        ) as handle:
            adjudication = list(csv.DictReader(handle))
        self.assertEqual({row["document_id"] for row in adjudication}, expected)
        self.assertTrue(
            all(
                row["coordinator_decision"].strip()
                and row["metadata_action"].strip()
                and row["rationale"].strip()
                and row["adjudicator_id"].strip()
                and row["adjudicated_at"].strip()
                for row in adjudication
            )
        )

    def test_crowdstrike_second_verifier_correction_and_blocks(self):
        manifest = json.loads(
            (DATA / "natural_001.json").read_text(encoding="utf-8")
        )
        tech_alert = next(
            row
            for row in manifest["documents"]
            if row["document_id"] == "natural_001_doc_011"
        )
        self.assertEqual(tech_alert["available_at"], "2024-07-19T05:30:00+00:00")
        self.assertEqual(tech_alert["revised_at"], "2024-07-19T09:45:00+00:00")
        with (DATA / "natural_001_retrieval_units_v1.csv").open(
            encoding="utf-8", newline=""
        ) as handle:
            units = {row["retrieval_unit_id"]: row for row in csv.DictReader(handle)}
        for unit_id in (
            "natural_001_doc_016_body_v1",
            "natural_001_doc_018_body_v1",
            "natural_001_doc_019_body_v1",
            "natural_001_doc_020_body_v1",
        ):
            self.assertEqual(
                units[unit_id]["ingest_status"],
                "blocked_historical_snapshot_required",
            )


if __name__ == "__main__":
    unittest.main()

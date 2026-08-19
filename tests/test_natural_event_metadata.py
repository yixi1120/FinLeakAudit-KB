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


if __name__ == "__main__":
    unittest.main()

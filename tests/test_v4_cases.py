import json
import unittest
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "数据线" / "cases_pilot_v4_new7_verified.jsonl"


def parse_timestamp(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


class V4CaseValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = [
            json.loads(line)
            for line in CASES_PATH.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]

    def test_expected_case_count_and_unique_ids(self):
        self.assertEqual(len(self.cases), 7)
        case_ids = [case["case_id"] for case in self.cases]
        self.assertEqual(len(case_ids), len(set(case_ids)))

    def test_evidence_counts_and_urls(self):
        for case in self.cases:
            with self.subTest(case_id=case["case_id"]):
                self.assertEqual(len(case["clean_evidence"]), 3)
                self.assertEqual(len(case["leaked_evidence"]), 1)
                evidence = case["clean_evidence"] + case["leaked_evidence"]
                self.assertEqual(
                    len({item["id"] for item in evidence}),
                    len(evidence),
                )
                for item in evidence:
                    self.assertTrue(item["source_ref"].startswith("https://"))
                    self.assertTrue(item["time_source_ref"].startswith("https://"))

    def test_strict_timeline_ordering(self):
        for case in self.cases:
            cutoff = parse_timestamp(case["prediction_date"])
            outcome = parse_timestamp(case["outcome_time"])
            with self.subTest(case_id=case["case_id"]):
                self.assertLess(cutoff, outcome)
                for item in case["clean_evidence"]:
                    self.assertLessEqual(parse_timestamp(item["available_at"]), cutoff)
                for item in case["leaked_evidence"]:
                    available = parse_timestamp(item["available_at"])
                    self.assertLess(cutoff, available)
                    self.assertLess(available, outcome)

    def test_outcome_return_and_label_are_reproducible(self):
        for case in self.cases:
            calculated = case["outcome_price"] / case["cutoff_price"] - 1
            expected_label = "UP" if calculated > 0 else "DOWN" if calculated < 0 else "NEUTRAL"
            with self.subTest(case_id=case["case_id"]):
                self.assertAlmostEqual(calculated, case["outcome_return"], places=6)
                self.assertEqual(case["label"], expected_label)
                self.assertEqual(case["outcome_label"], expected_label)


if __name__ == "__main__":
    unittest.main()

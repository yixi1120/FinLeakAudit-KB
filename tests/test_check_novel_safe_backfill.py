import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "experiments"
sys.path.insert(0, str(EXPERIMENTS))

from check_novel_safe_backfill import eligibility_rows  # noqa: E402


class NovelSafeBackfillEligibilityTests(unittest.TestCase):
    def test_frozen_complete_case_set(self):
        rows = eligibility_rows(top_k=8)
        complete = {
            row["event_id"]
            for row in rows
            if row["novel_safe_backfill_complete"]
        }

        self.assertEqual(len(rows), 10)
        self.assertEqual(
            complete,
            {
                "natural_002",
                "natural_005",
                "natural_006",
                "natural_007",
                "natural_009",
                "natural_010",
            },
        )


if __name__ == "__main__":
    unittest.main()

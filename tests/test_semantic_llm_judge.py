import sys
import unittest
from pathlib import Path


EXPERIMENTS_DIR = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS_DIR))

from run_semantic_llm_judge import (  # noqa: E402
    format_pre_cutoff,
    normalize_judgment,
)


class SemanticLlmJudgeTests(unittest.TestCase):
    def test_format_pre_cutoff_hides_ids(self):
        formatted = format_pre_cutoff('[{"id":"e1","text":"Known fact."}]')
        self.assertEqual(formatted, "- Known fact.")
        self.assertNotIn("e1", formatted)

    def test_normalize_judgment_clamps_and_validates(self):
        normalized = normalize_judgment(
            {
                "semantic_dependency": "YES",
                "relation": "SUPPORT",
                "confidence": 1.2,
                "reason": " Candidate adds the number. ",
            }
        )
        self.assertEqual(normalized["semantic_dependency"], "yes")
        self.assertEqual(normalized["relation"], "support")
        self.assertEqual(normalized["confidence"], 1.0)
        self.assertEqual(normalized["reason"], "Candidate adds the number.")

    def test_invalid_enums_become_uncertain(self):
        normalized = normalize_judgment(
            {"semantic_dependency": "likely", "relation": "mixed"}
        )
        self.assertEqual(normalized["semantic_dependency"], "uncertain")
        self.assertEqual(normalized["relation"], "uncertain")


if __name__ == "__main__":
    unittest.main()

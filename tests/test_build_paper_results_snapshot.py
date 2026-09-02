import hashlib
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPERIMENTS = ROOT / "experiments"
sys.path.insert(0, str(EXPERIMENTS))

from build_paper_results_snapshot import (  # noqa: E402
    CONTROLLED_INPUTS,
    NATURAL_INPUTS,
    SEMANTIC_INPUT,
    aggregate_forecast,
    controlled_rows,
    natural_rows,
    semantic_rows,
    wrap_label,
)


class PaperResultsSnapshotTests(unittest.TestCase):
    def test_controlled_frozen_totals_match_reported_results(self):
        rows = controlled_rows(CONTROLLED_INPUTS)
        overall = aggregate_forecast(rows, "controlled_injection")

        self.assertEqual(overall["n_model_cases"], 30)
        self.assertEqual(overall["model_calls"], 210)
        self.assertEqual(overall["future_cited_n"], 28)
        self.assertEqual(overall["direction_flip_n"], 12)
        self.assertEqual(overall["recovered_flip_n"], 12)
        self.assertEqual(overall["clean_correct_n"], 8)
        self.assertEqual(overall["contaminated_correct_n"], 18)
        self.assertEqual(overall["audited_correct_n"], 8)

    def test_natural_snapshot_accepts_optional_qwen_result(self):
        rows = natural_rows(NATURAL_INPUTS)
        overall = aggregate_forecast(rows, "natural_replay")

        self.assertEqual(len(rows), 3)
        self.assertEqual(overall["n_model_cases"], 15)
        self.assertEqual(overall["model_calls"], 45)
        self.assertEqual(overall["future_cited_n"], 13)
        self.assertEqual(overall["direction_flip_n"], 6)
        self.assertEqual(overall["recovered_flip_n"], 6)
        self.assertEqual(overall["audited_drift_without_initial_flip_n"], 1)
        self.assertEqual(overall["clean_correct_n"], 6)
        self.assertEqual(overall["contaminated_correct_n"], 12)
        self.assertEqual(overall["audited_correct_n"], 5)

    def test_semantic_metrics_preserve_negative_result(self):
        rows = semantic_rows(SEMANTIC_INPUT)
        by_method = {row["method"]: row for row in rows}

        self.assertEqual(len(rows), 4)
        self.assertEqual(by_method["Citation-only"]["evaluated_pairs"], 78)
        self.assertAlmostEqual(by_method["Citation-only"]["f1"], 0.94117647)
        self.assertAlmostEqual(by_method["DeepSeek LLM judge"]["f1"], 0.93670886)
        self.assertGreater(
            by_method["Citation-only"]["f1"],
            by_method["DeepSeek LLM judge"]["f1"],
        )

    def test_long_chart_labels_wrap_without_losing_words(self):
        lines = wrap_label("Audited drift if no flip")

        self.assertEqual(len(lines), 2)
        self.assertEqual(" ".join(lines), "Audited drift if no flip")

    def test_qwen_runtime_manifest_matches_frozen_result(self):
        manifest_path = (
            ROOT
            / "experiments"
            / "analysis"
            / "qwen_natural_runtime_manifest_2026_09_03.json"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        result_path = ROOT / manifest["experiment"]["result_path"]

        self.assertEqual(
            hashlib.sha256(result_path.read_bytes()).hexdigest(),
            manifest["experiment"]["result_sha256"],
        )
        self.assertEqual(manifest["experiment"]["events"], 5)
        self.assertEqual(manifest["experiment"]["prediction_calls"], 15)
        self.assertTrue(manifest["shutdown_verified"])


if __name__ == "__main__":
    unittest.main()

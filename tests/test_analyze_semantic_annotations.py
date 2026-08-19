import sys
import unittest
from pathlib import Path


EXPERIMENTS_DIR = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS_DIR))

from analyze_semantic_annotations import (  # noqa: E402
    align_annotations,
    build_disagreements,
    cohens_kappa,
    summarize_agreement,
    validate_annotations,
)


def annotation(sample_id="semantic_v1_001", dependency="yes", annotator="a"):
    return {
        "sample_id": sample_id,
        "forecast_prediction": "UP",
        "claim_text": "Revenue reached $20 million.",
        "claim_direction": "supports UP",
        "pre_cutoff_evidence": "[]",
        "post_cutoff_evidence_id": "e4",
        "post_cutoff_evidence_text": "Revenue reached $20 million.",
        "label_semantic_dependency": dependency,
        "label_relation": "support" if dependency == "yes" else "irrelevant",
        "label_exclusive_to_post_cutoff": dependency,
        "label_should_remove": dependency,
        "matched_claim_span": "Revenue reached $20 million" if dependency == "yes" else "",
        "confidence_1_to_5": "5",
        "annotator_id": annotator,
        "notes": "test",
    }


class SemanticAnnotationAnalysisTests(unittest.TestCase):
    def test_perfect_agreement_has_kappa_one(self):
        rows_a = [annotation(annotator="a")]
        rows_b = [annotation(annotator="b")]
        validate_annotations(rows_a, "a")
        validate_annotations(rows_b, "b")
        summary = summarize_agreement(align_annotations(rows_a, rows_b))

        self.assertEqual(summary["n_pairs"], 1)
        self.assertEqual(
            summary["field_metrics"]["label_semantic_dependency"]["cohens_kappa"],
            1.0,
        )
        self.assertEqual(summary["semantic_dependency_disagreement_count"], 0)

    def test_exports_only_label_disagreements(self):
        rows_a = [annotation(dependency="yes", annotator="a")]
        rows_b = [annotation(dependency="no", annotator="b")]
        aligned = align_annotations(rows_a, rows_b)

        disagreements = build_disagreements(aligned)

        self.assertEqual(len(disagreements), 1)
        self.assertEqual(disagreements[0]["a_label_semantic_dependency"], "yes")
        self.assertEqual(disagreements[0]["b_label_semantic_dependency"], "no")
        self.assertEqual(disagreements[0]["adjudicated_label_semantic_dependency"], "")

    def test_rejects_span_not_copied_from_claim(self):
        row = annotation()
        row["matched_claim_span"] = "not in claim"

        with self.assertRaisesRegex(ValueError, "exact claim substring"):
            validate_annotations([row], "a")

    def test_kappa_for_partial_agreement(self):
        value = cohens_kappa(["yes", "yes", "no", "no"], ["yes", "no", "no", "no"])
        self.assertAlmostEqual(value, 0.5)


if __name__ == "__main__":
    unittest.main()

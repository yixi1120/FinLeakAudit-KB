import sys
import unittest
from pathlib import Path


EXPERIMENTS_DIR = Path(__file__).resolve().parents[1] / "experiments"
sys.path.insert(0, str(EXPERIMENTS_DIR))

from run_semantic_embedding_baseline import (  # noqa: E402
    collect_unique_texts,
    cosine,
    score_rows,
)


class SemanticEmbeddingBaselineTests(unittest.TestCase):
    def test_cosine_similarity(self):
        self.assertAlmostEqual(cosine([1.0, 0.0], [1.0, 0.0]), 1.0)
        self.assertAlmostEqual(cosine([1.0, 0.0], [0.0, 1.0]), 0.0)

    def test_collect_unique_texts_deduplicates(self):
        rows = [{
            "claim_text": "claim",
            "post_cutoff_evidence_text": "future",
            "pre_cutoff_evidence": '[{"text":"claim"},{"text":"past"}]',
        }]
        self.assertEqual(
            collect_unique_texts(rows), ["claim", "future", "past"]
        )

    def test_pre_cutoff_similarity_can_block_candidate(self):
        rows = [{
            "sample_id": "a",
            "claim_text": "claim",
            "post_cutoff_evidence_text": "future",
            "pre_cutoff_evidence": '[{"text":"past"}]',
        }]
        vectors = {
            "claim": [1.0, 0.0],
            "future": [0.8, 0.6],
            "past": [1.0, 0.0],
        }
        scored = score_rows(rows, vectors, threshold=0.65, margin_threshold=0.03)
        self.assertFalse(scored[0]["embedding_prediction"])


if __name__ == "__main__":
    unittest.main()

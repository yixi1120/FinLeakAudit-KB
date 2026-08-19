import tempfile
import unittest
from pathlib import Path


from tools.natural_retrieval import (
    cap_parent_versions,
    chunk_text,
    extract_text,
    predictor_view,
    rank_lexical,
)


class NaturalRetrievalTests(unittest.TestCase):
    def test_extracts_visible_html_without_script_or_inline_xbrl_header(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "source.htm"
            path.write_text(
                "<html><script>leak()</script><ix:header>metadata</ix:header>"
                "<body><h1>Results</h1><p>Revenue reached 20 million.</p></body></html>",
                encoding="utf-8",
            )
            text = extract_text(path)

        self.assertIn("Revenue reached 20 million", text)
        self.assertNotIn("leak()", text)
        self.assertNotIn("metadata", text)

    def test_chunks_have_stable_overlap(self):
        chunks = chunk_text("a " * 100, chunk_chars=40, overlap_chars=10)

        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 40 for chunk in chunks))

    def test_parent_cap_keeps_latest_versions(self):
        rows = [
            {
                "retrieval_unit_id": f"update_{index}",
                "parent_document_id": "status_page",
                "available_at": f"2024-01-01T0{index}:00:00+00:00",
            }
            for index in range(1, 5)
        ]

        selected = cap_parent_versions(rows, max_units_per_parent=2)

        self.assertEqual([row["retrieval_unit_id"] for row in selected], ["update_3", "update_4"])

    def test_ranking_caps_chunks_from_same_source(self):
        chunks = [
            {
                "chunk_id": f"a::{index}",
                "parent_document_id": "a",
                "title": "AI revenue",
                "text": "AI revenue growth",
            }
            for index in range(3)
        ] + [
            {
                "chunk_id": "b::1",
                "parent_document_id": "b",
                "title": "Revenue",
                "text": "revenue outlook",
            }
        ]

        ranked = rank_lexical("AI revenue", chunks, top_k=3, max_chunks_per_parent=2)

        self.assertEqual(sum(row["parent_document_id"] == "a" for row in ranked), 2)
        self.assertEqual(len(ranked), 3)

    def test_predictor_view_hides_time_and_url(self):
        view = predictor_view(
            [
                {
                    "chunk_id": "e1",
                    "title": "Title",
                    "source_type": "SEC",
                    "text": "Body",
                    "available_at": "2024-01-02T00:00:00+00:00",
                    "canonical_url": "https://example.com",
                }
            ]
        )

        self.assertNotIn("available_at", view[0])
        self.assertNotIn("canonical_url", view[0])


if __name__ == "__main__":
    unittest.main()

import csv
import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PAPER = (ROOT / "paper" / "main.tex").read_text(encoding="utf-8")
BIB = (ROOT / "paper" / "references.bib").read_text(encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


class PaperConsistencyTests(unittest.TestCase):
    def test_author_order_affiliations_and_contributions_are_frozen(self):
        ordered_authors = ["Ziyang Lu", "Junwei Chen", "Yating Zhang", "Minzhen Lai"]
        positions = [PAPER.index(author) for author in ordered_authors]
        normalized_paper = " ".join(PAPER.split())

        self.assertEqual(positions, sorted(positions))
        self.assertIn("The Hong Kong University of Science and Technology", PAPER)
        self.assertIn("Johns Hopkins University", PAPER)
        self.assertIn("South China Normal University", PAPER)
        self.assertIn("Imperial College London", PAPER)
        self.assertIn("Corresponding author", PAPER)
        self.assertIn("zluca@connect.ust.hk", PAPER)
        self.assertIn("Ziyang Lu led conceptualization", PAPER)
        self.assertIn("Junwei", PAPER)
        self.assertIn("curated the natural point-in-time corpus", PAPER)
        self.assertIn("Yating Zhang", PAPER)
        self.assertIn("claim-span refinement", PAPER)
        self.assertIn("Minzhen Lai", PAPER)
        self.assertIn("independent external reproduction", PAPER)
        self.assertIn("model-stratified robustness analysis", normalized_paper)

    def test_all_citations_resolve_to_bibliography_entries(self):
        cited = set()
        for group in re.findall(r"\\cite\{([^}]+)\}", PAPER):
            cited.update(key.strip() for key in group.split(","))
        defined = set(re.findall(r"^@\w+\{([^,]+),", BIB, flags=re.MULTILINE))

        self.assertTrue(cited)
        self.assertEqual(cited - defined, set())

    def test_withdrawn_finagent_rag_is_not_supporting_evidence(self):
        card = (ROOT / "wiki" / "papers" / "FinAgent_RAG.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("publication_status: withdrawn", card)
        self.assertNotIn("2605.05409", PAPER)
        self.assertNotIn("2605.05409", BIB)

    def test_forecast_counts_match_frozen_analysis(self):
        controlled = next(
            row
            for row in read_csv(
                ROOT
                / "experiments"
                / "analysis"
                / "paper_forecast_audit_metrics_2026_09_03.csv"
            )
            if row["study"] == "controlled_injection" and row["model"] == "All"
        )
        natural = read_csv(
            ROOT
            / "experiments"
            / "analysis"
            / "natural_pit_10event_three_model_summary_v1.csv"
        )[0]

        self.assertIn(
            f"{controlled['future_cited_n']}/{controlled['n_model_cases']}", PAPER
        )
        self.assertIn(
            f"{controlled['direction_flip_n']}/{controlled['n_model_cases']}", PAPER
        )
        self.assertIn(
            f"{controlled['recovered_flip_n']}/{controlled['direction_flip_n']}",
            PAPER,
        )
        self.assertIn(
            f"{natural['future_cited_count']}/{natural['n_model_events']}", PAPER
        )
        self.assertIn(
            f"{natural['initial_flip_count']}/{natural['n_model_events']}", PAPER
        )
        self.assertIn(
            f"{natural['sparse_recovery_count']}/{natural['initial_flip_count']}",
            PAPER,
        )
        self.assertIn(
            f"{natural['backfill_recovery_count']}/{natural['initial_flip_count']}",
            PAPER,
        )

    def test_attribution_metrics_and_claim_boundaries_are_present(self):
        metrics = json.loads(
            (
                ROOT
                / "experiments"
                / "analysis"
                / "semantic_baseline_results_v1.json"
            ).read_text(encoding="utf-8")
        )["overall"]

        for method in ("citation_only", "lexical_overlap", "embedding_similarity", "llm_judge"):
            self.assertIn(f"{metrics[method]['f1']:.3f}", PAPER)
        self.assertIn("do not estimate real-world leakage prevalence", PAPER)
        self.assertIn("does not establish a general Backfill advantage", PAPER)
        self.assertNotRegex(PAPER, r"\b(?:TODO|TBD|PLACEHOLDER)\b")

    def test_competitor_boundary_and_failure_modes_are_explicit(self):
        self.assertIn("model or agent\nbehavior across periods", PAPER)
        self.assertIn("intervenes\non its retrieved context", PAPER)
        self.assertIn("Qwen described CrowdStrike", PAPER)
        self.assertIn("support is not exclusive dependence", PAPER)
        self.assertIn("DeepSeek--Intel", PAPER)
        self.assertIn("ai4f-2026-submission-v1", PAPER)


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SHARED_EXAMPLES = ROOT / "skills" / "_shared" / "paper-production" / "examples"
RESEARCH_REFERENCE = ROOT / "skills" / "materials-research" / "references" / "paper-production-orchestrator.md"


class PaperProductionRouteSmokeTests(unittest.TestCase):
    def test_shared_wer_ea_mini_review_examples_expose_route_shape(self):
        weakness = SHARED_EXAMPLES / "wer-ea-mini-review-weakness-routing.csv"
        gate = SHARED_EXAMPLES / "wer-ea-mini-review-gate-report.md"

        self.assertTrue(weakness.is_file())
        self.assertTrue(gate.is_file())
        weakness_text = weakness.read_text(encoding="utf-8")
        gate_text = gate.read_text(encoding="utf-8")

        for marker in ["W-G2-001", "materials-reader", "reader-package/source_map.json"]:
            self.assertIn(marker, weakness_text)
        for marker in ["Literature Coverage", "Source Anchoring", "Reviewer Simulation"]:
            self.assertIn(marker, gate_text)

    def test_research_reference_links_shared_paper_production_artifacts(self):
        text = RESEARCH_REFERENCE.read_text(encoding="utf-8")
        self.assertIn("weakness-routing-template.csv", text)
        self.assertIn("paper-gate-report-template.md", text)
        self.assertIn("wer-ea-mini-review-weakness-routing.csv", text)
        self.assertIn("wer-ea-mini-review-gate-report.md", text)


if __name__ == "__main__":
    unittest.main()

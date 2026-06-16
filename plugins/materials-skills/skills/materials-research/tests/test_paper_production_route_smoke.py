import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
EXAMPLE = (
    ROOT
    / "skills"
    / "materials-research"
    / "examples"
    / "library"
    / "paper-production-mini-review-example.md"
)
LIBRARY_INDEX = (
    ROOT
    / "skills"
    / "materials-research"
    / "examples"
    / "library"
    / "library-index.md"
)


class PaperProductionRouteSmokeTests(unittest.TestCase):
    def test_wer_ea_mini_review_example_exposes_route_shape(self):
        self.assertTrue(EXAMPLE.is_file(), "paper-production example must exist")
        text = EXAMPLE.read_text(encoding="utf-8")

        for marker in [
            "# Paper Production Mini-Review Example",
            "Route: literature-review / asphalt-pavement / generic.",
            "`paper_stage`: screening",
            "`workflow_mode`: paper-production",
            "`output_package`: reader-package",
            "## Available Artifacts",
            "citation_handoff.csv",
            "## Blocked Gates",
            "materials-reader",
            "reader-package/source_map.json",
            "## Weakness Routing Rows To Update",
            "W-G2-001",
            "## Reviewer-Risk Note",
        ]:
            self.assertIn(marker, text)

    def test_example_library_indexes_paper_production_example(self):
        self.assertTrue(LIBRARY_INDEX.is_file(), "example library index must exist")
        index_text = LIBRARY_INDEX.read_text(encoding="utf-8")
        self.assertIn("paper-production-mini-review-example.md", index_text)
        self.assertIn("paper-production orchestrator", index_text)


if __name__ == "__main__":
    unittest.main()

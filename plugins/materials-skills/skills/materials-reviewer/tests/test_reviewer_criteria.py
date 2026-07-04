import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class ReviewerCriteriaTest(unittest.TestCase):
    _criteria_files = [
        "asphalt-reviewer-criteria.md",
        "cement-reviewer-criteria.md",
        "ceramics-reviewer-criteria.md",
        "polymers-reviewer-criteria.md",
        "metals-reviewer-criteria.md",
        "functional-reviewer-criteria.md",
        "nano-reviewer-criteria.md",
        "insulation-reviewer-criteria.md",
        "editorial-criteria.md",
    ]

    def test_all_reviewer_criteria_files_exist(self):
        for filename in self._criteria_files:
            path = SKILL_ROOT / "references" / filename
            self.assertTrue(path.exists(), f"{filename} should exist")

    def test_each_criteria_file_has_substantial_content(self):
        for filename in self._criteria_files:
            with self.subTest(filename=filename):
                text = (SKILL_ROOT / "references" / filename).read_text(encoding="utf-8")
                self.assertGreater(len(text.strip()), 200,
                                   f"{filename} should have substantial content (>200 chars)")
                self.assertIn("# ", text, f"{filename} should have a level-1 heading")

    def test_review_axes_covers_five_dimensions(self):
        path = SKILL_ROOT / "references" / "review-axes.md"
        self.assertTrue(path.exists(), "review-axes.md should exist")
        text = path.read_text(encoding="utf-8")

        expected_axes = [
            "Innovation",
            "Methodology",
            "Evidence completeness",
            "Writing quality",
            "Figure/table quality",
            "Journal fit",
        ]
        for axis in expected_axes:
            self.assertIn(axis, text, f"review-axes.md should cover axis '{axis}'")

        self.assertIn("0 to 5", text, "review-axes.md should mention scoring 0-5")

    def test_qa_checklist_contains_required_items(self):
        path = SKILL_ROOT / "references" / "qa-checklist.md"
        self.assertTrue(path.exists(), "qa-checklist.md should exist")
        text = path.read_text(encoding="utf-8")

        required_items = [
            "overclaim",
            "missing test conditions",
            "replicate",
            "scale bar",
            "novelty",
            "journal scope",
            "rejection",
        ]
        for item in required_items:
            self.assertIn(item.lower(), text.lower(),
                          f"qa-checklist.md should mention '{item}'")

    def test_mechanism_evidence_checklist_exists(self):
        path = SKILL_ROOT / "references" / "mechanism-evidence-checklist.md"
        self.assertTrue(path.exists(), "mechanism-evidence-checklist.md should exist")
        text = path.read_text(encoding="utf-8")

        for technique in ["FTIR", "SEM", "fluorescence", "rheology"]:
            self.assertIn(technique, text,
                          f"mechanism-evidence-checklist.md should mention '{technique}'")


if __name__ == "__main__":
    unittest.main()
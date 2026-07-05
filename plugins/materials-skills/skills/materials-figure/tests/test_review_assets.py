import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class PaperDerivedReviewAssetsTest(unittest.TestCase):
    def test_paper_derived_reference_documents_learning_boundary(self):
        reference = SKILL_ROOT / "references" / "paper-derived-visual-patterns.md"
        self.assertTrue(reference.exists())
        text = reference.read_text(encoding="utf-8")

        for phrase in [
            "paper-derived visual patterns",
            "do not copy paper figures",
            "claim-evidence-boundary",
        ]:
            self.assertIn(phrase, text)

    def test_review_first_generated_assets_are_not_part_of_current_package(self):
        roadmap = SKILL_ROOT / "references" / "visual-asset-roadmap.md"
        text = roadmap.read_text(encoding="utf-8")

        self.assertIn("pre-generated review-first assets have been removed", text)
        self.assertFalse((SKILL_ROOT / "assets" / "review-first").exists())
        self.assertFalse((SKILL_ROOT / "scripts" / "review_gallery_demo.py").exists())

    def test_current_showcase_proof_assets_replace_review_first_gallery(self):
        showcase = SKILL_ROOT / "assets" / "showcase-proof"
        self.assertTrue((showcase / "showcase_manifest.json").exists())
        self.assertGreaterEqual(len(list(showcase.glob("*.png"))), 4)


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class WerEaAtlasTest(unittest.TestCase):
    def test_wer_ea_review_contract_is_reference_based(self):
        reference = SKILL_ROOT / "references" / "wer-ea-review-figure-contract.md"
        template = SKILL_ROOT / "assets" / "templates" / "wer-ea-figure-contract-template.md"
        manifest_text = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")

        self.assertTrue(reference.exists())
        self.assertTrue(template.exists())
        self.assertIn("references/wer-ea-review-figure-contract.md", manifest_text)
        self.assertFalse((SKILL_ROOT / "assets" / "wer-ea-atlas").exists())
        self.assertFalse((SKILL_ROOT / "scripts" / "wer_ea_atlas").exists())

        combined = reference.read_text(encoding="utf-8") + template.read_text(encoding="utf-8")
        for phrase in [
            "WER-EA",
            "mechanism",
            "evidence",
            "caption",
            "reviewer",
        ]:
            self.assertIn(phrase, combined)

    def test_gallery_contains_current_wer_ea_proof_assets(self):
        showcase = SKILL_ROOT / "assets" / "showcase-proof"
        manifest = showcase / "showcase_manifest.json"

        self.assertTrue(manifest.exists())
        self.assertTrue((showcase / "wer_ea_figure_proof_board.png").exists())
        self.assertTrue((showcase / "sbr_wer_performance_proof_board.png").exists())


if __name__ == "__main__":
    unittest.main()

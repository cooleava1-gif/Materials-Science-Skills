import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class PptxAssetsTest(unittest.TestCase):
    def test_pptx_generation_reference_exists(self):
        path = SKILL_ROOT / "references" / "pptx-generation.md"
        self.assertTrue(path.exists(), "pptx-generation.md should exist")
        text = path.read_text(encoding="utf-8")

        self.assertIn("build_materials_pptx.py", text,
                      "pptx-generation.md should reference the build script")
        self.assertIn("--input", text, "pptx-generation.md should document --input flag")
        self.assertIn("--output", text, "pptx-generation.md should document --output flag")

    def test_visual_style_exists(self):
        path = SKILL_ROOT / "references" / "visual-style.md"
        self.assertTrue(path.exists(), "visual-style.md should exist")
        text = path.read_text(encoding="utf-8")

        for phrase in [
            "16:9",
            "short titles",
            "3-5 bullets",
            "high contrast",
            "accent colors",
            "figures larger",
        ]:
            self.assertIn(phrase.lower(), text.lower(),
                          f"visual-style.md should mention '{phrase}'")

    def test_contract_exists(self):
        path = SKILL_ROOT / "static" / "core" / "contract.md"
        self.assertTrue(path.exists(), "contract.md should exist")
        text = path.read_text(encoding="utf-8")

        for phrase in [
            "title slide",
            "engineering problem",
            "experiment",
            "key results",
            "mechanism",
            "limitations",
            "ppt/media/",
            "ppt/notesSlides/",
        ]:
            self.assertIn(phrase.lower(), text.lower(),
                          f"contract.md should mention '{phrase}'")

    def test_template_fragments_exist(self):
        for frag in ["academic.md", "defense.md", "journal-club.md"]:
            path = SKILL_ROOT / "static" / "fragments" / "template" / frag
            self.assertTrue(path.exists(), f"template fragment {frag} should exist")
            text = path.read_text(encoding="utf-8")
            self.assertGreater(len(text.strip()), 30,
                               f"template fragment {frag} should have meaningful content")

    def test_deck_structures_reference_exists(self):
        path = SKILL_ROOT / "references" / "deck-structures.md"
        self.assertTrue(path.exists(), "deck-structures.md should exist")
        text = path.read_text(encoding="utf-8")

        for deck_type in ["Research Report", "Journal Club", "Review Talk"]:
            self.assertIn(deck_type, text,
                          f"deck-structures.md should cover '{deck_type}'")

        self.assertIn("Title", text, "deck-structures.md should describe slide sequences")


if __name__ == "__main__":
    unittest.main()
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class Paper2PptAssetsTest(unittest.TestCase):
    def test_deck_structure_files_exist(self):
        deck_files = [
            "materials-experiment-arc.md",
            "journal-club-deck.md",
            "mechanism-deck.md",
            "project-report-deck.md",
            "review-talk-deck.md",
            "pptx-handoff.md",
        ]
        for filename in deck_files:
            path = SKILL_ROOT / "references" / filename
            self.assertTrue(path.exists(), f"{filename} should exist")

    def test_deck_structure_files_have_slide_sequences(self):
        for filename in ["materials-experiment-arc.md", "journal-club-deck.md"]:
            with self.subTest(filename=filename):
                text = (SKILL_ROOT / "references" / filename).read_text(encoding="utf-8")
                self.assertIn("slide", text.lower(),
                              f"{filename} should mention slide sequence")
                self.assertIn("# ", text, f"{filename} should have a heading")

    def test_ppt_contract_exists(self):
        path = SKILL_ROOT / "static" / "core" / "ppt-contract.md"
        self.assertTrue(path.exists(), "ppt-contract.md should exist")
        text = path.read_text(encoding="utf-8")

        for phrase in ["speaker", "notes", "slide", "figure", "claim"]:
            self.assertIn(phrase.lower(), text.lower(),
                          f"ppt-contract.md should mention '{phrase}'")

    def test_slide_task_fragments_exist(self):
        for frag in ["slide-outline.md", "pptx-deck.md"]:
            path = SKILL_ROOT / "static" / "fragments" / "task" / frag
            self.assertTrue(path.exists(), f"{frag} should exist")
            text = path.read_text(encoding="utf-8")
            self.assertGreater(len(text.strip()), 20,
                               f"{frag} should have meaningful content")

    def test_domain_context_fragment_exists(self):
        path = SKILL_ROOT / "static" / "fragments" / "domain" / "domain-context.md"
        self.assertTrue(path.exists(), "domain-context.md should exist")
        text = path.read_text(encoding="utf-8")

        for domain in ["Civil", "Polymers", "Metals", "Ceramics", "Functional", "Nanomaterials"]:
            self.assertIn(domain, text,
                          f"domain-context.md should cover '{domain}'")


if __name__ == "__main__":
    unittest.main()
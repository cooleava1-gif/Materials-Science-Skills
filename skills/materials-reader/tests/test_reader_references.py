import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class ReaderReferencesTest(unittest.TestCase):
    def test_microstructure_interpretation_is_routed_and_guarded_against_overclaiming(self):
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        manifest_text = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")
        reference = SKILL_ROOT / "references" / "microstructure-interpretation.md"

        self.assertTrue(reference.exists(), "microstructure-interpretation.md should exist")
        manifest_text = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")
        self.assertIn("microstructure-interpretation.md", manifest_text)
        self.assertIn("microstructure-interpretation", manifest_text)

        text = reference.read_text(encoding="utf-8")
        for phrase in ["sea-island", "co-continuous", "phase inversion", "fluorescence", "DSC/TG", "safer wording"]:
            self.assertIn(phrase, text)
        self.assertIn("whether the figure actually supports that claim", text)


if __name__ == "__main__":
    unittest.main()

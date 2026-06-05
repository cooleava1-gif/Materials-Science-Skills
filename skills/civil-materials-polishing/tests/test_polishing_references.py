import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class PolishingReferencesTest(unittest.TestCase):
    def test_key_section_references_include_before_after_examples(self):
        for filename in ["abstract.md", "introduction.md", "results-discussion.md", "cover-letter.md", "conclusions.md"]:
            with self.subTest(filename=filename):
                text = (SKILL_ROOT / "references" / filename).read_text(encoding="utf-8")
                self.assertIn("Before", text)
                self.assertIn("After", text)
                self.assertIn("Why", text)

    def test_manifest_routes_conclusions_and_chinese_english_polishing(self):
        manifest = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("references/conclusions.md", manifest)
        self.assertIn("conclusions.md", skill_text)
        self.assertIn("中译英", manifest)


if __name__ == "__main__":
    unittest.main()

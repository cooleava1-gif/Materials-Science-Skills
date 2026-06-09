import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class ResponseExamplesTest(unittest.TestCase):
    def test_response_examples_cover_major_minor_and_methodology_critiques(self):
        expected = [
            "cbm-major-revision-response-example.md",
            "ccc-methodology-critique-response-example.md",
            "rmpd-minor-revision-response-example.md",
        ]

        for filename in expected:
            with self.subTest(filename=filename):
                path = SKILL_ROOT / "examples" / filename
                self.assertTrue(path.exists())
                text = path.read_text(encoding="utf-8")
                for section in ["## Reviewer Comment", "## Good Response", "## Why This Works"]:
                    self.assertIn(section, text)

    def test_manifest_uses_clean_triggers_for_core_response_routes(self):
        manifest = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")

        for phrase in ["point-by-point", "revision plan", "CCC", "RMPD", "回复审稿人"]:
            self.assertIn(phrase, manifest)

    def test_response_pattern_and_document_format_references_cover_real_revision_scenarios(self):
        patterns = SKILL_ROOT / "references" / "response-patterns.md"
        document_format = SKILL_ROOT / "references" / "response-document-format.md"
        self.assertTrue(patterns.exists(), "response-patterns.md should exist")
        self.assertTrue(document_format.exists(), "response-document-format.md should exist")

        pattern_text = patterns.read_text(encoding="utf-8")
        document_text = document_format.read_text(encoding="utf-8")

        for phrase in [
            "English Needs Major Revision",
            "Add More References",
            "Incremental",
            "Sample size",
            "Error Bars",
            "Raw Data",
            "Conflicting Reviewer",
            "Beyond Scope",
        ]:
            self.assertIn(phrase.lower(), pattern_text.lower())
        for phrase in ["Author Response", "tracked", "cover letter", "Page X", "Lines Y-Z", "conflicting reviewer"]:
            self.assertIn(phrase.lower(), document_text.lower())

    def test_response_document_format_links_to_patterns_instead_of_duplicating_strategy_examples(self):
        document_text = (SKILL_ROOT / "references" / "response-document-format.md").read_text(encoding="utf-8")

        self.assertIn("response-patterns.md", document_text)
        self.assertIn("Pattern 11", document_text)
        self.assertIn("Pattern 12", document_text)
        self.assertIn("Key format rule", document_text)
        self.assertNotIn("Reviewer 1 requested a more detailed explanation", document_text)


if __name__ == "__main__":
    unittest.main()

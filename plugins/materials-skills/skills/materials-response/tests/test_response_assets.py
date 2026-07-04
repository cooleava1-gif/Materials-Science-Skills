import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class ResponseAssetsTest(unittest.TestCase):
    def test_response_contract_exists(self):
        path = SKILL_ROOT / "static" / "core" / "response-contract.md"
        self.assertTrue(path.exists(), "response-contract.md should exist")
        text = path.read_text(encoding="utf-8")

        for phrase in [
            "respectful",
            "evidence-bound",
            "specific about manuscript changes",
            "honest about limitations",
            "consistent with the revised manuscript",
        ]:
            self.assertIn(phrase.lower(), text.lower(),
                          f"response-contract.md should mention '{phrase}'")

        self.assertIn("never fabricate", text.lower(), "response-contract.md should prohibit fabrication")

    def test_response_patterns_covers_common_reviewer_comments(self):
        path = SKILL_ROOT / "references" / "response-patterns.md"
        self.assertTrue(path.exists(), "response-patterns.md should exist")
        text = path.read_text(encoding="utf-8")

        patterns = [
            "English Needs Major Revision",
            "Add More References",
            "Incremental",
            "Sample size",
            "Error Bars",
            "Raw Data",
            "Conflicting Reviewer",
            "Beyond Scope",
        ]
        for pattern in patterns:
            self.assertIn(pattern.lower(), text.lower(),
                          f"response-patterns.md should cover pattern '{pattern}'")

        self.assertIn("Strategy", text, "response-patterns.md should provide strategies")
        self.assertIn("Example", text, "response-patterns.md should provide examples")

    def test_language_bank_contains_domain_specific_phrases(self):
        path = SKILL_ROOT / "references" / "language-bank.md"
        self.assertTrue(path.exists(), "language-bank.md should exist")
        text = path.read_text(encoding="utf-8")

        sections = [
            "Acknowledge and Accept",
            "Clarification and Softening",
            "Disagreeing or Rebutting Politely",
        ]
        for section in sections:
            self.assertIn(section, text,
                          f"language-bank.md should contain section '{section}'")

        for phrase in [
            "We sincerely thank the reviewer",
            "Claim-Strength Ladder",
            "Limitation Phrasing",
            "Standards-Based Rebuttals",
            "Scope-Based Rebuttals",
        ]:
            self.assertIn(phrase, text,
                          f"language-bank.md should contain '{phrase}'")

    def test_response_document_format_exists(self):
        path = SKILL_ROOT / "references" / "response-document-format.md"
        self.assertTrue(path.exists(), "response-document-format.md should exist")
        text = path.read_text(encoding="utf-8")

        for phrase in ["Author Response", "tracked", "cover letter", "Page X", "Lines Y-Z"]:
            self.assertIn(phrase.lower(), text.lower(),
                          f"response-document-format.md should mention '{phrase}'")

    def test_reviewer_comment_patterns_exists(self):
        path = SKILL_ROOT / "references" / "reviewer-comment-patterns.md"
        self.assertTrue(path.exists(), "reviewer-comment-patterns.md should exist")
        text = path.read_text(encoding="utf-8")
        self.assertGreater(len(text.strip()), 100,
                           "reviewer-comment-patterns.md should have substantial content")


if __name__ == "__main__":
    unittest.main()
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class StyleGuardrailsTest(unittest.TestCase):
    def test_style_guardrails_exists_and_contains_key_rules(self):
        path = SKILL_ROOT / "references" / "style-guardrails.md"
        self.assertTrue(path.exists(), "style-guardrails.md should exist")
        text = path.read_text(encoding="utf-8")

        for rule in [
            "Academic style",
            "Articles",
            "Numbers and units",
            "Sentence and paragraph checks",
            "Overclaim checklist",
            "Integrity rules",
            "AI boundary",
        ]:
            self.assertIn(rule, text, f"style-guardrails.md should contain section '{rule}'")

        for phrase in [
            "avoid contractions",
            "SI units",
            "comma splices",
            "prove",
            "fabricated citations",
            "grammar and clarity",
        ]:
            self.assertIn(phrase.lower(), text.lower(), f"style-guardrails.md should mention '{phrase}'")

    def test_polishing_contract_exists_and_contains_required_sections(self):
        path = SKILL_ROOT / "static" / "core" / "polishing-contract.md"
        self.assertTrue(path.exists(), "polishing-contract.md should exist")
        text = path.read_text(encoding="utf-8")

        for section in ["Preserve", "Improve", "Flag rather than silently fix"]:
            self.assertIn(section, text, f"polishing-contract.md should contain '{section}'")

        for phrase in [
            "data",
            "units",
            "test conditions",
            "sentence clarity",
            "unsupported novelty",
            "missing statistical evidence",
        ]:
            self.assertIn(phrase.lower(), text.lower(), f"polishing-contract.md should mention '{phrase}'")

    def test_language_fragments_exist(self):
        en_path = SKILL_ROOT / "static" / "fragments" / "language" / "en.md"
        zh_path = SKILL_ROOT / "static" / "fragments" / "language" / "zh-to-en.md"

        self.assertTrue(en_path.exists(), "en.md language fragment should exist")
        self.assertTrue(zh_path.exists(), "zh-to-en.md language fragment should exist")

        en_text = en_path.read_text(encoding="utf-8")
        zh_text = zh_path.read_text(encoding="utf-8")

        self.assertIn("British English", en_text, "en.md should mention British English spelling")
        self.assertIn("hedging", en_text.lower(), "en.md should mention hedging")
        self.assertIn("Chinese-to-English", zh_text, "zh-to-en.md should mention Chinese-to-English")
        self.assertIn("preserve facts", zh_text.lower(), "zh-to-en.md should mention preserving facts")

    def test_style_guardrails_has_overclaim_safe_replacements(self):
        text = (SKILL_ROOT / "references" / "style-guardrails.md").read_text(encoding="utf-8")

        self.assertIn("Avoid", text)
        self.assertIn("Safer replacement", text)
        for avoid_word in ["prove", "unprecedented", "superior", "significant"]:
            self.assertIn(avoid_word, text, f"style-guardrails.md should list '{avoid_word}' as avoid-term")

    def test_polishing_contract_flags_claim_types(self):
        text = (SKILL_ROOT / "static" / "core" / "polishing-contract.md").read_text(encoding="utf-8")
        for flag_phrase in [
            "unsupported novelty",
            "missing statistical evidence",
            "vague mechanism claims",
            "sustainability claims",
        ]:
            self.assertIn(flag_phrase.lower(), text.lower(),
                          f"polishing-contract.md should flag '{flag_phrase}'")


if __name__ == "__main__":
    unittest.main()
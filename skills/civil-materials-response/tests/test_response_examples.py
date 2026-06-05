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


if __name__ == "__main__":
    unittest.main()

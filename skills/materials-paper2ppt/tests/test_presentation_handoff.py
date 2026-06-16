import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path



def _find_repo_root():
    p = Path(__file__).resolve()
    for parent in [p] + list(p.parents):
        if (parent / ".git").exists() or (parent / "AGENTS.md").exists():
            return parent
    return p.parents[3]
SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = _find_repo_root()


class Paper2PptStructureTest(unittest.TestCase):
    def test_skill_manifest_and_release_checks_cover_pptx_handoff(self):
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        manifest_text = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")
        contract_text = (SKILL_ROOT / "static" / "core" / "contract.md").read_text(encoding="utf-8")
        release_text = (REPO_ROOT / "scripts" / "run_release_checks.py").read_text(encoding="utf-8")

        self.assertIn("materials-pptx", skill_text)
        self.assertIn("--pptx-output", skill_text)
        self.assertIn("tests:", manifest_text)
        self.assertNotIn("tests: []", manifest_text)
        self.assertIn("speaker notes", contract_text.lower())
        self.assertIn("limitations", contract_text.lower())
        self.assertIn('"materials-paper2ppt" / "tests"', release_text)


class Paper2PptScriptTest(unittest.TestCase):
    def test_build_ppt_markdown_generates_markdown_and_optional_pptx(self):
        script = SKILL_ROOT / "scripts" / "build_ppt_markdown.py"
        self.assertTrue(script.exists(), "build_ppt_markdown.py should exist")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            markdown_path = tmp_path / "deck.md"
            pptx_path = tmp_path / "deck.pptx"

            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--title",
                    "WER-EA review outline",
                    "--deck-type",
                    "project-report",
                    "--language",
                    "en",
                    "--output",
                    str(markdown_path),
                    "--pptx-output",
                    str(pptx_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn(str(markdown_path), result.stdout)
            self.assertIn(str(pptx_path), result.stdout)

            markdown_text = markdown_path.read_text(encoding="utf-8")
            for phrase in [
                "## Slide 1 - Title",
                "Topic: WER-EA review outline",
                "Speaker note:",
                "## Slide 8 - Limitations and Next Work",
            ]:
                self.assertIn(phrase, markdown_text)

            with zipfile.ZipFile(pptx_path) as archive:
                names = set(archive.namelist())
            self.assertIn("ppt/presentation.xml", names)
            self.assertIn("ppt/slides/slide1.xml", names)
            self.assertIn("ppt/notesSlides/notesSlide1.xml", names)


if __name__ == "__main__":
    unittest.main()

import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

from scripts.skill_manifest import discover_skill_names



def _find_repo_root():
    p = Path(__file__).resolve()
    for parent in [p] + list(p.parents):
        if (parent / ".git").exists() or (parent / "AGENTS.md").exists():
            return parent
    return p.parents[3]
SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = _find_repo_root()

PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR"
    b"\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00"
    b"\x90wS\xde"
    b"\x00\x00\x00\x0cIDATx\x9cc`\x00\x00\x00\x02\x00\x01"
    b"\xe2!\xbc3"
    b"\x00\x00\x00\x00IEND\xaeB`\x82"
)


class PptxStructureTest(unittest.TestCase):
    def test_skill_manifest_contract_and_release_checks_cover_generation(self):
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        manifest_text = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")
        contract_text = (SKILL_ROOT / "static" / "core" / "contract.md").read_text(encoding="utf-8")
        release_text = (REPO_ROOT / "scripts" / "run_release_checks.py").read_text(encoding="utf-8")

        manifest_text = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")
        self.assertTrue((SKILL_ROOT / "references" / "deck-structures.md").exists())
        self.assertIn("template:", manifest_text)
        self.assertIn("speaker", contract_text.lower())
        contract_text_lower = contract_text.lower()
        self.assertIn("crop", contract_text_lower)
        self.assertIn("tests:", manifest_text)
        self.assertNotIn("tests: []", manifest_text)
        self.assertIn("ppt/media/", contract_text)
        self.assertIn("ppt/notesSlides/", contract_text)
        self.assertIn("discover_skill_names", release_text)
        self.assertIn("materials-pptx", discover_skill_names())


class PptxScriptTest(unittest.TestCase):
    def test_script_builds_pptx_with_notes_and_images_from_markdown(self):
        script = SKILL_ROOT / "scripts" / "build_materials_pptx.py"
        self.assertTrue(script.exists(), "build_materials_pptx.py should exist")

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            image_path = tmp_path / "figure.png"
            image_path.write_bytes(PNG_BYTES)
            markdown_path = tmp_path / "outline.md"
            markdown_path.write_text(
                "\n".join(
                    [
                        "## Slide 1 - Evidence Chain",
                        "- Claim: bonding improved in the conditioned interface test.",
                        f"![Interface SEM]({image_path.name})",
                        "Speaker note:",
                        "- Separate measured evidence from inferred mechanism.",
                    ]
                ),
                encoding="utf-8",
            )
            pptx_path = tmp_path / "deck.pptx"

            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--input",
                    str(markdown_path),
                    "--title",
                    "WER-EA deck",
                    "--output",
                    str(pptx_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn(str(pptx_path), result.stdout)
            with zipfile.ZipFile(pptx_path) as archive:
                names = set(archive.namelist())
                slide_xml = archive.read("ppt/slides/slide1.xml").decode("utf-8")
                notes_xml = archive.read("ppt/notesSlides/notesSlide1.xml").decode("utf-8")

            self.assertIn("ppt/presentation.xml", names)
            self.assertIn("ppt/media/image1.png", names)
            self.assertIn("ppt/notesSlides/notesSlide1.xml", names)
            self.assertIn("Evidence Chain", slide_xml)
            self.assertIn("Separate measured evidence from inferred mechanism.", notes_xml)


if __name__ == "__main__":
    unittest.main()

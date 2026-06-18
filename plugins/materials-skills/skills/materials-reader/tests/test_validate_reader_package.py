import importlib.util
import tempfile
import unittest
from pathlib import Path


READER_ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    path = READER_ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ValidateReaderPackageTests(unittest.TestCase):
    def build_package(self, tmp_path):
        builder = load_script("build_reader_package")
        package_dir = tmp_path / "reader-package"
        builder.build_reader_package(
            package_dir,
            {
                "source_type": "full-pdf",
                "paper_title": "Example package",
                "doi_or_url": "10.1234/example",
            },
            force=False,
        )
        return package_dir

    def test_validator_fails_missing_required_csv_header(self):
        validator = load_script("validate_reader_package")
        with tempfile.TemporaryDirectory() as tmp:
            package_dir = self.build_package(Path(tmp))
            (package_dir / "citation_handoff.csv").write_text(
                "claim_id,source_anchor\nCLAIM-001,S001\n",
                encoding="utf-8",
            )
            result = validator.validate_reader_package(package_dir)
            self.assertEqual("fail", result["status"])
            self.assertIn("citation_handoff.csv", "\n".join(result["errors"]))

    def test_validator_flags_absolute_path_leakage(self):
        validator = load_script("validate_reader_package")
        with tempfile.TemporaryDirectory() as tmp:
            package_dir = self.build_package(Path(tmp))
            (package_dir / "paper.md").write_text(
                "# Paper\n\nC:\\Users\\testuser\\secret.pdf\n",
                encoding="utf-8",
            )
            result = validator.validate_reader_package(package_dir)
            self.assertEqual("fail", result["status"])
            self.assertIn("absolute path", "\n".join(result["errors"]).lower())

    def test_validator_checks_obsidian_sections_when_note_exists(self):
        validator = load_script("validate_reader_package")
        with tempfile.TemporaryDirectory() as tmp:
            package_dir = self.build_package(Path(tmp))
            (package_dir / "obsidian_note.md").write_text(
                "# Example\n\n## Source Anchors\n",
                encoding="utf-8",
            )
            result = validator.validate_reader_package(package_dir)
            self.assertEqual("fail", result["status"])
            self.assertIn("obsidian_note.md", "\n".join(result["errors"]))


if __name__ == "__main__":
    unittest.main()

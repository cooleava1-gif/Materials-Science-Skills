import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


READER_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = READER_ROOT.parent
PLUGIN_ROOT = SKILLS_ROOT.parent
REPO_ROOT = PLUGIN_ROOT.parents[1]


def load_script(name):
    path = READER_ROOT / "scripts" / f"{name}.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReaderPackageScriptTests(unittest.TestCase):
    def test_builder_creates_valid_empty_package_and_json_cli(self):
        validate_module = load_script("validate_reader_package")
        builder_path = READER_ROOT / "scripts" / "build_reader_package.py"
        with tempfile.TemporaryDirectory() as tmp:
            package_dir = Path(tmp) / "reader-package"
            result = subprocess.run(
                [
                    sys.executable,
                    str(builder_path),
                    "--output-dir",
                    str(package_dir),
                    "--source-type",
                    "pasted-text",
                    "--title",
                    "Formula = Risk",
                    "--doi",
                    "10.1234/example",
                    "--json",
                ],
                cwd=REPO_ROOT,
                text=True,
                capture_output=True,
                check=True,
            )
            payload = json.loads(result.stdout)
            self.assertEqual("pass", payload["status"])
            self.assertTrue((package_dir / "package_manifest.json").exists())
            audit = validate_module.validate_reader_package(package_dir)
            self.assertEqual("pass", audit["status"], audit)

    def test_builder_refuses_non_empty_output_without_force(self):
        builder = load_script("build_reader_package")
        with tempfile.TemporaryDirectory() as tmp:
            package_dir = Path(tmp) / "reader-package"
            package_dir.mkdir()
            (package_dir / "keep.txt").write_text("existing", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                builder.build_reader_package(
                    package_dir,
                    {
                        "source_type": "pasted-text",
                        "paper_title": "Example",
                        "doi_or_url": "",
                    },
                    force=False,
                )

    def test_builder_escapes_formula_like_csv_cells(self):
        builder = load_script("build_reader_package")
        self.assertEqual("'=SUM(A1:A2)", builder.escape_csv_cell("=SUM(A1:A2)"))
        self.assertEqual("'+risk", builder.escape_csv_cell("+risk"))
        self.assertEqual("'-risk", builder.escape_csv_cell("-risk"))
        self.assertEqual("'@risk", builder.escape_csv_cell("@risk"))


if __name__ == "__main__":
    unittest.main()

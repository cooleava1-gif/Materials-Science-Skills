import json
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = SKILL_ROOT / "scripts" / "extract_pdf_visual_assets.py"


class PdfVisualAssetScriptTest(unittest.TestCase):
    def test_script_exists_and_reports_missing_pdf_without_dependency_import_failure(self):
        self.assertTrue(SCRIPT_PATH.exists(), "extract_pdf_visual_assets.py should exist")

        spec = importlib.util.spec_from_file_location("extract_pdf_visual_assets", SCRIPT_PATH)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            spec_path = tmp / "visual_asset_spec.json"
            spec_path.write_text(
                json.dumps(
                    {
                        "paper_id": "sample-paper",
                        "source_pdf_note": "sample source only",
                        "assets": [
                            {
                                "asset_id": "F001-01",
                                "kind": "figure",
                                "paper_label": "Fig. 1",
                                "source_page": 1,
                                "crop_box": [0, 0, 100, 100],
                                "claim_supported": "bounded claim",
                                "claim_too_strong": "overclaim",
                                "destination": "mechanism map",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            exit_code = module.main(
                [
                    "--pdf",
                    str(tmp / "missing.pdf"),
                    "--package-dir",
                    str(tmp / "package"),
                    "--spec",
                    str(spec_path),
                    "--json",
                ]
            )
        self.assertNotEqual(exit_code, 0)

    def test_ensure_dirs_removes_stale_generated_png_assets(self):
        spec = importlib.util.spec_from_file_location("extract_pdf_visual_assets", SCRIPT_PATH)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        with tempfile.TemporaryDirectory() as tmpdir:
            package = Path(tmpdir) / "package"
            stale_paths = [
                package / "assets" / "rendered_pages" / "old_page.png",
                package / "assets" / "figures" / "old_figure.png",
                package / "assets" / "tables" / "old_table.png",
            ]
            for stale_path in stale_paths:
                stale_path.parent.mkdir(parents=True, exist_ok=True)
                stale_path.write_bytes(b"stale")

            module.ensure_dirs(package)

            for stale_path in stale_paths:
                self.assertFalse(stale_path.exists(), f"{stale_path.name} should be removed before regeneration")


if __name__ == "__main__":
    unittest.main()

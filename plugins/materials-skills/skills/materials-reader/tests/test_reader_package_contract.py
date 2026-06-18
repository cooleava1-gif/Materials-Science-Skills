import json
import unittest
from pathlib import Path

READER_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = READER_ROOT.parent
PLUGIN_ROOT = SKILLS_ROOT.parent
REPO_ROOT = PLUGIN_ROOT.parents[1]
REMOVED_TOP_LEVEL_READER_ROOT = REPO_ROOT.joinpath("skills", "materials-reader")


class ReaderPackageContractTests(unittest.TestCase):
    def test_standard_output_contract_names_required_package_parts(self):
        contract = (
            READER_ROOT / "references" / "standard-output-package.md"
        ).read_text(encoding="utf-8")
        required_terms = [
            "package_manifest.json",
            "source_map.json",
            "paper.md",
            "translation_notes.md",
            "source_anchor_checklist.md",
            "figure_table_cards.md",
            "citation_handoff.csv",
            "figure_handoff.csv",
            "review_handoff.md",
            "obsidian_note.md",
            "qa_report.md",
            "assets/",
            "required",
            "optional",
        ]
        for term in required_terms:
            with self.subTest(term=term):
                self.assertIn(term, contract)

    def test_reader_package_schemas_are_valid_json_schema_documents(self):
        schema_dir = READER_ROOT / "assets" / "schemas"
        expected = {
            "source-map.schema.json",
            "visual-asset-spec.schema.json",
            "visual-asset-report.schema.json",
            "reader-package-manifest.schema.json",
        }
        self.assertEqual(expected, {path.name for path in schema_dir.glob("*.schema.json")})
        for path in schema_dir.glob("*.schema.json"):
            with self.subTest(path=path.name):
                schema = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual("object", schema["type"])
                self.assertIn("required", schema)

    def test_reader_package_files_live_only_in_plugin_layout(self):
        relative_paths = [
            "references/standard-output-package.md",
            "assets/schemas/source-map.schema.json",
            "assets/schemas/visual-asset-spec.schema.json",
            "assets/schemas/visual-asset-report.schema.json",
            "assets/schemas/reader-package-manifest.schema.json",
            "assets/templates/package-manifest-template.json",
            "assets/templates/qa-report-template.md",
            "scripts/build_reader_package.py",
            "scripts/audit_reader_package.py",
            "scripts/validate_reader_package.py",
            "tests/test_reader_package_contract.py",
            "tests/test_reader_package_scripts.py",
            "tests/test_validate_reader_package.py",
        ]
        for relative_path in relative_paths:
            with self.subTest(path=relative_path):
                self.assertTrue((READER_ROOT / relative_path).exists())
                self.assertFalse((REMOVED_TOP_LEVEL_READER_ROOT / relative_path).exists())


if __name__ == "__main__":
    unittest.main()

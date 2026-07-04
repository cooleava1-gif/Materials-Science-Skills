import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class DataSchemasTest(unittest.TestCase):
    _schema_names = ["civil", "polymers", "metals", "ceramics", "functional", "nano"]

    def test_all_six_schema_files_exist(self):
        for name in self._schema_names:
            path = SKILL_ROOT / "references" / f"{name}-data-schema.md"
            self.assertTrue(path.exists(), f"{name}-data-schema.md should exist")

    def test_each_schema_contains_required_fields(self):
        required_sections = [
            "Core Fields",
            "Field Specifications",
            "Common Tests",
            "Boundary Rule",
        ]
        for name in self._schema_names:
            with self.subTest(schema=name):
                text = (SKILL_ROOT / "references" / f"{name}-data-schema.md").read_text(encoding="utf-8")
                for section in required_sections:
                    self.assertIn(section, text, f"{name}-data-schema.md should contain '{section}'")

    def test_each_schema_has_field_table_with_columns(self):
        for name in self._schema_names:
            with self.subTest(schema=name):
                text = (SKILL_ROOT / "references" / f"{name}-data-schema.md").read_text(encoding="utf-8")
                for col in ["Type", "Unit or format", "Sanity check"]:
                    self.assertIn(col, text, f"{name}-data-schema.md should contain column '{col}'")

    def test_schemas_are_well_formed_markdown_with_headers(self):
        for name in self._schema_names:
            with self.subTest(schema=name):
                text = (SKILL_ROOT / "references" / f"{name}-data-schema.md").read_text(encoding="utf-8")
                self.assertIn("# ", text, f"{name}-data-schema.md should have a level-1 heading")
                self.assertIn("## ", text, f"{name}-data-schema.md should have level-2 headings")
                self.assertIn("sample_id", text, f"{name}-data-schema.md should reference sample_id")

    def test_schemas_are_non_empty_with_substantial_content(self):
        for name in self._schema_names:
            with self.subTest(schema=name):
                path = SKILL_ROOT / "references" / f"{name}-data-schema.md"
                text = path.read_text(encoding="utf-8")
                self.assertGreater(len(text.strip()), 500, f"{name}-data-schema.md should have substantial content (>500 chars)")


if __name__ == "__main__":
    unittest.main()
"""Tests for citation export formats (RIS, BibTeX, GB/T 7714)."""

import unittest
import sys
from pathlib import Path

# Ensure the mcp package is importable
MCP_ROOT = Path(__file__).resolve().parents[2] / "mcp"
if str(MCP_ROOT) not in sys.path:
    sys.path.insert(0, str(MCP_ROOT))

from academic_search.export.ris import build_ris_record, build_ris_file
from academic_search.export.bibtex import build_bibtex_entry, build_bibtex_file
from academic_search.export.formats import export_citations, build_gbt7714_entry


SAMPLE_RECORD = {
    "title": "Waterborne epoxy modified emulsified asphalt for pavement interlayer bonding",
    "authors": ["A. B. Smith", "C. D. Johnson", "E. F. Williams"],
    "journal": "Construction and Building Materials",
    "year": 2025,
    "volume": "412",
    "issue": "1",
    "pages": "135-148",
    "doi": "10.1016/j.conbuildmat.2025.01.001",
}

SAMPLE_RECORD_MINIMAL = {
    "title": "A minimal record",
    "authors": ["J. Doe"],
}


class RisExportTest(unittest.TestCase):
    def test_ris_record_contains_required_tags(self):
        ris = build_ris_record(SAMPLE_RECORD)
        self.assertIn("TY  - JOUR", ris)
        self.assertIn("TI  - Waterborne epoxy", ris)
        self.assertIn("AU  - A. B. Smith", ris)
        self.assertIn("AU  - C. D. Johnson", ris)
        self.assertIn("JO  - Construction and Building Materials", ris)
        self.assertIn("PY  - 2025", ris)
        self.assertIn("VL  - 412", ris)
        self.assertIn("IS  - 1", ris)
        self.assertIn("SP  - 135", ris)
        self.assertIn("EP  - 148", ris)
        self.assertIn("DO  - 10.1016/j.conbuildmat.2025.01.001", ris)
        self.assertIn("ER  -", ris)

    def test_ris_record_minimal(self):
        ris = build_ris_record(SAMPLE_RECORD_MINIMAL)
        self.assertIn("TY  - JOUR", ris)
        self.assertIn("TI  - A minimal record", ris)
        self.assertIn("AU  - J. Doe", ris)
        self.assertIn("ER  -", ris)
        # No volume/issue/pages for minimal record
        self.assertNotIn("VL  -", ris)

    def test_ris_file_multiple_records(self):
        records = [SAMPLE_RECORD, SAMPLE_RECORD_MINIMAL]
        ris = build_ris_file(records)
        # Two ER terminators
        self.assertEqual(ris.count("ER  -"), 2)

    def test_ris_html_stripped(self):
        record = {"title": "<b>Bold title</b> with <i>italic</i>", "authors": []}
        ris = build_ris_record(record)
        self.assertNotIn("<b>", ris)
        self.assertNotIn("<i>", ris)
        self.assertIn("TI  - Bold title with italic", ris)


class BibTeXExportTest(unittest.TestCase):
    def test_bibtex_entry_has_article_type(self):
        bib = build_bibtex_entry(SAMPLE_RECORD)
        self.assertTrue(bib.startswith("@article{"))
        self.assertIn("title", bib)
        self.assertIn("author", bib)
        self.assertIn("journal", bib)
        self.assertIn("year", bib)
        self.assertIn("doi", bib)

    def test_bibtex_citation_key_format(self):
        bib = build_bibtex_entry(SAMPLE_RECORD)
        # Key should be smith2025waterborne
        self.assertIn("smith2025waterborne", bib)

    def test_bibtex_authors_and_separated(self):
        bib = build_bibtex_entry(SAMPLE_RECORD)
        self.assertIn("A. B. Smith and C. D. Johnson and E. F. Williams", bib)

    def test_bibtex_special_chars_escaped(self):
        record = {"title": "Effects of 5% & 10% dosage on performance", "authors": ["J. Doe"], "year": 2024}
        bib = build_bibtex_entry(record)
        self.assertIn("\\&", bib)
        self.assertNotIn(" & ", bib)

    def test_bibtex_file_multiple_records(self):
        records = [SAMPLE_RECORD, SAMPLE_RECORD_MINIMAL]
        bib = build_bibtex_file(records)
        self.assertEqual(bib.count("@article{"), 2)


class GBT7714ExportTest(unittest.TestCase):
    def test_gbt7714_entry_format(self):
        ref = build_gbt7714_entry(SAMPLE_RECORD, 1)
        self.assertTrue(ref.startswith("[1]"))
        self.assertIn("SMITH", ref)
        self.assertIn("[J]", ref)
        self.assertIn("Construction and Building Materials", ref)
        self.assertIn("2025", ref)
        self.assertIn("412", ref)
        self.assertIn("DOI:", ref)

    def test_gbt7714_et_al_for_many_authors(self):
        record = {
            "title": "Test",
            "authors": ["A. One", "B. Two", "C. Three", "D. Four"],
            "year": 2024,
        }
        ref = build_gbt7714_entry(record, 5)
        self.assertIn("et al", ref)
        self.assertIn("[5]", ref)

    def test_gbt7714_numbering(self):
        records = [SAMPLE_RECORD, SAMPLE_RECORD_MINIMAL]
        from academic_search.export.formats import build_gbt7714_file
        text = build_gbt7714_file(records)
        self.assertIn("[1]", text)
        self.assertIn("[2]", text)


class UnifiedExportTest(unittest.TestCase):
    def test_export_ris(self):
        content = export_citations([SAMPLE_RECORD], "ris")
        self.assertIn("TY  - JOUR", content)

    def test_export_bibtex(self):
        content = export_citations([SAMPLE_RECORD], "bibtex")
        self.assertIn("@article{", content)

    def test_export_gbt7714(self):
        content = export_citations([SAMPLE_RECORD], "gbt7714")
        self.assertIn("[1]", content)
        self.assertIn("[J]", content)

    def test_export_unsupported_format_raises(self):
        with self.assertRaises(ValueError):
            export_citations([SAMPLE_RECORD], "unsupported")


if __name__ == "__main__":
    unittest.main()

import csv
import io
import sys
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE_ROOT))

from academic_search.service import AcademicSearchService


class FakeAdapter:
    name = "fake"

    def __init__(self, records):
        self.records = records

    def search(self, query, *, journals=None, year_range=None, limit=10):
        return self.records[:limit]

    def fetch(self, *, doi=None, title=None, external_id=None):
        for record in self.records:
            if doi and record.get("doi") == doi:
                return record
            if title and record.get("title") == title:
                return record
        return None


class AcademicSearchServiceTest(unittest.TestCase):
    def test_search_merges_records_and_adds_evidence_quality_fields(self):
        adapter_a = FakeAdapter(
            [
                {
                    "title": "Waterborne epoxy emulsified asphalt bonding interface study",
                    "doi": "10.1000/example",
                    "journal": "Construction and Building Materials",
                    "year": 2024,
                    "abstract": "Pull-off bonding, FTIR and moisture aging were measured.",
                    "source": "Crossref",
                }
            ]
        )
        adapter_b = FakeAdapter(
            [
                {
                    "title": "Waterborne epoxy emulsified asphalt bonding interface study",
                    "doi": "10.1000/example",
                    "journal": "Construction and Building Materials",
                    "year": 2023,
                    "citation_count": 12,
                    "source": "Semantic Scholar",
                }
            ]
        )
        service = AcademicSearchService(adapters=[adapter_a, adapter_b])

        result = service.search_civil_materials(
            {
                "topic": "waterborne epoxy modified emulsified asphalt bonding performance",
                "journal_family": ["CBM"],
                "evidence_layer": "bonding_interface",
                "limit": 5,
            }
        )

        self.assertTrue(result["records"])
        record = result["records"][0]
        self.assertEqual(record["doi"], "10.1000/example")
        self.assertIn("bonding_interface", record["evidence_layers"])
        self.assertIn("ftir_sem_fluorescence_rheology", record["evidence_layers"])
        self.assertIn("metadata_conflicts", record)
        self.assertIn("year", record["metadata_conflicts"])
        self.assertIn("source_provenance", record)
        self.assertEqual(len(record["source_provenance"]), 2)

    def test_fetch_metadata_marks_missing_fields_and_source_provenance(self):
        service = AcademicSearchService(
            adapters=[
                FakeAdapter(
                    [
                        {
                            "title": "Storage stability of emulsified asphalt",
                            "doi": "10.1000/storage",
                            "journal": "Road Materials and Pavement Design",
                            "year": 2022,
                            "source": "Crossref",
                        }
                    ]
                )
            ]
        )

        result = service.fetch_paper_metadata({"doi": "10.1000/storage"})

        self.assertEqual(result["record"]["doi"], "10.1000/storage")
        self.assertIn("abstract", result["record"]["missing_fields"])
        self.assertEqual(result["record"]["source_provenance"][0]["source"], "Crossref")

    def test_export_citation_matrix_matches_existing_csv_schema(self):
        service = AcademicSearchService(adapters=[])

        result = service.export_citation_matrix(
            {
                "topic": "waterborne epoxy modified emulsified asphalt",
                "claims": [
                    "Bond strength improvement",
                    "FTIR mechanism evidence",
                ],
                "target_journals": ["CBM", "JBE"],
            }
        )

        reader = csv.DictReader(io.StringIO(result["csv"]))
        rows = list(reader)

        self.assertEqual(
            reader.fieldnames,
            [
                "priority",
                "claim_or_need",
                "search_query",
                "target_journals",
                "evidence_type",
                "candidate_source",
                "status",
                "manuscript_location",
                "risk_note",
            ],
        )
        self.assertEqual(rows[0]["claim_or_need"], "Bond strength improvement")
        self.assertEqual(rows[0]["evidence_type"], "performance")
        self.assertEqual(rows[1]["evidence_type"], "mechanism")


if __name__ == "__main__":
    unittest.main()

import csv
import io
import sys
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE_ROOT))

from academic_search.adapters import AdapterDisabled, AdapterError
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


class FailingAdapter:
    def __init__(self, exc):
        self.exc = exc

    def search(self, query, *, journals=None, year_range=None, limit=10):
        raise self.exc

    def fetch(self, *, doi=None, title=None, external_id=None):
        raise self.exc


class MeshAdapter(FakeAdapter):
    name = "PubMed"

    def lookup_mesh(self, topic, *, limit=10):
        return {
            "topic": topic,
            "mesh_terms": ["Epoxy Resins", "Emulsions"],
            "scope_notes": ["Polymeric compounds containing epoxy groups."],
            "source": "PubMed MeSH",
        }


class AcademicSearchServiceTest(unittest.TestCase):
    def test_default_service_includes_pubmed_adapter(self):
        service = AcademicSearchService()

        self.assertIn("PubMed", [adapter.name for adapter in service.adapters])

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

        result = service.search_materials(
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
        self.assertIn("bonding_interface_performance", record["evidence_layers"])
        self.assertIn("microstructure_chemistry", record["evidence_layers"])
        self.assertIn("metadata_conflicts", record)
        self.assertIn("year", record["metadata_conflicts"])
        self.assertIn("source_provenance", record)
        self.assertEqual(len(record["source_provenance"]), 2)

    def test_search_uses_safe_limit_default_and_collects_adapter_warnings(self):
        service = AcademicSearchService(
            adapters=[
                FailingAdapter(AdapterDisabled("disabled source")),
                FailingAdapter(AdapterError("transient upstream failure")),
                FakeAdapter(
                    [
                        {
                            "title": "Bonding interface of waterborne epoxy emulsified asphalt",
                            "doi": "10.1000/bond",
                            "journal": "Construction and Building Materials",
                            "year": 2025,
                            "abstract": "Pull-off bonding interface data.",
                            "source": "Crossref",
                        }
                    ]
                ),
            ]
        )

        result = service.search_materials(
            {
                "topic": "waterborne epoxy modified emulsified asphalt bonding performance",
                "limit": "not-a-number",
            }
        )

        self.assertEqual(len(result["records"]), 1)
        self.assertEqual(result["warnings"], ["disabled source", "transient upstream failure"])

    def test_search_logs_adapter_failures(self):
        service = AcademicSearchService(
            adapters=[
                FailingAdapter(AdapterDisabled("disabled source")),
                FailingAdapter(AdapterError("transient upstream failure")),
            ]
        )

        with self.assertLogs("academic_search.service", level="WARNING") as captured:
            result = service.search_materials(
                {
                    "topic": "waterborne epoxy modified emulsified asphalt bonding performance",
                }
            )

        self.assertEqual(result["records"], [])
        self.assertIn("disabled source", "\n".join(captured.output))
        self.assertIn("transient upstream failure", "\n".join(captured.output))

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

    def test_build_claim_source_map_matches_records_by_explicit_evidence_type(self):
        service = AcademicSearchService(adapters=[])

        result = service.build_claim_source_map(
            {
                "topic": "waterborne epoxy modified emulsified asphalt",
                "claims": ["The material improves bonding performance."],
                "candidate_records": [
                    {
                        "title": "Storage stability only",
                        "evidence_layers": ["emulsion_stability"],
                    },
                    {
                        "title": "Pull-off bonding strength study",
                        "evidence_layers": ["bonding_interface_performance"],
                    },
                ],
            }
        )

        candidates = result["claim_source_map"][0]["candidate_records"]

        self.assertEqual([record["title"] for record in candidates], ["Pull-off bonding strength study"])

    def test_export_citation_matrix_matches_expanded_csv_schema(self):
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
                "claim_id",
                "priority",
                "claim_or_need",
                "evidence_layer",
                "source_role",
                "source_quality",
                "mechanism_directness",
                "durability_relevance",
                "service_relevance",
                "reader_anchor",
                "figure_handoff",
                "reviewer_risk",
                "search_query",
                "target_journals",
                "evidence_type",
                "candidate_source",
                "status",
                "manuscript_location",
                "risk_note",
            ],
        )
        self.assertEqual(rows[0]["claim_id"], "CIT-001")
        self.assertEqual(rows[0]["claim_or_need"], "Bond strength improvement")
        self.assertEqual(rows[0]["evidence_layer"], "bonding_interface_performance")
        self.assertEqual(rows[0]["source_role"], "primary experimental evidence")
        self.assertEqual(rows[0]["source_quality"], "screening needed")
        self.assertEqual(rows[0]["figure_handoff"], "not assessed")
        self.assertEqual(rows[0]["reviewer_risk"], "must-fix")
        self.assertEqual(rows[0]["evidence_type"], "performance")
        self.assertEqual(rows[1]["evidence_type"], "mechanism")
        self.assertEqual(rows[1]["mechanism_directness"], "direct mechanism evidence needed")

    def test_export_citation_matrix_escapes_excel_formula_cells(self):
        service = AcademicSearchService(adapters=[])

        result = service.export_citation_matrix(
            {
                "topic": "waterborne epoxy modified emulsified asphalt",
                "claims": ["=CMD('calc')"],
                "target_journals": ["CBM"],
            }
        )

        row = next(csv.DictReader(io.StringIO(result["csv"])))

        self.assertEqual(row["claim_or_need"], "'=CMD('calc')")

    def test_lookup_mesh_delegates_to_pubmed_capable_adapter(self):
        service = AcademicSearchService(adapters=[MeshAdapter([])])

        result = service.lookup_mesh({"topic": "epoxy resin", "limit": 5})

        self.assertEqual(result["topic"], "epoxy resin")
        self.assertEqual(result["mesh_terms"], ["Epoxy Resins", "Emulsions"])
        self.assertEqual(result["source"], "PubMed MeSH")


if __name__ == "__main__":
    unittest.main()

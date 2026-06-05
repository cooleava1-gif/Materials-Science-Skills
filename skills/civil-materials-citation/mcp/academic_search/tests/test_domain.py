import sys
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE_ROOT))

from academic_search.domain.classifier import classify_evidence_layers, evidence_type_for_claim
from academic_search.domain.journals import canonical_journal_family, expand_journal_terms
from academic_search.domain.queries import suggest_queries


class DomainRulesTest(unittest.TestCase):
    def test_classifies_waterborne_epoxy_asphalt_evidence_layers(self):
        text = (
            "Waterborne epoxy modified emulsified asphalt showed improved pull-off "
            "bonding strength after demulsification. FTIR and fluorescence microscopy "
            "confirmed curing and phase compatibility under moisture aging."
        )

        layers = classify_evidence_layers(text)

        self.assertIn("demulsification", layers)
        self.assertIn("epoxy_curing", layers)
        self.assertIn("bonding_interface", layers)
        self.assertIn("ftir_sem_fluorescence_rheology", layers)
        self.assertIn("moisture_aging_service", layers)

    def test_claim_evidence_type_separates_mechanism_performance_and_durability(self):
        self.assertEqual(evidence_type_for_claim("FTIR explains the curing mechanism"), "mechanism")
        self.assertEqual(evidence_type_for_claim("bond strength increased after modification"), "performance")
        self.assertEqual(evidence_type_for_claim("moisture aging durability should be improved"), "durability")
        self.assertEqual(evidence_type_for_claim("recent progress and research gap"), "review/positioning")

    def test_journal_alias_expansion_supports_civil_materials_targets(self):
        self.assertEqual(canonical_journal_family("CBM"), "Construction and Building Materials")
        self.assertEqual(canonical_journal_family("ccc"), "Cement and Concrete Composites")

        terms = expand_journal_terms(["CBM", "RMPD", "IJPE", "JRE", "CSCM"])

        self.assertIn("Construction and Building Materials", terms)
        self.assertIn("Road Materials and Pavement Design", terms)
        self.assertIn("International Journal of Pavement Engineering", terms)
        self.assertIn("Journal of Road Engineering", terms)
        self.assertIn("Case Studies in Construction Materials", terms)

    def test_query_suggestions_include_topic_evidence_and_journal_terms(self):
        queries = suggest_queries(
            topic="waterborne epoxy modified emulsified asphalt",
            journal_family=["CBM", "RMPD"],
            evidence_layer="bonding_interface",
            year_range="2020-2026",
        )

        self.assertTrue(queries)
        query = queries[0]["query"]
        self.assertIn('"waterborne epoxy modified emulsified asphalt"', query)
        self.assertIn("bonding", query)
        self.assertIn("Construction and Building Materials", query)
        self.assertIn("Road Materials and Pavement Design", query)
        self.assertEqual(queries[0]["year_range"], "2020-2026")


if __name__ == "__main__":
    unittest.main()

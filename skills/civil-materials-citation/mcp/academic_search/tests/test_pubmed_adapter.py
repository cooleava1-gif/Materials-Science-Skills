import sys
import unittest
from pathlib import Path
from unittest.mock import patch


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE_ROOT))

from academic_search.adapters.pubmed import PubMedAdapter


class FakeResponse:
    def __init__(self, text, status_code=200):
        self.text = text
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


ESEARCH_XML = """<?xml version="1.0" encoding="UTF-8"?>
<eSearchResult>
  <Count>1</Count>
  <QueryKey>1</QueryKey>
  <WebEnv>NCBI_WEbenv</WebEnv>
</eSearchResult>
"""

EFETCH_XML = """<?xml version="1.0" encoding="UTF-8"?>
<PubmedArticleSet>
  <PubmedArticle>
    <MedlineCitation>
      <PMID>12345678</PMID>
      <Article>
        <ArticleTitle>Waterborne epoxy modified emulsified asphalt bonding performance</ArticleTitle>
        <Abstract>
          <AbstractText Label="Objective">Pull-off bonding was measured.</AbstractText>
          <AbstractText>FTIR and SEM supported the curing mechanism.</AbstractText>
        </Abstract>
        <AuthorList>
          <Author><LastName>Zhang</LastName><ForeName>Haoran</ForeName></Author>
          <Author><CollectiveName>Civil Materials Group</CollectiveName></Author>
        </AuthorList>
        <Journal>
          <Title>Construction and Building Materials</Title>
          <JournalIssue><PubDate><Year>2024</Year></PubDate></JournalIssue>
        </Journal>
        <ELocationID EIdType="doi">10.1016/j.conbuildmat.2024.123456</ELocationID>
      </Article>
    </MedlineCitation>
  </PubmedArticle>
</PubmedArticleSet>
"""

MESH_XML = """<?xml version="1.0" encoding="UTF-8"?>
<eSearchResult>
  <IdList><Id>68004815</Id><Id>68016454</Id></IdList>
</eSearchResult>
"""

MESH_FETCH_XML = """<?xml version="1.0" encoding="UTF-8"?>
<eSummaryResult>
  <DocumentSummarySet>
    <DocumentSummary uid="68004815">
      <DS_MeshTerms><string>Epoxy Resins</string></DS_MeshTerms>
      <ConceptList><Concept><ScopeNote>Polymeric compounds containing epoxy groups.</ScopeNote></Concept></ConceptList>
    </DocumentSummary>
    <DocumentSummary uid="68016454">
      <DS_MeshTerms><string>Emulsions</string></DS_MeshTerms>
    </DocumentSummary>
  </DocumentSummarySet>
</eSummaryResult>
"""


class PubMedAdapterTest(unittest.TestCase):
    def test_search_uses_history_and_parses_medline_xml(self):
        calls = []

        def fake_get_response(url, *, params=None, **kwargs):
            calls.append((url, params))
            if url.endswith("esearch.fcgi"):
                return FakeResponse(ESEARCH_XML)
            if url.endswith("efetch.fcgi"):
                return FakeResponse(EFETCH_XML)
            raise AssertionError(f"unexpected URL: {url}")

        adapter = PubMedAdapter(email="haoran@example.com", sleep=lambda _: None)

        with patch("academic_search.adapters.pubmed.get_response_with_retries", side_effect=fake_get_response):
            records = adapter.search(
                '"waterborne epoxy" AND bonding',
                journals=["Construction and Building Materials"],
                year_range="2020-2026",
                limit=5,
            )

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["source"], "PubMed")
        self.assertEqual(records[0]["doi"], "10.1016/j.conbuildmat.2024.123456")
        self.assertEqual(records[0]["external_ids"]["pmid"], "12345678")
        self.assertEqual(records[0]["authors"], ["Haoran Zhang", "Civil Materials Group"])
        self.assertIn("Objective: Pull-off bonding was measured.", records[0]["abstract"])
        self.assertIn("FTIR and SEM", records[0]["abstract"])
        self.assertEqual(records[0]["year"], 2024)
        self.assertIn("2020:2026[pdat]", calls[0][1]["term"])
        self.assertEqual(calls[1][1]["WebEnv"], "NCBI_WEbenv")
        self.assertEqual(calls[1][1]["query_key"], "1")

    def test_fetch_treats_numeric_external_id_as_pmid(self):
        def fake_get_response(url, *, params=None, **kwargs):
            self.assertTrue(url.endswith("efetch.fcgi"))
            self.assertEqual(params["id"], "12345678")
            return FakeResponse(EFETCH_XML)

        adapter = PubMedAdapter(email="haoran@example.com", sleep=lambda _: None)

        with patch("academic_search.adapters.pubmed.get_response_with_retries", side_effect=fake_get_response):
            record = adapter.fetch(external_id="12345678")

        self.assertEqual(record["title"], "Waterborne epoxy modified emulsified asphalt bonding performance")
        self.assertEqual(record["external_ids"]["pmid"], "12345678")

    def test_lookup_mesh_returns_standard_terms_and_scope_notes(self):
        def fake_get_response(url, *, params=None, **kwargs):
            if url.endswith("esearch.fcgi"):
                self.assertEqual(params["db"], "mesh")
                return FakeResponse(MESH_XML)
            if url.endswith("esummary.fcgi"):
                self.assertEqual(params["id"], "68004815,68016454")
                return FakeResponse(MESH_FETCH_XML)
            raise AssertionError(f"unexpected URL: {url}")

        adapter = PubMedAdapter(email="haoran@example.com", sleep=lambda _: None)

        with patch("academic_search.adapters.pubmed.get_response_with_retries", side_effect=fake_get_response):
            result = adapter.lookup_mesh("epoxy resin")

        self.assertEqual(result["topic"], "epoxy resin")
        self.assertEqual(result["mesh_terms"], ["Epoxy Resins", "Emulsions"])
        self.assertIn("Polymeric compounds", result["scope_notes"][0])


if __name__ == "__main__":
    unittest.main()

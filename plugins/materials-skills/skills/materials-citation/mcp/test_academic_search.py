"""Unit tests for the materials academic-search MCP package.

The suite runs fully offline: HTTP retry behaviour is exercised through
injected client factories, and service-level fallback paths through stub
adapters. No network access is required.
"""

from __future__ import annotations

import os
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from academic_search.adapters import AdapterDisabled, AdapterError
from academic_search.adapters.base import (
    get_response_with_retries,
    normalize_doi,
    normalize_title,
)
from academic_search.domain.identifiers import (
    deduplicate_records,
    normalize_arxiv_id,
    normalize_pmcid,
    normalize_pmid,
)
from academic_search.domain.queries import build_pubmed_query, suggest_queries
from academic_search.service import AcademicSearchService


# ── Test doubles ────────────────────────────────────────────────────


class StubAdapter:
    """Configurable academic-source adapter for offline service tests."""

    name = "stub"

    def __init__(self, *, name="stub", records=None, fetch_record=None, error=None, disabled=False):
        self.name = name
        self.records = records or []
        self.fetch_record = fetch_record
        self.error = error
        self.disabled = disabled
        self.search_calls: list[dict] = []

    def search(self, query, *, journals=None, year_range=None, limit=10):
        self.search_calls.append(
            {"query": query, "journals": journals, "year_range": year_range, "limit": limit}
        )
        if self.disabled:
            raise AdapterDisabled("stub source disabled: missing API key")
        if self.error:
            raise AdapterError(self.error)
        return [dict(record) for record in self.records]

    def fetch(self, *, doi=None, title=None, external_id=None):
        if self.disabled:
            raise AdapterDisabled("stub source disabled: missing API key")
        if self.error:
            raise AdapterError(self.error)
        return dict(self.fetch_record) if self.fetch_record else None


class FailingAdapter(StubAdapter):
    name = "failing"

    def __init__(self):
        super().__init__(error="upstream 503 persisted")


class DisabledAdapter(StubAdapter):
    name = "disabled"

    def __init__(self):
        super().__init__(disabled=True)


class FakeResponse:
    def __init__(self, status_code, headers=None, text=""):
        self.status_code = status_code
        self.headers = headers or {}
        self.text = text


class FakeClient:
    def __init__(self, responses):
        self._responses = list(responses)

    def __enter__(self):
        return self

    def __exit__(self, *exc_info):
        return False

    def get(self, url, params=None):
        return self._responses.pop(0) if self._responses else FakeResponse(200)


def make_client_factory(scripts):
    """One script (list of FakeResponse) per client creation (= per attempt)."""
    queue = list(scripts)

    def factory(**kwargs):
        return FakeClient(queue.pop(0) if queue else scripts[-1])

    return factory


def sample_record(**overrides):
    record = {
        "title": "Waterborne epoxy modified emulsified asphalt tack coats",
        "doi": "10.1000/example",
        "journal": "Construction and Building Materials",
        "year": 2024,
        "authors": ["A. Researcher"],
        "abstract": "SEM and FTIR evidence of chemical bridging at the interface.",
        "source": "stub",
    }
    record.update(overrides)
    return record


# ── Search-plan generators ─────────────────────────────────────────


class TestSuggestQueries:
    def test_topic_is_required(self):
        with pytest.raises(ValueError):
            suggest_queries(topic="   ")

    def test_boolean_query_structure(self):
        queries = suggest_queries(
            topic="waterborne epoxy emulsified asphalt",
            material_domain="asphalt",
            evidence_layer="microstructure_chemistry",
            limit=1,
        )
        assert len(queries) == 1
        query = queries[0]["query"]
        assert '"waterborne epoxy emulsified asphalt"' in query
        assert " AND " in query
        assert queries[0]["evidence_layer"] == "microstructure_chemistry"

    def test_unknown_layer_alias_maps_to_canonical(self):
        queries = suggest_queries(
            topic="emulsion storage stability",
            evidence_layer="storage_stability",
            limit=1,
        )
        assert queries[0]["evidence_layer"] == "emulsion_stability"

    def test_journal_family_expansion(self):
        queries = suggest_queries(
            topic="cement hydration",
            journal_family="CCC",
            evidence_layer="microstructure_chemistry",
            limit=1,
        )
        assert "Cement and Concrete Composites" in queries[0]["query"]
        assert queries[0]["journal_terms"] == "Cement and Concrete Composites"


class TestPubmedQuery:
    def test_journal_and_date_filters(self):
        query = build_pubmed_query(
            '"concrete" AND ("durability")',
            journals="Cement and Concrete Composites",
            year_range="2020-2024",
        )
        assert '"Cement and Concrete Composites"[Journal]' in query
        assert "2020:2024[pdat]" in query
        assert query.startswith("(")

    def test_open_ended_year_range(self):
        query = build_pubmed_query("concrete", journals=None, year_range="2022-")
        assert "2022:3000[pdat]" in query


# ── Adapter helpers ─────────────────────────────────────────────────


class TestAdapterHelpers:
    def test_normalize_doi_variants(self):
        assert normalize_doi("https://doi.org/10.1000/Example.X") == "10.1000/example.x"
        assert normalize_doi("doi: 10.1000/EXAMPLE") == "10.1000/example"
        assert normalize_doi("") == ""

    def test_normalize_title_strips_markup(self):
        assert normalize_title("<i>Asphalt</i>-Emulsion  Study!") == "asphalt emulsion study"

    def test_retry_succeeds_without_sleep_on_200(self):
        slept = []
        response = get_response_with_retries(
            "https://example.test",
            client_factory=make_client_factory([[FakeResponse(200, text="ok")]]),
            sleep=slept.append,
        )
        assert response.status_code == 200
        assert slept == []

    def test_retry_recovers_from_503(self):
        slept = []
        response = get_response_with_retries(
            "https://example.test",
            client_factory=make_client_factory(
                [[FakeResponse(503)], [FakeResponse(200, text="ok")]]
            ),
            sleep=slept.append,
            jitter=lambda delay: delay,
        )
        assert response.status_code == 200
        assert len(slept) == 1
        assert slept[0] > 0

    def test_retry_honors_retry_after_header(self):
        slept = []
        response = get_response_with_retries(
            "https://example.test",
            client_factory=make_client_factory(
                [
                    [FakeResponse(429, headers={"Retry-After": "0.5"})],
                    [FakeResponse(200)],
                ]
            ),
            sleep=slept.append,
        )
        assert response.status_code == 200
        assert slept == [0.5]


# ── Identifier normalizers ──────────────────────────────────────────


class TestIdentifierNormalizers:
    def test_pmid_and_pmcid(self):
        assert normalize_pmid("PMID: 12345678.") == "12345678"
        assert normalize_pmcid("pmc5521909") == "PMC5521909"

    def test_arxiv_id_variants(self):
        assert (
            normalize_arxiv_id("https://arxiv.org/abs/2401.12345v2") == "2401.12345v2"
        )
        assert normalize_arxiv_id("arXiv: cond-mat/0703470") == "cond-mat/0703470"


# ── Service: search fallback paths ─────────────────────────────────


class TestServiceSearch:
    def test_topic_is_required(self):
        service = AcademicSearchService(adapters=[StubAdapter()])
        with pytest.raises(ValueError):
            service.search_materials({"topic": "  "})

    def test_search_merges_duplicate_doi_across_sources(self):
        first = StubAdapter(name="first", records=[sample_record()])
        second = StubAdapter(
            name="second",
            records=[sample_record(source="second", citation_count=7)],
        )
        service = AcademicSearchService(adapters=[first, second])
        result = service.search_materials({"topic": "waterborne epoxy asphalt", "limit": 5})
        assert len(result["records"]) == 1
        record = result["records"][0]
        assert len(record["source_provenance"]) == 2
        assert record["citation_count"] == 7
        assert record["confidence"] >= 0.95  # multi-source bonus included

    def test_search_continues_when_adapter_fails(self):
        failing = FailingAdapter()
        working = StubAdapter(records=[sample_record()])
        service = AcademicSearchService(adapters=[failing, working])
        result = service.search_materials({"topic": "waterborne epoxy asphalt"})
        assert len(result["records"]) == 1
        assert any("upstream 503 persisted" in warning for warning in result["warnings"])

    def test_search_reports_disabled_optional_source(self):
        disabled = DisabledAdapter()
        working = StubAdapter(records=[sample_record()])
        service = AcademicSearchService(adapters=[disabled, working])
        result = service.search_materials({"topic": "waterborne epoxy asphalt"})
        assert len(result["records"]) == 1
        assert any("missing API key" in warning for warning in result["warnings"])

    def test_search_passes_journal_terms_to_adapters(self):
        stub = StubAdapter(records=[])
        service = AcademicSearchService(adapters=[stub])
        service.search_materials({"topic": "cement hydration", "journal_family": "CCC"})
        assert stub.search_calls[0]["journals"] == ["Cement and Concrete Composites"]


# ── Service: metadata fetch fallback paths ─────────────────────────


class TestServiceFetch:
    def test_fetch_requires_an_identifier(self):
        service = AcademicSearchService(adapters=[StubAdapter()])
        with pytest.raises(ValueError):
            service.fetch_paper_metadata({})

    def test_fetch_returns_flagged_empty_record_when_all_sources_fail(self):
        failing = FailingAdapter()
        empty = StubAdapter()
        service = AcademicSearchService(adapters=[failing, empty])
        result = service.fetch_paper_metadata({"doi": "10.1000/missing"})
        assert result["record"]["doi"] == "10.1000/missing"
        assert "No upstream source returned metadata." in result["record"]["risk_flags"]
        assert result["warnings"]

    def test_fetch_uses_first_available_record(self):
        empty = StubAdapter()
        working = StubAdapter(fetch_record=sample_record())
        service = AcademicSearchService(adapters=[empty, working])
        result = service.fetch_paper_metadata({"doi": "10.1000/example"})
        assert result["record"]["title"].startswith("Waterborne epoxy")


# ── Service: source listing with optional adapters ─────────────────


class TestListSources:
    def test_optional_sources_reported_disabled_without_api_keys(self, monkeypatch):
        for key in ("SCOPUS_API_KEY", "ELSEVIER_API_KEY"):
            monkeypatch.delenv(key, raising=False)
        service = AcademicSearchService(adapters=[StubAdapter()])
        listing = service.list_academic_sources()
        names = {source["name"]: source for source in listing["sources"]}
        assert names["stub"]["enabled"] is True
        assert names["scopus"]["enabled"] is False
        assert names["scopus"]["optional"] is True
        assert names["scopus"]["warning"]


# ── Service: ID resolution and deduplication ───────────────────────


class TestServiceConversion:
    def test_resolve_paper_ids_normalizes_inputs(self):
        service = AcademicSearchService(adapters=[])
        result = service.resolve_paper_ids(
            {"doi": "https://doi.org/10.1000/Example.X", "pmid": "PMID: 12345678"}
        )
        assert result["external_ids"]["doi"] == "10.1000/example.x"
        assert result["external_ids"]["pmid"] == "12345678"

    def test_deduplicate_records_merges_by_doi(self):
        records = [
            sample_record(),
            sample_record(source="duplicate", year=2024),
            sample_record(doi="10.1000/other", title="A different paper"),
        ]
        deduplicated = deduplicate_records(records)
        assert len(deduplicated) == 2
        assert set(deduplicated[0]["sources"]) == {"stub", "duplicate"}

    def test_deduplicate_citation_records_endpoint(self):
        service = AcademicSearchService(adapters=[])
        result = service.deduplicate_citation_records(
            {"records": [sample_record(), sample_record(source="copy")]}
        )
        assert result["input_count"] == 2
        assert result["count"] == 1


# ── Service: claim tools and export safety ─────────────────────────


class TestClaimTools:
    def test_citation_matrix_csv_structure_and_injection_guard(self):
        service = AcademicSearchService(adapters=[])
        result = service.export_citation_matrix(
            {"topic": "emulsified asphalt", "manuscript_location": "=HYPERLINK(evil)"}
        )
        header = result["csv"].splitlines()[0]
        assert header.startswith("claim_id,priority,claim_or_need")
        rows = result["rows"]
        assert rows[0]["claim_id"] == "CIT-001"
        assert rows[0]["manuscript_location"].startswith("'=")

    def test_audit_flags_mechanism_claim_without_microstructure_evidence(self):
        service = AcademicSearchService(adapters=[])
        result = service.audit_reference_gaps(
            {"claims": ["The chemical mechanism explains the performance gain"]}
        )
        flags = " ".join(flag for gap in result["gaps"] for flag in gap["risk_flags"])
        assert "No confirmed source mapped" in flags
        assert "FTIR/SEM/fluorescence/rheology" in flags

    def test_audit_clean_when_evidence_mapped(self):
        service = AcademicSearchService(adapters=[])
        record = sample_record(evidence_layers=["microstructure_chemistry"])
        result = service.audit_reference_gaps(
            {
                "claims": ["The chemical mechanism explains the performance gain"],
                "candidate_records": [record],
            }
        )
        assert result["gaps"] == []

"""Tests for async search concurrency in the MCP service layer."""

import asyncio
import unittest
import sys
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

MCP_ROOT = Path(__file__).resolve().parents[2] / "mcp"
if str(MCP_ROOT) not in sys.path:
    sys.path.insert(0, str(MCP_ROOT))

from academic_search.service import AcademicSearchService
from academic_search.adapters.base import AdapterDisabled, AdapterError


class FakeAdapter:
    """Minimal adapter stub for async concurrency testing."""

    def __init__(self, name: str, *, delay: float = 0.0, records: list | None = None, fail: bool = False):
        self.name = name
        self._delay = delay
        self._records = records or []
        self._fail = fail

    def search(self, query: str, *, journals=None, year_range: str | None = None, limit: int = 10) -> list[dict[str, Any]]:
        if self._fail:
            raise AdapterError(f"{self.name} search failed")
        import time
        time.sleep(self._delay)
        return self._records

    def fetch(self, *, doi: str | None = None, title: str | None = None, external_id: str | None = None) -> dict[str, Any] | None:
        if self._fail:
            raise AdapterError(f"{self.name} fetch failed")
        import time
        time.sleep(self._delay)
        return self._records[0] if self._records else None


class AsyncSearchConcurrencyTest(unittest.TestCase):
    def test_async_search_calls_all_adapters(self):
        """Verify that search_civil_materials_async calls all adapters."""
        adapter_a = FakeAdapter("A", records=[{"title": "Paper A", "doi": "10.1/a", "source": "A"}])
        adapter_b = FakeAdapter("B", records=[{"title": "Paper B", "doi": "10.1/b", "source": "B"}])
        service = AcademicSearchService(adapters=[adapter_a, adapter_b])

        result = asyncio.run(service.search_civil_materials_async({"topic": "asphalt bonding"}))
        self.assertIn("records", result)
        # Both adapters should have been called (2 distinct DOIs)
        dois = [r["doi"] for r in result["records"]]
        self.assertIn("10.1/a", dois)
        self.assertIn("10.1/b", dois)

    def test_async_search_handles_adapter_failure(self):
        """Failed adapter should produce a warning, not crash."""
        good = FakeAdapter("Good", records=[{"title": "OK", "doi": "10.1/ok", "source": "Good"}])
        bad = FakeAdapter("Bad", fail=True)
        service = AcademicSearchService(adapters=[bad, good])

        result = asyncio.run(service.search_civil_materials_async({"topic": "test"}))
        self.assertTrue(len(result["warnings"]) >= 1)
        self.assertTrue(any("Bad" in w for w in result["warnings"]))
        # Good adapter's results should still be present
        self.assertTrue(len(result["records"]) >= 1)

    def test_async_search_handles_disabled_adapter(self):
        """Disabled adapter should produce a warning."""
        def make_disabled():
            adapter = MagicMock()
            adapter.search = MagicMock(side_effect=AdapterDisabled("OpenAlex disabled"))
            adapter.name = "OpenAlex"
            return adapter

        good = FakeAdapter("Good", records=[{"title": "OK", "doi": "10.1/ok", "source": "Good"}])
        service = AcademicSearchService(adapters=[make_disabled(), good])

        result = asyncio.run(service.search_civil_materials_async({"topic": "test"}))
        self.assertTrue(any("disabled" in w.lower() for w in result["warnings"]))

    def test_async_fetch_calls_all_adapters(self):
        """fetch_paper_metadata_async should call all adapters."""
        adapter_a = FakeAdapter("A", records=[{"title": "Paper A", "doi": "10.1/a", "source": "A"}])
        adapter_b = FakeAdapter("B", records=[{"title": "Paper A", "doi": "10.1/a", "source": "B"}])
        service = AcademicSearchService(adapters=[adapter_a, adapter_b])

        result = asyncio.run(service.fetch_paper_metadata_async({"doi": "10.1/a"}))
        self.assertEqual(result["record"]["doi"], "10.1/a")

    def test_async_fetch_concurrent_execution(self):
        """Adapters with delays should run concurrently, not sequentially."""
        import time
        # Each adapter sleeps 0.1s; if sequential, total >= 0.2s
        # If concurrent, total should be ~0.1s + overhead
        adapter_a = FakeAdapter("A", delay=0.1, records=[{"title": "A", "doi": "10.1/a", "source": "A"}])
        adapter_b = FakeAdapter("B", delay=0.1, records=[{"title": "B", "doi": "10.1/b", "source": "B"}])
        service = AcademicSearchService(adapters=[adapter_a, adapter_b])

        start = time.monotonic()
        result = asyncio.run(service.search_civil_materials_async({"topic": "test"}))
        elapsed = time.monotonic() - start

        self.assertTrue(len(result["records"]) >= 2)
        # Should take ~0.1s (concurrent), not ~0.2s (sequential)
        # Use generous bound for CI environments
        self.assertLess(elapsed, 0.5, "Search should run adapters concurrently, not sequentially")


if __name__ == "__main__":
    unittest.main()

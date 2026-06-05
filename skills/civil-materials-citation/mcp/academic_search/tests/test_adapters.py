import sys
import unittest
from pathlib import Path

import httpx


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE_ROOT))

from academic_search.adapters.base import AcademicSourceAdapter, get_json_with_retries


class FakeResponse:
    def __init__(self, status_code, payload=None):
        self.status_code = status_code
        self.payload = payload or {}
        self.request = httpx.Request("GET", "https://example.test")
        self.response = httpx.Response(status_code, request=self.request)

    def json(self):
        return self.payload

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("upstream error", request=self.request, response=self.response)


class FakeClient:
    def __init__(self, responses, calls):
        self.responses = responses
        self.calls = calls

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def get(self, url, params=None):
        self.calls.append({"url": url, "params": params})
        return self.responses.pop(0)


class AdapterBaseTest(unittest.TestCase):
    def test_academic_source_adapter_protocol_documents_required_methods(self):
        self.assertTrue(hasattr(AcademicSourceAdapter, "search"))
        self.assertTrue(hasattr(AcademicSourceAdapter, "fetch"))

    def test_get_json_with_retries_retries_429_with_backoff(self):
        calls = []
        sleeps = []
        responses = [FakeResponse(429), FakeResponse(200, {"ok": True})]

        def client_factory(**kwargs):
            return FakeClient(responses, calls)

        payload = get_json_with_retries(
            "https://example.test/works",
            params={"query": "waterborne epoxy"},
            timeout=1.0,
            client_factory=client_factory,
            sleep=sleeps.append,
        )

        self.assertEqual(payload, {"ok": True})
        self.assertEqual(len(calls), 2)
        self.assertEqual(sleeps, [1.0])

    def test_get_json_with_retries_does_not_retry_404(self):
        calls = []
        sleeps = []
        responses = [FakeResponse(404)]

        def client_factory(**kwargs):
            return FakeClient(responses, calls)

        with self.assertRaises(httpx.HTTPStatusError):
            get_json_with_retries(
                "https://example.test/missing",
                timeout=1.0,
                client_factory=client_factory,
                sleep=sleeps.append,
            )

        self.assertEqual(len(calls), 1)
        self.assertEqual(sleeps, [])


if __name__ == "__main__":
    unittest.main()

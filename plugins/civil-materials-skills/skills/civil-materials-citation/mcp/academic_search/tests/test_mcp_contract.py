import sys
import unittest
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PACKAGE_ROOT))

from academic_search.server import handle_message


class StubService:
    def search_civil_materials(self, args):
        return {"records": [{"title": args["topic"], "source_provenance": []}], "warnings": []}

    def fetch_paper_metadata(self, args):
        return {"record": {"doi": args.get("doi"), "source_provenance": []}, "warnings": []}

    def suggest_search_queries(self, args):
        return {"queries": [{"query": '"topic" AND bonding'}]}

    def build_claim_source_map(self, args):
        return {"claim_source_map": [{"claim": "bonding", "risk_flags": []}]}

    def audit_reference_gaps(self, args):
        return {"gaps": [{"claim": "mechanism", "risk": "missing mechanism evidence"}]}

    def export_citation_matrix(self, args):
        return {"rows": [], "csv": "priority,claim_or_need\n"}

    def lookup_mesh(self, args):
        return {"topic": args["topic"], "mesh_terms": ["Epoxy Resins"], "scope_notes": []}

    def get_formatted_citation(self, args):
        doi = args.get("doi", "")
        fmt = args.get("format", "ris")
        return {"format": fmt, "count": 1, "content": f"Formatted citation for {doi}", "warnings": []}


class McpContractTest(unittest.TestCase):
    def test_initialize_response_advertises_tools_capability(self):
        response = handle_message(
            {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
            service=StubService(),
        )

        self.assertEqual(response["id"], 1)
        self.assertEqual(response["result"]["serverInfo"]["name"], "civil-materials-academic-search")
        self.assertIn("tools", response["result"]["capabilities"])

    def test_tools_list_contains_public_academic_search_tools(self):
        response = handle_message(
            {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
            service=StubService(),
        )

        names = {tool["name"] for tool in response["result"]["tools"]}

        self.assertEqual(
            names,
            {
                "search_civil_materials",
                "fetch_paper_metadata",
                "suggest_search_queries",
                "build_claim_source_map",
                "audit_reference_gaps",
                "export_citation_matrix",
                "lookup_mesh",
                "get_formatted_citation",
            },
        )

    def test_tools_call_returns_text_content_and_structured_content(self):
        response = handle_message(
            {
                "jsonrpc": "2.0",
                "id": 3,
                "method": "tools/call",
                "params": {
                    "name": "search_civil_materials",
                    "arguments": {"topic": "waterborne epoxy modified emulsified asphalt"},
                },
            },
            service=StubService(),
        )

        result = response["result"]
        self.assertEqual(result["content"][0]["type"], "text")
        self.assertEqual(
            result["structuredContent"]["records"][0]["title"],
            "waterborne epoxy modified emulsified asphalt",
        )

    def test_all_public_tools_return_structured_content_through_protocol(self):
        calls = [
            ("fetch_paper_metadata", {"doi": "10.1000/example"}, "record"),
            ("suggest_search_queries", {"topic": "waterborne epoxy modified emulsified asphalt"}, "queries"),
            ("build_claim_source_map", {"claims": ["bonding strength improves"]}, "claim_source_map"),
            ("audit_reference_gaps", {"claims": ["mechanism is proven"]}, "gaps"),
            ("export_citation_matrix", {"claims": ["bonding strength improves"]}, "rows"),
            ("lookup_mesh", {"topic": "epoxy resin"}, "mesh_terms"),
            ("get_formatted_citation", {"doi": "10.1000/example", "format": "ris"}, "content"),
        ]

        for index, (tool_name, arguments, expected_key) in enumerate(calls, start=10):
            with self.subTest(tool_name=tool_name):
                response = handle_message(
                    {
                        "jsonrpc": "2.0",
                        "id": index,
                        "method": "tools/call",
                        "params": {"name": tool_name, "arguments": arguments},
                    },
                    service=StubService(),
                )

                self.assertIn(expected_key, response["result"]["structuredContent"])

    def test_tool_validation_errors_return_invalid_params(self):
        class ValidationService(StubService):
            def fetch_paper_metadata(self, args):
                raise ValueError("doi, title, or external_id is required")

        response = handle_message(
            {
                "jsonrpc": "2.0",
                "id": 30,
                "method": "tools/call",
                "params": {"name": "fetch_paper_metadata", "arguments": {}},
            },
            service=ValidationService(),
        )

        self.assertEqual(response["error"]["code"], -32602)
        self.assertIn("doi, title, or external_id", response["error"]["message"])

    def test_unknown_tool_returns_json_rpc_error(self):
        response = handle_message(
            {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {"name": "missing_tool", "arguments": {}},
            },
            service=StubService(),
        )

        self.assertEqual(response["error"]["code"], -32601)
        self.assertIn("missing_tool", response["error"]["message"])


if __name__ == "__main__":
    unittest.main()

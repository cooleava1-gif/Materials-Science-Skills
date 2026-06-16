"""Test the stdio JSON-RPC MCP server."""
import json
import subprocess
import sys
import unittest
from pathlib import Path


SERVER_DIR = Path(__file__).resolve().parents[2]
SERVER_SCRIPT = SERVER_DIR / "server.py"
PACKAGE_ROOT = Path(__file__).resolve().parents[2]


class StdioMCPContractTest(unittest.TestCase):
    """Test that the server responds correctly to MCP protocol messages."""

    def _send(self, message: dict) -> dict:
        """Send a JSON-RPC message to the server and return the response."""
        proc = subprocess.Popen(
            [sys.executable, str(SERVER_SCRIPT)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=str(SERVER_DIR),
            text=True,
        )
        # Send initialize first
        init_msg = json.dumps({
            "jsonrpc": "2.0", "id": 1, "method": "initialize",
            "params": {"protocolVersion": "2025-06-18", "capabilities": {}, "clientInfo": {"name": "test", "version": "0.1.0"}},
        })
        tool_msg = json.dumps(message)
        stdout, stderr = proc.communicate(input=f"{init_msg}\n{tool_msg}\n", timeout=10)

        # Parse the response lines
        responses = []
        for line in stdout.strip().split("\n"):
            if line.strip():
                try:
                    responses.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

        # Return the second response (first is initialize, second is our tool call)
        if len(responses) >= 2:
            return responses[1]
        return responses[0] if responses else {}

    def test_tools_list(self):
        """tools/list returns a list of tools."""
        response = self._send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        self.assertIn("result", response)
        tools = response["result"].get("tools", [])
        self.assertGreater(len(tools), 5)

    def test_tools_list_contains_expected_tools(self):
        """tools/list contains search_civil_materials and other expected tools."""
        response = self._send({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        tools = response["result"].get("tools", [])
        tool_names = {t["name"] for t in tools}
        for expected in ["search_civil_materials", "fetch_paper_metadata", "list_academic_sources",
                         "suggest_search_queries", "lookup_mesh", "get_formatted_citation",
                         "convert_citation_records", "resolve_paper_ids"]:
            self.assertIn(expected, tool_names)

    def test_list_academic_sources(self):
        """list_academic_sources tool returns a list of sources."""
        response = self._send({
            "jsonrpc": "2.0", "id": 3, "method": "tools/call",
            "params": {"name": "list_academic_sources", "arguments": {}},
        })
        self.assertIn("result", response)
        content = response["result"].get("content", [])
        self.assertTrue(any("crossref" in str(c).lower() for c in content))


if __name__ == "__main__":
    unittest.main()

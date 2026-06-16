"""Regression tests for release architecture discovery and MCP entrypoints."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

from scripts.skill_manifest import discover_skill_names


REPO_ROOT = Path(__file__).resolve().parents[1]


class DynamicReleaseArchitectureTest(unittest.TestCase):
    def test_skill_discovery_reads_current_material_skill_directories(self):
        discovered = discover_skill_names(REPO_ROOT / "skills")
        actual = sorted(
            path.name
            for path in (REPO_ROOT / "skills").glob("materials-*")
            if path.is_dir() and (path / "manifest.yaml").exists()
        )

        self.assertEqual(actual, discovered)
        self.assertIn("materials-doe", discovered)

    def test_release_check_has_no_static_materials_skill_list(self):
        release_text = (REPO_ROOT / "scripts" / "run_release_checks.py").read_text(encoding="utf-8")

        self.assertNotIn("ALL_SKILLS = [", release_text)
        self.assertIn("discover_skill_names", release_text)

    def test_root_mcp_entrypoint_uses_shared_stdio_server_without_fastmcp_dependency(self):
        root_server = REPO_ROOT / "mcp-server" / "materials-academic-search" / "server.py"
        server_text = root_server.read_text(encoding="utf-8")
        docs_text = (REPO_ROOT / "mcp-server" / "materials-academic-search" / "README.md").read_text(
            encoding="utf-8"
        )

        self.assertNotIn("mcp.server.fastmcp", server_text)
        self.assertNotIn("FastMCP", docs_text)

        init = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "test", "version": "0.1.0"},
                },
            }
        )
        tools = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        result = subprocess.run(
            [sys.executable, str(root_server)],
            input=f"{init}\n{tools}\n",
            cwd=root_server.parent,
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        responses = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        self.assertEqual("materials-academic-search", responses[0]["result"]["serverInfo"]["name"])
        tool_names = {tool["name"] for tool in responses[1]["result"]["tools"]}
        self.assertIn("search_civil_materials", tool_names)

    def test_install_docs_and_mcp_config_use_same_mcp_server_location(self):
        install_text = (REPO_ROOT / "install.md").read_text(encoding="utf-8")
        release_notes = (REPO_ROOT / "RELEASE_NOTES.md").read_text(encoding="utf-8")
        mcp_config = json.loads((REPO_ROOT / ".mcp.json").read_text(encoding="utf-8"))
        args = mcp_config["mcpServers"]["materials-academic-search"]["args"]
        cwd = mcp_config["mcpServers"]["materials-academic-search"]["cwd"]

        self.assertIn("mcp-server/materials-academic-search", install_text.replace("\\", "/"))
        self.assertIn("mcp-server\\materials-academic-search\\requirements.txt", release_notes)
        self.assertIn("cwd = \"mcp-server/materials-academic-search\"", release_notes)
        self.assertEqual(["server.py"], args)
        self.assertEqual("mcp-server/materials-academic-search", cwd)

    def test_root_mcp_requirements_match_imported_runtime_dependencies(self):
        requirements = (
            REPO_ROOT / "mcp-server" / "materials-academic-search" / "requirements.txt"
        ).read_text(encoding="utf-8")
        docs_text = (REPO_ROOT / "install.md").read_text(encoding="utf-8")

        self.assertIn("httpx", requirements)
        self.assertNotIn("mcp>=", requirements)
        self.assertIn("mcp-server\\materials-academic-search\\requirements.txt", docs_text)

    def test_root_and_skill_mcp_tool_schemas_stay_in_lockstep(self):
        root_tools = self._list_mcp_tools(
            REPO_ROOT / "mcp-server" / "materials-academic-search" / "server.py"
        )
        skill_tools = self._list_mcp_tools(
            REPO_ROOT / "skills" / "materials-citation" / "mcp" / "academic_search" / "server.py",
        )

        self.assertEqual(skill_tools, root_tools)

    def _list_mcp_tools(self, server_path: Path) -> list[dict]:
        init = json.dumps(
            {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {"name": "test", "version": "0.1.0"},
                },
            }
        )
        tools = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        result = subprocess.run(
            [sys.executable, str(server_path)],
            input=f"{init}\n{tools}\n",
            cwd=server_path.parent,
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        responses = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        return responses[1]["result"]["tools"]


if __name__ == "__main__":
    unittest.main()

"""Regression tests for release architecture discovery and MCP entrypoints."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from scripts.skill_manifest import discover_skill_names


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "materials-skills"
SKILLS_ROOT = PLUGIN_ROOT / "skills"
MCP_SERVER = (
    SKILLS_ROOT / "materials-citation" / "mcp" / "academic_search" / "server.py"
)


class DynamicReleaseArchitectureTest(unittest.TestCase):
    def test_skill_discovery_reads_current_material_skill_directories(self):
        discovered = discover_skill_names(SKILLS_ROOT)
        discovered_by_default = discover_skill_names()
        actual = sorted(
            path.name
            for path in SKILLS_ROOT.glob("materials-*")
            if path.is_dir() and (path / "manifest.yaml").exists()
        )

        self.assertEqual(actual, discovered)
        self.assertEqual(actual, discovered_by_default)
        self.assertIn("materials-doe", discovered)

    def test_release_check_has_no_static_materials_skill_list(self):
        release_text = (REPO_ROOT / "scripts" / "run_release_checks.py").read_text(
            encoding="utf-8"
        )

        self.assertNotIn("ALL_SKILLS = [", release_text)
        self.assertIn("discover_skill_names", release_text)

    def test_plugin_package_exposes_plugin_descriptor(self):
        self.assertTrue((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").is_file())

    def test_generate_narrative_help_uses_plugin_default_output(self):
        script_text = (REPO_ROOT / "scripts" / "generate_narrative.py").read_text(
            encoding="utf-8"
        )

        self.assertIn(
            "skills/materials-writing/references/<id>-narrative.md",
            script_text,
        )
        self.assertNotIn(
            "plugins/materials-skills/skills/materials-writing/references/<id>-narrative.md",
            script_text,
        )

    def test_plugin_mcp_entrypoint_uses_shared_stdio_server_without_fastmcp_dependency(
        self,
    ):
        server_text = MCP_SERVER.read_text(encoding="utf-8")
        docs_text = (
            SKILLS_ROOT / "materials-citation" / "mcp" / "academic_search" / "README.md"
        ).read_text(encoding="utf-8")

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
            [sys.executable, str(MCP_SERVER)],
            input=f"{init}\n{tools}\n",
            cwd=MCP_SERVER.parent,
            capture_output=True,
            text=True,
            check=True,
            timeout=10,
        )
        responses = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        self.assertEqual("materials-academic-search", responses[0]["result"]["serverInfo"]["name"])
        tool_names = {tool["name"] for tool in responses[1]["result"]["tools"]}
        self.assertIn("search_materials", tool_names)

    def test_install_docs_use_repo_root_example_for_mcp_server_location(self):
        install_text = (REPO_ROOT / "install.md").read_text(encoding="utf-8")

        self.assertIn(
            "plugins/materials-skills/skills/materials-citation/mcp/academic_search",
            install_text.replace("\\", "/"),
        )
        self.assertIn('args = ["./skills/materials-citation/mcp/academic_search/server.py"]', install_text)
        self.assertIn('cwd = "plugins/materials-skills"', install_text)

    def test_plugin_mcp_config_resolves_inside_packaged_plugin_root(self):
        plugin_mcp_config = json.loads(
            (PLUGIN_ROOT / ".mcp.json").read_text(encoding="utf-8")
        )
        server = plugin_mcp_config["mcpServers"]["materials-academic-search"]
        cwd = server.get("cwd", ".")
        args = server["args"]
        resolved_cwd = (PLUGIN_ROOT / cwd).resolve()
        resolved_server = (resolved_cwd / args[0]).resolve()

        self.assertTrue(resolved_cwd.exists(), resolved_cwd)
        self.assertEqual(MCP_SERVER.resolve(), resolved_server)
        self.assertTrue(resolved_server.is_file(), resolved_server)

    def test_manual_install_preserves_manifest_shared_contract_paths(self):
        powershell = shutil.which("pwsh") or shutil.which("powershell")
        if powershell is None:
            self.skipTest("PowerShell is required to exercise install.ps1")

        with tempfile.TemporaryDirectory() as tmp:
            env = os.environ.copy()
            env["CODEX_HOME"] = tmp
            subprocess.run(
                [powershell, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", str(REPO_ROOT / "scripts" / "install.ps1")],
                cwd=REPO_ROOT,
                env=env,
                capture_output=True,
                text=True,
                check=True,
                timeout=60,
            )
            installed_skill = Path(tmp) / "skills" / "materials-data"
            contract = (installed_skill / ".." / ".." / "_shared" / "contracts" / "data-package.yaml").resolve()

            self.assertTrue((Path(tmp) / "skills" / "_shared").is_dir())
            self.assertTrue((Path(tmp) / "_shared").is_dir())
            self.assertTrue(contract.is_file(), contract)

    def test_plugin_mcp_requirements_match_imported_runtime_dependencies(self):
        requirements = (
            SKILLS_ROOT
            / "materials-citation"
            / "mcp"
            / "academic_search"
            / "requirements.txt"
        ).read_text(encoding="utf-8")
        docs_text = (REPO_ROOT / "install.md").read_text(encoding="utf-8")

        self.assertIn("httpx", requirements)
        self.assertNotIn("mcp>=", requirements)
        self.assertIn(
            "plugins\\materials-skills\\skills\\materials-citation\\mcp\\academic_search\\requirements.txt",
            docs_text,
        )
        self.assertIn('cwd = "plugins/materials-skills"', docs_text)


if __name__ == "__main__":
    unittest.main()

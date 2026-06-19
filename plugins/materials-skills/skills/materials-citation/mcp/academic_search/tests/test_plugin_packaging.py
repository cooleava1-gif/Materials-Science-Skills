import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

import yaml


TEST_ROOT = Path(__file__).resolve()
PLUGIN_ROOT = TEST_ROOT.parents[5]
SKILLS_ROOT = PLUGIN_ROOT / "skills"


class PluginPackagingTest(unittest.TestCase):
    def test_plugin_mcp_config_resolves_inside_packaged_plugin_root(self):
        config = json.loads((PLUGIN_ROOT / ".mcp.json").read_text(encoding="utf-8"))
        server = config["mcpServers"]["materials-academic-search"]

        server_cwd = (PLUGIN_ROOT / server.get("cwd", ".")).resolve()
        server_script = (server_cwd / server["args"][0]).resolve()

        self.assertTrue(server_cwd.exists(), f"MCP cwd should exist inside plugin package: {server_cwd}")
        self.assertTrue(server_script.exists(), f"MCP server script should resolve from cwd: {server_script}")

    def test_skill_manifests_reference_release_checks_that_exist_inside_plugin(self):
        for manifest_path in sorted(SKILLS_ROOT.glob("materials-*/manifest.yaml")):
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
            release_checks = manifest.get("release_checks", []) or []

            with self.subTest(skill=manifest_path.parent.name):
                self.assertTrue(release_checks, "release_checks should not be empty")
                for command in release_checks:
                    text = str(command)
                    if "run_release_checks.py" in text:
                        self.assertTrue(
                            (PLUGIN_ROOT / "scripts" / "run_release_checks.py").exists(),
                            "plugin package should ship scripts/run_release_checks.py",
                        )
                    if "check_skill_architecture.py" in text:
                        self.assertTrue(
                            (PLUGIN_ROOT / "scripts" / "check_skill_architecture.py").exists(),
                            "plugin package should ship scripts/check_skill_architecture.py",
                        )

    def test_skill_readmes_bundle_verification_points_to_existing_plugin_script(self):
        required = PLUGIN_ROOT / "scripts" / "run_release_checks.py"
        self.assertTrue(required.exists(), "plugin package should ship scripts/run_release_checks.py")

        for readme_path in sorted(SKILLS_ROOT.glob("materials-*/README.md")):
            text = readme_path.read_text(encoding="utf-8")
            with self.subTest(skill=readme_path.parent.name):
                self.assertIn("run_release_checks.py --json", text)

    def test_plugin_release_checks_entrypoint_runs_from_plugin_root(self):
        env = os.environ.copy()
        env["MATERIALS_SKIP_MCP_TESTS"] = "1"
        result = subprocess.run(
            [sys.executable, "scripts/run_release_checks.py", "--json"],
            cwd=PLUGIN_ROOT,
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=20,
        )

        output = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
        self.assertEqual(result.returncode, 0, output)
        report = json.loads(result.stdout)
        self.assertEqual(report.get("status"), "pass", output)


if __name__ == "__main__":
    unittest.main()

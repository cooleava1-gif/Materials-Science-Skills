import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = SKILL_ROOT / "scripts"
MCP_TESTS_ROOT = SKILL_ROOT / "mcp" / "academic_search" / "tests"


def load_build_module():
    spec = importlib.util.spec_from_file_location("build_citation_matrix", SCRIPTS_ROOT / "build_citation_matrix.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load build_citation_matrix.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CitationSkillStructureTest(unittest.TestCase):
    def test_skill_core_files_exist(self):
        required = [
            "SKILL.md",
            "manifest.yaml",
            "README.md",
            "agents/openai.yaml",
            "static/core/contract.md",
            "static/core/citation-contract.md",
            "static/core/workflow.md",
        ]
        for relative in required:
            self.assertTrue((SKILL_ROOT / relative).exists(), f"{relative} should exist")

    def test_skill_entrypoint_manifest_and_agent_exist(self):
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Use when", skill_text)
        self.assertIn("citation", skill_text.lower())

        manifest_text = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")
        self.assertIn("axes", manifest_text)
        self.assertIn("citation-map", manifest_text)

    def test_templates_include_required_fields(self):
        csv_template = (SKILL_ROOT / "assets/templates/citation-matrix-template.csv").read_text(encoding="utf-8")
        search_template = (SKILL_ROOT / "assets/templates/search-plan-template.md").read_text(encoding="utf-8")

        for field in ["claim_id", "evidence_layer", "source_role", "reviewer_risk", "search_query"]:
            self.assertIn(field, csv_template)
        self.assertIn("Search Plan", search_template)

    def test_research_router_lists_citation_companion_skill(self):
        research_manifest = SKILL_ROOT.parent / "materials-research" / "manifest.yaml"
        if research_manifest.exists():
            text = research_manifest.read_text(encoding="utf-8")
            self.assertIn("materials-citation", text)

    def test_mcp_tests_exist(self):
        self.assertTrue(MCP_TESTS_ROOT.exists(), "mcp/academic_search/tests should exist")
        test_files = list(MCP_TESTS_ROOT.glob("test_*.py"))
        self.assertGreaterEqual(len(test_files), 10, "Should have at least 10 MCP test files")


class CitationScriptTest(unittest.TestCase):
    def test_build_citation_matrix_creates_csv(self):
        script = SCRIPTS_ROOT / "build_citation_matrix.py"
        self.assertTrue(script.exists(), "build_citation_matrix.py should exist")

        with tempfile.TemporaryDirectory() as tmp:
            output_file = str(Path(tmp) / "test-matrix.csv")
            result = subprocess.run(
                [sys.executable, str(script), "--topic", "waterborne epoxy emulsified asphalt", "--output", output_file],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertTrue(Path(output_file).exists(), "CSV output should be created")
            content = Path(output_file).read_text(encoding="utf-8-sig")
            self.assertIn("claim_id", content)
            self.assertIn("evidence_layer", content)

    def test_build_citation_matrix_module_exposes_expected_functions(self):
        module = load_build_module()
        for name in ["DEFAULT_CLAIMS", "CSV_FIELDS", "split_items"]:
            self.assertTrue(hasattr(module, name), f"{name} should be exposed")


if __name__ == "__main__":
    unittest.main()

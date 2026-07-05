import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path



def _find_repo_root():
    p = Path(__file__).resolve()
    for parent in [p] + list(p.parents):
        if (parent / ".git").exists() or (parent / "AGENTS.md").exists():
            return parent
    return p.parents[3]
SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = _find_repo_root()


class FigureHardWorkflowStructureTest(unittest.TestCase):
    def test_router_manifest_and_core_define_python_only_backend(self):
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        manifest_text = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")
        contract_text = (SKILL_ROOT / "static" / "core" / "figure-contract.md").read_text(encoding="utf-8")
        stance_text = (SKILL_ROOT / "static" / "core" / "stance.md").read_text(encoding="utf-8")
        workflow_text = (SKILL_ROOT / "static" / "core" / "workflow.md").read_text(encoding="utf-8")

        for phrase in [
            "Python backend",
            "figure contract",
        ]:
            self.assertIn(phrase, skill_text)
        for forbidden in ["Python or R?", "static/fragments/backend/r.md", "plot.R", "ggplot2"]:
            self.assertNotIn(forbidden, skill_text + manifest_text + contract_text + workflow_text)

        for phrase in [
            "backend:",
            "static/fragments/backend/python.md",
            "references/figure-package-protocol.md",
            "references/figure-qa-contract.md",
        ]:
            self.assertIn(phrase, manifest_text)

        for phrase in [
            "Core conclusion",
            "Evidence chain",
            "Archetype",
            "Python backend",
            "Journal/export contract",
            "WER-EA boundary",
        ]:
            self.assertIn(phrase, contract_text)

        for phrase in [
            "figure's role",
            "claim",
            "Reviewer-safe",
            "source data",
        ]:
            self.assertIn(phrase, stance_text)

        for phrase in [
            "Use the Python backend",
            "Build and validate the figure contract",
            "Create the figure package",
            "Run visual QA",
            "Return the package",
        ]:
            self.assertIn(phrase, workflow_text)

    def test_python_backend_fragment_and_package_templates_exist(self):
        expected_files = [
            "README.md",
            "evals/evals.json",
            "static/fragments/backend/python.md",
            "references/figure-package-protocol.md",
            "assets/templates/figure-contract-template.md",
            "assets/templates/figure-package/figure_contract.md",
            "assets/templates/figure-package/caption.md",
            "assets/templates/figure-package/qa_report.md",
            "assets/templates/figure-package/asset_manifest.md",
            "assets/templates/figure-package/source_data.csv",
            "scripts/audit_figure_package.py",
        ]
        for relative in expected_files:
            self.assertTrue((SKILL_ROOT / relative).exists(), f"{relative} should exist")
        removed_files = [
            "static/fragments/backend/r.md",
            "references/r-workflow.md",
            "references/r-template-index.md",
            "scripts/r/palettes.R",
            "scripts/r/theme_materials.R",
        ]
        for relative in removed_files:
            self.assertFalse((SKILL_ROOT / relative).exists(), f"{relative} should be removed from Python-only figure skill")

        python_text = (SKILL_ROOT / "static" / "fragments" / "backend" / "python.md").read_text(encoding="utf-8")
        protocol_text = (SKILL_ROOT / "references" / "figure-package-protocol.md").read_text(encoding="utf-8")

        for phrase in ["matplotlib", "seaborn", "SVG", "PDF", "TIFF", "Python"]:
            self.assertIn(phrase, python_text)
        self.assertIn("figure.png", protocol_text)
        for phrase in [
            "figure_contract.md",
            "source_data.csv",
            "figure.svg",
            "figure.pdf",
            "figure.png",
            "figure.tiff",
            "caption.md",
            "qa_report.md",
            "asset_manifest.md",
        ]:
            self.assertIn(phrase, protocol_text)
        self.assertNotIn("plot.R", protocol_text)


class FigurePackageAuditScriptTest(unittest.TestCase):
    def test_audit_fails_minimal_incomplete_package(self):
        script = SKILL_ROOT / "scripts" / "audit_figure_package.py"
        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp) / "bad-package"
            package.mkdir()
            result = subprocess.run(
                [sys.executable, str(script), "--package-dir", str(package), "--json"],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "incomplete")
        self.assertTrue(payload["issues"])

    def test_bundled_storyboard_packages_keep_current_boundary_files(self):
        sample_root = SKILL_ROOT / "examples" / "figure-packages"
        expected = {
            "wer-ea-full",
            "thermal-insulation-partial-to-full",
            "polymer-composites-partial-to-full",
        }
        actual = {path.name for path in sample_root.iterdir() if path.is_dir()}
        self.assertTrue(expected.issubset(actual), f"Missing expected packages: {expected - actual}")

        for name in sorted(expected):
            package = sample_root / name
            with self.subTest(package=name):
                for fname in ["README.md", "figure_storyboard.yaml", "caption_boundary.md", "figure_qa_report.md"]:
                    self.assertTrue((package / fname).exists(), f"{name}/{fname} should exist")

    def test_default_audit_still_requires_production_exports(self):
        script = SKILL_ROOT / "scripts" / "audit_figure_package.py"
        package = SKILL_ROOT / "examples" / "figure-packages" / "wer-ea-full"
        result = subprocess.run(
            [sys.executable, str(script), "--package-dir", str(package), "--json"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertNotEqual(result.returncode, 0)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "incomplete")
        self.assertEqual(payload["mode"], "production")
        self.assertIn("missing figure.svg", payload["issues"])
        self.assertIn("missing figure.tiff", payload["issues"])

    def test_release_check_tracks_figure_hard_workflow(self):
        release_text = (
            REPO_ROOT / "plugins" / "materials-skills" / "scripts" / "run_release_checks.py"
        ).read_text(encoding="utf-8")
        for phrase in [
            "figure_hard_workflow",
            "FIGURE_HARD_WORKFLOW_FILES",
            "FIGURE_CURRENT_ASSET_FILES",
            "audit_figure_package.py",
            "assets/showcase-proof/showcase_manifest.json",
            "assets/materials4papers/README.md",
        ]:
            self.assertIn(phrase, release_text)

    def test_readme_and_evals_document_nature_style_hard_edges(self):
        readme_text = (SKILL_ROOT / "README.md").read_text(encoding="utf-8")
        evals_path = SKILL_ROOT / "evals" / "evals.json"
        evals = json.loads(evals_path.read_text(encoding="utf-8"))

        for phrase in [
            "Python backend",
            "contract",
            "Figure package structure",
            "WER-EA",
        ]:
            self.assertIn(phrase, readme_text)

        self.assertEqual("materials-figure", evals["skill_name"])
        ids = {case["id"] for case in evals["evals"]}
        self.assertGreaterEqual(
            ids,
            {
                "pre-render-contract-gate",
                "package_completeness_check",
                "caption_boundary_overclaim",
                "storyboard_dag_validation",
            },
        )
        eval_text = json.dumps(evals, ensure_ascii=False)
        self.assertIn("Python", eval_text)
        self.assertNotIn("Python or R", eval_text)
        self.assertIn("figure package", eval_text)


if __name__ == "__main__":
    unittest.main()

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parents[1]


class FigureHardWorkflowStructureTest(unittest.TestCase):
    def test_router_manifest_and_core_define_backend_gate(self):
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        manifest_text = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")
        contract_text = (SKILL_ROOT / "static" / "core" / "figure-contract.md").read_text(encoding="utf-8")
        stance_text = (SKILL_ROOT / "static" / "core" / "stance.md").read_text(encoding="utf-8")
        workflow_text = (SKILL_ROOT / "static" / "core" / "workflow.md").read_text(encoding="utf-8")

        for phrase in [
            "backend gate",
            "Python or R?",
            "Do not default",
            "selected backend is exclusive",
            "figure package",
        ]:
            self.assertIn(phrase, skill_text)

        for phrase in [
            "backend:",
            "static/fragments/backend/python.md",
            "static/fragments/backend/r.md",
            "references/backend-selection.md",
            "references/figure-package-protocol.md",
            "references/figure-qa-contract.md",
        ]:
            self.assertIn(phrase, manifest_text)

        for phrase in [
            "Core conclusion",
            "Evidence chain",
            "Archetype",
            "Backend",
            "Journal/export contract",
            "WER-EA boundary",
        ]:
            self.assertIn(phrase, contract_text)

        for phrase in [
            "visual argument",
            "claim boundary",
            "reviewer-safe",
            "source data",
        ]:
            self.assertIn(phrase, stance_text)

        for phrase in [
            "Resolve the backend",
            "Build the figure contract",
            "Create the figure package",
            "Run visual QA",
            "Return the package",
        ]:
            self.assertIn(phrase, workflow_text)

    def test_backend_fragments_and_package_templates_exist(self):
        expected_files = [
            "README.md",
            "evals/evals.json",
            "static/fragments/backend/python.md",
            "static/fragments/backend/r.md",
            "references/backend-selection.md",
            "references/figure-package-protocol.md",
            "assets/templates/figure-contract-template.md",
            "assets/templates/figure-package/figure_contract.md",
            "assets/templates/figure-package/caption.md",
            "assets/templates/figure-package/qa_report.md",
            "assets/templates/figure-package/asset_manifest.md",
            "assets/templates/figure-package/source_data.csv",
            "assets/templates/figure-package/plot.py",
            "scripts/audit_figure_package.py",
        ]
        for relative in expected_files:
            self.assertTrue((SKILL_ROOT / relative).exists(), f"{relative} should exist")

        python_text = (SKILL_ROOT / "static" / "fragments" / "backend" / "python.md").read_text(encoding="utf-8")
        r_text = (SKILL_ROOT / "static" / "fragments" / "backend" / "r.md").read_text(encoding="utf-8")
        protocol_text = (SKILL_ROOT / "references" / "figure-package-protocol.md").read_text(encoding="utf-8")

        for phrase in ["matplotlib", "seaborn", "SVG", "PDF", "TIFF", "PNG", "same backend"]:
            self.assertIn(phrase, python_text)
        for phrase in ["ggplot2", "patchwork", "ComplexHeatmap", "SVG", "PDF", "TIFF", "same backend"]:
            self.assertIn(phrase, r_text)
        for phrase in [
            "figure_contract.md",
            "source_data.csv",
            "plot.py",
            "figure.svg",
            "figure.pdf",
            "figure.png",
            "figure.tiff",
            "caption.md",
            "qa_report.md",
            "asset_manifest.md",
        ]:
            self.assertIn(phrase, protocol_text)


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

    def test_audit_passes_bundled_wer_ea_packages(self):
        script = SKILL_ROOT / "scripts" / "audit_figure_package.py"
        sample_root = SKILL_ROOT / "examples" / "figure-packages"
        expected = {
            "wer-ea-mechanism-map",
            "wer-ea-evidence-heatmap",
            "wer-ea-dosage-window",
        }
        self.assertEqual(expected, {path.name for path in sample_root.iterdir() if path.is_dir()})

        for package in sorted(sample_root.iterdir()):
            if not package.is_dir():
                continue
            with self.subTest(package=package.name):
                result = subprocess.run(
                    [sys.executable, str(script), "--package-dir", str(package), "--json"],
                    check=True,
                    capture_output=True,
                    text=True,
                )
                payload = json.loads(result.stdout)
                self.assertEqual(payload["status"], "pass")
                self.assertGreaterEqual(payload["checked_files"], 10)

    def test_release_check_tracks_figure_hard_workflow(self):
        release_text = (REPO_ROOT / "scripts" / "run_release_checks.py").read_text(encoding="utf-8")
        for phrase in [
            "figure_hard_workflow",
            "FIGURE_HARD_WORKFLOW_FILES",
            "FIGURE_HARD_WORKFLOW_EVAL_IDS",
            "FIGURE_PACKAGE_SAMPLE_NAMES",
            "audit_figure_package.py",
        ]:
            self.assertIn(phrase, release_text)

    def test_readme_and_evals_document_nature_style_hard_edges(self):
        readme_text = (SKILL_ROOT / "README.md").read_text(encoding="utf-8")
        evals_path = SKILL_ROOT / "evals" / "evals.json"
        evals = json.loads(evals_path.read_text(encoding="utf-8"))

        for phrase in [
            "Nature-style",
            "Python or R?",
            "Backend and contract rules",
            "Figure package structure",
            "WER-EA",
            "Reproduction checklist",
        ]:
            self.assertIn(phrase, readme_text)

        self.assertEqual("civil-materials-figure", evals["skill_name"])
        ids = {case["id"] for case in evals["evals"]}
        self.assertEqual(
            {
                "backend-exclusivity-r-missing-runtime",
                "backend-exclusivity-python-missing-package",
                "journal-ready-package-audit",
            },
            ids,
        )
        for case in evals["evals"]:
            text = json.dumps(case, ensure_ascii=False)
            self.assertIn("Python or R", text)
            self.assertIn("figure package", text)


if __name__ == "__main__":
    unittest.main()

import json
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
AUDIT_SCRIPT = SKILL_ROOT / "scripts" / "audit_fair_dataset.py"


def load_audit_module():
    spec = importlib.util.spec_from_file_location("audit_fair_dataset", AUDIT_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load audit_fair_dataset.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CivilMaterialsDataSkillStructureTest(unittest.TestCase):
    def test_skill_core_files_exist_and_describe_data_fair_work(self):
        required = [
            "SKILL.md",
            "manifest.yaml",
            "static/core/data-contract.md",
            "static/core/workflow.md",
            "references/fair-checklist.md",
            "references/dataset-package.md",
            "references/asphalt-data-schema.md",
            "references/cement-concrete-data-schema.md",
            "references/data-availability-statements.md",
            "assets/templates/metadata-template.md",
            "assets/templates/dataset-readme-template.md",
            "assets/templates/data-availability-template.md",
            "assets/templates/experiment-data-template.csv",
            "examples/waterborne-epoxy-fair-package.md",
        ]
        for relative in required:
            self.assertTrue((SKILL_ROOT / relative).exists(), f"{relative} should exist")

        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Use when", skill_text)
        self.assertIn("FAIR", skill_text)
        self.assertIn("waterborne epoxy", skill_text)

    def test_templates_include_civil_materials_metadata_fields(self):
        metadata = (SKILL_ROOT / "assets/templates/metadata-template.md").read_text(encoding="utf-8")
        data_csv = (SKILL_ROOT / "assets/templates/experiment-data-template.csv").read_text(encoding="utf-8")
        statement = (SKILL_ROOT / "assets/templates/data-availability-template.md").read_text(encoding="utf-8")

        for field in [
            "asphalt_type",
            "emulsifier_type",
            "epoxy_dosage",
            "curing_condition",
            "test_standard",
            "temperature",
            "humidity",
            "aging_condition",
            "replicate_count",
        ]:
            self.assertIn(field, metadata + data_csv)
        self.assertIn("Data Availability Statement", statement)

    def test_domain_schemas_include_units_ranges_and_sanity_checks(self):
        asphalt_schema = (SKILL_ROOT / "references" / "asphalt-data-schema.md").read_text(encoding="utf-8")
        concrete_schema = (SKILL_ROOT / "references" / "cement-concrete-data-schema.md").read_text(encoding="utf-8")

        for phrase in ["Type", "Unit or format", "Typical/allowed values", "Sanity check", "epoxy_dosage", "curing_condition"]:
            self.assertIn(phrase, asphalt_schema)
        for phrase in ["Type", "Unit or format", "Typical/allowed values", "Sanity check", "binder_type", "allowed_values"]:
            self.assertIn(phrase, concrete_schema)

    def test_generated_waterborne_epoxy_example_package_exists(self):
        package_dir = (
            SKILL_ROOT
            / "examples"
            / "generated"
            / "waterborne_epoxy_modified_emulsified_asphalt_bonding_performance_cbm_fair_package"
        )
        self.assertTrue(package_dir.exists())
        self.assertTrue((package_dir / "metadata.md").exists())
        self.assertTrue((package_dir / "raw_data" / "experiment_data_template.csv").exists())


class CivilMaterialsDataScriptsTest(unittest.TestCase):
    def test_build_fair_package_creates_submission_ready_structure(self):
        script = SKILL_ROOT / "scripts" / "build_fair_package.py"
        self.assertTrue(script.exists(), "build_fair_package.py should exist")

        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--topic",
                    "waterborne epoxy modified emulsified asphalt bonding performance",
                    "--domain",
                    "asphalt",
                    "--journal",
                    "CBM",
                    "--output-dir",
                    tmp,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            package_dir = Path(result.stdout.strip())
            self.assertTrue(package_dir.exists())
            for relative in [
                "raw_data",
                "processed_data",
                "figures",
                "metadata.md",
                "README.md",
                "data_availability_statement.md",
                "fair_audit.md",
                "raw_data/experiment_data_template.csv",
            ]:
                self.assertTrue((package_dir / relative).exists(), f"{relative} should exist")
            readme = (package_dir / "README.md").read_text(encoding="utf-8")
            self.assertIn("waterborne epoxy modified emulsified asphalt", readme)
            self.assertIn("CBM", readme)

    def test_audit_fair_dataset_reports_missing_items_and_passes_generated_package(self):
        build_script = SKILL_ROOT / "scripts" / "build_fair_package.py"
        audit_script = SKILL_ROOT / "scripts" / "audit_fair_dataset.py"
        self.assertTrue(audit_script.exists(), "audit_fair_dataset.py should exist")

        with tempfile.TemporaryDirectory() as tmp:
            empty_result = subprocess.run(
                [sys.executable, str(audit_script), "--dataset-dir", tmp, "--json"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(empty_result.returncode, 1)
            empty_report = json.loads(empty_result.stdout)
            self.assertEqual(empty_report["status"], "incomplete")
            self.assertIn("metadata.md", empty_report["missing"])

        with tempfile.TemporaryDirectory() as tmp:
            package_result = subprocess.run(
                [
                    sys.executable,
                    str(build_script),
                    "--topic",
                    "waterborne epoxy modified emulsified asphalt bonding performance",
                    "--domain",
                    "asphalt",
                    "--journal",
                    "RMPD",
                    "--output-dir",
                    tmp,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            package_dir = Path(package_result.stdout.strip())
            audit_result = subprocess.run(
                [sys.executable, str(audit_script), "--dataset-dir", str(package_dir), "--json"],
                check=True,
                capture_output=True,
                text=True,
            )
            report = json.loads(audit_result.stdout)
            self.assertEqual(report["status"], "pass")
            for fair_key in ["findable", "accessible", "interoperable", "reusable"]:
                self.assertIn(fair_key, report["fair"])

    def test_audit_fair_dataset_validates_csv_headers_not_comment_text(self):
        audit_script = SKILL_ROOT / "scripts" / "audit_fair_dataset.py"

        with tempfile.TemporaryDirectory() as tmp:
            package_dir = Path(tmp)
            for relative in ["raw_data", "processed_data", "figures"]:
                (package_dir / relative).mkdir()
            (package_dir / "metadata.md").write_text(
                "\n".join(
                    [
                        "test_standard: JTG E20",
                        "replicate_count: 3",
                        "temperature: 25 C",
                        "humidity: 50%",
                        "curing_condition: 7 d",
                        "aging_condition: moisture aging",
                    ]
                ),
                encoding="utf-8",
            )
            (package_dir / "README.md").write_text("Dataset README", encoding="utf-8")
            (package_dir / "data_availability_statement.md").write_text("Available on request.", encoding="utf-8")
            (package_dir / "raw_data" / "experiment.csv").write_text(
                "comment,value\nthis note mentions sample_id and unit,1\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(audit_script), "--dataset-dir", str(package_dir), "--json"],
                check=False,
                capture_output=True,
                text=True,
            )
            report = json.loads(result.stdout)

            self.assertEqual(result.returncode, 1)
            self.assertFalse(report["fair"]["interoperable"])

    def test_audit_fair_dataset_reports_missing_dataset_dir_to_stderr(self):
        missing_dir = Path(tempfile.gettempdir()) / "civil_materials_missing_dataset_dir_for_test"
        result = subprocess.run(
            [sys.executable, str(AUDIT_SCRIPT), "--dataset-dir", str(missing_dir), "--json"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertIn("directory not found", result.stderr)
        self.assertIn(str(missing_dir), result.stderr)

    def test_render_markdown_uses_explicit_type_validation(self):
        audit_module = load_audit_module()

        with self.assertRaises(TypeError):
            audit_module.render_markdown(
                {
                    "status": "incomplete",
                    "dataset_dir": "example",
                    "fair": [],
                    "missing": [],
                    "actions": [],
                }
            )


class CivilMaterialsDataRouterIntegrationTest(unittest.TestCase):
    def test_research_router_lists_data_fair_companion_skill(self):
        research_root = SKILL_ROOT.parent / "civil-materials-research"
        skill_text = (research_root / "SKILL.md").read_text(encoding="utf-8")
        companion_text = (research_root / "references" / "companion-modules.md").read_text(encoding="utf-8")
        manifest_text = (research_root / "manifest.yaml").read_text(encoding="utf-8")

        self.assertIn("civil-materials-data", skill_text)
        self.assertIn("civil-materials-data", companion_text)
        self.assertIn("data: civil-materials-data", manifest_text)


if __name__ == "__main__":
    unittest.main()

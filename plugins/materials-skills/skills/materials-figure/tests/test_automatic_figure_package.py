import importlib.util
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = SKILL_ROOT / "scripts"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class AutomaticFigurePackageTest(unittest.TestCase):
    def test_current_contract_points_to_shipped_figure_tools(self):
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        manifest_text = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")
        workflow_text = (SKILL_ROOT / "static" / "core" / "workflow.md").read_text(encoding="utf-8")
        readme_text = (SKILL_ROOT / "README.md").read_text(encoding="utf-8")
        reference_text = (SKILL_ROOT / "references" / "automatic-figure-package.md").read_text(encoding="utf-8")

        for relative in [
            "scripts/audit_figure_package.py",
            "scripts/compose_multipanel_figure.py",
            "scripts/data_package_to_figure_handoff.py",
            "scripts/validate_materials_claims.py",
            "assets/templates/figure_storyboard.yaml",
            "assets/templates/figure-contract-template.md",
        ]:
            self.assertTrue((SKILL_ROOT / relative).exists(), f"{relative} should be shipped")

        combined = skill_text + manifest_text + workflow_text + readme_text + reference_text
        for phrase in [
            "Python backend",
            "figure_contract.md",
            "qa_report.md",
            "references/automatic-figure-package.md",
        ]:
            self.assertIn(phrase, combined)
        for removed_script in [
            "scripts/data_diagnose.py",
            "scripts/recommend_chart.py",
            "scripts/generate_figure_package.py",
        ]:
            self.assertNotIn(removed_script, manifest_text)
            self.assertFalse((SKILL_ROOT / removed_script).exists())

    def test_validate_materials_claims_prefers_property_units_over_temperature_values(self):
        validator = load_module("validate_materials_claims", SCRIPTS_ROOT / "validate_materials_claims.py")

        claims = validator.extract_performance_claims(
            "Al2O3 flexural strength at 25 C was 350 MPa."
        )

        self.assertEqual(len(claims), 1)
        self.assertEqual(claims[0]["property"], "flexural_strength")
        self.assertEqual(claims[0]["value"], 350.0)
        self.assertEqual(claims[0]["unit"], "MPa")

    def test_validate_materials_claims_normalizes_equivalent_units(self):
        validator = load_module("validate_materials_claims", SCRIPTS_ROOT / "validate_materials_claims.py")
        kb = validator.load_kb(validator.KB_PATH)

        result = validator.validate_contract(
            "Al2O3 elastic modulus was 380000 MPa.",
            kb,
        )

        self.assertEqual(result["status"], "pass")
        self.assertEqual(result["checks"][0]["result"], "confirmed")


if __name__ == "__main__":
    unittest.main()

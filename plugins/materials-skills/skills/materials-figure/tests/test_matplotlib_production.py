import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = SKILL_ROOT / "scripts"
MATERIALS4PAPERS = SKILL_ROOT / "assets" / "materials4papers"


class MatplotlibProductionContractTest(unittest.TestCase):
    def test_current_python_backend_tools_are_shipped(self):
        for relative in [
            "compose_multipanel_figure.py",
            "audit_figure_package.py",
            "validate_materials_claims.py",
            "check_storyboard.py",
            "data_package_to_figure_handoff.py",
        ]:
            self.assertTrue((SCRIPTS_ROOT / relative).exists(), f"{relative} should exist")

    def test_legacy_materials_plot_lib_contract_is_not_shipped(self):
        chart_atlas = (SKILL_ROOT / "references" / "chart-atlas.md").read_text(encoding="utf-8")
        tutorials = (SKILL_ROOT / "references" / "tutorials.md").read_text(encoding="utf-8")

        self.assertFalse((SCRIPTS_ROOT / "materials_plot_lib.py").exists())
        self.assertIn("materials_plot_lib was removed", chart_atlas)
        self.assertIn("kept as reference examples", tutorials)

    def test_materials4papers_plot_scripts_are_python_matplotlib_sources(self):
        plot_scripts = sorted(MATERIALS4PAPERS.glob("*/plot.py"))
        self.assertGreaterEqual(len(plot_scripts), 15)
        for script in plot_scripts:
            with self.subTest(script=script.parent.name):
                text = script.read_text(encoding="utf-8")
                self.assertIn("matplotlib", text.lower())


if __name__ == "__main__":
    unittest.main()

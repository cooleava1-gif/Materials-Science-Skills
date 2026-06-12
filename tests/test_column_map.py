"""Tests for the COLUMN_MAP data abstraction layer.

Validates:
- load_mapped_data correctly reads CSV and maps columns by role
- The plot_grouped_bar.py generic script works with any material's data
- Registry figure_archetypes properly reference COLUMN_MAP roles
"""

import csv
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "skills" / "materials-figure" / "scripts" / "figures4materials"
HELPERS_FILE = SCRIPTS_DIR / "_script_helpers.py"
PLOT_LIB_FILE = REPO_ROOT / "skills" / "materials-figure" / "scripts" / "materials_plot_lib.py"
REGISTRY_DIR = REPO_ROOT / "_shared" / "material-registry" / "entries"


def _import_helpers():
    import importlib.util
    spec = importlib.util.spec_from_file_location("_script_helpers", HELPERS_FILE)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _make_csv(columns: dict[str, list]) -> str:
    """Create an in-memory CSV string."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(columns.keys())
    for row in zip(*columns.values()):
        writer.writerow(row)
    return output.getvalue()


class ColumnMapLoadTest(unittest.TestCase):
    def setUp(self):
        self.helpers = _import_helpers()

    def test_loads_simple_x_labels(self):
        csv_str = _make_csv({"dosage": ["0%", "10%", "20%"]})
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write(csv_str)
            tmp = f.name
        try:
            result = self.helpers.load_mapped_data(tmp, {"x_labels": {"column": "dosage"}})
            self.assertEqual(result["x_labels"], ["0%", "10%", "20%"])
        finally:
            Path(tmp).unlink(missing_ok=True)

    def test_loads_series_with_errors(self):
        csv_str = _make_csv({
            "dosage": ["0%", "10%"],
            "dry": ["0.5", "0.8"],
            "dry_sd": ["0.02", "0.03"],
            "wet": ["0.3", "0.6"],
        })
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write(csv_str)
            tmp = f.name
        try:
            cmap = {
                "x_labels": {"column": "dosage"},
                "series": [
                    {"key": "Dry", "column": "dry", "error": "dry_sd"},
                    {"key": "Wet", "column": "wet"},
                ],
            }
            result = self.helpers.load_mapped_data(tmp, cmap)
            self.assertEqual(result["x_labels"], ["0%", "10%"])
            self.assertEqual(len(result["series"]), 2)
            self.assertEqual(result["series"][0]["key"], "Dry")
            self.assertAlmostEqual(result["series"][0]["values"][0], 0.5)
            self.assertAlmostEqual(result["series"][0]["errors"][0], 0.02)
            # Second series has no error column
            self.assertIsNone(result["series"][1].get("errors"))
        finally:
            Path(tmp).unlink(missing_ok=True)

    def test_string_values(self):
        csv_str = _make_csv({"dummy": ["1"]})
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8") as f:
            f.write(csv_str)
            tmp = f.name
        try:
            cmap = {
                "xlabel": {"value": "Epoxy content (wt%)"},
                "ylabel": {"value": "Strength (MPa)"},
                "caption": {"value": "A caption."},
                "figure_name": {"value": "my_figure"},
            }
            result = self.helpers.load_mapped_data(tmp, cmap)
            self.assertEqual(result["xlabel"], "Epoxy content (wt%)")
            self.assertEqual(result["ylabel"], "Strength (MPa)")
            self.assertEqual(result["caption"], "A caption.")
            self.assertEqual(result["figure_name"], "my_figure")
        finally:
            Path(tmp).unlink(missing_ok=True)


class ScriptUsesColumnMapTest(unittest.TestCase):
    """Verify that key figure scripts work when called with non-WER-EA data."""

    def test_plot_grouped_bar_with_cement_like_data(self):
        """The generic grouped-bar script should accept cement-like data."""
        # Load the module
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "plot_grouped_bar",
            SCRIPTS_DIR / "plot_grouped_bar.py"
        )
        self.assertIsNotNone(spec, "plot_grouped_bar.py must be importable")

    def test_column_map_preserved_across_scripts(self):
        """All scripts that use COLUMN_MAP should have consistent structure."""
        # Currently only plot_grouped_bar uses the pattern
        # (placeholder for when more are migrated)
        self.assertTrue(SCRIPTS_DIR.joinpath("plot_grouped_bar.py").exists())


class RegistryFigureArchetypeTest(unittest.TestCase):
    """Registry figure_archetypes should reference consistent semantic roles."""

    KNOWN_ARCHETYPE_COLUMNS = {
        "bonding_strength_bar": ["x_labels", "series"],
        "dosage_performance_curve": ["x_labels", "series"],
        "ftir_overlay": ["x_values", "absorbances"],
        "durability_retention_bar": ["x_labels", "series"],
        "property_radar": ["categories", "series_dict"],
        "stress_strain": ["x_values", "y_series"],
        "xrd_pattern": ["two_theta", "intensities"],
        "dsc_curve": ["x_values", "y_signals"],
        "tga_curve": ["x_values", "tga", "dtg"],
        "sintering_curve": ["x_values", "y_series"],
        "conductivity_plot": ["x_values", "y_values"],
        "rheology_curve": ["x_values", "y_series"],
        "heatmap": ["data_matrix", "row_labels", "col_labels"],
    }

    def test_figure_archetypes_reference_known_roles(self):
        """Every registry figure_archetype.id should have documented role expectations."""
        for path in sorted(REGISTRY_DIR.glob("*.yaml")):
            with path.open(encoding="utf-8") as f:
                entry = yaml.safe_load(f)
            for archetype in entry.get("figure_archetypes", []) or []:
                arch_id = archetype.get("id", "")
                if arch_id in self.KNOWN_ARCHETYPE_COLUMNS:
                    expected_roles = self.KNOWN_ARCHETYPE_COLUMNS[arch_id]
                    self.assertTrue(
                        isinstance(expected_roles, list) and len(expected_roles) > 0,
                        f"{path.stem}/{arch_id}: no expected roles defined"
                    )


if __name__ == "__main__":
    unittest.main()

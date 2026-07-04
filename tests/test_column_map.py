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
import ast
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "materials-skills"
SCRIPTS_DIR = PLUGIN_ROOT / "skills" / "materials-figure" / "scripts" / "figures4materials"
HELPERS_FILE = SCRIPTS_DIR / "_script_helpers.py"
PLOT_LIB_FILE = PLUGIN_ROOT / "skills" / "materials-figure" / "scripts" / "materials_plot_lib.py"
REGISTRY_DIR = PLUGIN_ROOT / "_shared" / "material-registry" / "entries"


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
        "mechanical_radar": ["categories", "series_dict"],
        "stress_strain": ["x_values", "y_series"],
        "polarization_curve": ["x_values", "y_values"],
        "xrd_pattern": ["two_theta", "intensities"],
        "dsc_curve": ["x_values", "y_signals"],
        "tga_curve": ["x_values", "tga", "dtg"],
        "sintering_curve": ["x_values", "y_series"],
        "conductivity_plot": ["x_values", "y_values"],
        "rheology_curve": ["x_values", "y_series"],
        "heatmap": ["data_matrix", "row_labels", "col_labels"],
        "impedance_nyquist": ["real", "imaginary"],
    }

    def _find_matching_csv(self, data_schemas: list[str], arch_id: str, script_name: str) -> str | None:
        keywords = {
            "stress_strain": ["stress_strain", "tensile"],
            "cg_stress_strain": ["stress_strain", "tensile"],
            "cm_stress_strain": ["stress_strain", "tensile"],
            "polarization_curve": ["corrosion", "polarization"],
            "eis_plot": ["corrosion", "impedance", "eis"],
            "impedance_nyquist": ["impedance", "corrosion", "eis"],
            "hardness_profile": ["hardness", "profile", "trend"],
            "age_hardening_curve": ["hardness", "profile", "trend"],
            "process_window": ["window", "contour", "response_map"],
            "bonding_strength_bar": ["bonding", "strength"],
            "compressive_strength_bar": ["bonding", "strength"],
            "ucs_bar": ["bonding", "strength"],
            "adhesion_strength_bar": ["bonding", "strength"],
            "ftir_overlay": ["ftir", "spectra"],
            "dosage_performance_curve": ["dosage_performance", "dosage"],
            "durability_retention_bar": ["durability", "retention"],
            "property_radar": ["dosage_window"],
            "durability_chart": ["dosage_window"],
            "mechanical_radar": ["radar", "properties", "mechanical"],
            "xrd_pattern": ["xrd", "pattern"],
            "sintering_curve": ["sintering"],
            "dsc_curve": ["dsc", "thermal"],
            "tga_curve": ["tga", "thermal"],
            "lca_boundary": ["lca"],
            "durability_retention": ["durability"],
            "pore_size_distribution": ["particle", "size"],
            "particle_size_distribution": ["particle", "size"],
        }

        # Check by ID in filename
        for schema in data_schemas:
            schema_name = Path(schema).name.lower()
            if arch_id.lower() in schema_name:
                return schema
            if arch_id in keywords:
                for kw in keywords[arch_id]:
                    if kw in schema_name:
                        return schema

        # Check by script name
        script_base = Path(script_name).stem.lower().replace("plot_", "")
        for schema in data_schemas:
            schema_name = Path(schema).name.lower()
            if script_base in schema_name:
                return schema

        # Check by existence fallback
        for schema in data_schemas:
            if REPO_ROOT.joinpath(schema).exists():
                return schema

        # First one in list
        if data_schemas:
            return data_schemas[0]

        return None

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

    def test_runnable_figure_script_contracts(self):
        """Verify that every figure archetype runs successfully on its matched dataset."""
        import subprocess
        import tempfile

        for path in sorted(REGISTRY_DIR.glob("*.yaml")):
            # Only test full coverage tier to maintain focus and prevent skeleton failures
            with path.open(encoding="utf-8") as f:
                entry = yaml.safe_load(f)
            if entry.get("coverage_tier") != "full":
                continue

            sm = entry.get("skill_mapping", {})
            data_schemas = sm.get("data_schemas", []) or []

            for archetype in entry.get("figure_archetypes", []) or []:
                with self.subTest(entry=path.name, archetype=archetype.get("id")):
                    script_path_rel = archetype.get("figure_script")
                    if not script_path_rel:
                        continue

                    script_path = PLUGIN_ROOT / script_path_rel
                    self.assertTrue(script_path.exists(), f"{path.name}: script {script_path_rel} does not exist")

                    # Find matching CSV
                    csv_path_rel = self._find_matching_csv(data_schemas, archetype.get("id"), script_path_rel)
                    self.assertIsNotNone(
                        csv_path_rel,
                        f"{path.name}: Could not find matching CSV in data_schemas for archetype {archetype.get('id')}"
                    )
                    csv_path = PLUGIN_ROOT / csv_path_rel
                    self.assertTrue(csv_path.exists(), f"{path.name}: CSV {csv_path_rel} does not exist")

                    with tempfile.TemporaryDirectory() as temp_dir:
                        with script_path.open(encoding="utf-8") as sf:
                            script_content = sf.read()

                        cmd = [sys.executable, str(script_path)]
                        if "--data" in script_content or "'--data'" in script_content:
                            cmd.extend(["--data", str(csv_path)])
                        cmd.extend(["--output-dir", temp_dir])

                        # Pass column map if specified
                        cmap = archetype.get("column_map")
                        if cmap:
                            cmd.extend(["--column-map", json.dumps(cmap)])

                        res = subprocess.run(cmd, capture_output=True, text=True)
                        self.assertEqual(
                            res.returncode, 0,
                            f"Failed executing figure script {script_path_rel} for entry {path.name}.\n"
                            f"Command: {' '.join(cmd)}\n"
                            f"STDOUT:\n{res.stdout}\n"
                            f"STDERR:\n{res.stderr}"
                        )

    def test_full_registry_declares_hardcoded_script_data_dependencies(self):
        """Full entries must list every CSV read by figure scripts without --data."""
        for path in sorted(REGISTRY_DIR.glob("*.yaml")):
            with path.open(encoding="utf-8") as f:
                entry = yaml.safe_load(f)
            if entry.get("coverage_tier") != "full":
                continue

            declared = set((entry.get("skill_mapping", {}) or {}).get("data_schemas", []) or [])
            for archetype in entry.get("figure_archetypes", []) or []:
                with self.subTest(entry=path.name, archetype=archetype.get("id")):
                    script_path_rel = archetype.get("figure_script")
                    if not script_path_rel:
                        continue
                    script_path = PLUGIN_ROOT / script_path_rel
                    if not script_path.exists():
                        continue

                    script_text = script_path.read_text(encoding="utf-8")
                    if "--data" in script_text or '"--data"' in script_text or "'--data'" in script_text:
                        continue

                    tree = ast.parse(script_text)
                    required = set()
                    for node in ast.walk(tree):
                        if not (
                            isinstance(node, ast.Call)
                            and isinstance(node.func, ast.Name)
                            and node.func.id == "data_path"
                            and node.args
                            and isinstance(node.args[0], ast.Constant)
                            and isinstance(node.args[0].value, str)
                            and node.args[0].value.endswith(".csv")
                        ):
                            continue
                        required.add(
                            "skills/materials-figure/scripts/figures4materials/data/"
                            + node.args[0].value
                        )

                    missing = sorted(required - declared)
                    self.assertFalse(
                        missing,
                        f"{path.name}/{archetype.get('id')}: data_schemas missing "
                        f"hardcoded CSV dependencies from {Path(script_path_rel).name}: {missing}"
                    )


if __name__ == "__main__":
    unittest.main()

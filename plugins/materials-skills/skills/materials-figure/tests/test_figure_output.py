"""Figure QA automated tests: verify script outputs meet publication standards."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
FIGURE_SCRIPTS = REPO_ROOT / "skills" / "materials-figure" / "scripts" / "figures4materials"
DATA_DIR = FIGURE_SCRIPTS / "data"

SCRIPTS_TO_TEST = [
    ("plot_ceramic_strength.py", "ceramic_strength_comparison"),
    ("plot_insulation_multipanel.py", "insulation_multipanel"),
    ("plot_bonding_strength_comparison.py", "bonding_strength_comparison"),
    ("plot_dosage_performance_curve.py", "dosage_performance_curve"),
    ("plot_ftir_curing_evidence.py", "ftir_curing_evidence"),
    ("plot_durability_retention.py", "durability_retention"),
    ("plot_asphalt_multipanel.py", "asphalt_multipanel"),
    ("plot_insulation_conductivity_vs_temp.py", "insulation_conductivity_vs_temp"),
    ("plot_insulation_conductivity_vs_density.py", "insulation_conductivity_vs_density"),
    ("plot_insulation_stress_strain.py", "insulation_stress_strain"),
]

MIN_PNG_BYTES = 5000
MIN_SVG_BYTES = 500


class FigureOutputTest(unittest.TestCase):
    """Verify that figure scripts produce valid SVG and PNG outputs."""

    def _run_script(self, script_name: str, output_dir: Path) -> subprocess.CompletedProcess:
        script_path = FIGURE_SCRIPTS / script_name
        return subprocess.run(
            [sys.executable, str(script_path), "--output-dir", str(output_dir)],
            capture_output=True,
            text=True,
            cwd=str(FIGURE_SCRIPTS),
        )

    def _check_svg_has_text_nodes(self, svg_path: Path) -> bool:
        """Verify SVG contains <text> elements (svg.fonttype='none' is active)."""
        content = svg_path.read_text(encoding="utf-8")
        return "<text" in content

    def test_all_scripts_produce_svg_and_png(self):
        """Every figure script must produce both SVG and PNG files."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            for script_name, output_name in SCRIPTS_TO_TEST:
                with self.subTest(script=script_name):
                    result = self._run_script(script_name, tmp_path)
                    self.assertEqual(
                        result.returncode, 0,
                        f"{script_name} failed: {result.stderr}"
                    )
                    png_path = tmp_path / f"{output_name}.png"
                    svg_path = tmp_path / f"{output_name}.svg"
                    self.assertTrue(png_path.exists(), f"Missing PNG: {png_path.name}")
                    self.assertTrue(svg_path.exists(), f"Missing SVG: {svg_path.name}")

    def test_png_files_exceed_minimum_size(self):
        """PNG files must be substantive (not empty or trivial)."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            for script_name, output_name in SCRIPTS_TO_TEST:
                with self.subTest(script=script_name):
                    self._run_script(script_name, tmp_path)
                    png_path = tmp_path / f"{output_name}.png"
                    if png_path.exists():
                        size = png_path.stat().st_size
                        self.assertGreaterEqual(
                            size, MIN_PNG_BYTES,
                            f"{png_path.name} is only {size} bytes (min {MIN_PNG_BYTES})"
                        )

    def test_svg_files_exceed_minimum_size(self):
        """SVG files must be substantive."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            for script_name, output_name in SCRIPTS_TO_TEST:
                with self.subTest(script=script_name):
                    self._run_script(script_name, tmp_path)
                    svg_path = tmp_path / f"{output_name}.svg"
                    if svg_path.exists():
                        size = svg_path.stat().st_size
                        self.assertGreaterEqual(
                            size, MIN_SVG_BYTES,
                            f"{svg_path.name} is only {size} bytes (min {MIN_SVG_BYTES})"
                        )

    def test_svg_contains_editable_text_nodes(self):
        """SVG must contain <text> nodes, confirming svg.fonttype='none' is active."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            for script_name, output_name in SCRIPTS_TO_TEST:
                with self.subTest(script=script_name):
                    self._run_script(script_name, tmp_path)
                    svg_path = tmp_path / f"{output_name}.svg"
                    if svg_path.exists():
                        self.assertTrue(
                            self._check_svg_has_text_nodes(svg_path),
                            f"{svg_path.name} has no <text> nodes — svg.fonttype='none' may not be active"
                        )


class ChartAtlasOutputTest(unittest.TestCase):
    """Verify chart atlas generator produces all expected outputs."""

    ATLAS_SCRIPT = REPO_ROOT / "skills" / "materials-figure" / "scripts" / "generate_chart_atlas.py"
    EXPECTED_ATLASES = [
        "atlas-bar-charts",
        "atlas-line-trends",
        "atlas-heatmaps",
        "atlas-scatter-bubble",
        "atlas-radar-polar",
        "atlas-distributions",
        "atlas-characterization",
    ]

    def test_atlas_generator_produces_all_families(self):
        """Chart atlas must generate all 7 chart family images."""
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [sys.executable, str(self.ATLAS_SCRIPT), "--output-dir", tmp],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, f"Atlas generator failed: {result.stderr}")
            for name in self.EXPECTED_ATLASES:
                png = Path(tmp) / f"{name}.png"
                svg = Path(tmp) / f"{name}.svg"
                self.assertTrue(png.exists(), f"Missing atlas PNG: {name}.png")
                self.assertTrue(svg.exists(), f"Missing atlas SVG: {name}.svg")


if __name__ == "__main__":
    unittest.main()

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = SKILL_ROOT / "scripts"
FIGURES_ROOT = SCRIPTS_ROOT / "figures4materials"


class MatplotlibProductionLibraryTest(unittest.TestCase):
    def load_plot_lib(self):
        module_path = SCRIPTS_ROOT / "civil_materials_plot_lib.py"
        self.assertTrue(module_path.exists(), "civil_materials_plot_lib.py should exist")
        spec = importlib.util.spec_from_file_location("civil_materials_plot_lib", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_plot_lib_exposes_publication_ready_helpers(self):
        lib = self.load_plot_lib()

        for name in [
            "PUB_RC",
            "PALETTE_CBM",
            "PALETTE_CCC",
            "apply_pub_style",
            "make_grouped_bar",
            "make_line_trend",
            "make_radar",
            "make_xrd_pattern",
            "make_ftir_overlay",
            "add_panel_label",
            "add_error_bars",
            "finalize_figure",
        ]:
            self.assertTrue(hasattr(lib, name), f"{name} should be exposed")

    def test_plot_lib_generates_vector_and_raster_outputs(self):
        lib = self.load_plot_lib()
        lib.apply_pub_style()

        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(5, 3))
        lib.make_grouped_bar(
            ax,
            labels=["0%", "10%", "20%"],
            groups=["Dry", "Wet"],
            values=[[0.42, 0.55, 0.61], [0.28, 0.41, 0.49]],
            palette=lib.PALETTE_CBM,
            error_bars=[[0.02, 0.03, 0.02], [0.03, 0.02, 0.03]],
            ylabel="Pull-off strength (MPa)",
        )
        lib.add_panel_label(ax, "(a)")

        with tempfile.TemporaryDirectory() as tmp:
            outputs = lib.finalize_figure(fig, "bonding_strength", output_dir=tmp, formats=("svg", "png"), dpi=120)

            self.assertEqual({Path(path).suffix for path in outputs}, {".svg", ".png"})
            for path in outputs:
                self.assertTrue(Path(path).exists())
            self.assertIn("<svg", Path(tmp, "bonding_strength.svg").read_text(encoding="utf-8"))


class FigureProductionScriptsTest(unittest.TestCase):
    EXPECTED_SCRIPTS = [
        "plot_bonding_strength_comparison.py",
        "plot_dosage_performance_curve.py",
        "plot_ftir_curing_evidence.py",
        "plot_durability_retention.py",
        "plot_mechanical_property_radar.py",
    ]
    EXPECTED_DATA = [
        "bonding_strength.csv",
        "dosage_performance.csv",
        "ftir_spectra.csv",
        "durability_retention.csv",
        "mechanical_properties.csv",
    ]

    def test_figures4materials_scripts_and_data_exist(self):
        for script in self.EXPECTED_SCRIPTS:
            self.assertTrue((FIGURES_ROOT / script).exists(), f"{script} should exist")
        for data_file in self.EXPECTED_DATA:
            self.assertTrue((FIGURES_ROOT / "data" / data_file).exists(), f"{data_file} should exist")

    def test_each_figures4materials_script_generates_svg_png_and_caption(self):
        for script in self.EXPECTED_SCRIPTS:
            with self.subTest(script=script), tempfile.TemporaryDirectory() as tmp:
                result = subprocess.run(
                    [
                        sys.executable,
                        str(FIGURES_ROOT / script),
                        "--output-dir",
                        tmp,
                    ],
                    check=True,
                    capture_output=True,
                    text=True,
                )

                self.assertIn("Caption:", result.stdout)
                self.assertEqual(len(list(Path(tmp).glob("*.svg"))), 1)
                self.assertEqual(len(list(Path(tmp).glob("*.png"))), 1)


class FigureDesignReferenceTest(unittest.TestCase):
    def test_production_references_cover_chart_atlas_design_theory_and_qa(self):
        expected = {
            "chart-atlas.md": ["bonding strength", "dosage-performance", "FTIR", "radar", "code pattern"],
            "figure-design-theory.md": ["information hierarchy", "colorblind", "grayscale", "multi-panel"],
            "figure-qa-contract.md": ["DPI", "error bars", "replicate", "scale bar", "caption boundary"],
        }
        for filename, phrases in expected.items():
            path = SKILL_ROOT / "references" / filename
            self.assertTrue(path.exists(), f"{filename} should exist")
            text = path.read_text(encoding="utf-8")
            for phrase in phrases:
                self.assertIn(phrase, text)

    def test_visual_asset_roadmap_and_rich_gallery_assets_exist(self):
        roadmap = SKILL_ROOT / "references" / "visual-asset-roadmap.md"
        self.assertTrue(roadmap.exists(), "visual-asset-roadmap.md should exist")
        roadmap_text = roadmap.read_text(encoding="utf-8")
        for phrase in ["visual richness", "30 assets", "60 assets", "100 assets", "SVG-first"]:
            self.assertIn(phrase, roadmap_text)

        generated_dir = SKILL_ROOT / "assets" / "rich-gallery" / "generated"
        self.assertTrue(generated_dir.exists(), "rich gallery generated assets should exist")
        svgs = sorted(generated_dir.glob("*.svg"))
        self.assertGreaterEqual(len(svgs), 10)
        for svg in svgs[:10]:
            text = svg.read_text(encoding="utf-8")
            self.assertIn("<svg", text)
            self.assertIn("Civil Materials Rich Gallery", text)

    def test_rich_gallery_demo_regenerates_ten_visual_assets(self):
        script = SCRIPTS_ROOT / "rich_gallery_demo.py"
        self.assertTrue(script.exists(), "rich_gallery_demo.py should exist")

        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--output-dir",
                    tmp,
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            outputs = sorted(Path(tmp).glob("*.svg"))
            self.assertEqual(len(outputs), 10)
            self.assertIn("interface_mechanism_map.svg", result.stdout)


if __name__ == "__main__":
    unittest.main()

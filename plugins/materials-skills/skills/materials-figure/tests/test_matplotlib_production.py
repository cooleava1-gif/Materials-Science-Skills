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
        module_path = SCRIPTS_ROOT / "materials_plot_lib.py"
        self.assertTrue(module_path.exists(), "materials_plot_lib.py should exist")
        spec = importlib.util.spec_from_file_location("materials_plot_lib", module_path)
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
            "make_scatter_regression",
            "make_boxplot_with_points",
            "make_violin_plot",
            "make_contour_map",
            "make_3d_surface",
            "make_polar_plot",
            "make_errorbar_trend",
            "make_dual_axis_trend",
            "make_correlation_heatmap",
            "make_stacked_composition_bar",
        ]:
            self.assertTrue(hasattr(lib, name), f"{name} should be exposed")

    def test_expanded_python_helpers_render_core_chart_families(self):
        lib = self.load_plot_lib()
        lib.apply_pub_style()

        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import numpy as np

        with tempfile.TemporaryDirectory() as tmp:
            fig, axes = plt.subplots(2, 2, figsize=(8, 6))
            lib.make_scatter_regression(
                axes[0, 0],
                x=[0, 5, 10, 15, 20],
                y=[0.42, 0.54, 0.70, 0.79, 0.73],
                palette=lib.PALETTE_ASPHALT,
                xlabel="WER content (%)",
                ylabel="Bond strength (MPa)",
            )
            lib.make_boxplot_with_points(
                axes[0, 1],
                groups=["Control", "10% WER", "15% WER"],
                data_dict={"Control": [0.41, 0.44, 0.40], "10% WER": [0.58, 0.62, 0.59], "15% WER": [0.74, 0.78, 0.81]},
                palette=lib.PALETTE_ASPHALT,
                ylabel="Strength (MPa)",
            )
            lib.make_violin_plot(
                axes[1, 0],
                groups=["Dry", "Wet"],
                data_dict={"Dry": [0.70, 0.76, 0.79, 0.82], "Wet": [0.51, 0.55, 0.58, 0.61]},
                palette=lib.PALETTE_ASPHALT,
                ylabel="Bond strength (MPa)",
            )
            lib.make_errorbar_trend(
                axes[1, 1],
                x=[0, 10, 20],
                y=[0.42, 0.68, 0.61],
                yerr=[0.03, 0.04, 0.04],
                palette=lib.PALETTE_ASPHALT,
                xlabel="WER content (%)",
                ylabel="Strength (MPa)",
            )
            outputs = lib.finalize_figure(fig, "expanded_helpers_a", output_dir=tmp, formats=("svg", "png"), dpi=120)
            self.assertEqual({Path(path).suffix for path in outputs}, {".svg", ".png"})

            fig2, axes2 = plt.subplots(2, 2, figsize=(8, 6), subplot_kw={"projection": None})
            xx, yy = np.meshgrid(np.linspace(0, 20, 5), np.linspace(20, 60, 5))
            zz = 0.3 + 0.02 * xx - 0.001 * (yy - 40) ** 2
            lib.make_contour_map(axes2[0, 0], xx, yy, zz, xlabel="WER (%)", ylabel="Curing temp (C)")
            lib.make_dual_axis_trend(
                axes2[0, 1],
                x=[0, 10, 20],
                y_left=[0.42, 0.68, 0.61],
                y_right=[220, 360, 410],
                palette=lib.PALETTE_ASPHALT,
                left_label="Strength (MPa)",
                right_label="Viscosity (mPa s)",
            )
            lib.make_correlation_heatmap(
                axes2[1, 0],
                data=np.array([[1, 0.8], [0.8, 1]]),
                labels=["Strength", "Retention"],
            )
            lib.make_stacked_composition_bar(
                axes2[1, 1],
                labels=["Control", "WER-EA"],
                series_dict={"Asphalt": [92, 80], "Water": [8, 10], "WER": [0, 10]},
                palette=lib.PALETTE_ASPHALT,
                ylabel="Composition (%)",
            )
            outputs2 = lib.finalize_figure(fig2, "expanded_helpers_b", output_dir=tmp, formats=("svg", "png"), dpi=120)
            self.assertEqual({Path(path).suffix for path in outputs2}, {".svg", ".png"})

            fig3 = plt.figure(figsize=(8, 4))
            ax3d = fig3.add_subplot(1, 2, 1, projection="3d")
            lib.make_3d_surface(ax3d, xx, yy, zz, xlabel="WER (%)", ylabel="Temp (C)", zlabel="Strength")
            axp = fig3.add_subplot(1, 2, 2, projection="polar")
            lib.make_polar_plot(
                axp,
                theta=[0, 1.2, 2.4, 3.6, 4.8],
                radius=[0.5, 0.7, 0.8, 0.65, 0.55],
                label="15% WER",
                palette=lib.PALETTE_ASPHALT,
            )
            outputs3 = lib.finalize_figure(fig3, "expanded_helpers_c", output_dir=tmp, formats=("svg", "png"), dpi=120)
            self.assertEqual({Path(path).suffix for path in outputs3}, {".svg", ".png"})

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
        "plot_rheology_curve.py",
        "plot_tga_dtg_curve.py",
        "plot_dosage_window.py",
        "plot_particle_size_distribution.py",
        "plot_sem_analysis.py",
        "plot_sintering_curve.py",
        "plot_ceramic_strength.py",
        "plot_ceramic_conductivity.py",
        "plot_insulation_conductivity_vs_density.py",
        "plot_insulation_stress_strain.py",
        "plot_insulation_conductivity_vs_temp.py",
        "plot_polymers_multipanel.py",
        "plot_metals_multipanel.py",
        "plot_nano_multipanel.py",
        "plot_functional_multipanel.py",
        "plot_scatter_regression.py",
        "plot_boxplot_points.py",
        "plot_violin_distribution.py",
        "plot_contour_response_map.py",
        "plot_3d_response_surface.py",
        "plot_polar_performance.py",
        "plot_errorbar_trend.py",
        "plot_dual_axis_trend.py",
        "plot_correlation_heatmap.py",
        "plot_stacked_composition.py",
    ]
    EXPECTED_DATA = [
        "bonding_strength.csv",
        "dosage_performance.csv",
        "ftir_spectra.csv",
        "durability_retention.csv",
        "mechanical_properties.csv",
        "rheology_curve.csv",
        "tga_dtg_curve.csv",
        "dosage_window.csv",
        "particle_size_distribution.csv",
        "sem_analysis.csv",
        "sintering_curve.csv",
        "ceramic_composition_strength.csv",
        "ceramic_conductivity.csv",
        "insulation_conductivity_vs_density.csv",
        "insulation_stress_strain.csv",
        "insulation_conductivity_humidity.csv",
        "polymer_tensile.csv",
        "polymer_dsc.csv",
        "polymer_stress_strain.csv",
        "polymer_aging.csv",
        "metals_tensile.csv",
        "metals_stress_strain.csv",
        "metals_hardness_profile.csv",
        "metals_corrosion.csv",
        "nano_loading.csv",
        "nano_size_dist.csv",
        "nano_xrd.csv",
        "nano_uvis.csv",
        "functional_dielectric.csv",
        "functional_freq_sweep.csv",
        "functional_pe_loop.csv",
        "functional_impedance.csv",
        "scatter_regression.csv",
        "boxplot_points.csv",
        "violin_distribution.csv",
        "contour_response_map.csv",
        "response_surface_grid.csv",
        "polar_performance.csv",
        "errorbar_trend.csv",
        "dual_axis_trend.csv",
        "correlation_heatmap.csv",
        "stacked_composition.csv",
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
            "chart-atlas.md": ["bonding strength", "dosage-performance", "FTIR", "radar", "scatter regression", "3D response surface", "code pattern"],
            "figure-design-theory.md": ["information hierarchy", "colorblind", "grayscale", "multi-panel"],
            "figure-qa-contract.md": ["DPI", "error bars", "replicate", "scale bar", "caption boundary"],
            "tutorials.md": ["Python-only expanded chart gallery", "contour response map", "correlation heatmap"],
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
            self.assertIn("Materials Science Rich Gallery", text)

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

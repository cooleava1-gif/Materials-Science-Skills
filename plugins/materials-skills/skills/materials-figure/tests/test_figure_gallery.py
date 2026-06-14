import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


SKILL_ROOT = Path(__file__).resolve().parents[1]
SHOWCASE_PROOF_ASSETS = [
    "reader_package_proof_wall.png",
    "wer_ea_figure_proof_board.png",
    "sbr_wer_performance_proof_board.png",
    "interlayer_fatigue_proof_board.png",
]
SHOWCASE_MANIFEST = "showcase_manifest.json"


def has_visual_signal(path: Path) -> bool:
    with Image.open(path) as image:
        rgba = image.convert("RGBA")
        extrema = rgba.getextrema()
        return rgba.width >= 1200 and rgba.height >= 700 and any(
            (high - low) >= 40 for low, high in extrema[:3]
        )


def read_showcase_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class FigureGalleryAssetsTest(unittest.TestCase):
    def test_gallery_reference_and_style_presets_exist(self):
        gallery = SKILL_ROOT / "references" / "figure-gallery.md"
        production_spec = SKILL_ROOT / "references" / "figure-production-spec.md"
        presets = SKILL_ROOT / "assets" / "templates" / "figure-style-presets.yaml"

        self.assertTrue(gallery.exists(), "figure-gallery.md should document the gallery workflow")
        self.assertTrue(production_spec.exists(), "figure-production-spec.md should document submission production rules")
        self.assertTrue(presets.exists(), "figure-style-presets.yaml should define journal style presets")

        gallery_text = gallery.read_text(encoding="utf-8")
        production_text = production_spec.read_text(encoding="utf-8")
        preset_text = presets.read_text(encoding="utf-8")

        for phrase in [
            "bonding strength",
            "dosage-performance",
            "FTIR peak annotation",
            "SEM/fluorescence",
            "durability radar",
            "mechanism schematic",
        ]:
            self.assertIn(phrase, gallery_text)
        for preset in ["cbm", "ccc", "rmpd_ijpe", "jbe"]:
            self.assertIn(f"{preset}:", preset_text)
        for phrase in ["dpi", "TIFF", "EPS", "single column", "double column", "SEM"]:
            self.assertIn(phrase, production_text)
        for phrase in ["dpi:", "preferred_formats:", "single_column_width_mm:", "double_column_width_mm:", "min_font_size_pt:"]:
            self.assertIn(phrase, preset_text)

    def test_gallery_example_cards_have_claim_caption_and_risk(self):
        expected = [
            "bonding-strength-bar.md",
            "dosage-performance-curve.md",
            "ftir-peak-annotation.md",
            "sem-fluorescence-plate.md",
            "durability-radar.md",
            "mechanism-schematic.md",
        ]
        for filename in expected:
            path = SKILL_ROOT / "examples" / "gallery" / filename
            self.assertTrue(path.exists(), f"{filename} should exist")
            text = path.read_text(encoding="utf-8")
            for section in ["## Figure Intent", "## Data Structure", "## Caption Pattern", "## Reviewer Risk"]:
                self.assertIn(section, text, f"{filename} should include {section}")

    def test_generated_gallery_svgs_are_available_as_visual_examples(self):
        expected = [
            "bonding_strength_bar.svg",
            "dosage_performance_curve.svg",
            "ftir_peak_annotation.svg",
            "sem_fluorescence_plate.svg",
            "durability_radar.svg",
            "mechanism_schematic.svg",
        ]
        for filename in expected:
            path = SKILL_ROOT / "examples" / "gallery" / "generated" / filename
            self.assertTrue(path.exists(), f"{filename} should be generated and available")
            text = path.read_text(encoding="utf-8")
            self.assertIn("Materials Science Figure Gallery", text)

    def test_showcase_proof_assets_exist_and_have_visual_signal(self):
        showcase_root = SKILL_ROOT / "assets" / "showcase-proof"
        self.assertTrue(showcase_root.exists(), "showcase-proof assets should exist")
        for filename in SHOWCASE_PROOF_ASSETS:
            path = showcase_root / filename
            self.assertTrue(path.exists(), f"{filename} should exist")
            self.assertTrue(has_visual_signal(path), f"{filename} should be content-bearing, not a flat placeholder")
            with Image.open(path) as image:
                self.assertGreaterEqual(image.width, 1800, f"{filename} should use a high-resolution editorial canvas")
                self.assertGreaterEqual(image.height, 1100, f"{filename} should use a high-resolution editorial canvas")

    def test_showcase_manifest_records_editorial_narrative_and_source_tiles(self):
        manifest_path = SKILL_ROOT / "assets" / "showcase-proof" / SHOWCASE_MANIFEST
        self.assertTrue(manifest_path.exists(), "showcase manifest should exist")

        manifest = read_showcase_manifest(manifest_path)
        self.assertEqual(manifest["visual_language"], "editorial-proof-boards")
        self.assertEqual(manifest["narrative_layers"], ["overview", "deviation", "relationship"])

        boards = manifest["boards"]
        self.assertEqual(sorted(board["filename"] for board in boards), sorted(SHOWCASE_PROOF_ASSETS))
        for board in boards:
            self.assertIn(board["layout_family"], {"editorial_mosaic", "editorial_triptych"})
            self.assertGreaterEqual(len(board["tiles"]), 3, f'{board["filename"]} should expose multiple evidence tiles')

            roles = {tile["role"] for tile in board["tiles"]}
            self.assertIn("overview", roles, f'{board["filename"]} should include an overview tile')
            self.assertIn("deviation", roles, f'{board["filename"]} should include a deviation tile')
            self.assertIn("relationship", roles, f'{board["filename"]} should include a relationship tile')

            for tile in board["tiles"]:
                self.assertIn("source_path", tile)
                self.assertIn("crop", tile)
                self.assertEqual(sorted(tile["crop"].keys()), ["bottom", "left", "right", "top"])


class FigureGalleryDemoScriptTest(unittest.TestCase):
    def test_plot_svg_reports_missing_required_columns(self):
        script = SKILL_ROOT / "scripts" / "materials_plot_svg.py"
        self.assertTrue(script.exists(), "materials_plot_svg.py should exist")

        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "bad.csv"
            csv_path.write_text("sample,value\ncontrol,1.0\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    str(csv_path),
                    "--output",
                    str(Path(tmp) / "out.svg"),
                ],
                check=False,
                capture_output=True,
                text=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("CSV must include columns: label, value", result.stderr)

    def test_plot_svg_generates_svg_from_valid_csv(self):
        script = SKILL_ROOT / "scripts" / "materials_plot_svg.py"
        self.assertTrue(script.exists(), "materials_plot_svg.py should exist")

        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "bonding.csv"
            output_path = Path(tmp) / "bonding.svg"
            csv_path.write_text("label,value\nControl,0.42\nEpoxy 15%,0.68\n", encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    str(csv_path),
                    "--title",
                    "Bonding strength",
                    "--ylabel",
                    "Pull-off strength (MPa)",
                    "--output",
                    str(output_path),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn(str(output_path), result.stdout)
            self.assertTrue(output_path.exists())
            svg = output_path.read_text(encoding="utf-8")
            self.assertIn("<svg", svg)
            self.assertIn("<rect", svg)
            self.assertIn("<text", svg)

    def test_characterization_figures_include_fluorescence_microscopy_plate(self):
        reference = SKILL_ROOT / "references" / "characterization-figures.md"
        text = reference.read_text(encoding="utf-8")

        for phrase in [
            "Fluorescence Microscopy Plate",
            "excitation wavelength",
            "emission",
            "Scale bar",
            "representative",
            "ImageJ",
            "FTIR, DSC, rheology",
        ]:
            self.assertIn(phrase, text)

    def test_gallery_demo_generates_all_svg_examples(self):
        script = SKILL_ROOT / "scripts" / "gallery_demo.py"
        self.assertTrue(script.exists(), "gallery_demo.py should exist")

        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--output-dir",
                    tmp,
                    "--preset",
                    "cbm",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertIn("bonding_strength_bar.svg", result.stdout)
            outputs = sorted(Path(tmp).glob("*.svg"))
            self.assertEqual(len(outputs), 6)
            for svg in outputs:
                text = svg.read_text(encoding="utf-8")
                self.assertIn("<svg", text)
                self.assertIn("Materials Science Figure Gallery", text)

    def test_showcase_builder_generates_real_png_proof_assets(self):
        script = SKILL_ROOT / "scripts" / "build_showcase_proof_assets.py"
        self.assertTrue(script.exists(), "build_showcase_proof_assets.py should exist")

        sample_image = SKILL_ROOT.parents[1] / "outputs" / "wer-ea-30-reading-sample" / "015-curing-agent-structure-wer-ea" / "assets" / "contact_sheet.png"
        if not sample_image.exists():
            self.skipTest("wer-ea-30-reading-sample source images not available")

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
            for filename in SHOWCASE_PROOF_ASSETS:
                self.assertIn(filename, result.stdout)
                output_path = Path(tmp) / filename
                self.assertTrue(has_visual_signal(output_path))
                with Image.open(output_path) as image:
                    self.assertGreaterEqual(image.width, 1800)
                    self.assertGreaterEqual(image.height, 1100)

            manifest_path = Path(tmp) / SHOWCASE_MANIFEST
            self.assertTrue(manifest_path.exists(), "showcase builder should emit a manifest")
            manifest = read_showcase_manifest(manifest_path)
            self.assertEqual(len(manifest["boards"]), len(SHOWCASE_PROOF_ASSETS))
            self.assertEqual(manifest["narrative_layers"], ["overview", "deviation", "relationship"])


if __name__ == "__main__":
    unittest.main()

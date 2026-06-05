import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]


class FigureGalleryAssetsTest(unittest.TestCase):
    def test_gallery_reference_and_style_presets_exist(self):
        gallery = SKILL_ROOT / "references" / "figure-gallery.md"
        presets = SKILL_ROOT / "assets" / "templates" / "figure-style-presets.yaml"

        self.assertTrue(gallery.exists(), "figure-gallery.md should document the gallery workflow")
        self.assertTrue(presets.exists(), "figure-style-presets.yaml should define journal style presets")

        gallery_text = gallery.read_text(encoding="utf-8")
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
            self.assertIn("Civil Materials Figure Gallery", text)


class FigureGalleryDemoScriptTest(unittest.TestCase):
    def test_plot_svg_reports_missing_required_columns(self):
        script = SKILL_ROOT / "scripts" / "civil_materials_plot_svg.py"
        self.assertTrue(script.exists(), "civil_materials_plot_svg.py should exist")

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
                self.assertIn("Civil Materials Figure Gallery", text)


if __name__ == "__main__":
    unittest.main()

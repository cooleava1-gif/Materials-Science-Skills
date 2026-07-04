import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "materials-skills"
FIGURE_ROOT = PLUGIN_ROOT / "skills" / "materials-figure"


class FigureStoryboardContractTest(unittest.TestCase):
    def test_materials_figure_atlas_defines_fixed_research_archetypes(self):
        path = FIGURE_ROOT / "references" / "materials-figure-atlas.md"
        self.assertTrue(path.exists(), f"{path} should exist")
        text = path.read_text(encoding="utf-8").lower()
        expected = {
            "property-performance": ["strength", "viscosity", "thermal conductivity", "modulus", "water absorption"],
            "process-structure-property": ["processing parameter", "microstructure", "performance"],
            "mechanism-evidence": ["ftir", "xrd", "sem", "dsc", "tga"],
            "durability-aging": ["aging", "freeze-thaw", "hygrothermal", "uv", "fatigue retention"],
            "comparison-window": ["dosage window", "performance radar", "integrated scoring"],
            "review-evidence-map": ["research gap heatmap", "evidence-grade matrix", "screening flow"],
        }
        for archetype, phrases in expected.items():
            self.assertIn(archetype, text)
            for phrase in phrases:
                self.assertIn(phrase, text, f"{archetype} should include {phrase}")

    def test_storyboard_templates_and_boundary_documents_exist(self):
        expected = {
            "assets/templates/figure_storyboard.yaml": ["layout", "panels", "role", "claim", "evidence", "source"],
            "references/caption_boundary.md": ["panel", "claim", "evidence", "must not exceed"],
            "references/figure_qa_report.md": ["font", "font size", "legend", "units", "resolution", "svg text"],
        }
        for relative, phrases in expected.items():
            path = FIGURE_ROOT / relative
            self.assertTrue(path.exists(), f"{relative} should exist")
            text = path.read_text(encoding="utf-8").lower()
            for phrase in phrases:
                self.assertIn(phrase, text, f"{relative} should contain {phrase}")

    def test_multipanel_composer_creates_svg_png_caption_and_qa_outputs(self):
        script = FIGURE_ROOT / "scripts" / "compose_multipanel_figure.py"
        self.assertTrue(script.exists(), "multipanel composer should exist")

        storyboard = """
layout: 2x2
title: Synthetic materials figure
panels:
  - id: A
    role: property-performance
    title: Strength window
    claim: Strength increases within the tested dosage window.
    evidence: Synthetic compressive strength source data.
    source: synthetic_strength.csv
  - id: B
    role: mechanism-evidence
    title: FTIR evidence
    claim: FTIR peak changes are associated with curing.
    evidence: Synthetic FTIR peak intensity source data.
    source: synthetic_ftir.csv
  - id: C
    role: durability-aging
    title: Aging retention
    claim: Retention is reported within the aging protocol.
    evidence: Synthetic retention source data.
    source: synthetic_aging.csv
  - id: D
    role: review-evidence-map
    title: Evidence map
    claim: Literature coverage is strongest for bonding tests.
    evidence: Synthetic evidence-grade matrix.
    source: synthetic_evidence.csv
"""

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            storyboard_path = tmp_path / "figure_storyboard.yaml"
            storyboard_path.write_text(storyboard, encoding="utf-8")
            output_dir = tmp_path / "out"
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--storyboard",
                    str(storyboard_path),
                    "--output-dir",
                    str(output_dir),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn(str(output_dir), result.stdout)
            for name in ["figure.svg", "figure.png", "caption_boundary.md", "figure_qa_report.md", "asset_manifest.json"]:
                self.assertTrue((output_dir / name).exists(), f"{name} should be generated")
            self.assertIn(">A<", (output_dir / "figure.svg").read_text(encoding="utf-8"))
            manifest = json.loads((output_dir / "asset_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual("2x2", manifest["layout"])
            self.assertEqual(4, len(manifest["panels"]))

    def test_three_golden_figure_packages_exist_with_storyboards(self):
        packages = {
            "wer-ea-full": ["mechanism", "performance", "evidence heatmap", "literature screening"],
            "thermal-insulation-partial-to-full": [
                "conductivity-density",
                "pore structure",
                "hygrothermal aging",
                "application window",
            ],
            "polymer-composites-partial-to-full": [
                "stress-strain",
                "fiber orientation",
                "interface mechanism",
                "fatigue",
                "interlaminar shear",
            ],
        }
        root = FIGURE_ROOT / "examples" / "figure-packages"
        for package, phrases in packages.items():
            package_dir = root / package
            self.assertTrue(package_dir.exists(), f"{package} should exist")
            for name in ["README.md", "figure_storyboard.yaml", "caption_boundary.md", "figure_qa_report.md"]:
                self.assertTrue((package_dir / name).exists(), f"{package}/{name} should exist")
            combined = "\n".join(
                (package_dir / name).read_text(encoding="utf-8").lower()
                for name in ["README.md", "figure_storyboard.yaml", "caption_boundary.md", "figure_qa_report.md"]
            )
            for phrase in phrases:
                self.assertIn(phrase, combined, f"{package} should cover {phrase}")

    def test_release_gate_tracks_figure_maturity_assets(self):
        release_text = (REPO_ROOT / "scripts" / "run_release_checks.py").read_text(encoding="utf-8")
        for phrase in [
            "FIGURE_GOLDEN_PACKAGES",
            "materials-figure-atlas.md",
            "figure_storyboard.yaml",
            "caption_boundary.md",
            "figure_qa_report.md",
            "compose_multipanel_figure.py",
            "wer-ea-full",
            "thermal-insulation-partial-to-full",
            "polymer-composites-partial-to-full",
        ]:
            self.assertIn(phrase, release_text)


if __name__ == "__main__":
    unittest.main()

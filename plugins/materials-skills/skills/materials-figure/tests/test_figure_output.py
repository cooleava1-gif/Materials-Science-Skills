"""Figure asset smoke tests for the currently shipped package."""

from __future__ import annotations

import unittest
from pathlib import Path


FIGURE_ROOT = Path(__file__).resolve().parents[1]
MATERIALS4PAPERS = FIGURE_ROOT / "assets" / "materials4papers"


class FigureOutputTest(unittest.TestCase):
    def test_materials4papers_examples_ship_plot_sources(self):
        example_dirs = [path for path in MATERIALS4PAPERS.iterdir() if path.is_dir()]

        self.assertGreaterEqual(len(example_dirs), 15)
        for package in example_dirs:
            with self.subTest(package=package.name):
                self.assertTrue((package / "plot.py").exists(), f"{package.name} needs plot.py")

    def test_materials4papers_examples_keep_data_or_readme_context(self):
        for package in MATERIALS4PAPERS.iterdir():
            if not package.is_dir():
                continue
            with self.subTest(package=package.name):
                has_data = (package / "data").is_dir() and any((package / "data").iterdir())
                has_readme = (package / "README.md").exists()
                self.assertTrue(has_data or has_readme, f"{package.name} needs data or README context")

    def test_generated_visual_assets_are_substantive_when_shipped(self):
        generated = list(MATERIALS4PAPERS.glob("*/figures/*"))
        self.assertGreaterEqual(len(generated), 10)
        for asset in generated:
            with self.subTest(asset=asset.name):
                self.assertGreater(asset.stat().st_size, 100, f"{asset.name} should not be empty")


if __name__ == "__main__":
    unittest.main()

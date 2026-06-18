import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"

sys.path.insert(0, str(SCRIPTS_DIR))
from mix_design_calc import dense_packing, empirical_correction, volume_method


class MixDesignCalcTest(unittest.TestCase):
    def test_dense_packing_returns_valid_fractions(self):
        components = [
            {"name": "coarse", "size_min_mm": 4.75, "size_max_mm": 19.0, "packing_density": 0.55},
            {"name": "fine", "size_min_mm": 0.15, "size_max_mm": 4.75, "packing_density": 0.40},
            {"name": "filler", "size_min_mm": 0.0, "size_max_mm": 0.15, "packing_density": 0.30},
        ]
        result = dense_packing(components)
        total = sum(c["volume_fraction"] for c in result)
        self.assertLessEqual(total, 1.0 + 1e-6)
        self.assertGreater(total, 0.0)
        for c in result:
            self.assertGreaterEqual(c["volume_fraction"], 0.0)

    def test_volume_method_returns_proportions(self):
        result = volume_method(target_strength=30.0, wc_ratio=0.45)
        self.assertGreater(result["components"]["cement"]["mass_kg_m3"], 0)
        self.assertGreater(result["components"]["water"]["mass_kg_m3"], 0)
        self.assertGreater(result["components"]["coarse_aggregate"]["mass_kg_m3"], 0)
        self.assertGreater(result["components"]["fine_aggregate"]["mass_kg_m3"], 0)

    def test_empirical_correction_applies_factors(self):
        base = {"cement": 400.0, "water": 180.0, "aggregate": 1700.0}
        corrections = {"cement": 1.10, "water": 0.95}
        result = empirical_correction(base, corrections)
        self.assertAlmostEqual(result["cement"], 440.0, places=1)
        self.assertAlmostEqual(result["water"], 171.0, places=1)
        self.assertAlmostEqual(result["aggregate"], 1700.0, places=1)


if __name__ == "__main__":
    unittest.main()

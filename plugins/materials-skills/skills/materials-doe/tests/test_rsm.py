import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"

sys.path.insert(0, str(SCRIPTS_DIR))
from rsm_analysis import (
    fit_quadratic_model,
    generate_bbd_matrix,
    generate_ccd_matrix,
    optimize_rsm,
)


class CCDGenerationTest(unittest.TestCase):
    def test_ccd_generation(self):
        """3-factor CCD: 2^3=8 factorial + 2*3=6 axial + 5 center = 19 rows."""
        df = generate_ccd_matrix(["A", "B", "C"], center_points=5)
        self.assertEqual(len(df), 19)
        self.assertEqual(list(df.columns), ["A", "B", "C"])

        # Factorial portion: 8 rows with all combinations of +/-1
        factorial = df.iloc[:8]
        for col in ["A", "B", "C"]:
            vals = sorted(factorial[col].unique())
            self.assertAlmostEqual(vals[0], -1.0)
            self.assertAlmostEqual(vals[-1], 1.0)

        # Axial portion: 6 rows, each with one factor at +/-alpha, rest at 0
        axial = df.iloc[8:14]
        alpha = 2 ** (3 / 4)  # rotatable alpha for k=3
        for _, row in axial.iterrows():
            nonzero = [v for v in row.values if abs(v) > 1e-10]
            self.assertEqual(len(nonzero), 1)
            self.assertAlmostEqual(abs(nonzero[0]), alpha, places=10)

        # Center points: 5 rows all zeros
        center = df.iloc[14:]
        self.assertEqual(len(center), 5)
        for _, row in center.iterrows():
            for v in row.values:
                self.assertAlmostEqual(v, 0.0)


class BBDGenerationTest(unittest.TestCase):
    def test_bbd_generation(self):
        """3-factor BBD: C(3,2)*4=12 edge + 5 center = 17 rows."""
        df = generate_bbd_matrix(["A", "B", "C"], center_points=5)
        self.assertEqual(len(df), 17)
        self.assertEqual(list(df.columns), ["A", "B", "C"])

        # Edge points: 12 rows, each has exactly 2 non-zero values at +/-1
        edge = df.iloc[:12]
        for _, row in edge.iterrows():
            nonzero = [v for v in row.values if abs(v) > 1e-10]
            self.assertEqual(len(nonzero), 2)
            for v in nonzero:
                self.assertAlmostEqual(abs(v), 1.0)

        # Center points: 5 rows all zeros
        center = df.iloc[12:]
        self.assertEqual(len(center), 5)


class QuadraticFitTest(unittest.TestCase):
    def _make_exact_quadratic_data(self):
        """Generate data from a known quadratic model with zero noise."""
        coded = generate_ccd_matrix(["x1", "x2", "x3"], center_points=5)
        # Known coefficients
        # y = 5 + 2*x1 - 1.5*x2 + 0.8*x3
        #     + 1.2*x1*x2 - 0.5*x1*x3 + 0.3*x2*x3
        #     - 0.7*x1^2 + 0.4*x2^2 - 0.9*x3^2
        x1 = coded["x1"].values
        x2 = coded["x2"].values
        x3 = coded["x3"].values
        y = (
            5.0
            + 2.0 * x1 - 1.5 * x2 + 0.8 * x3
            + 1.2 * x1 * x2 - 0.5 * x1 * x3 + 0.3 * x2 * x3
            - 0.7 * x1**2 + 0.4 * x2**2 - 0.9 * x3**2
        )
        coded["y"] = y
        return coded

    def test_quadratic_fit(self):
        """Recover known coefficients from exact quadratic data (tol 1e-6)."""
        df = self._make_exact_quadratic_data()
        result = fit_quadratic_model(df, ["x1", "x2", "x3"], "y")

        # Build expected coefficient map
        expected = {
            "Intercept": 5.0,
            "x1": 2.0,
            "x2": -1.5,
            "x3": 0.8,
            "x1x2": 1.2,
            "x1x3": -0.5,
            "x2x3": 0.3,
            "x1^2": -0.7,
            "x2^2": 0.4,
            "x3^2": -0.9,
        }

        for coeff in result["coefficients"]:
            term = coeff["term"]
            self.assertIn(term, expected)
            self.assertAlmostEqual(
                coeff["coefficient"],
                expected[term],
                places=6,
                msg=f"Coefficient mismatch for term '{term}'",
            )


class ANOVAStructureTest(unittest.TestCase):
    def test_anova_structure(self):
        """Verify ANOVA output contains all required fields."""
        coded = generate_ccd_matrix(["A", "B", "C"], center_points=5)
        x1 = coded["A"].values
        x2 = coded["B"].values
        x3 = coded["C"].values
        coded["y"] = 3.0 + x1 + 0.5 * x2 - 0.3 * x1**2 + 0.1 * x2 * x3

        result = fit_quadratic_model(coded, ["A", "B", "C"], "y")
        anova = result["anova"]

        # Top-level ANOVA keys
        for key in ["model", "residual", "lack_of_fit", "pure_error", "total",
                     "R2", "adj_R2", "pred_R2", "alpha"]:
            self.assertIn(key, anova, msg=f"Missing ANOVA key: {key}")

        # Model sub-keys
        for key in ["SS", "df", "MS", "F", "p_value"]:
            self.assertIn(key, anova["model"], msg=f"Missing model key: {key}")

        # Lack-of-fit sub-keys
        for key in ["SS", "df", "MS", "F", "p_value"]:
            self.assertIn(key, anova["lack_of_fit"], msg=f"Missing lof key: {key}")

        # Pure error sub-keys
        for key in ["SS", "df", "MS"]:
            self.assertIn(key, anova["pure_error"], msg=f"Missing pure_error key: {key}")

        # Total sub-keys
        for key in ["SS", "df"]:
            self.assertIn(key, anova["total"], msg=f"Missing total key: {key}")

        # R² values should be numeric
        self.assertIsInstance(anova["R2"], float)
        self.assertIsInstance(anova["adj_R2"], float)
        self.assertIsInstance(anova["pred_R2"], float)

        # Coefficient table should have required fields
        for coeff in result["coefficients"]:
            for key in ["term", "coefficient", "SE", "t_value", "p_value"]:
                self.assertIn(key, coeff, msg=f"Missing coefficient key: {key}")


class OptimizeTest(unittest.TestCase):
    def test_optimize_returns_dict(self):
        """Verify optimization output contains required keys."""
        coded = generate_ccd_matrix(["A", "B", "C"], center_points=5)
        x1 = coded["A"].values
        x2 = coded["B"].values
        x3 = coded["C"].values
        # Simple quadratic with clear maximum near origin
        coded["y"] = 10.0 - x1**2 - x2**2 - x3**2

        result = optimize_rsm(coded, ["A", "B", "C"], "y", goal="max")

        self.assertIsInstance(result, dict)
        self.assertIn("optimal_coded", result)
        self.assertIn("predicted_response", result)
        self.assertIn("goal", result)
        self.assertEqual(result["goal"], "max")
        self.assertIsInstance(result["optimal_coded"], dict)
        self.assertIsInstance(result["predicted_response"], float)

        # Optimal should be near center (0,0,0) for this symmetric model
        for factor in ["A", "B", "C"]:
            self.assertAlmostEqual(result["optimal_coded"][factor], 0.0, places=3)
        self.assertAlmostEqual(result["predicted_response"], 10.0, places=3)


if __name__ == "__main__":
    unittest.main()

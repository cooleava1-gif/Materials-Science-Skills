import sys
import unittest
from pathlib import Path

import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = REPO_ROOT / "skills" / "materials-doe" / "scripts"

sys.path.insert(0, str(SCRIPTS_DIR))
from orthogonal_analysis import anova_analysis, predict_optimal, range_analysis


def _make_l9_data():
    factors = ["A", "B", "C"]
    rows = [
        {"A": 1, "B": 1, "C": 1, "y": 3.1},
        {"A": 1, "B": 2, "C": 2, "y": 5.4},
        {"A": 1, "B": 3, "C": 3, "y": 3.8},
        {"A": 2, "B": 1, "C": 2, "y": 6.2},
        {"A": 2, "B": 2, "C": 3, "y": 7.5},
        {"A": 2, "B": 3, "C": 1, "y": 5.1},
        {"A": 3, "B": 1, "C": 3, "y": 4.9},
        {"A": 3, "B": 2, "C": 1, "y": 8.3},
        {"A": 3, "B": 3, "C": 2, "y": 6.7},
    ]
    return pd.DataFrame(rows)


class OrthogonalAnalysisTest(unittest.TestCase):
    def test_range_analysis_identifies_most_influential_factor(self):
        df = _make_l9_data()
        result = range_analysis(df, ["A", "B", "C"], "y")
        factors = result["factors"]
        r_values = [f["R"] for f in factors]
        self.assertEqual(r_values, sorted(r_values, reverse=True))
        self.assertEqual(factors[0]["factor"], "A")

    def test_anova_produces_f_values(self):
        df = _make_l9_data()
        result = anova_analysis(df, ["A", "B", "C"], "y")
        for f in result["factors"]:
            self.assertIn("F", f)
            self.assertIn("significant", f)
            self.assertIsInstance(f["F"], float)
            self.assertIn(type(f["significant"]).__name__, ("bool", "bool_"))

    def test_predict_optimal_returns_valid_combination(self):
        df = _make_l9_data()
        result = predict_optimal(df, ["A", "B", "C"], "y", goal="max")
        self.assertIn("optimal_levels", result)
        self.assertIsInstance(result["optimal_levels"], dict)
        for factor in ["A", "B", "C"]:
            self.assertIn(factor, result["optimal_levels"])


if __name__ == "__main__":
    unittest.main()

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = SKILL_ROOT / "scripts"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AutomaticFigurePackageTest(unittest.TestCase):
    def test_skill_docs_expose_automatic_table_to_figure_loop(self):
        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8")
        manifest_text = (SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8")
        workflow_text = (SKILL_ROOT / "static" / "core" / "workflow.md").read_text(encoding="utf-8")
        readme_text = (SKILL_ROOT / "README.md").read_text(encoding="utf-8")
        reference_text = (SKILL_ROOT / "references" / "automatic-figure-package.md").read_text(encoding="utf-8")

        for phrase in [
            "data diagnosis -> chart recommendation -> SVG/PNG export -> QA report",
            "generate_figure_package.py",
            "figure_intake.yaml",
            "qa_report.md",
        ]:
            self.assertIn(phrase, workflow_text + readme_text + reference_text)

        self.assertIn("references/automatic-figure-package.md", manifest_text)
        self.assertIn("scripts/data_diagnose.py", manifest_text)
        self.assertIn("scripts/recommend_chart.py", manifest_text)
        self.assertIn("scripts/generate_figure_package.py", manifest_text)
        self.assertIn("automatic figure-package loop", skill_text)

    def test_data_diagnosis_and_chart_recommendation_for_dosage_table(self):
        data_diagnose = load_module("data_diagnose", SCRIPTS_ROOT / "data_diagnose.py")
        recommend_chart = load_module("recommend_chart", SCRIPTS_ROOT / "recommend_chart.py")

        with tempfile.TemporaryDirectory() as tmp:
            csv_path = Path(tmp) / "wer_bond_strength.csv"
            csv_path.write_text(
                "\n".join(
                    [
                        "WER content (%),Bond strength (MPa),SD,Condition",
                        "0,0.42,0.03,Dry",
                        "5,0.55,0.04,Dry",
                        "10,0.68,0.04,Dry",
                        "15,0.79,0.05,Dry",
                        "20,0.72,0.04,Dry",
                    ]
                ),
                encoding="utf-8",
            )

            profile = data_diagnose.diagnose_table(csv_path)
            recommendation = recommend_chart.recommend_chart(profile, goal="optimize WER dosage for bonding strength")

        self.assertEqual(profile.row_count, 5)
        self.assertIn("WER content (%)", profile.numeric_columns)
        self.assertIn("Bond strength (MPa)", profile.numeric_columns)
        self.assertEqual(profile.error_columns, ["SD"])
        self.assertEqual(profile.unit_map["Bond strength (MPa)"], "MPa")
        self.assertEqual(recommendation.chart_type, "errorbar_trend")
        self.assertIn("SVG", recommendation.export_formats)
        self.assertIn("replicate count", " ".join(recommendation.reviewer_risks).lower())

    def test_generate_figure_package_cli_exports_svg_png_and_qa_report(self):
        script = SCRIPTS_ROOT / "generate_figure_package.py"
        audit_script = SCRIPTS_ROOT / "audit_figure_package.py"

        with tempfile.TemporaryDirectory() as tmp:
            input_csv = Path(tmp) / "wer_bond_strength.csv"
            input_csv.write_text(
                "\n".join(
                    [
                        "WER content (%),Bond strength (MPa),SD,Condition",
                        "0,0.42,0.03,Dry",
                        "5,0.55,0.04,Dry",
                        "10,0.68,0.04,Dry",
                        "15,0.79,0.05,Dry",
                        "20,0.72,0.04,Dry",
                    ]
                ),
                encoding="utf-8",
            )
            package_dir = Path(tmp) / "package"
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--data",
                    str(input_csv),
                    "--output-dir",
                    str(package_dir),
                    "--goal",
                    "Show the optimum WER dosage window for bonding strength.",
                    "--figure-name",
                    "wer_bond_strength",
                    "--json",
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            payload = json.loads(result.stdout)

            self.assertEqual(payload["status"], "pass")
            self.assertEqual(payload["recommendation"]["chart_type"], "errorbar_trend")
            for relative in [
                "figure_intake.yaml",
                "source_data.csv",
                "plot.py",
                "materials_plot_lib.py",
                "figure.svg",
                "figure.png",
                "figure.pdf",
                "figure.tiff",
                "caption.md",
                "qa_report.md",
                "asset_manifest.md",
                "figure_contract.md",
            ]:
                self.assertTrue((package_dir / relative).exists(), f"{relative} should be generated")

            svg_text = (package_dir / "figure.svg").read_text(encoding="utf-8")
            plot_text = (package_dir / "plot.py").read_text(encoding="utf-8")
            qa_text = (package_dir / "qa_report.md").read_text(encoding="utf-8")
            contract_text = (package_dir / "figure_contract.md").read_text(encoding="utf-8")
            audit = subprocess.run(
                [sys.executable, str(audit_script), "--package-dir", str(package_dir), "--json"],
                check=True,
                capture_output=True,
                text=True,
            )
            audit_payload = json.loads(audit.stdout)

        self.assertIn("<svg", svg_text)
        self.assertNotIn("skills\\\\materials-figure\\\\scripts", plot_text)
        self.assertNotIn("skills/materials-figure/scripts", plot_text)
        self.assertIn("## Data Check", qa_text)
        self.assertIn("## Chart Choice Check", qa_text)
        self.assertIn("QA Status", qa_text)
        self.assertIn("errorbar_trend", qa_text)
        self.assertIn("Core Conclusion", contract_text)
        self.assertEqual(audit_payload["status"], "pass")

    def test_generator_renders_grouped_bar_and_correlation_heatmap_recommendations(self):
        script = SCRIPTS_ROOT / "generate_figure_package.py"

        with tempfile.TemporaryDirectory() as tmp:
            grouped_csv = Path(tmp) / "grouped.csv"
            grouped_csv.write_text(
                "\n".join(
                    [
                        "Condition,Bond strength (MPa)",
                        "Control,0.42",
                        "10% WER,0.62",
                        "15% WER,0.79",
                    ]
                ),
                encoding="utf-8",
            )
            grouped_package = Path(tmp) / "grouped-package"
            grouped_result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--data",
                    str(grouped_csv),
                    "--output-dir",
                    str(grouped_package),
                    "--goal",
                    "Compare bonding strength across material conditions.",
                    "--figure-name",
                    "grouped_strength",
                    "--json",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            grouped_payload = json.loads(grouped_result.stdout)

            corr_csv = Path(tmp) / "correlation.csv"
            corr_csv.write_text(
                "\n".join(
                    [
                        "Bond strength (MPa),Retention (%),Viscosity (mPa s),Curing time (d)",
                        "0.42,64,220,1",
                        "0.55,72,280,3",
                        "0.68,84,340,7",
                        "0.79,88,390,14",
                    ]
                ),
                encoding="utf-8",
            )
            corr_package = Path(tmp) / "corr-package"
            corr_result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--data",
                    str(corr_csv),
                    "--output-dir",
                    str(corr_package),
                    "--goal",
                    "Screen correlations among measured material properties.",
                    "--figure-name",
                    "property_correlation",
                    "--json",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            corr_payload = json.loads(corr_result.stdout)

            self.assertEqual(grouped_payload["recommendation"]["chart_type"], "grouped_bar")
            self.assertEqual(corr_payload["recommendation"]["chart_type"], "correlation_heatmap")
            for package in [grouped_package, corr_package]:
                self.assertTrue((package / "figure.svg").exists())
            self.assertTrue((package / "figure.png").exists())
            self.assertIn("<svg", (package / "figure.svg").read_text(encoding="utf-8"))

    def test_generator_renders_replicate_groups_as_boxplot_points(self):
        script = SCRIPTS_ROOT / "generate_figure_package.py"

        with tempfile.TemporaryDirectory() as tmp:
            replicate_csv = Path(tmp) / "replicates.csv"
            replicate_csv.write_text(
                "\n".join(
                    [
                        "Condition,Bond strength (MPa)",
                        "Control,0.39",
                        "Control,0.42",
                        "Control,0.44",
                        "15% WER,0.74",
                        "15% WER,0.79",
                        "15% WER,0.81",
                    ]
                ),
                encoding="utf-8",
            )
            package = Path(tmp) / "replicate-package"
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--data",
                    str(replicate_csv),
                    "--output-dir",
                    str(package),
                    "--goal",
                    "Compare replicate bonding strength distributions.",
                    "--figure-name",
                    "replicate_strength",
                    "--json",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            payload = json.loads(result.stdout)
            svg_exists = (package / "figure.svg").exists()
            png_exists = (package / "figure.png").exists()
            qa_text = (package / "qa_report.md").read_text(encoding="utf-8")

        self.assertEqual(payload["recommendation"]["chart_type"], "boxplot_points")
        self.assertTrue(svg_exists)
        self.assertTrue(png_exists)
        self.assertIn("boxplot_points", qa_text)


if __name__ == "__main__":
    unittest.main()

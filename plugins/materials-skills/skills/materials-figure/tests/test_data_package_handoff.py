import sys
import tempfile
import unittest
from pathlib import Path

import yaml


FIGURE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(FIGURE_ROOT / "scripts"))

from data_package_to_figure_handoff import generate_figure_package


def _make_fair_package(tmpdir: Path) -> Path:
    """Create a minimal FAIR package for testing."""
    dataset_dir = tmpdir / "test_fair_package"
    raw_dir = dataset_dir / "raw_data"
    processed_dir = dataset_dir / "processed_data"
    figures_dir = dataset_dir / "figures"
    for directory in (raw_dir, processed_dir, figures_dir):
        directory.mkdir(parents=True, exist_ok=True)

    (raw_dir / "experiment_data_template.csv").write_text(
        "run_id,temperature,additive,strength,replicate_count,notes\n", encoding="utf-8"
    )
    (dataset_dir / "metadata.md").write_text(
        "# Dataset Metadata\n\n- topic: Test sintering\n- design_type: L9\n", encoding="utf-8"
    )
    (dataset_dir / "README.md").write_text("# README\n", encoding="utf-8")
    (dataset_dir / "data_availability_statement.md").write_text("# Statement\n", encoding="utf-8")
    (dataset_dir / "fair_audit.md").write_text("# Audit\n", encoding="utf-8")

    record_path = tmpdir / "experiment-record.yaml"
    record = {
        "version": "1.0.0",
        "record_type": "experiment-design",
        "study_id": "test-001",
        "title": "Test sintering",
        "created_by": "materials-doe",
        "created_at": "2026-07-04",
        "direction_profile": {"material_family": "ceramics", "domain": "ceramics", "application": ""},
        "objectives": [{"description": "maximize strength", "response_variable": "strength", "optimization": "maximize"}],
        "response_variables": [{"name": "strength", "unit": "MPa", "measurement_method": "tensile", "replicate_count": 3}],
        "factors": [
            {"name": "temperature", "unit": "degC", "type": "continuous", "levels": [1400, 1500, 1600]},
            {"name": "additive", "unit": "wt%", "type": "continuous", "levels": [0, 1, 2]},
        ],
        "design": {"type": "L9", "runs": []},
        "materials": [],
        "processing": [],
        "characterization": [],
        "evidence_links": [],
        "terminology": [],
    }
    record_path.write_text(yaml.safe_dump(record, sort_keys=False, allow_unicode=True), encoding="utf-8")

    (dataset_dir / "experiment_record_link.yaml").write_text(
        f"source_record_path: {record_path}\nrecord_version: 1.0.0\n", encoding="utf-8"
    )
    return dataset_dir


class DataPackageHandoffTest(unittest.TestCase):
    def test_generate_figure_package_from_fair_package(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dataset_dir = _make_fair_package(Path(tmpdir))
            output_dir = Path(tmpdir) / "figures"
            package_dir = generate_figure_package(
                dataset_dir=dataset_dir,
                output_dir=output_dir,
                claim="Temperature and additive jointly affect strength.",
            )

            self.assertTrue(package_dir.exists())
            for fname in ("figure_storyboard.yaml", "figure_contract.md", "caption_boundary.md", "figure_qa_report.md", "source_data.csv", "plot.py", "README.md"):
                self.assertTrue((package_dir / fname).exists(), f"missing {fname}")

            storyboard = yaml.safe_load((package_dir / "figure_storyboard.yaml").read_text(encoding="utf-8"))
            self.assertEqual(len(storyboard["panels"]), 1)
            self.assertEqual(storyboard["panels"][0]["title"], "Effect on strength")
            self.assertIn("temperature", storyboard["panels"][0]["claim"])

    def test_generated_markdown_scaffold_uses_ascii_punctuation(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dataset_dir = _make_fair_package(Path(tmpdir))
            output_dir = Path(tmpdir) / "figures"
            package_dir = generate_figure_package(
                dataset_dir=dataset_dir,
                output_dir=output_dir,
                claim="Temperature affects strength.",
            )

            for fname in ("README.md", "figure_contract.md", "figure_qa_report.md"):
                text = (package_dir / fname).read_text(encoding="utf-8")
                try:
                    text.encode("ascii")
                except UnicodeEncodeError as exc:
                    self.fail(f"{fname} contains non-ASCII punctuation: {exc}")

    def test_script_entrypoint_runs(self):
        import subprocess
        import sys

        with tempfile.TemporaryDirectory() as tmpdir:
            dataset_dir = _make_fair_package(Path(tmpdir))
            output_dir = Path(tmpdir) / "figures"
            result = subprocess.run(
                [
                    sys.executable,
                    str(FIGURE_ROOT / "scripts" / "data_package_to_figure_handoff.py"),
                    "--dataset-dir",
                    str(dataset_dir),
                    "--output-dir",
                    str(output_dir),
                    "--claim",
                    "Temperature affects strength.",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output_dir.exists())


if __name__ == "__main__":
    unittest.main()

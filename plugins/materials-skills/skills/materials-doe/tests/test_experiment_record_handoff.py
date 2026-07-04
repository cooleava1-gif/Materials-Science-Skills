import sys
import tempfile
import unittest
from pathlib import Path

import yaml


DOE_ROOT = Path(__file__).resolve().parents[1]
PLAN_CSV = DOE_ROOT / "assets" / "templates" / "experiment-plan-template.csv"
sys.path.insert(0, str(DOE_ROOT / "scripts"))

import doe_plan_to_experiment_record as handoff_module
from doe_plan_to_experiment_record import build_record


class ExperimentRecordHandoffTest(unittest.TestCase):
    def test_default_schema_path_resolves_to_shared_core_schema(self):
        self.assertTrue(handoff_module.DEFAULT_SCHEMA.exists())
        self.assertEqual(handoff_module.DEFAULT_SCHEMA.name, "experiment-record-schema.yaml")

    def test_build_record_from_plan_csv(self):
        record = build_record(
            plan_csv=PLAN_CSV,
            study_id="ceramics-sintering-001",
            title="Ceramics sintering optimization",
            material_family="ceramics",
            domain="ceramics",
            application="structural ceramics",
            design_type="L9",
            factor_specs=[
                {"name": "sintering_temperature", "unit": "degC", "type": "continuous"},
                {"name": "additive_content", "unit": "wt%", "type": "continuous"},
                {"name": "heating_rate", "unit": "degC/min", "type": "continuous"},
                {"name": "dwell_time", "unit": "min", "type": "continuous"},
            ],
            response_specs=[
                {"name": "bulk_density", "unit": "g/cm3", "measurement_method": "Archimedes", "replicate_count": 3}
            ],
            factor_cols=None,
            response_cols=None,
            created_by="materials-doe",
            created_at="2026-07-04",
        )
        self.assertEqual(record["version"], "1.0.0")
        self.assertEqual(record["study_id"], "ceramics-sintering-001")
        self.assertEqual(len(record["design"]["runs"]), 9)
        self.assertEqual(
            [f["name"] for f in record["factors"]],
            ["sintering_temperature", "additive_content", "heating_rate", "dwell_time"],
        )
        self.assertEqual([r["name"] for r in record["response_variables"]], ["bulk_density"])
        self.assertEqual(record["design"]["runs"][0]["run_id"], "1")

    def test_response_specs_must_match_response_columns(self):
        with self.assertRaisesRegex(SystemExit, "--responses length"):
            build_record(
                plan_csv=PLAN_CSV,
                study_id="ceramics-sintering-001",
                title="Ceramics sintering optimization",
                material_family="ceramics",
                domain="ceramics",
                application="structural ceramics",
                design_type="L9",
                factor_specs=[
                    {"name": "sintering_temperature", "unit": "degC", "type": "continuous"},
                    {"name": "additive_content", "unit": "wt%", "type": "continuous"},
                    {"name": "heating_rate", "unit": "degC/min", "type": "continuous"},
                    {"name": "dwell_time", "unit": "min", "type": "continuous"},
                ],
                response_specs=[
                    {"name": "bulk_density", "unit": "g/cm3", "measurement_method": "Archimedes", "replicate_count": 3}
                ],
                factor_cols=None,
                response_cols=["response_1", "response_2"],
                created_by="materials-doe",
                created_at="2026-07-04",
            )

    def test_l9_design_type_is_canonicalized_for_schema(self):
        record = build_record(
            plan_csv=PLAN_CSV,
            study_id="ceramics-sintering-001",
            title="Ceramics sintering optimization",
            material_family="ceramics",
            domain="ceramics",
            application="structural ceramics",
            design_type="L9",
            factor_specs=[
                {"name": "sintering_temperature", "unit": "degC", "type": "continuous"},
                {"name": "additive_content", "unit": "wt%", "type": "continuous"},
                {"name": "heating_rate", "unit": "degC/min", "type": "continuous"},
                {"name": "dwell_time", "unit": "min", "type": "continuous"},
            ],
            response_specs=[
                {"name": "bulk_density", "unit": "g/cm3", "measurement_method": "Archimedes", "replicate_count": 3}
            ],
            factor_cols=None,
            response_cols=None,
            created_by="materials-doe",
            created_at="2026-07-04",
        )

        self.assertEqual(record["design"]["type"], "Taguchi")
        self.assertIn("L9", record["design"]["notes"])

    def test_script_entrypoint_writes_valid_yaml(self):
        import subprocess
        import sys

        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "record.yaml"
            result = subprocess.run(
                [
                    sys.executable,
                    str(DOE_ROOT / "scripts" / "doe_plan_to_experiment_record.py"),
                    "--plan-csv",
                    str(PLAN_CSV),
                    "--output",
                    str(output),
                    "--study-id",
                    "test-001",
                    "--title",
                    "Test",
                    "--material-family",
                    "ceramics",
                    "--domain",
                    "ceramics",
                    "--design-type",
                    "L9",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue(output.exists())
            record = yaml.safe_load(output.read_text(encoding="utf-8"))
            self.assertEqual(record["study_id"], "test-001")


if __name__ == "__main__":
    unittest.main()

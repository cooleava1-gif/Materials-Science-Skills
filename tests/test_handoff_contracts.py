"""Test handoff contract validator."""
import json
import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
VALIDATOR = SCRIPTS_DIR / "validate_handoffs.py"
RELEASE_CHECK = SCRIPTS_DIR / "run_release_checks.py"


def _load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_handoffs", VALIDATOR)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class HandoffContractValidatorTest(unittest.TestCase):
    def test_validator_runs_without_error(self):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "--json"],
            capture_output=True, text=True, check=True,
        )
        report = json.loads(result.stdout)
        self.assertIn("status", report)

    def test_validator_passes_on_current_state(self):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "--json"],
            capture_output=True, text=True, check=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "pass")

    def test_validator_discovers_doe_handoff_from_manifests(self):
        validator = _load_validator_module()
        topology = validator.collect_manifest_handoff_topology()

        self.assertIn("materials-doe", topology["provides_by_skill"])
        self.assertIn("doe-handoff", topology["provides_by_skill"]["materials-doe"])
        self.assertEqual(
            "materials-doe",
            topology["provider_by_handoff"]["doe-handoff"],
        )
        self.assertGreaterEqual(
            topology["consumers_by_handoff"].get("doe-handoff", set()),
            {"materials-writing", "materials-figure", "materials-data", "materials-research"},
        )

    def test_self_consumed_handoffs_are_declared_in_contracts_not_special_cased(self):
        validator_text = VALIDATOR.read_text(encoding="utf-8")
        validator = _load_validator_module()
        topology = validator.collect_manifest_handoff_topology()
        gate_report = validator.load_contract("gate-report")

        self.assertNotIn("SELF_CONSUMED_HANDOFFS", validator_text)
        self.assertIsNotNone(gate_report)
        self.assertIn("materials-research", gate_report["consumed_by"])
        self.assertIn(
            "materials-research",
            topology["consumers_by_handoff"].get("gate-report", set()),
        )

    def test_release_check_includes_handoff_validation(self):
        result = subprocess.run(
            [sys.executable, str(RELEASE_CHECK), "--json"],
            capture_output=True, text=True, check=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "pass")


if __name__ == "__main__":
    unittest.main()

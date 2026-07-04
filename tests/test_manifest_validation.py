"""Test manifest and eval contract validation."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = SCRIPTS_DIR / "validate_manifest.py"


def _load_release_checks_module():
    sys.path.insert(0, str(SCRIPTS_DIR))
    try:
        spec = importlib.util.spec_from_file_location(
            "run_release_checks", SCRIPTS_DIR / "run_release_checks.py"
        )
        module = importlib.util.module_from_spec(spec)
        assert spec and spec.loader
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.pop(0)


class ManifestValidationTest(unittest.TestCase):
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

    def test_reader_has_no_dangling_references(self):
        result = subprocess.run(
            [sys.executable, str(VALIDATOR), "--skill", "materials-reader", "--json"],
            capture_output=True, text=True, check=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "pass")

    def test_release_check_includes_manifest_validation(self):
        release = SCRIPTS_DIR / "run_release_checks.py"
        result = subprocess.run(
            [sys.executable, str(release), "--json"],
            capture_output=True, text=True, check=True,
        )
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "pass")

    def test_release_check_includes_eval_contract_validation(self):
        release_text = (SCRIPTS_DIR / "run_release_checks.py").read_text(encoding="utf-8")
        self.assertIn("collect_eval_contract_issues", release_text)
        self.assertIn("eval_contract", release_text)

    def test_eval_contract_validator_flags_malformed_eval_file(self):
        release_checks = _load_release_checks_module()
        with tempfile.TemporaryDirectory() as tmp:
            skills_root = Path(tmp)
            skill_dir = skills_root / "materials-fake"
            evals_dir = skill_dir / "evals"
            evals_dir.mkdir(parents=True)
            (skill_dir / "manifest.yaml").write_text("version: '0.0.1'\n", encoding="utf-8")
            (evals_dir / "evals.json").write_text(
                json.dumps(
                    {
                        "skill_name": "materials-wrong",
                        "evals": [
                            {
                                "id": "missing-prompt",
                                "expected_output": "x",
                                "assertions": [],
                                "files": [],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )

            issues = release_checks.collect_eval_contract_issues(skills_root)

        self.assertTrue(issues)
        self.assertTrue(any("materials-fake" in issue for issue in issues), issues)

    def test_eval_contract_validator_passes_for_current_repo_state(self):
        release_checks = _load_release_checks_module()
        issues = release_checks.collect_eval_contract_issues(
            REPO_ROOT / "plugins" / "materials-skills" / "skills"
        )
        self.assertEqual([], issues)


if __name__ == "__main__":
    unittest.main()

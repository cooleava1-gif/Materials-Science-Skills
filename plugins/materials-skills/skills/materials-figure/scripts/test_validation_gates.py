"""Deterministic regression tests for the materials-figure validation gates."""

from __future__ import annotations

import argparse
import csv
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

import yaml


SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

try:
    import run_validation_gates
except ModuleNotFoundError:
    run_validation_gates = None  # type: ignore[assignment]


def write_storyboard(
    path: Path,
    *,
    valid: bool = True,
    warning: bool = False,
) -> None:
    payload: dict[str, object] = {
        "title": "Deterministic validation-gate regression",
        "manuscript_type": "review",
        "target_journal": "cbm",
        "narrative_arc": [
            {
                "figure_id": "fig1",
                "figure_name": "System overview",
                "role": "establish_system",
                "claim": "The review establishes the material system.",
                "contract_path": "fig1/figure_contract.md",
                "evidence_depends_on": [],
            },
            {
                "figure_id": "fig2",
                "figure_name": "Evidence summary",
                "role": "summarize",
                "claim": "The evidence supports a bounded summary.",
                "contract_path": "fig2/figure_contract.md",
                "evidence_depends_on": ["fig1"],
            },
        ],
        "cross_figure_constraints": [
            {"type": "style_consistency", "shared_palette": "cbm"}
        ],
        "validation": {
            "min_figures": 1,
            "max_figures": 12,
            "allow_cycles": False,
        },
    }
    if not valid:
        payload.pop("narrative_arc")
    elif warning:
        payload["narrative_arc"] = payload["narrative_arc"][:1]
    path.write_text(yaml.safe_dump(payload, sort_keys=False), encoding="utf-8")


def write_package(path: Path, *, invalid_material_claim: bool = False) -> None:
    path.mkdir(parents=True, exist_ok=True)
    with (path / "source_data.csv").open("w", encoding="utf-8", newline="") as handle:
        if invalid_material_claim:
            writer = csv.DictWriter(handle, fieldnames=["two_theta", "phase"])
            writer.writeheader()
            writer.writerow({"two_theta": "30.2", "phase": "Al2O3"})
        else:
            writer = csv.DictWriter(handle, fieldnames=["note"])
            writer.writeheader()
            writer.writerow({"note": "no material claim"})


class ValidationGateTests(unittest.TestCase):
    def require_runner(self):
        self.assertIsNotNone(
            run_validation_gates,
            "run_validation_gates.py must provide the deterministic coordinator",
        )
        return run_validation_gates

    def test_both_gates_pass_in_fixed_order(self) -> None:
        runner = self.require_runner()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            storyboard = root / "figure_storyboard.yaml"
            package_a = root / "z-package"
            package_b = root / "a-package"
            write_storyboard(storyboard)
            write_package(package_a)
            write_package(package_b)

            report = runner.run_validation_gates(
                storyboard_path=storyboard,
                package_dirs=[package_a, package_b, package_a],
            )

        self.assertEqual(report["status"], "pass")
        self.assertEqual(
            report["execution_order"],
            ["storyboard", "materials_claims"],
        )
        self.assertEqual(
            [gate["gate"] for gate in report["gates"]],
            ["storyboard", "materials_claims"],
        )
        self.assertEqual(report["gates"][0]["status"], "pass")
        self.assertEqual(report["gates"][1]["status"], "pass")
        self.assertEqual(
            [package["package"] for package in report["gates"][1]["packages"]],
            sorted(
                [
                    package_a.resolve().as_posix(),
                    package_b.resolve().as_posix(),
                ],
                key=str.casefold,
            ),
        )

    def test_cli_json_reports_both_gates_pass(self) -> None:
        runner = self.require_runner()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            storyboard = root / "figure_storyboard.yaml"
            package = root / "fig1"
            write_storyboard(storyboard)
            write_package(package)
            stdout = StringIO()
            stderr = StringIO()

            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = runner.main(
                    [
                        "--storyboard",
                        str(storyboard),
                        "--package-dir",
                        str(package),
                        "--json",
                    ]
                )

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr.getvalue(), "")
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["status"], "pass")
        self.assertEqual(payload["exit_code"], 0)

    def test_storyboard_failure_short_circuits_materials_gate(self) -> None:
        runner = self.require_runner()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            storyboard = root / "figure_storyboard.yaml"
            package = root / "fig1"
            write_storyboard(storyboard, valid=False)
            write_package(package, invalid_material_claim=True)

            report = runner.run_validation_gates(
                storyboard_path=storyboard,
                package_dirs=[package],
            )

        self.assertEqual(report["status"], "error")
        self.assertEqual(report["gates"][0]["status"], "error")
        self.assertEqual(report["gates"][1]["status"], "skipped")
        self.assertFalse(report["gates"][1]["executed"])
        self.assertEqual(report["gates"][1]["reason"], "storyboard gate failed")

    def test_materials_failure_is_reported_after_storyboard(self) -> None:
        runner = self.require_runner()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            storyboard = root / "figure_storyboard.yaml"
            package = root / "fig1"
            write_storyboard(storyboard)
            write_package(package, invalid_material_claim=True)

            report = runner.run_validation_gates(
                storyboard_path=storyboard,
                package_dirs=[package],
            )

        materials_gate = report["gates"][1]
        self.assertEqual(report["status"], "error")
        self.assertEqual(report["gates"][0]["status"], "pass")
        self.assertEqual(materials_gate["status"], "error")
        self.assertEqual(materials_gate["packages"][0]["status"], "error")
        self.assertEqual(materials_gate["packages"][0]["exit_code"], 2)
        self.assertIn(
            "xrd_peak_phase_mismatch",
            {issue["rule"] for issue in materials_gate["packages"][0]["errors"]},
        )

    def test_cli_json_reports_materials_failure(self) -> None:
        runner = self.require_runner()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            storyboard = root / "figure_storyboard.yaml"
            package = root / "fig1"
            write_storyboard(storyboard)
            write_package(package, invalid_material_claim=True)
            stdout = StringIO()
            stderr = StringIO()

            with redirect_stdout(stdout), redirect_stderr(stderr):
                exit_code = runner.main(
                    [
                        "--storyboard",
                        str(storyboard),
                        "--package-dir",
                        str(package),
                        "--json",
                    ]
                )

        self.assertEqual(exit_code, 2)
        self.assertEqual(stderr.getvalue(), "")
        payload = json.loads(stdout.getvalue())
        self.assertEqual(payload["status"], "error")
        self.assertEqual(payload["exit_code"], 2)
        self.assertEqual(payload["gates"][1]["status"], "error")

    def test_storyboard_warning_does_not_skip_materials_gate(self) -> None:
        runner = self.require_runner()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            storyboard = root / "figure_storyboard.yaml"
            package = root / "fig1"
            write_storyboard(storyboard, warning=True)
            write_package(package)

            report = runner.run_validation_gates(
                storyboard_path=storyboard,
                package_dirs=[package],
            )

        self.assertEqual(report["status"], "warning")
        self.assertEqual(report["gates"][0]["status"], "warning")
        self.assertEqual(report["gates"][1]["status"], "pass")
        self.assertTrue(report["gates"][1]["executed"])

    def test_storyboard_warning_and_materials_failure_are_both_reported(self) -> None:
        runner = self.require_runner()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            storyboard = root / "figure_storyboard.yaml"
            package = root / "fig1"
            write_storyboard(storyboard, warning=True)
            write_package(package, invalid_material_claim=True)

            report = runner.run_validation_gates(
                storyboard_path=storyboard,
                package_dirs=[package],
            )

        self.assertEqual(report["status"], "error")
        self.assertEqual(report["gates"][0]["status"], "warning")
        self.assertEqual(report["gates"][1]["status"], "error")
        self.assertTrue(report["gates"][1]["executed"])

    def test_missing_storyboard_is_structured_and_short_circuits(self) -> None:
        runner = self.require_runner()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "fig1"
            write_package(package)

            report = runner.run_validation_gates(
                storyboard_path=root / "missing.yaml",
                package_dirs=[package],
            )

        self.assertEqual(report["status"], "error")
        self.assertEqual(report["gates"][0]["status"], "error")
        self.assertEqual(report["gates"][0]["checks"][0]["check"], "load")
        self.assertEqual(report["gates"][1]["status"], "skipped")

    def test_storyboard_read_exception_is_structured(self) -> None:
        runner = self.require_runner()
        with tempfile.TemporaryDirectory() as directory:
            storyboard = Path(directory) / "invalid-encoding.yaml"
            storyboard.write_bytes(b"\xff\xfe\x00")

            report = runner.run_validation_gates(storyboard_path=storyboard)

        self.assertEqual(report["status"], "error")
        self.assertEqual(report["gates"][0]["checks"][0]["check"], "load")
        self.assertIn(
            "storyboard load failed",
            report["gates"][0]["checks"][0]["message"],
        )

    def test_loadable_malformed_storyboard_is_structured(self) -> None:
        runner = self.require_runner()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            storyboard = root / "malformed-storyboard.yaml"
            storyboard.write_text(
                "narrative_arc: []\nvalidation: invalid\n",
                encoding="utf-8",
            )
            report = runner.run_validation_gates(
                storyboard_path=storyboard,
                package_dirs=[root / "missing-package"],
            )

        self.assertEqual(report["status"], "error")
        self.assertEqual(report["gates"][0]["status"], "error")
        self.assertEqual(report["gates"][0]["checks"][0]["check"], "validation")
        self.assertIn(
            "storyboard validation failed",
            report["gates"][0]["checks"][0]["message"],
        )
        self.assertEqual(report["gates"][1]["status"], "skipped")

    def test_missing_package_and_empty_inputs_are_structured(self) -> None:
        runner = self.require_runner()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            storyboard = root / "figure_storyboard.yaml"
            write_storyboard(storyboard)

            missing_package_report = runner.run_validation_gates(
                storyboard_path=storyboard,
                package_dirs=[root / "missing-package"],
            )
            empty_report = runner.run_validation_gates()

        self.assertEqual(missing_package_report["status"], "error")
        package_result = missing_package_report["gates"][1]["packages"][0]
        self.assertEqual(package_result["status"], "error")
        self.assertEqual(package_result["errors"][0]["rule"], "package_files_missing")
        self.assertEqual(empty_report["status"], "error")
        self.assertIn("at least one validation input", empty_report["issues"][0])


TEST_CASES = {
    "both-pass": "test_both_gates_pass_in_fixed_order",
    "cli-both-pass": "test_cli_json_reports_both_gates_pass",
    "cli-materials-fail": "test_cli_json_reports_materials_failure",
    "storyboard-fail": "test_storyboard_failure_short_circuits_materials_gate",
    "materials-fail": "test_materials_failure_is_reported_after_storyboard",
    "storyboard-warning": "test_storyboard_warning_does_not_skip_materials_gate",
    "warning-materials-fail": "test_storyboard_warning_and_materials_failure_are_both_reported",
    "storyboard-load-error": "test_storyboard_read_exception_is_structured",
    "input-errors": "test_missing_package_and_empty_inputs_are_structured",
    "all": None,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", choices=sorted(TEST_CASES), default="all")
    args = parser.parse_args(argv)

    if args.case == "all":
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(ValidationGateTests)
    else:
        suite = unittest.TestSuite(
            [ValidationGateTests(TEST_CASES[args.case])]  # type: ignore[arg-type]
        )

    result = unittest.TextTestRunner(verbosity=1).run(suite)
    if result.wasSuccessful():
        print(f"PASS {args.case}")
        return 0
    print(f"FAIL {args.case}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())

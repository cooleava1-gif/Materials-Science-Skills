#!/usr/bin/env python3
"""Run the deterministic materials-figure validation gates in a fixed order."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Iterable

import check_storyboard
import validate_materials_claims


GATE_ORDER = ("storyboard", "materials_claims")
STATUS_EXIT_CODES = {"pass": 0, "warning": 1, "error": 2}


def _coerce_path(value: object, label: str) -> Path:
    if isinstance(value, Path):
        raw = value
    elif isinstance(value, str) and value.strip():
        raw = Path(value)
    else:
        raise ValueError(f"{label} must be a non-empty path")
    return raw.expanduser().resolve()


def _normalise_package_paths(
    package_dirs: Iterable[Path | str] | Path | str | None,
) -> tuple[list[Path], str | None]:
    if package_dirs is None:
        return [], None
    if isinstance(package_dirs, (Path, str)):
        raw_values = [package_dirs]
    else:
        try:
            raw_values = list(package_dirs)
        except TypeError as exc:
            return [], f"package_dirs must be an iterable of paths: {exc}"

    paths: dict[str, Path] = {}
    for value in raw_values:
        try:
            path = _coerce_path(value, "package directory")
        except ValueError as exc:
            return [], str(exc)
        paths.setdefault(path.as_posix().casefold(), path)
    return sorted(paths.values(), key=lambda path: path.as_posix().casefold()), None


def _empty_report() -> dict[str, object]:
    return {
        "status": "pass",
        "exit_code": 0,
        "gate_order": list(GATE_ORDER),
        "execution_order": [],
        "gates": [],
        "issues": [],
    }


def _skipped_gate(gate: str, reason: str) -> dict[str, object]:
    return {
        "gate": gate,
        "status": "skipped",
        "executed": False,
        "exit_code": None,
        "reason": reason,
        "checks": [],
    }


def _issue_dict(issue: object) -> dict[str, object]:
    severity = getattr(issue, "severity", None)
    severity_value = getattr(severity, "value", str(severity))
    return {
        "rule": getattr(issue, "rule", "unknown"),
        "severity": severity_value,
        "message": getattr(issue, "message", str(issue)),
        "row": getattr(issue, "row", None),
        "context": dict(getattr(issue, "context", {}) or {}),
    }


def _gate_status(statuses: Iterable[str]) -> str:
    values = list(statuses)
    if "error" in values:
        return "error"
    if "warning" in values:
        return "warning"
    return "pass"


def _gate_messages(gate: dict[str, object]) -> list[str]:
    messages: list[str] = []
    gate_name = str(gate["gate"])
    for check in gate.get("checks", []):
        if not isinstance(check, dict):
            continue
        if check.get("result") in {"error", "warning"}:
            messages.append(
                f"{gate_name}:{check.get('check', 'check')}:"
                f"{check.get('message', 'validation issue')}"
            )
    for package in gate.get("packages", []):
        if not isinstance(package, dict):
            continue
        package_name = package.get("package", "<package>")
        for issue in package.get("errors", []) + package.get("warnings", []):
            if isinstance(issue, dict):
                messages.append(
                    f"{gate_name}:{package_name}:{issue.get('rule', 'check')}:"
                    f"{issue.get('message', 'validation issue')}"
                )
    return messages


def _finalise(report: dict[str, object]) -> dict[str, object]:
    gates = report.get("gates", [])
    statuses = [
        str(gate.get("status"))
        for gate in gates
        if isinstance(gate, dict) and gate.get("status") != "skipped"
    ]
    status = _gate_status(statuses) if statuses else "error"
    report["status"] = status
    report["exit_code"] = STATUS_EXIT_CODES[status]

    issues = list(report.get("issues", []))
    for gate in gates:
        if isinstance(gate, dict):
            issues.extend(_gate_messages(gate))
    report["issues"] = issues
    return report


def _run_storyboard_gate(
    report: dict[str, object],
    storyboard_path: object,
) -> dict[str, object]:
    try:
        path = _coerce_path(storyboard_path, "storyboard")
    except ValueError as exc:
        gate = {
            "gate": "storyboard",
            "status": "error",
            "executed": False,
            "exit_code": 2,
            "input": str(storyboard_path),
            "checks": [
                {"check": "input", "result": "error", "message": str(exc)}
            ],
        }
        report["gates"].append(gate)
        return gate

    try:
        storyboard, load_error = check_storyboard.load_storyboard(path)
    except Exception as exc:
        storyboard, load_error = None, f"storyboard load failed: {exc}"
    if load_error is not None:
        gate = {
            "gate": "storyboard",
            "status": "error",
            "executed": True,
            "exit_code": 2,
            "input": path.as_posix(),
            "checks": [
                {"check": "load", "result": "error", "message": load_error}
            ],
        }
        report["execution_order"].append("storyboard")
        report["gates"].append(gate)
        return gate

    try:
        checks = check_storyboard.run_checks(storyboard, path.parent)
    except Exception as exc:
        gate = {
            "gate": "storyboard",
            "status": "error",
            "executed": True,
            "exit_code": 2,
            "input": path.as_posix(),
            "checks": [
                {
                    "check": "validation",
                    "result": "error",
                    "message": f"storyboard validation failed: {exc}",
                }
            ],
        }
        report["execution_order"].append("storyboard")
        report["gates"].append(gate)
        return gate

    status = check_storyboard.aggregate_status(checks)
    gate = {
        "gate": "storyboard",
        "status": status,
        "executed": True,
        "exit_code": check_storyboard.exit_code_for(status),
        "input": path.as_posix(),
        "checks": checks,
    }
    report["execution_order"].append("storyboard")
    report["gates"].append(gate)
    return gate


def _run_materials_gate(
    report: dict[str, object],
    package_paths: list[Path],
    input_issue: str | None,
) -> dict[str, object]:
    if input_issue is not None:
        gate = {
            "gate": "materials_claims",
            "status": "error",
            "executed": False,
            "exit_code": 2,
            "checks": [
                {"check": "input", "result": "error", "message": input_issue}
            ],
            "packages": [],
        }
        report["gates"].append(gate)
        return gate

    if not package_paths:
        gate = _skipped_gate("materials_claims", "no package inputs")
        gate["packages"] = []
        report["gates"].append(gate)
        return gate

    packages: list[dict[str, object]] = []
    for package_path in package_paths:
        try:
            validation = validate_materials_claims.validate_figure_package(
                package_path
            )
            errors = [_issue_dict(issue) for issue in validation.errors]
            warnings = [_issue_dict(issue) for issue in validation.warnings]
            package_statuses: list[str] = []
            if errors:
                package_statuses.append("error")
            if warnings:
                package_statuses.append("warning")
            package_status = _gate_status(package_statuses)
            packages.append(
                {
                    "package": package_path.as_posix(),
                    "status": package_status,
                    "executed": True,
                    "exit_code": STATUS_EXIT_CODES[package_status],
                    "errors": errors,
                    "warnings": warnings,
                }
            )
        except Exception as exc:
            packages.append(
                {
                    "package": package_path.as_posix(),
                    "status": "error",
                    "executed": False,
                    "exit_code": 2,
                    "errors": [
                        {
                            "rule": "input_error",
                            "severity": "error",
                            "message": str(exc),
                            "row": None,
                            "context": {},
                        }
                    ],
                    "warnings": [],
                }
            )

    status = _gate_status(
        [str(package["status"]) for package in packages]
    )
    gate = {
        "gate": "materials_claims",
        "status": status,
        "executed": True,
        "exit_code": STATUS_EXIT_CODES[status],
        "packages": packages,
        "checks": [],
    }
    report["execution_order"].append("materials_claims")
    report["gates"].append(gate)
    return gate


def run_validation_gates(
    storyboard_path: Path | str | None = None,
    package_dirs: Iterable[Path | str] | Path | str | None = None,
) -> dict[str, object]:
    """Run storyboard first, then materials claims when applicable.

    A storyboard error, including a load or input error, short-circuits the
    materials gate. Storyboard warnings remain non-blocking and allow material
    validation to run.
    """

    report = _empty_report()
    try:
        package_paths, package_issue = _normalise_package_paths(package_dirs)
    except Exception as exc:
        package_paths, package_issue = [], f"invalid package inputs: {exc}"

    has_storyboard = storyboard_path is not None
    has_packages = package_dirs is not None and (
        isinstance(package_dirs, (Path, str)) or bool(package_paths) or package_issue
    )
    if not has_storyboard and not has_packages:
        report["gates"] = [
            _skipped_gate("storyboard", "not provided"),
            _skipped_gate("materials_claims", "not provided"),
        ]
        report["issues"].append(
            "at least one validation input (storyboard or package directory) is required"
        )
        return _finalise(report)

    if has_storyboard:
        storyboard_gate = _run_storyboard_gate(report, storyboard_path)
    else:
        storyboard_gate = _skipped_gate("storyboard", "not provided")
        report["gates"].append(storyboard_gate)

    if storyboard_gate["status"] == "error":
        skipped = _skipped_gate("materials_claims", "storyboard gate failed")
        skipped["packages"] = []
        report["gates"].append(skipped)
        return _finalise(report)

    _run_materials_gate(report, package_paths, package_issue)
    return _finalise(report)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--storyboard",
        type=Path,
        default=None,
        help="Path to a multi-figure figure_storyboard.yaml.",
    )
    parser.add_argument(
        "--package-dir",
        action="append",
        type=Path,
        default=[],
        help="Figure package directory; repeat for multiple packages.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit the structured JSON report.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    report = run_validation_gates(
        storyboard_path=args.storyboard,
        package_dirs=args.package_dir,
    )
    if args.json:
        print(json.dumps(report, ensure_ascii=True, indent=2))
    else:
        print(f"STATUS: {str(report['status']).upper()}")
        print(f"EXECUTION ORDER: {', '.join(report['execution_order']) or 'none'}")
        for gate in report["gates"]:
            print(
                f"  [{str(gate['status']).upper():7}] "
                f"{gate['gate']}: exit_code={gate['exit_code']}"
            )
        for issue in report["issues"]:
            print(f"  ISSUE: {issue}", file=sys.stderr)
    return int(report["exit_code"])


if __name__ == "__main__":
    raise SystemExit(main())

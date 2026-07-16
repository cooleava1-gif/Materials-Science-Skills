#!/usr/bin/env python3
"""Standalone regression checks for Task 2 eval smoke integration."""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from types import ModuleType, SimpleNamespace


SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parents[2]
PLUGIN_RUNNER = SCRIPT_DIR / "run_eval_smoke.py"
ROOT_RUNNER = REPO_ROOT / "scripts" / "run_eval_smoke.py"
RELEASE_CHECKS = SCRIPT_DIR / "run_release_checks.py"


def normalize_report(report: dict[str, object]) -> dict[str, object]:
    cases = report.get("cases")
    if not isinstance(cases, list):
        return report

    for case in cases:
        if not isinstance(case, dict):
            continue
        if case.get("id") != "template-driven-rendering-regressions":
            continue
        stderr = case.get("stderr")
        if isinstance(stderr, str):
            case["stderr"] = re.sub(
                r"(Ran \d+ tests in )\d+(?:\.\d+)?s",
                r"\1<duration>s",
                stderr,
            )
    return report


def load_module(path: Path, name: str) -> ModuleType:
    if not path.exists():
        raise AssertionError(f"module does not exist: {path}")
    if str(path.parent) not in sys.path:
        sys.path.insert(0, str(path.parent))
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise AssertionError(f"could not load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_json_result(path: Path, *arguments: str) -> tuple[int, dict[str, object]]:
    result = subprocess.run(
        [sys.executable, str(path), "--json", *arguments],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    try:
        report = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise AssertionError(
            f"{path} did not emit JSON:\n{result.stdout}\n{result.stderr}"
        ) from exc
    if not isinstance(report, dict):
        raise AssertionError(f"{path} emitted non-object JSON: {report!r}")
    return result.returncode, normalize_report(report)


def run_json(path: Path, *arguments: str) -> dict[str, object]:
    returncode, report = run_json_result(path, *arguments)
    if returncode != 0:
        raise AssertionError(
            f"{path} exited with {returncode}\n"
            f"report:\n{json.dumps(report, ensure_ascii=False, indent=2)}"
        )
    return report


def run_release_main(module: ModuleType) -> tuple[int, dict[str, object]]:
    original_argv = sys.argv
    output = StringIO()
    try:
        sys.argv = [str(RELEASE_CHECKS), "--json"]
        with redirect_stdout(output):
            returncode = module.main()
    finally:
        sys.argv = original_argv

    try:
        report = json.loads(output.getvalue())
    except json.JSONDecodeError as exc:
        raise AssertionError(
            f"release checker did not emit JSON:\n{output.getvalue()}"
        ) from exc
    if not isinstance(report, dict):
        raise AssertionError(f"release checker emitted non-object JSON: {report!r}")
    return returncode, report


def test_root_and_plugin_entrypoints_match() -> None:
    plugin = run_json(
        PLUGIN_RUNNER,
        "--skill",
        "materials-submission",
    )
    root = run_json(
        ROOT_RUNNER,
        "--skill",
        "materials-submission",
    )

    assert root == plugin
    assert root["status"] == "pass"
    summary = root["summary"]
    assert isinstance(summary, dict)
    assert summary["pass"] == 22


def test_root_and_plugin_invalid_skill_exit_match() -> None:
    selector = "../materials-submission"
    plugin_code, plugin = run_json_result(PLUGIN_RUNNER, "--skill", selector)
    root_code, root = run_json_result(ROOT_RUNNER, "--skill", selector)

    assert plugin_code == 1
    assert root_code == 1
    assert root == plugin
    assert root["status"] == "fail"
    assert root["cases"] == []


def test_collect_eval_smoke_issues_preserves_failures() -> None:
    release_module = load_module(RELEASE_CHECKS, "_task_2_release_checks")

    failed_calls: list[Path] = []

    def failed_report(skills_root: Path) -> dict[str, object]:
        failed_calls.append(skills_root)
        return {
            "status": "fail",
            "issues": ["materials-submission:dry-run-output: missing output"],
        }

    issues = release_module.collect_eval_smoke_issues(failed_report)
    assert issues == ["materials-submission:dry-run-output: missing output"]
    assert failed_calls == [release_module.SKILLS_ROOT]

    passing_calls: list[Path] = []

    def passing_report(skills_root: Path) -> dict[str, object]:
        passing_calls.append(skills_root)
        return {
            "status": "pass",
            "summary": {"not_executable": 1},
            "issues": [],
        }

    assert release_module.collect_eval_smoke_issues(passing_report) == []
    assert passing_calls == [release_module.SKILLS_ROOT]


def test_collect_eval_smoke_issues_captures_injected_runner_errors() -> None:
    release_module = load_module(RELEASE_CHECKS, "_task_2_release_checks_raises")
    calls: list[Path] = []

    def raising_report(skills_root: Path) -> dict[str, object]:
        calls.append(skills_root)
        raise RuntimeError("simulated injected runner failure")

    issues = release_module.collect_eval_smoke_issues(raising_report)
    assert issues == [
        "eval smoke runner execution failed: simulated injected runner failure"
    ]
    assert calls == [release_module.SKILLS_ROOT]


def test_collect_eval_smoke_issues_captures_malformed_reports() -> None:
    release_module = load_module(RELEASE_CHECKS, "_task_3_release_checks_shapes")

    assert release_module.collect_eval_smoke_issues(lambda _: None) == [
        "eval smoke runner returned a non-dict report"
    ]
    assert release_module.collect_eval_smoke_issues(
        lambda _: {"status": "fail", "issues": "not-a-list"}
    ) == ["eval smoke runner returned malformed issues data"]
    assert release_module.collect_eval_smoke_issues(
        lambda _: {"status": "fail", "issues": ["valid", 7]}
    ) == ["eval smoke runner returned malformed issues data"]
    assert release_module.collect_eval_smoke_issues(
        lambda _: {"status": "unknown", "issues": []}
    ) == ["eval smoke runner returned malformed report status"]
    assert release_module.collect_eval_smoke_issues(
        lambda _: {"status": ["fail"], "issues": []}
    ) == ["eval smoke runner returned malformed report status"]


def test_collect_eval_smoke_issues_captures_default_runner_errors() -> None:
    release_module = load_module(RELEASE_CHECKS, "_task_2_release_checks_default")
    calls: list[Path] = []

    def raising_report(skills_root: Path) -> dict[str, object]:
        calls.append(skills_root)
        raise RuntimeError("simulated default runner failure")

    original_loader = release_module._load_eval_smoke_module
    release_module._load_eval_smoke_module = lambda: SimpleNamespace(
        run_smoke_checks=raising_report
    )
    try:
        issues = release_module.collect_eval_smoke_issues()
    finally:
        release_module._load_eval_smoke_module = original_loader

    assert issues == [
        "eval smoke runner execution failed: simulated default runner failure"
    ]
    assert calls == [release_module.SKILLS_ROOT]


def test_release_main_serializes_malformed_eval_report() -> None:
    release_module = load_module(RELEASE_CHECKS, "_task_3_release_checks_main")

    def malformed_report(skills_root: Path) -> dict[str, object]:
        return {"status": "fail", "issues": "not-a-list"}

    original_loader = release_module._load_eval_smoke_module
    release_module._load_eval_smoke_module = lambda: SimpleNamespace(
        run_smoke_checks=malformed_report
    )
    try:
        returncode, report = run_release_main(release_module)
    finally:
        release_module._load_eval_smoke_module = original_loader

    assert returncode == 1
    assert report["status"] == "fail"
    issues = report["issues"]
    assert isinstance(issues, dict)
    assert issues["eval_smoke"] == [
        "eval smoke runner returned malformed issues data"
    ]


def test_release_main_serializes_eval_loader_errors() -> None:
    release_module = load_module(RELEASE_CHECKS, "_task_2_release_checks_loader")

    def failing_loader() -> ModuleType:
        raise OSError("simulated canonical runner load failure")

    original_loader = release_module._load_eval_smoke_module
    release_module._load_eval_smoke_module = failing_loader
    try:
        returncode, report = run_release_main(release_module)
    finally:
        release_module._load_eval_smoke_module = original_loader

    assert returncode == 1
    assert report["status"] == "fail"
    issues = report["issues"]
    assert isinstance(issues, dict)
    assert issues["eval_smoke"] == [
        "eval smoke runner load failed: simulated canonical runner load failure"
    ]


def main() -> int:
    tests = [
        test_root_and_plugin_entrypoints_match,
        test_root_and_plugin_invalid_skill_exit_match,
        test_collect_eval_smoke_issues_preserves_failures,
        test_collect_eval_smoke_issues_captures_injected_runner_errors,
        test_collect_eval_smoke_issues_captures_malformed_reports,
        test_collect_eval_smoke_issues_captures_default_runner_errors,
        test_release_main_serializes_malformed_eval_report,
        test_release_main_serializes_eval_loader_errors,
    ]
    failures: list[str] = []
    for test in tests:
        try:
            test()
        except Exception as exc:
            failures.append(f"{test.__name__}: {type(exc).__name__}: {exc}")

    if failures:
        for failure in failures:
            print(failure, file=sys.stderr)
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

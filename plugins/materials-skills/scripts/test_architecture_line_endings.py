#!/usr/bin/env python3
"""Regression checks for platform-independent architecture context budgets."""

from __future__ import annotations

import importlib.util
import tempfile
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
CHECKER_PATH = SCRIPT_DIR / "check_skill_architecture.py"


def _require(condition: bool, message: object) -> None:
    if not condition:
        raise AssertionError(message)


def _load_checker() -> Any:
    spec = importlib.util.spec_from_file_location(
        "architecture_line_ending_checker",
        CHECKER_PATH,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {CHECKER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _write(path: Path, text: str, newline: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.replace("\n", newline).encode("utf-8"))


def _write_skill(
    skill_dir: Path,
    *,
    name: str,
    newline: str,
    shared_path: str,
) -> None:
    manifest = f"""name: {name}
always_load:
  - {shared_path}
  - static/core/contract.md
axes:
  mode:
    default: basic
    values:
      basic:
        path: static/fragments/basic.md
references:
  on_demand:
    extra:
      path: references/extra.md
      when: "Extra context is required."
"""
    files = {
        "SKILL.md": "\ufeff# 技能\nUse the manifest axes.\n",
        "manifest.yaml": manifest,
        "static/core/contract.md": "# Contract\nShared behavior.\n",
        "static/fragments/basic.md": "# Basic\nSelected route.\n",
        "references/extra.md": "# Extra\nOptional route.\n",
    }
    for relative, text in files.items():
        _write(skill_dir / relative, text, newline)


def _fixture_reports(
    checker: Any,
    root: Path,
    newline: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    skills_root = root / "skills"
    shared = root / "_shared/core/shared.md"
    _write(shared, "# Shared\n跨技能 context.\n", newline)
    shared_path = "../../_shared/core/shared.md"
    _write_skill(
        skills_root / "primary",
        name="primary",
        newline=newline,
        shared_path=shared_path,
    )
    _write_skill(
        skills_root / "companion",
        name="companion",
        newline=newline,
        shared_path=shared_path,
    )
    budget = {
        "required_route_axes": ["mode"],
        "required_route_scenarios": ["composed"],
        "route_scenarios": [
            {
                "name": "composed",
                "axes": {"mode": "basic"},
                "on_demand": ["extra"],
                "companions": [
                    {
                        "skill": "companion",
                        "required_axes": ["mode"],
                        "axes": {"mode": "basic"},
                        "on_demand": ["extra"],
                    }
                ],
                "target_bytes": 100000,
                "max_bytes": 100000,
            }
        ],
    }
    reports, warnings, failures = checker._route_scenario_reports(
        skills_root,
        skills_root / "primary",
        budget,
    )
    _require(not warnings, warnings)
    _require(not failures, failures)
    _require(len(reports) == 1, reports)

    manifest = checker._read_yaml(skills_root / "primary/manifest.yaml")
    manifest["context_budget"] = {
        "target_activation_bytes": 100000,
        "max_activation_bytes": 100000,
        "max_always_load": 3,
        "max_skill_lines": 100,
        "max_workflow_lines": 100,
    }
    context_report = checker._context_budget_report(
        skills_root,
        skills_root / "primary",
        manifest,
    )
    _require(not context_report["hard_failures"], context_report)
    return reports[0], context_report


def main() -> int:
    checker = _load_checker()
    normalized = "\ufeff标题\nvalue\n".encode("utf-8")
    with tempfile.TemporaryDirectory() as temp:
        root = Path(temp)
        sizes = []
        for index, newline in enumerate(("\n", "\r\n", "\r")):
            path = root / f"text-{index}.md"
            _write(path, "\ufeff标题\nvalue\n", newline)
            sizes.append(checker._context_size(path))
        _require(sizes == [len(normalized)] * 3, sizes)

        binary = root / "binary.dat"
        binary.write_bytes(b"\xff\r\n\x00")
        _require(checker._context_size(binary) == 4, "binary fallback size changed")

        route_reports = []
        context_reports = []
        for index, newline in enumerate(("\n", "\r\n", "\r")):
            route_report, context_report = _fixture_reports(
                checker,
                root / str(index),
                newline,
            )
            route_reports.append(route_report)
            context_reports.append(context_report)

        baseline = route_reports[0]
        for report in route_reports[1:]:
            _require(
                report["activation_bytes"] == baseline["activation_bytes"],
                (baseline, report),
            )
            _require(report["skill_bytes"] == baseline["skill_bytes"], (baseline, report))

        metric_names = (
            "activation_bytes",
            "skill_bytes",
            "manifest_bytes",
            "always_load_bytes",
        )
        baseline_metrics = context_reports[0]["metrics"]
        for report in context_reports[1:]:
            metrics = report["metrics"]
            for name in metric_names:
                _require(
                    metrics[name] == baseline_metrics[name],
                    (name, baseline_metrics, metrics),
                )

        shared = (root / "0/_shared/core/shared.md").resolve()
        unique_files = {Path(path).resolve() for path in baseline["files"]}
        expected_total = sum(checker._context_size(path) for path in unique_files)
        _require(baseline["activation_bytes"] == expected_total, baseline)
        _require(shared in unique_files, unique_files)

        primary_files, primary_failures = checker._route_skill_payload(
            root / "0/skills",
            "primary",
            {"mode": "basic"},
            ["extra"],
        )
        _require(not primary_failures, primary_failures)
        expected_primary = sum(
            checker._context_size(path.resolve())
            for path in dict.fromkeys(primary_files)
            if path.is_file()
        )
        _require(
            baseline["skill_bytes"]["primary"] == expected_primary,
            baseline["skill_bytes"],
        )
        _require(
            baseline["skill_bytes"]["companion"]
            == baseline["activation_bytes"] - expected_primary,
            baseline["skill_bytes"],
        )

    print("PASS: architecture context bytes are line-ending invariant")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

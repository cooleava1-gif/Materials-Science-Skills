#!/usr/bin/env python3
"""Run release checks across all materials skills.

Checks file presence, manifest validity, trigger coverage, and asset completeness.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from skill_manifest import discover_skill_names

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"

FIGURE_HARD_WORKFLOW_FILES = [
    "static/core/contract.md",
    "static/core/stance.md",
    "manifest.yaml",
    "SKILL.md",
    "references/materials-figure-atlas.md",
    "references/caption_boundary.md",
    "references/figure_qa_report.md",
    "assets/templates/figure_storyboard.yaml",
    "scripts/compose_multipanel_figure.py",
]

WRITING_MATURITY_FILES = [
    "references/section-patterns/abstract-claim-arc.md",
    "references/section-patterns/introduction-gap-ladder.md",
    "references/section-patterns/results-discussion-evidence-chain.md",
    "references/section-patterns/conclusion-boundary.md",
    "references/section-patterns/review-synthesis-patterns.md",
    "references/phrase-banks/wer-ea.md",
    "references/phrase-banks/thermal-insulation.md",
    "references/phrase-banks/polymer-composites.md",
    "scripts/audit_materials_manuscript.py",
]

EVAL_REQUIRED_FIELDS = ("id", "prompt", "expected_output", "assertions")

def collect_paper_production_orchestrator_issues(skill_root: Path) -> list[str]:
    issues = []
    shared = skill_root / "_shared" / "paper-production"
    for name in [
        "weakness-routing.md",
        "weakness-routing-template.csv",
        "paper-gate-report-template.md",
    ]:
        if not (shared / name).exists():
            issues.append(f"missing skills/_shared/paper-production/{name}")
    examples = shared / "examples"
    for name in [
        "wer-ea-mini-review-weakness-routing.csv",
        "wer-ea-mini-review-gate-report.md",
    ]:
        if not (examples / name).exists():
            issues.append(f"missing skills/_shared/paper-production/examples/{name}")
    return issues


def collect_writing_maturity_issues(skill_root: Path) -> list[str]:
    issues = []
    writing_root = skill_root / "materials-writing"
    for name in WRITING_MATURITY_FILES:
        if not (writing_root / name).exists():
            issues.append(f"missing materials-writing/{name}")
    return issues


def check_skill_basics(skill_name: str) -> list[str]:
    issues = []
    root = SKILLS_ROOT / skill_name
    if not root.exists():
        issues.append(f"{skill_name}: directory missing")
        return issues
    for fname in ["SKILL.md", "manifest.yaml"]:
        if not (root / fname).exists():
            issues.append(f"{skill_name}: missing {fname}")
    return issues


def collect_eval_contract_issues(skills_root: Path = SKILLS_ROOT) -> list[str]:
    """Validate per-skill eval assets used for release regression coverage."""

    issues: list[str] = []
    for skill_name in discover_skill_names(skills_root):
        eval_path = skills_root / skill_name / "evals" / "evals.json"
        if not eval_path.exists():
            issues.append(f"{skill_name}: missing evals/evals.json")
            continue

        try:
            payload = json.loads(eval_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            issues.append(f"{skill_name}: invalid evals/evals.json ({exc})")
            continue

        if not isinstance(payload, dict):
            issues.append(f"{skill_name}: evals/evals.json must contain a JSON object")
            continue

        if payload.get("skill_name") != skill_name:
            issues.append(
                f"{skill_name}: evals/evals.json skill_name must equal '{skill_name}'"
            )

        evals = payload.get("evals")
        if not isinstance(evals, list) or not evals:
            issues.append(f"{skill_name}: evals/evals.json must define a non-empty evals list")
            continue

        for index, eval_case in enumerate(evals, start=1):
            label = f"{skill_name}: eval #{index}"
            if not isinstance(eval_case, dict):
                issues.append(f"{label} must be a JSON object")
                continue

            missing = [
                field for field in EVAL_REQUIRED_FIELDS if not eval_case.get(field)
            ]
            if missing:
                issues.append(f"{label} missing required fields: {', '.join(missing)}")
                continue

            assertions = eval_case.get("assertions")
            if not isinstance(assertions, list) or not assertions:
                issues.append(f"{label} assertions must be a non-empty list")

            files = eval_case.get("files", [])
            if files is not None and not isinstance(files, list):
                issues.append(f"{label} files must be a list when provided")

    return issues


def collect_mcp_server_drift_issues() -> list[str]:
    """Detect drift between the canonical MCP server and the skill/plugin copy.

    Deprecated: the canonical MCP server now lives inside the plugin package.
    This check is kept for API compatibility and always returns an empty list.
    """
    return []


def collect_mcp_server_issues() -> list[str]:
    """Run academic-search MCP tests inside the plugin package."""

    tests_root = SKILLS_ROOT / "materials-citation" / "mcp" / "academic_search" / "tests"
    if not tests_root.exists():
        return ["missing skills/materials-citation/mcp/academic_search/tests"]
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "unittest",
            "discover",
            "-s",
            str(tests_root),
            "-p",
            "test_*.py",
            "-v",
        ],
        cwd=SKILLS_ROOT.parent,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return []
    output = "\n".join(part for part in (result.stdout, result.stderr) if part).strip()
    return [output[-4000:] or f"MCP server tests failed with exit {result.returncode}"]


def should_skip_mcp_tests() -> bool:
    return os.environ.get("MATERIALS_SKIP_MCP_TESTS") == "1"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="JSON output.")
    parser.add_argument("--skill", help="Check one skill only.")
    args = parser.parse_args()

    skills = [args.skill] if args.skill else discover_skill_names(SKILLS_ROOT)
    all_issues: dict[str, list[str]] = {}

    for skill in skills:
        issues = check_skill_basics(skill)
        if issues:
            all_issues[skill] = issues

    eval_contract_issues = collect_eval_contract_issues(SKILLS_ROOT)
    if eval_contract_issues:
        all_issues["eval_contract"] = eval_contract_issues

    # paper-production orchestrator check
    orchestrator_issues = collect_paper_production_orchestrator_issues(SKILLS_ROOT)
    if orchestrator_issues:
        all_issues["paper_production_orchestrator"] = orchestrator_issues

    writing_maturity_issues = collect_writing_maturity_issues(SKILLS_ROOT)
    if writing_maturity_issues:
        all_issues["writing_maturity"] = writing_maturity_issues

    # figure_hard_workflow check
    figure_root = SKILLS_ROOT / "materials-figure"
    figure_issues = []
    for fname in FIGURE_HARD_WORKFLOW_FILES:
        if not (figure_root / fname).exists():
            figure_issues.append(f"missing {fname}")
    audit_script = figure_root / "scripts" / "audit_figure_package.py"
    if not audit_script.exists():
        figure_issues.append("missing scripts/audit_figure_package.py")
    if figure_issues:
        all_issues["figure_hard_workflow"] = figure_issues

    # handoff contract validation
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "validate_handoffs",
            Path(__file__).parent / "validate_handoffs.py"
        )
        if spec and spec.loader:
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            handoff_issues = mod.validate_all()
            if handoff_issues:
                for key, vals in handoff_issues.items():
                    all_issues.setdefault(key, []).extend(vals)
    except ImportError:
        all_issues["handoff_contracts"] = ["validate_handoffs module not available"]
    except Exception as exc:
        all_issues["handoff_contracts"] = [f"handoff validation error: {exc}"]

    # manifest validation
    try:
        spec2 = importlib.util.spec_from_file_location(
            "validate_manifest",
            Path(__file__).parent / "validate_manifest.py"
        )
        if spec2 and spec2.loader:
            mod2 = importlib.util.module_from_spec(spec2)
            spec2.loader.exec_module(mod2)
            manifest_issues = mod2.validate_all()
            if manifest_issues:
                for key, vals in manifest_issues.items():
                    all_issues.setdefault(key, []).extend(vals)
    except Exception as exc:
        all_issues["manifest_validation"] = [f"manifest validation error: {exc}"]

    # behavioral contract test discovery (record count only)
    try:
        spec3 = importlib.util.spec_from_file_location(
            "run_behavioral_tests",
            Path(__file__).parent / "run_behavioral_tests.py"
        )
        if spec3 and spec3.loader:
            mod3 = importlib.util.module_from_spec(spec3)
            spec3.loader.exec_module(mod3)
            bt_issues = mod3.run_all(silent=True)
            total_scenarios = sum(len(v) for v in bt_issues.values())
            if total_scenarios == 0:
                all_issues.setdefault("behavioral_tests", []).append(
                    "no behavioral test scenarios found under skills/*/tests/scenarios/"
                )
    except Exception as exc:
        all_issues["behavioral_tests"] = [f"behavioral test error: {exc}"]

    # material registry validation
    try:
        spec4 = importlib.util.spec_from_file_location(
            "validate_registry",
            Path(__file__).parent / "validate_registry.py"
        )
        if spec4 and spec4.loader:
            mod4 = importlib.util.module_from_spec(spec4)
            spec4.loader.exec_module(mod4)
            registry_issues = mod4.validate_all()
            if registry_issues:
                for key, vals in registry_issues.items():
                    all_issues.setdefault(key, []).extend(vals)
    except ImportError:
        all_issues["material_registry"] = ["validate_registry module not available"]
    except Exception as exc:
        all_issues["material_registry"] = [f"registry validation error: {exc}"]

    # architecture and plugin mirror validation
    try:
        spec5 = importlib.util.spec_from_file_location(
            "check_skill_architecture",
            Path(__file__).parent / "check_skill_architecture.py",
        )
        if spec5 and spec5.loader:
            mod5 = importlib.util.module_from_spec(spec5)
            spec5.loader.exec_module(mod5)
            architecture_report = mod5.inspect_all(SKILLS_ROOT)
            if architecture_report.get("status") != "pass":
                hard_failures = architecture_report.get("summary", {}).get("hard_failures", [])
                all_issues.setdefault("architecture", []).append(
                    f"architecture checker failed: {hard_failures}"
                )
                plugin_mirror = architecture_report.get("plugin_mirror", {})
                for key in ("missing_plugin_skills", "missing_plugin_files", "extra_plugin_files", "different_files"):
                    for value in plugin_mirror.get(key, []) or []:
                        all_issues.setdefault("architecture", []).append(f"plugin_mirror.{key}: {value}")
                shared_mirror = architecture_report.get("shared_mirror", {})
                for key in ("missing_files", "extra_files", "different_files"):
                    for value in shared_mirror.get(key, []) or []:
                        all_issues.setdefault("architecture", []).append(f"shared_mirror.{key}: {value}")
    except Exception as exc:
        all_issues["architecture"] = [f"architecture validation error: {exc}"]

    if not should_skip_mcp_tests():
        mcp_issues = collect_mcp_server_issues()
        if mcp_issues:
            all_issues["mcp_server"] = mcp_issues

    mcp_drift_issues = collect_mcp_server_drift_issues()
    if mcp_drift_issues:
        all_issues.setdefault("mcp_server", []).extend(mcp_drift_issues)

    if args.json:
        print(json.dumps({"status": "pass" if not all_issues else "fail", "issues": all_issues}, indent=2))
    else:
        if all_issues:
            for skill, issues in all_issues.items():
                for issue in issues:
                    print(f"[{skill}] {issue}")
            print(f"\nFAIL: {sum(len(v) for v in all_issues.values())} issues found")
        else:
            print("PASS: all checks passed")

    return 0 if not all_issues else 1


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Run release checks across all materials skills.

Checks file presence, manifest validity, trigger coverage, and asset completeness.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

SKILLS_ROOT = Path(__file__).resolve().parents[1] / "skills"
REPO_ROOT = Path(__file__).resolve().parents[1]

ALL_SKILLS = [
    "materials-citation",
    "materials-data",
    "materials-doe",
    "materials-figure",
    "materials-paper2ppt",
    "materials-polishing",
    "materials-pptx",
    "materials-reader",
    "materials-research",
    "materials-response",
    "materials-reviewer",
    "materials-writing",
]

# Each skill's test directory, checked for presence
SKILL_TEST_DIRS = [
    '"materials-citation" / "tests"',
    '"materials-data" / "tests"',
    '"materials-doe" / "tests"',
    '"materials-figure" / "tests"',
    '"materials-paper2ppt" / "tests"',
    '"materials-polishing" / "tests"',
    '"materials-pptx" / "tests"',
    '"materials-reader" / "tests"',
    '"materials-research" / "tests"',
    '"materials-response" / "tests"',
    '"materials-reviewer" / "tests"',
    '"materials-writing" / "tests"',
]

FIGURE_PACKAGE_SAMPLE_NAMES = [
    "kong-2024-cbm-bonding",
    "zhang-2017-cbm-tack-coat",
    "yao-2022-cbm-wer-sbr",
]

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

FIGURE_HARD_WORKFLOW_EVAL_IDS = [
    "backend-exclusivity-python-missing-package",
    "journal-ready-package-audit",
    "python-only-expanded-chart-gallery",
]

paper_production_orchestrator = "paper-production-orchestrator"

PAPER_PRODUCTION_EXAMPLES = [
    "paper-production-mini-review-example.md",
    "wer-ea-mini-review-weakness-routing.csv",
    "wer-ea-mini-review-gate-report.md",
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

FIGURE_GOLDEN_PACKAGES = [
    "wer-ea-full",
    "thermal-insulation-partial-to-full",
    "polymer-composites-partial-to-full",
]


def collect_paper_production_orchestrator_issues(skill_root: Path) -> list[str]:
    issues = []
    shared = skill_root / "_shared" / "paper-production"
    for name in [
        "weakness-routing.md",
        "weakness-routing-template.csv",
        "paper-gate-report-template.md",
    ]:
        if not (shared / name).exists():
            issues.append(f"missing _shared/paper-production/{name}")
    examples = shared / "examples"
    for name in [
        "wer-ea-mini-review-weakness-routing.csv",
        "wer-ea-mini-review-gate-report.md",
    ]:
        if not (examples / name).exists():
            issues.append(f"missing _shared/paper-production/examples/{name}")
    return issues


def collect_writing_maturity_issues(skill_root: Path) -> list[str]:
    issues = []
    writing_root = skill_root / "materials-writing"
    for name in WRITING_MATURITY_FILES:
        if not (writing_root / name).exists():
            issues.append(f"missing materials-writing/{name}")
    return issues


def collect_figure_maturity_issues(skill_root: Path) -> list[str]:
    issues = []
    figure_root = skill_root / "materials-figure"
    packages_root = figure_root / "examples" / "figure-packages"
    for package in FIGURE_GOLDEN_PACKAGES:
        package_root = packages_root / package
        if not package_root.exists():
            issues.append(f"missing materials-figure/examples/figure-packages/{package}")
            continue
        for name in [
            "README.md",
            "figure_storyboard.yaml",
            "caption_boundary.md",
            "figure_qa_report.md",
            "figure.svg",
            "figure.pdf",
            "figure.png",
            "figure.tiff",
        ]:
            if not (package_root / name).exists():
                issues.append(f"missing materials-figure/examples/figure-packages/{package}/{name}")
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="JSON output.")
    parser.add_argument("--skill", help="Check one skill only.")
    args = parser.parse_args()

    skills = [args.skill] if args.skill else ALL_SKILLS
    all_issues: dict[str, list[str]] = {}

    for skill in skills:
        issues = check_skill_basics(skill)
        if issues:
            all_issues[skill] = issues

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

    figure_maturity_issues = collect_figure_maturity_issues(SKILLS_ROOT)
    if figure_maturity_issues:
        all_issues["figure_maturity"] = figure_maturity_issues

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
    except Exception as exc:
        all_issues["architecture"] = [f"architecture validation error: {exc}"]

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

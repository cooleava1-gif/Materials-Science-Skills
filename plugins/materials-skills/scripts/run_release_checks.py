#!/usr/bin/env python3
"""Run public release checks across all materials skills.

The public GitHub package is an installable skill bundle, not the full internal
regression workspace. This gate checks manifests, declared paths, core skill
directories, shared contracts, and representative visual assets.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml
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

FIGURE_REPRESENTATIVE_ASSET_FILES = [
    "references/automatic-figure-package.md",
    "references/figure-gallery.md",
    "references/review-figure-intake.md",
    "references/wer-ea-review-figure-contract.md",
    "references/chart-atlas.md",
    "references/demos.md",
    "assets/templates/review-figure-intake-template.csv",
    "assets/templates/wer-ea-figure-contract-template.md",
    "scripts/check_storyboard.py",
    "scripts/data_package_to_figure_handoff.py",
    "scripts/validate_materials_claims.py",
]

HTML_DECK_PUBLIC_FILES = [
    "SKILL.md",
    "README.md",
    "manifest.yaml",
    "agents/openai.yaml",
    "assets/templates/deck-outline-template.json",
    "assets/templates/deck-outline-template.md",
    "evals/evals.json",
    "references/html-deck-generation.md",
    "references/html-first-academic-deck.md",
    "references/playwright-verification.md",
    "scripts/build_deck.mjs",
    "scripts/render_html_deck.mjs",
    "scripts/verify_deck_html.mjs",
    "static/core/contract.md",
    "static/core/workflow.md",
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

WRITING_STATE_MACHINE_FILES = [
    "assets/templates/foundation/00_scope.md",
    "assets/templates/foundation/01_research_canon.md",
    "assets/templates/foundation/02_evidence_table.md",
    "assets/templates/foundation/03_argument_map.md",
    "assets/templates/foundation/04_section_contracts.md",
    "assets/templates/foundation/05_style_guide.md",
    "assets/templates/foundation/state-template.json",
    "references/state-machine/foundation-files.md",
    "references/state-machine/evaluation-rubric.md",
    "references/state-machine/stopping-rules.md",
    "references/state-machine/validation-checklist.md",
    "static/fragments/writing_mode/compose.md",
    "static/fragments/writing_mode/revise.md",
    "static/fragments/writing_mode/hybrid.md",
    "static/fragments/writing_mode/qa.md",
    "scripts/init_writing_project.py",
]

EXPERIMENT_RECORD_FILES = [
    "skills/_shared/core/experiment-record-schema.yaml",
    "skills/_shared/core/experiment-record-example.yaml",
    "skills/materials-doe/static/core/experiment-record-output.md",
    "skills/materials-doe/assets/templates/experiment-record-template.yaml",
    "skills/materials-data/static/core/experiment-record-input.md",
    "skills/materials-data/references/experiment-record-to-dataset.md",
    "skills/materials-writing/static/fragments/section/methods-from-record.md",
    "skills/materials-writing/static/fragments/section/results-from-record.md",
    "skills/materials-writing/static/fragments/section/discussion-mechanism.md",
    "skills/materials-writing/static/fragments/section/cover-letter.md",
    "skills/materials-writing/static/fragments/section/highlights.md",
    "skills/materials-writing/references/experiment-record-for-writing.md",
]

STRATEGIC_UPGRADE_FILES = [
    "skills/_shared/core/research-state-contract.md",
    "skills/_shared/core/research-state-template.yaml",
    "skills/materials-literature-pipeline/SKILL.md",
    "skills/materials-literature-pipeline/README.md",
    "skills/materials-literature-pipeline/manifest.yaml",
    "skills/materials-literature-pipeline/static/core/contract.md",
    "skills/materials-literature-pipeline/static/core/workflow.md",
    "skills/materials-literature-pipeline/static/core/scoring.md",
    "skills/materials-literature-pipeline/references/cron-operations.md",
    "skills/materials-literature-pipeline/references/push-format.md",
    "skills/materials-literature-pipeline/references/degradation-strategy.md",
    "skills/materials-literature-pipeline/references/gap-analysis.md",
    "skills/materials-literature-pipeline/references/review-compilation-workflow.md",
    "skills/materials-literature-pipeline/assets/templates/literature-pipeline-digest.md",
    "skills/materials-literature-pipeline/assets/templates/literature-candidate-table.csv",
    "skills/materials-writing/references/content-first-qa-pipeline.md",
    "_shared/contracts/literature-pipeline-handoff.yaml",
]


def check_experiment_record_files() -> list[str]:
    issues = []
    for rel in EXPERIMENT_RECORD_FILES:
        if not (REPO_ROOT / rel).exists():
            issues.append(f"missing {rel}")
    return issues


def check_strategic_upgrade_files() -> list[str]:
    issues = []
    for rel in STRATEGIC_UPGRADE_FILES:
        if not (REPO_ROOT / rel).exists():
            issues.append(f"missing {rel}")
    return issues


def check_experiment_record() -> list[str]:
    """Validate the experiment-record example against the shared schema.

    Skips schema validation when jsonschema is not installed; file existence
    is still enforced by check_experiment_record_files().
    """
    issues = []
    schema_path = REPO_ROOT / "skills/_shared/core/experiment-record-schema.yaml"
    example_path = REPO_ROOT / "skills/_shared/core/experiment-record-example.yaml"
    try:
        import jsonschema
        schema = yaml.safe_load(schema_path.read_text(encoding="utf-8"))
        example = yaml.safe_load(example_path.read_text(encoding="utf-8"))
        jsonschema.validate(example, schema)
    except ImportError:
        # Schema validation is optional when dependency is missing.
        pass
    except Exception as exc:  # pragma: no cover
        issues.append(f"experiment-record example validation failed: {exc}")
    return issues


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


def collect_writing_state_machine_issues(skill_root: Path) -> list[str]:
    issues = []
    writing_root = skill_root / "materials-writing"
    for name in WRITING_STATE_MACHINE_FILES:
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


def collect_materials_submission_template_issues() -> list[str]:
    """Run the submission skill's declarative template validator."""
    script = (
        SKILLS_ROOT
        / "materials-submission"
        / "scripts"
        / "validate_journal_templates.py"
    )
    if not script.exists():
        return [f"missing {script.relative_to(REPO_ROOT)}"]
    script_dir = str(script.parent)
    if script_dir not in sys.path:
        sys.path.insert(0, script_dir)
    spec = importlib.util.spec_from_file_location(
        "materials_submission_template_validator",
        script,
    )
    if spec is None or spec.loader is None:
        return ["could not load materials-submission template validator"]
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        return module.validate_templates()
    except Exception as exc:
        return [f"template validation error: {exc}"]


def collect_materials_submission_rendering_issues() -> list[str]:
    """Run the submission skill's template-driven rendering regression tests."""
    skill_root = SKILLS_ROOT / "materials-submission"
    test_script = skill_root / "scripts" / "test_template_driven_outputs.py"
    if not test_script.exists():
        return [f"missing {test_script.relative_to(REPO_ROOT)}"]
    result = subprocess.run(
        [sys.executable, str(test_script)],
        cwd=skill_root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        return []
    output = "\n".join(
        part.strip()
        for part in (result.stdout, result.stderr)
        if part.strip()
    )
    return [f"template-driven rendering tests failed: {output}"]


def collect_public_boundary_issues(skills_root: Path = SKILLS_ROOT) -> list[str]:
    """Keep internal tests, vendored experiments, and retired skills out of GitHub delivery."""

    issues: list[str] = []
    retired_skills = ["materials-" + "paper2" + "ppt", "materials-" + "pptx"]
    for skill_name in retired_skills:
        if (skills_root / skill_name).exists():
            issues.append(f"retired public skill still present: {skill_name}")

    def is_ignored(path: Path) -> bool:
        try:
            result = subprocess.run(
                ["git", "check-ignore", "-q", str(path)],
                cwd=REPO_ROOT,
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except (OSError, ValueError):
            return False
        return result.returncode == 0

    def should_block(path: Path) -> bool:
        return path.exists() and not is_ignored(path)

    for skill_dir in skills_root.glob("materials-*"):
        for rel in ["tests", "scripts/tests", "third_party"]:
            if should_block(skill_dir / rel):
                issues.append(f"{skill_dir.name}: public package must not include {rel}")

    blocked_paths = [
        REPO_ROOT / "tests",
        REPO_ROOT / "scripts" / "tests",
        REPO_ROOT / "skills" / "_shared" / "tests",
    ]
    for path in blocked_paths:
        if should_block(path):
            issues.append(f"public package must not include {path.relative_to(REPO_ROOT).as_posix()}")
    return issues


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

    submission_template_issues = collect_materials_submission_template_issues()
    if submission_template_issues:
        all_issues["materials_submission_templates"] = submission_template_issues

    submission_rendering_issues = collect_materials_submission_rendering_issues()
    if submission_rendering_issues:
        all_issues["materials_submission_rendering"] = submission_rendering_issues

    # paper-production orchestrator check
    orchestrator_issues = collect_paper_production_orchestrator_issues(SKILLS_ROOT)
    if orchestrator_issues:
        all_issues["paper_production_orchestrator"] = orchestrator_issues

    writing_maturity_issues = collect_writing_maturity_issues(SKILLS_ROOT)
    if writing_maturity_issues:
        all_issues["writing_maturity"] = writing_maturity_issues

    writing_state_machine_issues = collect_writing_state_machine_issues(SKILLS_ROOT)
    if writing_state_machine_issues:
        all_issues["writing_state_machine"] = writing_state_machine_issues

    # Representative figure delivery boundary check.
    figure_root = SKILLS_ROOT / "materials-figure"
    figure_issues = []
    for fname in FIGURE_HARD_WORKFLOW_FILES:
        if not (figure_root / fname).exists():
            figure_issues.append(f"missing {fname}")
    for fname in FIGURE_REPRESENTATIVE_ASSET_FILES:
        if not (figure_root / fname).exists():
            figure_issues.append(f"missing {fname}")
    audit_script = figure_root / "scripts" / "audit_figure_package.py"
    if not audit_script.exists():
        figure_issues.append("missing scripts/audit_figure_package.py")
    if figure_issues:
        all_issues["figure_hard_workflow"] = figure_issues

    html_deck_root = SKILLS_ROOT / "materials-html-deck"
    html_deck_issues = []
    for fname in HTML_DECK_PUBLIC_FILES:
        if not (html_deck_root / fname).exists():
            html_deck_issues.append(f"missing {fname}")
    if html_deck_issues:
        all_issues["html_deck_public_boundary"] = html_deck_issues

    public_boundary_issues = collect_public_boundary_issues(SKILLS_ROOT)
    if public_boundary_issues:
        all_issues["public_delivery_boundary"] = public_boundary_issues

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

    experiment_record_issues = check_experiment_record_files() + check_experiment_record()
    if experiment_record_issues:
        all_issues["experiment_record_contract"] = experiment_record_issues

    strategic_upgrade_issues = check_strategic_upgrade_files()
    if strategic_upgrade_issues:
        all_issues["strategic_upgrade"] = strategic_upgrade_issues

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

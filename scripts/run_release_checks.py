#!/usr/bin/env python3
"""Run release checks for the civil-materials skill bundle."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


REQUIRED_SKILLS = [
    "civil-materials-research",
    "civil-materials-reader",
    "civil-materials-citation",
    "civil-materials-writing",
    "civil-materials-polishing",
    "civil-materials-response",
    "civil-materials-reviewer",
    "civil-materials-paper2ppt",
    "civil-materials-pptx",
    "civil-materials-figure",
    "civil-materials-data",
]

REQUIRED_SHARED_FILES = [
    "core/stance.md",
    "core/evidence-contract.md",
    "core/ethics.md",
    "core/claim-strength-ladder.md",
    "core/terminology-ledger.md",
    "journal-formats/cbm.md",
    "journal-formats/ccc.md",
    "journal-formats/jbe.md",
    "journal-formats/rmpd.md",
]

PLUGIN_NAME = "civil-materials-skills"
PLUGIN_ROOT = Path("plugins") / PLUGIN_NAME
MARKETPLACE_PATH = Path(".agents") / "plugins" / "marketplace.json"
SKILLS_INDEX_PATH = Path("docs") / "skills-index.md"

README_STATUS_COLUMNS = [
    "Module",
    "Maturity",
    "Scripts",
    "Tests",
    "Typical input",
    "Typical product",
]

WER_EA_REQUIRED_TERMS = [
    "wer-ea",
    "literature screening",
    "mechanism evidence chain",
    "review outline",
    "figure planning",
    "submission route",
]

READER_FULLTEXT_ANCHOR_FILES = [
    Path("civil-materials-reader") / "references" / "fulltext-figure-anchored-reading.md",
    Path("civil-materials-reader") / "references" / "wer-ea-intensive-reading-package.md",
    Path("civil-materials-reader") / "references" / "pdf-visual-asset-extraction.md",
    Path("civil-materials-reader") / "assets" / "templates" / "paper-md-template.md",
    Path("civil-materials-reader") / "assets" / "templates" / "source-map-template.json",
    Path("civil-materials-reader") / "assets" / "templates" / "translation-notes-template.md",
    Path("civil-materials-reader") / "assets" / "templates" / "figure-table-card-template.md",
    Path("civil-materials-reader") / "assets" / "templates" / "mechanism-evidence-table-template.md",
    Path("civil-materials-reader") / "assets" / "templates" / "dosage-window-table-template.md",
    Path("civil-materials-reader") / "assets" / "templates" / "review-handoff-template.md",
    Path("civil-materials-reader") / "assets" / "templates" / "obsidian-note-template.md",
    Path("civil-materials-reader") / "scripts" / "extract_pdf_visual_assets.py",
]
READER_FULLTEXT_ANCHOR_TERMS = [
    "paper.md",
    "source_map.json",
    "translation_notes.md",
    "assets/",
    "original excerpt",
    "chinese understanding",
    "figure card",
    "table card",
    "mechanism_evidence_table.md",
    "dosage_window_table.md",
    "review_handoff.md",
    "obsidian_note.md",
    "claim-evidence-boundary",
    "borrowable writing",
    "dosage window",
    "Obsidian",
    "assets/README.md",
    "visual_asset_spec.json",
    "asset_manifest.md",
    "visual_asset_report.json",
    "contact_sheet.png",
    "rendered_pages",
    "visual_checked",
    "asset_file",
    "crop_status",
    "qa_status",
]

SAMPLE_VISUAL_ASSET_ROOT = Path("outputs") / "wer-ea-30-reading-sample"
SAMPLE_VISUAL_ASSET_FILES = [
    "visual_asset_spec.json",
    "assets/asset_manifest.md",
    "assets/visual_asset_report.json",
    "assets/contact_sheet.png",
]

WER_EA_REVIEW_PIPELINE_FILES = [
    Path("civil-materials-writing") / "references" / "wer-ea-mini-review-pipeline.md",
    Path("civil-materials-writing") / "assets" / "templates" / "wer-ea-mini-review-template.md",
]
WER_EA_REVIEW_PIPELINE_TERMS = [
    "research question",
    "screening criteria",
    "evidence matrix",
    "review outline",
    "paragraph skeleton",
    "gap wording",
    "reviewer risk",
]

FIGURE_REVIEW_MAP_FILES = [
    Path("civil-materials-figure") / "references" / "wer-ea-review-figure-contract.md",
    Path("civil-materials-figure") / "assets" / "templates" / "wer-ea-figure-contract-template.md",
]
FIGURE_REVIEW_MAP_TERMS = [
    "figure contract",
    "mechanism map",
    "evidence heatmap",
    "material-system map",
    "performance-mechanism boundary",
    "literature-screening flow",
    "graphical abstract",
]

FIGURE_HARD_WORKFLOW_FILES = [
    Path("civil-materials-figure") / "SKILL.md",
    Path("civil-materials-figure") / "README.md",
    Path("civil-materials-figure") / "manifest.yaml",
    Path("civil-materials-figure") / "evals" / "evals.json",
    Path("civil-materials-figure") / "static" / "core" / "figure-contract.md",
    Path("civil-materials-figure") / "static" / "core" / "stance.md",
    Path("civil-materials-figure") / "static" / "core" / "workflow.md",
    Path("civil-materials-figure") / "static" / "fragments" / "backend" / "python.md",
    Path("civil-materials-figure") / "static" / "fragments" / "backend" / "r.md",
    Path("civil-materials-figure") / "references" / "backend-selection.md",
    Path("civil-materials-figure") / "references" / "figure-package-protocol.md",
    Path("civil-materials-figure") / "references" / "figure-qa-contract.md",
    Path("civil-materials-figure") / "assets" / "templates" / "figure-contract-template.md",
    Path("civil-materials-figure") / "assets" / "templates" / "figure-package" / "figure_contract.md",
    Path("civil-materials-figure") / "assets" / "templates" / "figure-package" / "caption.md",
    Path("civil-materials-figure") / "assets" / "templates" / "figure-package" / "qa_report.md",
    Path("civil-materials-figure") / "assets" / "templates" / "figure-package" / "asset_manifest.md",
    Path("civil-materials-figure") / "assets" / "templates" / "figure-package" / "source_data.csv",
    Path("civil-materials-figure") / "assets" / "templates" / "figure-package" / "plot.py",
    Path("civil-materials-figure") / "scripts" / "audit_figure_package.py",
]
FIGURE_HARD_WORKFLOW_TERMS = [
    "backend gate",
    "Python or R?",
    "Do not default",
    "selected backend is exclusive",
    "figure package",
    "Core conclusion",
    "Evidence chain",
    "WER-EA boundary",
    "source data",
    "claim boundary",
    "QA Status",
    "same backend",
    "matplotlib",
    "ggplot2",
]
FIGURE_HARD_WORKFLOW_EVAL_IDS = [
    "backend-exclusivity-r-missing-runtime",
    "backend-exclusivity-python-missing-package",
    "journal-ready-package-audit",
]
FIGURE_PACKAGE_SAMPLE_NAMES = [
    "wer-ea-mechanism-map",
    "wer-ea-evidence-heatmap",
    "wer-ea-dosage-window",
]

TABLE_SYSTEM_SKILLS = [
    "civil-materials-reader",
    "civil-materials-writing",
    "civil-materials-data",
    "civil-materials-figure",
]
TABLE_SYSTEM_TERMS = [
    "literature-screening-table",
    "mechanism-evidence-table",
    "test-method-table",
    "performance-comparison-table",
    "durability-evidence-table",
    "journal-positioning-table",
]

MOJIBAKE_TARGET_SKILLS = [
    "civil-materials-reader",
    "civil-materials-writing",
    "civil-materials-figure",
]


def _chars(hex_values: str) -> str:
    return "".join(chr(int(value, 16)) for value in hex_values.split())


MOJIBAKE_MARKERS = [
    _chars("93c2 56e9 5c1e"),  # mojibake for Chinese trigger text
    _chars("7eee 6a0a 521b"),
    _chars("7eee 6377"),
    _chars("934f 3126 67ab"),
    _chars("6d93 e185 5ad8"),
    _chars("7f01 8270 582a"),
    _chars("7487 4f7a 6d47"),
    _chars("7019 ff00 5d58"),
    _chars("934f 637f 3013"),
    _chars("59d8 5b58 20ac"),
    _chars("93c8 60e7 7de5"),
    _chars("934f 9e43 9801"),
    _chars("943a 719f 6d58"),
    _chars("93c4 60e7 4e95"),
    _chars("5be4 e060"),
    _chars("59f9 56e6"),
    _chars("93c8 6a0a"),
    _chars("5bee 66df"),
    _chars("93c2 89c4 7845"),
    _chars("7f01 64bc"),
    _chars("7481 3128"),
    _chars("7f01 64b9"),
    _chars("7481 70d8 6783"),
    _chars("5f20 54c4"),
    _chars("9edb 5fdd"),
    _chars("9470 6124"),
    _chars("59d8 5b58 5d2f"),
    _chars("93c8 54c4"),
    _chars("9437 5ca8 6f70"),
    _chars("741b 3125 7ddb"),
    _chars("9350 592f"),
    _chars("942b e060"),
    _chars("934f 529e"),
    _chars("93c9 56fe"),
]

TEXT_EXTENSIONS = {
    ".md",
    ".yaml",
    ".yml",
    ".py",
    ".csv",
    ".json",
    ".txt",
    ".toml",
}

LOCAL_PATH_MARKERS = [
    "C:" + "\\" + "Users" + "\\" + "97218",
    "/".join(["C:", "Users", "97218"]),
]
SECRET_MARKERS = ["yujian" + "wudi"]
SECRET_TOKEN_RE = re.compile("sk-" + r"[A-Za-z0-9]{20,}")


def run(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=str(cwd), check=True)


def run_pressure_tests(root: Path, skill_root: Path) -> None:
    run(
        [
            sys.executable,
            str(root / "scripts" / "run_pressure_tests.py"),
            "--skill-root",
            str(skill_root),
            "--json",
        ],
        root,
    )


def clean_generated_artifacts(root: Path) -> None:
    for path in sorted(root.rglob("__pycache__"), reverse=True):
        if path.is_dir():
            shutil.rmtree(path)
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in {".pyc", ".pyo"}:
            path.unlink()


def collect_release_issues(root: Path) -> dict[str, list[str]]:
    issues = {
        "missing_skills": [],
        "missing_shared": [],
        "plugin_wrapper": [],
        "marketplace": [],
        "skills_index": [],
        "wer_ea_pipeline": [],
        "reader_fulltext_anchor": [],
        "wer_ea_review_pipeline": [],
        "figure_review_maps": [],
        "figure_hard_workflow": [],
        "sample_visual_assets": [],
        "table_system": [],
        "openai_yaml_format": [],
        "generated_artifacts": [],
        "local_paths": [],
        "mojibake": [],
        "possible_secrets": [],
    }
    shared_root = root / "skills" / "_shared"
    if not shared_root.is_dir():
        issues["missing_shared"].append("skills/_shared")
    for shared_file in REQUIRED_SHARED_FILES:
        if not (shared_root / shared_file).is_file():
            issues["missing_shared"].append(f"skills/_shared/{shared_file}")

    for skill in REQUIRED_SKILLS:
        skill_root = root / "skills" / skill
        if not (skill_root / "SKILL.md").exists():
            issues["missing_skills"].append(skill)
        openai_yaml = skill_root / "agents" / "openai.yaml"
        if not openai_yaml.exists():
            issues["openai_yaml_format"].append(f"{skill}: missing agents/openai.yaml")
        else:
            text = openai_yaml.read_text(encoding="utf-8", errors="ignore")
            if "interface:" not in text or "policy:" not in text or "allow_implicit_invocation" not in text:
                issues["openai_yaml_format"].append(f"{skill}: expected interface/policy wrapper")

    collect_plugin_issues(root, issues)
    collect_skills_index_issues(root, issues)
    collect_wer_ea_pipeline_issues(root, issues)
    collect_advanced_skill_upgrade_issues(root, issues)
    collect_sample_visual_asset_issues(root, issues)
    collect_mojibake_issues(root, issues)

    for path in root.rglob("*"):
        if path.is_dir() and path.name == "__pycache__":
            issues["generated_artifacts"].append(str(path.relative_to(root)))
        if path.is_file() and path.suffix in {".pyc", ".pyo"}:
            issues["generated_artifacts"].append(str(path.relative_to(root)))
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(marker in text for marker in LOCAL_PATH_MARKERS):
            issues["local_paths"].append(str(path.relative_to(root)))
        if any(marker in text for marker in SECRET_MARKERS) or SECRET_TOKEN_RE.search(text):
            issues["possible_secrets"].append(str(path.relative_to(root)))
    return issues


def collect_mojibake_issues(root: Path, issues: dict[str, list[str]]) -> None:
    for label, skills_root in iter_skill_roots(root):
        for skill in MOJIBAKE_TARGET_SKILLS:
            skill_root = skills_root / skill
            if not skill_root.is_dir():
                continue
            for path in skill_root.rglob("*"):
                if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
                for line_number, line in enumerate(text.splitlines(), 1):
                    if "\ufffd" in line:
                        issues["mojibake"].append(
                            f"{label}: {path.relative_to(root)}:{line_number} contains replacement character"
                        )
                    if any("\ue000" <= char <= "\uf8ff" for char in line):
                        issues["mojibake"].append(
                            f"{label}: {path.relative_to(root)}:{line_number} contains private-use character"
                        )
                    marker = next((marker for marker in MOJIBAKE_MARKERS if marker in line), None)
                    if marker is not None:
                        issues["mojibake"].append(
                            f"{label}: {path.relative_to(root)}:{line_number} contains likely mojibake marker {marker!r}"
                        )


def iter_skill_roots(root: Path) -> list[tuple[str, Path]]:
    skill_roots = [("root", root / "skills")]
    plugin_skills_root = root / PLUGIN_ROOT / "skills"
    if plugin_skills_root.is_dir():
        skill_roots.append(("plugin", plugin_skills_root))
    return skill_roots


def collect_skills_index_issues(root: Path, issues: dict[str, list[str]]) -> None:
    readme_path = root / "README.md"
    index_path = root / SKILLS_INDEX_PATH
    if not readme_path.is_file():
        issues["skills_index"].append("README.md is missing")
        readme_text = ""
    else:
        readme_text = readme_path.read_text(encoding="utf-8", errors="ignore")
        if "## Skill Status Index" not in readme_text:
            issues["skills_index"].append("README.md must include a Skill Status Index section")
        for column in README_STATUS_COLUMNS:
            if column not in readme_text:
                issues["skills_index"].append(f"README.md status table missing column {column!r}")

    if not index_path.is_file():
        issues["skills_index"].append(f"{SKILLS_INDEX_PATH.as_posix()} is missing")
        index_text = ""
    else:
        index_text = index_path.read_text(encoding="utf-8", errors="ignore")
        if "Human-Readable Skills Index" not in index_text:
            issues["skills_index"].append(f"{SKILLS_INDEX_PATH.as_posix()} missing title")

    for skill in REQUIRED_SKILLS:
        marker = f"`{skill}`"
        if marker not in readme_text:
            issues["skills_index"].append(f"README.md status table missing {skill}")
        if marker not in index_text:
            issues["skills_index"].append(f"{SKILLS_INDEX_PATH.as_posix()} missing {skill}")


def collect_wer_ea_pipeline_issues(root: Path, issues: dict[str, list[str]]) -> None:
    skill_paths = [
        Path("civil-materials-research") / "SKILL.md",
        Path("civil-materials-reader") / "SKILL.md",
        Path("civil-materials-writing") / "SKILL.md",
    ]
    skill_roots = [("root", root / "skills")]
    plugin_skills_root = root / PLUGIN_ROOT / "skills"
    if plugin_skills_root.is_dir():
        skill_roots.append(("plugin", plugin_skills_root))

    for label, skills_root in skill_roots:
        combined_parts = []
        for relative_path in skill_paths:
            path = skills_root / relative_path
            if not path.is_file():
                issues["wer_ea_pipeline"].append(f"{label}: missing {path.relative_to(root)}")
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            combined_parts.append(text)
            if "WER-EA" not in text:
                issues["wer_ea_pipeline"].append(f"{label}: {path.relative_to(root)} missing WER-EA marker")
        combined_text = "\n".join(combined_parts).lower()
        for term in WER_EA_REQUIRED_TERMS:
            if term not in combined_text:
                issues["wer_ea_pipeline"].append(f"{label}: WER-EA pipeline missing {term!r}")


def collect_advanced_skill_upgrade_issues(root: Path, issues: dict[str, list[str]]) -> None:
    skill_roots = [("root", root / "skills")]
    plugin_skills_root = root / PLUGIN_ROOT / "skills"
    if plugin_skills_root.is_dir():
        skill_roots.append(("plugin", plugin_skills_root))

    for label, skills_root in skill_roots:
        collect_required_file_terms(
            root,
            label,
            skills_root,
            READER_FULLTEXT_ANCHOR_FILES,
            READER_FULLTEXT_ANCHOR_TERMS,
            issues["reader_fulltext_anchor"],
        )
        collect_required_file_terms(
            root,
            label,
            skills_root,
            WER_EA_REVIEW_PIPELINE_FILES,
            WER_EA_REVIEW_PIPELINE_TERMS,
            issues["wer_ea_review_pipeline"],
        )
        collect_required_file_terms(
            root,
            label,
            skills_root,
            FIGURE_REVIEW_MAP_FILES,
            FIGURE_REVIEW_MAP_TERMS,
            issues["figure_review_maps"],
        )
        collect_figure_hard_workflow_issues(root, label, skills_root, issues["figure_hard_workflow"])
        collect_table_system_issues(root, label, skills_root, issues["table_system"])


def collect_required_file_terms(
    root: Path,
    label: str,
    skills_root: Path,
    relative_files: list[Path],
    required_terms: list[str],
    issue_list: list[str],
) -> None:
    combined_text_parts = []
    for relative_file in relative_files:
        path = skills_root / relative_file
        if not path.is_file():
            issue_list.append(f"{label}: missing {path.relative_to(root)}")
            continue
        combined_text_parts.append(path.read_text(encoding="utf-8", errors="ignore"))
    combined_text = "\n".join(combined_text_parts).lower()
    for term in required_terms:
        if term.lower() not in combined_text:
            issue_list.append(f"{label}: missing term {term!r}")


def collect_table_system_issues(root: Path, label: str, skills_root: Path, issue_list: list[str]) -> None:
    combined_parts = []
    for skill in TABLE_SYSTEM_SKILLS:
        reference_path = skills_root / skill / "references" / "table-system.md"
        template_path = skills_root / skill / "assets" / "templates" / "table-system-template.md"
        skill_path = skills_root / skill / "SKILL.md"
        for path in [reference_path, template_path]:
            if not path.is_file():
                issue_list.append(f"{label}: missing {path.relative_to(root)}")
            else:
                combined_parts.append(path.read_text(encoding="utf-8", errors="ignore"))
        if not skill_path.is_file():
            issue_list.append(f"{label}: missing {skill_path.relative_to(root)}")
        else:
            skill_text = skill_path.read_text(encoding="utf-8", errors="ignore")
            combined_parts.append(skill_text)
            if "table-system.md" not in skill_text:
                issue_list.append(f"{label}: {skill_path.relative_to(root)} must mention table-system.md")
            if "table-system-template.md" not in skill_text:
                issue_list.append(f"{label}: {skill_path.relative_to(root)} must mention table-system-template.md")
    combined_text = "\n".join(combined_parts).lower()
    for term in TABLE_SYSTEM_TERMS:
        if term not in combined_text:
            issue_list.append(f"{label}: table system missing {term!r}")


def collect_figure_hard_workflow_issues(root: Path, label: str, skills_root: Path, issue_list: list[str]) -> None:
    collect_required_file_terms(
        root,
        label,
        skills_root,
        FIGURE_HARD_WORKFLOW_FILES,
        FIGURE_HARD_WORKFLOW_TERMS,
        issue_list,
    )

    figure_root = skills_root / "civil-materials-figure"
    evals_path = figure_root / "evals" / "evals.json"
    evals_payload = read_json(evals_path, issue_list, f"{label}: figure_hard_workflow")
    if evals_payload is not None:
        if evals_payload.get("skill_name") != "civil-materials-figure":
            issue_list.append(f"{label}: figure evals skill_name mismatch")
        evals = evals_payload.get("evals")
        if not isinstance(evals, list):
            issue_list.append(f"{label}: figure evals must contain an evals list")
        else:
            ids = sorted(case.get("id") for case in evals if isinstance(case, dict))
            if ids != sorted(FIGURE_HARD_WORKFLOW_EVAL_IDS):
                issue_list.append(
                    f"{label}: figure eval ids expected {sorted(FIGURE_HARD_WORKFLOW_EVAL_IDS)}, got {ids}"
                )

    sample_root = figure_root / "examples" / "figure-packages"
    audit_script = figure_root / "scripts" / "audit_figure_package.py"
    if not sample_root.is_dir():
        issue_list.append(f"{label}: missing {sample_root.relative_to(root)}")
        return
    if not audit_script.is_file():
        issue_list.append(f"{label}: missing {audit_script.relative_to(root)}")
        return

    sample_names = sorted(path.name for path in sample_root.iterdir() if path.is_dir())
    if sample_names != sorted(FIGURE_PACKAGE_SAMPLE_NAMES):
        issue_list.append(
            f"{label}: figure package samples expected {sorted(FIGURE_PACKAGE_SAMPLE_NAMES)}, got {sample_names}"
        )

    for sample_name in FIGURE_PACKAGE_SAMPLE_NAMES:
        package_dir = sample_root / sample_name
        if not package_dir.is_dir():
            issue_list.append(f"{label}: missing {package_dir.relative_to(root)}")
            continue
        result = subprocess.run(
            [
                sys.executable,
                str(audit_script),
                "--package-dir",
                str(package_dir),
                "--json",
            ],
            cwd=str(root),
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if result.returncode != 0:
            detail = result.stdout.strip() or result.stderr.strip()
            issue_list.append(f"{label}: {sample_name} failed audit_figure_package.py: {detail}")


def collect_sample_visual_asset_issues(root: Path, issues: dict[str, list[str]]) -> None:
    sample_root = root / SAMPLE_VISUAL_ASSET_ROOT
    if not sample_root.is_dir():
        issues["sample_visual_assets"].append(f"missing {SAMPLE_VISUAL_ASSET_ROOT.as_posix()}")
        return
    paper_dirs = [path for path in sample_root.iterdir() if path.is_dir()]
    if len(paper_dirs) < 3:
        issues["sample_visual_assets"].append("expected at least 3 sample paper directories")
    for paper_dir in paper_dirs:
        for relative_file in SAMPLE_VISUAL_ASSET_FILES:
            if not (paper_dir / relative_file).is_file():
                issues["sample_visual_assets"].append(
                    f"missing {(paper_dir / relative_file).relative_to(root)}"
                )
        rendered = list((paper_dir / "assets" / "rendered_pages").glob("*.png"))
        figures = list((paper_dir / "assets" / "figures").glob("*.png"))
        tables = list((paper_dir / "assets" / "tables").glob("*.png"))
        if not rendered:
            issues["sample_visual_assets"].append(f"{paper_dir.relative_to(root)} missing rendered page PNG")
        if not figures and not tables:
            issues["sample_visual_assets"].append(f"{paper_dir.relative_to(root)} missing cropped visual PNG")
        cards_path = paper_dir / "figure_table_cards.md"
        if not cards_path.is_file():
            issues["sample_visual_assets"].append(f"{paper_dir.relative_to(root)} missing figure_table_cards.md")
            continue
        cards_text = cards_path.read_text(encoding="utf-8", errors="ignore").lower()
        for term in ["visual_checked", "asset_file", "crop_status", "qa_status"]:
            if term not in cards_text:
                issues["sample_visual_assets"].append(
                    f"{cards_path.relative_to(root)} missing {term}"
                )


def read_json(path: Path, issue_list: list[str], label: str) -> dict | None:
    if not path.is_file():
        issue_list.append(f"{label}: missing {path.as_posix()}")
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        issue_list.append(f"{label}: invalid JSON in {path.as_posix()}: {exc}")
        return None
    if not isinstance(payload, dict):
        issue_list.append(f"{label}: {path.as_posix()} must contain a JSON object")
        return None
    return payload


def collect_plugin_issues(root: Path, issues: dict[str, list[str]]) -> None:
    plugin_root = root / PLUGIN_ROOT
    plugin_json_path = plugin_root / ".codex-plugin" / "plugin.json"
    plugin_skills_root = plugin_root / "skills"
    plugin_shared_root = plugin_skills_root / "_shared"
    plugin_mcp_path = plugin_root / ".mcp.json"
    marketplace_path = root / MARKETPLACE_PATH

    plugin_json = read_json(plugin_json_path, issues["plugin_wrapper"], "plugin_wrapper")
    if plugin_json is not None:
        expected_plugin_fields = {
            "name": PLUGIN_NAME,
            "version": "1.0.0",
            "skills": "./skills/",
            "mcpServers": "./.mcp.json",
            "license": "MIT",
            "repository": "https://github.com/cooleava1-gif/civil-materials-skills",
            "homepage": "https://github.com/cooleava1-gif/civil-materials-skills",
        }
        for key, expected in expected_plugin_fields.items():
            if plugin_json.get(key) != expected:
                issues["plugin_wrapper"].append(
                    f"plugin.json field {key!r} expected {expected!r}, got {plugin_json.get(key)!r}"
                )
        author = plugin_json.get("author")
        if not isinstance(author, dict) or author.get("name") != "Civil Materials Skills contributors":
            issues["plugin_wrapper"].append("plugin.json author.name must be Civil Materials Skills contributors")
        interface = plugin_json.get("interface")
        if not isinstance(interface, dict):
            issues["plugin_wrapper"].append("plugin.json interface must be an object")
        else:
            if interface.get("displayName") != "Civil Materials Skills":
                issues["plugin_wrapper"].append("plugin.json interface.displayName mismatch")
            if interface.get("category") != "Research":
                issues["plugin_wrapper"].append("plugin.json interface.category must be Research")
            if interface.get("capabilities") != ["Interactive", "Read", "Write"]:
                issues["plugin_wrapper"].append("plugin.json interface.capabilities mismatch")
            prompts = interface.get("defaultPrompt")
            if not isinstance(prompts, list) or len(prompts) != 3 or not all(isinstance(item, str) and item for item in prompts):
                issues["plugin_wrapper"].append("plugin.json interface.defaultPrompt must contain three non-empty strings")

    mcp_json = read_json(plugin_mcp_path, issues["plugin_wrapper"], "plugin_wrapper")
    if mcp_json is not None:
        servers = mcp_json.get("mcpServers")
        server = servers.get("civil-materials-academic-search") if isinstance(servers, dict) else None
        if not isinstance(server, dict):
            issues["plugin_wrapper"].append(".mcp.json must define civil-materials-academic-search")
        else:
            if server.get("command") != "python":
                issues["plugin_wrapper"].append(".mcp.json civil-materials-academic-search command must be python")
            expected_args = ["./skills/civil-materials-citation/mcp/academic_search/server.py"]
            if server.get("args") != expected_args:
                issues["plugin_wrapper"].append(".mcp.json civil-materials-academic-search args mismatch")
            entrypoint = plugin_root / "skills" / "civil-materials-citation" / "mcp" / "academic_search" / "server.py"
            if not entrypoint.is_file():
                issues["plugin_wrapper"].append("plugin MCP server entrypoint is missing")

    if not plugin_skills_root.is_dir():
        issues["plugin_wrapper"].append("plugins/civil-materials-skills/skills")
    if not plugin_shared_root.is_dir():
        issues["plugin_wrapper"].append("plugins/civil-materials-skills/skills/_shared")
    for shared_file in REQUIRED_SHARED_FILES:
        if not (plugin_shared_root / shared_file).is_file():
            issues["plugin_wrapper"].append(f"plugins/civil-materials-skills/skills/_shared/{shared_file}")
    for skill in REQUIRED_SKILLS:
        skill_root = plugin_skills_root / skill
        if not (skill_root / "SKILL.md").is_file():
            issues["plugin_wrapper"].append(f"plugins/civil-materials-skills/skills/{skill}/SKILL.md")
        if not (skill_root / "agents" / "openai.yaml").is_file():
            issues["plugin_wrapper"].append(f"plugins/civil-materials-skills/skills/{skill}/agents/openai.yaml")
    if plugin_skills_root.is_dir():
        plugin_skill_names = sorted(
            child.name
            for child in plugin_skills_root.iterdir()
            if child.is_dir() and child.name.startswith("civil-materials-")
        )
        if plugin_skill_names != sorted(REQUIRED_SKILLS):
            issues["plugin_wrapper"].append("plugin skill directory list does not match REQUIRED_SKILLS")

    marketplace = read_json(marketplace_path, issues["marketplace"], "marketplace")
    if marketplace is not None:
        if marketplace.get("name") != PLUGIN_NAME:
            issues["marketplace"].append("marketplace name must be civil-materials-skills")
        interface = marketplace.get("interface")
        if not isinstance(interface, dict) or interface.get("displayName") != "Civil Materials Skills":
            issues["marketplace"].append("marketplace interface.displayName mismatch")
        plugins = marketplace.get("plugins")
        if not isinstance(plugins, list) or len(plugins) != 1 or not isinstance(plugins[0], dict):
            issues["marketplace"].append("marketplace must contain exactly one plugin entry")
        else:
            entry = plugins[0]
            if entry.get("name") != PLUGIN_NAME:
                issues["marketplace"].append("marketplace plugin name mismatch")
            if entry.get("source") != {"source": "local", "path": "./plugins/civil-materials-skills"}:
                issues["marketplace"].append("marketplace plugin source mismatch")
            if entry.get("policy") != {"installation": "AVAILABLE", "authentication": "ON_INSTALL"}:
                issues["marketplace"].append("marketplace plugin policy mismatch")
            if entry.get("category") != "Research":
                issues["marketplace"].append("marketplace plugin category must be Research")


def run_tests(root: Path) -> None:
    test_roots = [
        root / "skills" / "civil-materials-research" / "tests",
        root / "skills" / "civil-materials-reader" / "tests",
        root / "skills" / "civil-materials-data" / "tests",
        root / "skills" / "civil-materials-writing" / "tests",
        root / "skills" / "civil-materials-figure" / "tests",
        root / "skills" / "civil-materials-polishing" / "tests",
        root / "skills" / "civil-materials-response" / "tests",
        root / "skills" / "civil-materials-reviewer" / "tests",
        root / "skills" / "civil-materials-citation" / "mcp" / "academic_search" / "tests",
    ]
    for test_root in test_roots:
        run([sys.executable, "-m", "unittest", "discover", "-s", str(test_root), "-p", "test_*.py", "-v"], root)

    run_pressure_tests(root, root / "skills")
    plugin_skills_root = root / PLUGIN_ROOT / "skills"
    if plugin_skills_root.is_dir():
        run_pressure_tests(root, plugin_skills_root)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    clean_generated_artifacts(root)
    run_tests(root)
    clean_generated_artifacts(root)
    issues = collect_release_issues(root)
    status = "pass" if all(not value for value in issues.values()) else "incomplete"
    report = {"status": status, "issues": issues}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

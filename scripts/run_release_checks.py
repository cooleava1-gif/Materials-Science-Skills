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
    "paper-production/weakness-routing.md",
    "paper-production/weakness-routing-template.csv",
    "paper-production/paper-gate-report-template.md",
    "paper-production/audit_paper_production.py",
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
ROOT_README_PRODUCT_MARKERS = [
    "## Quick Start",
    "## Four Workflow Entry Points",
    "## Installation Paths",
    "## Skill Status Index",
    "## Guided Demos",
    "## Visual Gallery",
]
INSTALL_GUIDE_MARKERS = [
    "# Install Civil Materials Skills",
    "## Option 1: Codex Plugin",
    "## Option 2: Manual Skills Install",
    "## Verify The Install",
    "## Five-Minute Walkthrough",
    "## Guided Demo Routes",
]
WORKFLOW_DOCS = {
    "wer-ea-mini-review.md": "WER-EA mini-review",
    "experimental-manuscript.md": "Experimental manuscript",
    "revision-loop.md": "Revision loop",
    "paper-to-presentation.md": "Paper to presentation",
}
WORKFLOW_DOC_REQUIRED_MARKERS = [
    "## Route Summary",
    "## Demo Prompt",
    "## Workflow Steps",
    "## Expected Artifacts",
    "## What Good Looks Like",
]
GALLERY_MARKERS = [
    "# Civil Materials Gallery",
    "## Screenshot Gallery",
    "## Workflow Proof",
    "## Artifact Deep Dives",
    "wer_ea_mechanism_map.png",
    "wer_ea_evidence_heatmap.png",
    "wer_ea_dosage_window.png",
    "contact_sheet.png",
]
SKILL_README_REQUIRED_HEADINGS = [
    "## When To Use",
    "## Inputs",
    "## Outputs",
    "## Example",
    "## Validation",
    "## Boundaries",
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
    Path("civil-materials-reader") / "references" / "evidence-to-review-handoff.md",
    Path("civil-materials-reader") / "assets" / "templates" / "paper-md-template.md",
    Path("civil-materials-reader") / "assets" / "templates" / "source-map-template.json",
    Path("civil-materials-reader") / "assets" / "templates" / "source-anchor-checklist.md",
    Path("civil-materials-reader") / "assets" / "templates" / "translation-notes-template.md",
    Path("civil-materials-reader") / "assets" / "templates" / "figure-table-card-template.md",
    Path("civil-materials-reader") / "assets" / "templates" / "mechanism-evidence-table-template.md",
    Path("civil-materials-reader") / "assets" / "templates" / "dosage-window-table-template.md",
    Path("civil-materials-reader") / "assets" / "templates" / "citation-handoff-template.csv",
    Path("civil-materials-reader") / "assets" / "templates" / "figure-handoff-template.csv",
    Path("civil-materials-reader") / "assets" / "templates" / "review-handoff-template.md",
    Path("civil-materials-reader") / "assets" / "templates" / "obsidian-note-template.md",
    Path("civil-materials-reader") / "scripts" / "extract_pdf_visual_assets.py",
]
READER_FULLTEXT_ANCHOR_TERMS = [
    "paper.md",
    "source_map.json",
    "source_anchor_checklist.md",
    "translation_notes.md",
    "citation_handoff.csv",
    "figure_handoff.csv",
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
    "source_anchor",
    "citation_role",
    "figure_archetype",
    "handoff_target",
]

CITATION_REVIEW_HANDOFF_FILES = [
    Path("civil-materials-citation") / "SKILL.md",
    Path("civil-materials-citation") / "manifest.yaml",
    Path("civil-materials-citation") / "assets" / "templates" / "citation-matrix-template.csv",
    Path("civil-materials-citation") / "references" / "claim-citation-mapping.md",
    Path("civil-materials-citation") / "references" / "reference-gap-audit.md",
    Path("civil-materials-citation") / "references" / "wer-ea-screening-and-source-quality.md",
    Path("civil-materials-citation") / "scripts" / "build_citation_matrix.py",
    Path("civil-materials-citation") / "mcp" / "academic_search" / "domain" / "classifier.py",
    Path("civil-materials-citation") / "mcp" / "academic_search" / "service.py",
]
CITATION_REVIEW_HANDOFF_TERMS = [
    "wer-ea-screening",
    "source-quality",
    "reviewer-safe-package",
    "claim_id",
    "evidence_layer",
    "source_role",
    "source_quality",
    "mechanism_directness",
    "durability_relevance",
    "service_relevance",
    "reader_anchor",
    "figure_handoff",
    "reviewer_risk",
    "material_formulation",
    "emulsion_stability",
    "bonding_interface_performance",
    "rheology",
    "curing_demulsification",
    "microstructure_chemistry",
    "moisture_aging_durability",
    "service_field_relevance",
    "review_background",
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
    Path("civil-materials-figure") / "references" / "review-figure-intake.md",
    Path("civil-materials-figure") / "assets" / "templates" / "wer-ea-figure-contract-template.md",
    Path("civil-materials-figure") / "assets" / "templates" / "review-figure-intake-template.csv",
]
FIGURE_REVIEW_MAP_TERMS = [
    "figure contract",
    "mechanism map",
    "evidence heatmap",
    "material-system map",
    "performance-mechanism boundary",
    "literature-screening flow",
    "graphical abstract",
    "review-figure intake",
    "certainty_tier",
    "caption_boundary",
    "missing_evidence_marker",
    "measured",
    "inferred",
    "speculative",
    "missing",
]

READER_STANDARD_PACKAGE_FILES = [
    Path("civil-materials-reader") / "references" / "standard-output-package.md",
    Path("civil-materials-reader") / "assets" / "schemas" / "source-map.schema.json",
    Path("civil-materials-reader") / "assets" / "schemas" / "visual-asset-spec.schema.json",
    Path("civil-materials-reader") / "assets" / "schemas" / "visual-asset-report.schema.json",
    Path("civil-materials-reader") / "assets" / "schemas" / "reader-package-manifest.schema.json",
    Path("civil-materials-reader") / "assets" / "templates" / "package-manifest-template.json",
    Path("civil-materials-reader") / "assets" / "templates" / "qa-report-template.md",
    Path("civil-materials-reader") / "scripts" / "build_reader_package.py",
    Path("civil-materials-reader") / "scripts" / "audit_reader_package.py",
    Path("civil-materials-reader") / "scripts" / "validate_reader_package.py",
]
READER_STANDARD_PACKAGE_TERMS = [
    "package_manifest.json",
    "source_map.json",
    "citation_handoff.csv",
    "figure_handoff.csv",
    "review_handoff.md",
    "qa_report.md",
    "civil-materials-reader-package",
    "source_anchor",
    "caption_boundary",
    "reviewer_risk",
]

ACADEMIC_SEARCH_EXPANDED_FILES = [
    Path("civil-materials-citation") / "mcp" / "academic_search" / "adapters" / "arxiv.py",
    Path("civil-materials-citation") / "mcp" / "academic_search" / "adapters" / "elsevier_common.py",
    Path("civil-materials-citation") / "mcp" / "academic_search" / "adapters" / "scopus.py",
    Path("civil-materials-citation") / "mcp" / "academic_search" / "adapters" / "sciencedirect.py",
    Path("civil-materials-citation") / "mcp" / "academic_search" / "domain" / "identifiers.py",
    Path("civil-materials-citation") / "mcp" / "academic_search" / "importers" / "citation_files.py",
    Path("civil-materials-citation") / "mcp" / "academic_search" / "export" / "csl_json.py",
    Path("civil-materials-citation") / "mcp" / "academic_search" / "export" / "jsonl.py",
    Path("civil-materials-citation") / "mcp" / "academic_search" / "server.py",
    Path("civil-materials-citation") / "mcp" / "academic_search" / "service.py",
]
ACADEMIC_SEARCH_EXPANDED_TERMS = [
    "ArxivAdapter",
    "ScopusAdapter",
    "ScienceDirectAdapter",
    "AdapterDisabled",
    "resolve_paper_ids",
    "list_academic_sources",
    "convert_citation_records",
    "deduplicate_citation_records",
    "csl-json",
    "jsonl",
]

WER_EA_ATLAS_FILES = [
    Path("civil-materials-figure") / "references" / "wer-ea-figure-atlas.md",
    Path("civil-materials-figure") / "assets" / "wer-ea-atlas" / "asset-specs.csv",
    Path("civil-materials-figure") / "assets" / "wer-ea-atlas" / "data" / "mechanism_edges.csv",
    Path("civil-materials-figure") / "assets" / "wer-ea-atlas" / "data" / "evidence_heatmap.csv",
    Path("civil-materials-figure") / "assets" / "wer-ea-atlas" / "data" / "material_systems.csv",
    Path("civil-materials-figure") / "assets" / "wer-ea-atlas" / "data" / "performance_boundary.csv",
    Path("civil-materials-figure") / "assets" / "wer-ea-atlas" / "data" / "screening_flow.csv",
    Path("civil-materials-figure") / "assets" / "wer-ea-atlas" / "data" / "dosage_window.csv",
    Path("civil-materials-figure") / "assets" / "wer-ea-atlas" / "data" / "durability_retention.csv",
    Path("civil-materials-figure") / "assets" / "wer-ea-atlas" / "data" / "characterization_panel.csv",
    Path("civil-materials-figure") / "assets" / "wer-ea-atlas" / "data" / "construction_workflow.csv",
    Path("civil-materials-figure") / "assets" / "wer-ea-atlas" / "data" / "lca_boundary.csv",
    Path("civil-materials-figure") / "assets" / "wer-ea-atlas" / "data" / "research_gap_matrix.csv",
    Path("civil-materials-figure") / "scripts" / "wer_ea_atlas" / "generate_atlas.py",
]
WER_EA_ATLAS_TERMS = [
    "wer-ea-mechanism-map",
    "evidence-heatmap",
    "material-system-map",
    "performance-mechanism-boundary",
    "literature-screening-flow",
    "graphical-abstract",
    "dosage-workability-window",
    "sustainability-lca-boundary-card",
    "template only",
    "measured",
    "inferred",
    "speculative",
    "missing",
]

PAPER_PRODUCTION_ORCHESTRATOR_FILES = [
    Path("civil-materials-research") / "SKILL.md",
    Path("civil-materials-research") / "manifest.yaml",
    Path("civil-materials-research") / "references" / "paper-production-orchestrator.md",
    Path("_shared") / "paper-production" / "weakness-routing.md",
    Path("_shared") / "paper-production" / "weakness-routing-template.csv",
    Path("_shared") / "paper-production" / "paper-gate-report-template.md",
    Path("_shared") / "paper-production" / "audit_paper_production.py",
    Path("civil-materials-writing") / "static" / "core" / "contract.md",
    Path("civil-materials-polishing") / "static" / "core" / "contract.md",
    Path("civil-materials-reviewer") / "static" / "core" / "contract.md",
    Path("civil-materials-response") / "static" / "core" / "contract.md",
    Path("civil-materials-figure") / "static" / "core" / "contract.md",
]
PAPER_PRODUCTION_ORCHESTRATOR_TERMS = [
    "paper-production",
    "paper_stage",
    "workflow_mode",
    "output_package",
    "WER-EA mini-review",
    "experimental manuscript",
    "weakness_id",
    "route_to",
    "regression_check",
    "Literature Coverage",
    "Source Anchoring",
    "Mechanism Boundary",
    "Figure And Table Integrity",
    "Manuscript Logic",
    "Reviewer Simulation",
    "Submission Fit",
    "reader-package",
    "gate report",
    "weakness-routing rows",
    "figure_handoff",
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
    "civil-materials-citation",
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
        "citation_review_handoff": [],
        "wer_ea_review_pipeline": [],
        "figure_review_maps": [],
        "reader_standard_package": [],
        "academic_search_expanded_sources": [],
        "wer_ea_asset_library": [],
        "paper_production_orchestrator": [],
        "skill_architecture": [],
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

    # Runtime smoke checks import helper scripts and can create bytecode caches.
    # Clean once more before scanning for generated artifacts in the release tree.
    clean_generated_artifacts(root)

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
    install_path = root / "install.md"
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
        for marker in ROOT_README_PRODUCT_MARKERS:
            if marker not in readme_text:
                issues["skills_index"].append(f"README.md missing product marker {marker!r}")

    if not install_path.is_file():
        issues["skills_index"].append("install.md is missing")
    else:
        install_text = install_path.read_text(encoding="utf-8", errors="ignore")
        for marker in INSTALL_GUIDE_MARKERS:
            if marker not in install_text:
                issues["skills_index"].append(f"install.md missing marker {marker!r}")

    workflow_root = root / "docs" / "workflows"
    workflow_index = workflow_root / "README.md"
    if not workflow_index.is_file():
        issues["skills_index"].append("docs/workflows/README.md is missing")
    else:
        workflow_index_text = workflow_index.read_text(encoding="utf-8", errors="ignore")
        for marker in ["# Workflow Demos", "## Workflow Index"]:
            if marker not in workflow_index_text:
                issues["skills_index"].append(f"docs/workflows/README.md missing marker {marker!r}")

    for filename, title in WORKFLOW_DOCS.items():
        workflow_path = workflow_root / filename
        if not workflow_path.is_file():
            issues["skills_index"].append(f"docs/workflows/{filename} is missing")
            continue
        workflow_text = workflow_path.read_text(encoding="utf-8", errors="ignore")
        if f"# {title}" not in workflow_text:
            issues["skills_index"].append(f"docs/workflows/{filename} missing title {title!r}")
        for marker in WORKFLOW_DOC_REQUIRED_MARKERS:
            if marker not in workflow_text:
                issues["skills_index"].append(f"docs/workflows/{filename} missing marker {marker!r}")

    gallery_path = root / "docs" / "gallery" / "README.md"
    if not gallery_path.is_file():
        issues["skills_index"].append("docs/gallery/README.md is missing")
    else:
        gallery_text = gallery_path.read_text(encoding="utf-8", errors="ignore")
        for marker in GALLERY_MARKERS:
            if marker not in gallery_text:
                issues["skills_index"].append(f"docs/gallery/README.md missing marker {marker!r}")

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

    for label, skills_root in iter_skill_roots(root):
        for skill in REQUIRED_SKILLS:
            skill_readme = skills_root / skill / "README.md"
            if not skill_readme.is_file():
                issues["skills_index"].append(f"{label}: missing {skill_readme.relative_to(root)}")
                continue
            skill_text = skill_readme.read_text(encoding="utf-8", errors="ignore")
            title = f"# {skill}"
            if title not in skill_text:
                issues["skills_index"].append(f"{label}: {skill_readme.relative_to(root)} missing title {title!r}")
            for heading in SKILL_README_REQUIRED_HEADINGS:
                if heading not in skill_text:
                    issues["skills_index"].append(
                        f"{label}: {skill_readme.relative_to(root)} missing section {heading!r}"
                    )


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
            CITATION_REVIEW_HANDOFF_FILES,
            CITATION_REVIEW_HANDOFF_TERMS,
            issues["citation_review_handoff"],
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
        collect_required_file_terms(
            root,
            label,
            skills_root,
            READER_STANDARD_PACKAGE_FILES,
            READER_STANDARD_PACKAGE_TERMS,
            issues["reader_standard_package"],
        )
        collect_required_file_terms(
            root,
            label,
            skills_root,
            ACADEMIC_SEARCH_EXPANDED_FILES,
            ACADEMIC_SEARCH_EXPANDED_TERMS,
            issues["academic_search_expanded_sources"],
        )
        collect_required_file_terms(
            root,
            label,
            skills_root,
            WER_EA_ATLAS_FILES,
            WER_EA_ATLAS_TERMS,
            issues["wer_ea_asset_library"],
        )
        collect_required_file_terms(
            root,
            label,
            skills_root,
            PAPER_PRODUCTION_ORCHESTRATOR_FILES,
            PAPER_PRODUCTION_ORCHESTRATOR_TERMS,
            issues["paper_production_orchestrator"],
        )
        collect_reader_standard_package_runtime_issues(root, label, skills_root, issues["reader_standard_package"])
        collect_wer_ea_atlas_runtime_issues(root, label, skills_root, issues["wer_ea_asset_library"])
        collect_paper_production_orchestrator_issues(root, label, skills_root, issues["paper_production_orchestrator"])
        collect_figure_hard_workflow_issues(root, label, skills_root, issues["figure_hard_workflow"])
        collect_table_system_issues(root, label, skills_root, issues["table_system"])
    collect_skill_architecture_issues(root, issues["skill_architecture"])


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


def collect_reader_standard_package_runtime_issues(
    root: Path,
    label: str,
    skills_root: Path,
    issue_list: list[str],
) -> None:
    reader_root = skills_root / "civil-materials-reader"
    build_script = reader_root / "scripts" / "build_reader_package.py"
    validate_script = reader_root / "scripts" / "validate_reader_package.py"
    if not build_script.is_file() or not validate_script.is_file():
        return

    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        package_dir = Path(tmp) / "reader-package"
        build_result = subprocess.run(
            [
                sys.executable,
                str(build_script),
                "--output-dir",
                str(package_dir),
                "--source-type",
                "pasted-text",
                "--title",
                "Release Gate Smoke",
                "--doi",
                "10.0000/release-gate",
                "--json",
            ],
            cwd=str(root),
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        if build_result.returncode != 0:
            detail = build_result.stdout.strip() or build_result.stderr.strip()
            issue_list.append(f"{label}: build_reader_package.py smoke failed: {detail}")
            return
        validate_result = subprocess.run(
            [
                sys.executable,
                str(validate_script),
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
        if validate_result.returncode != 0:
            detail = validate_result.stdout.strip() or validate_result.stderr.strip()
            issue_list.append(f"{label}: validate_reader_package.py smoke failed: {detail}")


def collect_wer_ea_atlas_runtime_issues(
    root: Path,
    label: str,
    skills_root: Path,
    issue_list: list[str],
) -> None:
    figure_root = skills_root / "civil-materials-figure"
    script = figure_root / "scripts" / "wer_ea_atlas" / "generate_atlas.py"
    if not script.is_file():
        return

    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        result = subprocess.run(
            [
                sys.executable,
                str(script),
                "--output-dir",
                tmp,
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
            issue_list.append(f"{label}: generate_atlas.py smoke failed: {detail}")
            return
        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            issue_list.append(f"{label}: generate_atlas.py returned invalid JSON: {exc}")
            return
        generated = payload.get("generated")
        if payload.get("status") != "pass" or not isinstance(generated, list) or len(generated) < 20:
            issue_list.append(f"{label}: generate_atlas.py expected at least 20 generated assets")
            return
        for row in generated[:3]:
            svg = Path(row.get("svg", ""))
            png = Path(row.get("png", ""))
            if not svg.is_file() or not png.is_file():
                issue_list.append(f"{label}: generate_atlas.py missing generated svg/png for {row.get('asset_id')}")


def collect_paper_production_orchestrator_issues(
    root: Path,
    label: str,
    skills_root: Path,
    issue_list: list[str],
) -> None:
    shared_root = skills_root / "_shared" / "paper-production"
    script = shared_root / "audit_paper_production.py"
    weakness = shared_root / "weakness-routing-template.csv"
    gate = shared_root / "paper-gate-report-template.md"
    if not script.is_file():
        issue_list.append(f"{label}: missing {script.relative_to(root)}")
        return
    result = subprocess.run(
        [
            sys.executable,
            str(script),
            "--weakness-routing",
            str(weakness),
            "--gate-report",
            str(gate),
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
        issue_list.append(f"{label}: audit_paper_production.py failed: {detail}")
        return
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        issue_list.append(f"{label}: audit_paper_production.py returned invalid JSON: {exc}")
        return
    if payload.get("status") != "pass":
        issue_list.append(f"{label}: audit_paper_production.py status is {payload.get('status')!r}")


def collect_skill_architecture_issues(root: Path, issue_list: list[str]) -> None:
    checker = root / "scripts" / "check_skill_architecture.py"
    if not checker.is_file():
        issue_list.append("missing scripts/check_skill_architecture.py")
        return
    result = subprocess.run(
        [sys.executable, str(checker), "--json"],
        cwd=str(root),
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        detail = result.stdout.strip() or result.stderr.strip()
        issue_list.append(f"check_skill_architecture.py failed: {detail}")
        return
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        issue_list.append(f"check_skill_architecture.py returned invalid JSON: {exc}")
        return
    if payload.get("status") != "pass":
        issue_list.append(f"check_skill_architecture.py status is {payload.get('status')!r}")


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
            screenshots = interface.get("screenshots")
            if not isinstance(screenshots, list) or len(screenshots) < 3:
                issues["plugin_wrapper"].append("plugin.json interface.screenshots must contain at least three png paths")
            else:
                for entry in screenshots:
                    if not isinstance(entry, str) or not entry.endswith(".png"):
                        issues["plugin_wrapper"].append(
                            "plugin.json interface.screenshots entries must be .png strings"
                        )
                        continue
                    relative = entry[2:] if entry.startswith("./") else entry
                    screenshot_path = plugin_root / relative
                    if not screenshot_path.is_file():
                        issues["plugin_wrapper"].append(
                            f"plugin.json screenshot path is missing: {screenshot_path.relative_to(root)}"
                        )

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
        root / "skills" / "civil-materials-paper2ppt" / "tests",
        root / "skills" / "civil-materials-pptx" / "tests",
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

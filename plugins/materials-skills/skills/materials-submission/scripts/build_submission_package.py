"""Assemble a submission package from a manifest.

Reads submission-manifest.yaml, checks refusal conditions, loads journal
facts and template, and writes submission-package/ with cover letter,
highlights, checklist, declarations, keywords, SOURCE stubs, and
reviewer-risk-regression. Use --dry-run to validate without writing.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import yaml

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
JOURNAL_FORMATS = PLUGIN_ROOT / "_shared" / "journal-formats"
JOURNAL_TEMPLATES = PLUGIN_ROOT / "_shared" / "journal-templates"

PILOT_JOURNALS = ("cbm", "ccc", "rmpd", "jbe")
SKILL_DIR = Path(__file__).resolve().parents[1]


def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_template(journal_id: str) -> dict:
    return load_yaml(JOURNAL_TEMPLATES / f"{journal_id}.yaml")


def check_refusal(manifest: dict) -> list[str]:
    reasons = []
    if not manifest.get("live_verification_acknowledged"):
        reasons.append("live_verification_acknowledged is false")
    journal = manifest.get("target_journal")
    if journal not in PILOT_JOURNALS:
        reasons.append(f"target_journal {journal!r} not in pilot journals {PILOT_JOURNALS}")
    if manifest.get("data_availability_status") == "pending" and not manifest.get("fair_package_path"):
        reasons.append("data_availability_status is pending but no fair_package_path set")
    if not manifest.get("title"):
        reasons.append("title is missing")
    if not manifest.get("corresponding_author"):
        reasons.append("corresponding_author is missing")
    return reasons


def read_writing_state(path: str) -> dict:
    if not path:
        return {}
    state = load_yaml(Path(path))
    return state


def read_weakness_routing(path: str) -> list[dict]:
    if not path:
        return []
    rows = []
    with Path(path).open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            rows.append(row)
    return rows


def compute_gate_status(rows: list[dict]) -> dict:
    g6 = "not_applicable"
    g7 = "not_applicable"
    for row in rows:
        gate = row.get("gate_id", "")
        status = row.get("status", "")
        if gate == "G6":
            g6 = status or g6
        if gate == "G7":
            g7 = status or g7
    return {"G6": g6, "G7": g7}


def render_manifest_md(manifest: dict, template: dict, writing_state: dict, gates: dict) -> str:
    lines = ["# Submission Package Manifest", ""]
    lines.append(f"Target journal: {manifest.get('target_journal')}")
    lines.append(f"Article type: {manifest.get('article_type')}")
    lines.append(f"Title: {manifest.get('title', '[missing]')}")
    lines.append(f"Corresponding author: {manifest.get('corresponding_author', '[missing]')}")
    lines.append("")
    lines.append("## Source artifacts")
    lines.append(f"- writing_state: {manifest.get('writing_state_path') or 'not supplied'}")
    lines.append(f"- figure_package: {manifest.get('figure_package_path') or 'not supplied'}")
    lines.append(f"- fair_package: {manifest.get('fair_package_path') or 'not supplied'}")
    lines.append(f"- weakness_routing: {manifest.get('weakness_routing_path') or 'not supplied'}")
    lines.append("")
    lines.append("## Gate status")
    lines.append(f"- G6 Reviewer Simulation: {gates.get('G6', 'not_applicable')}")
    lines.append(f"- G7 Submission Fit: {gates.get('G7', 'not_applicable')}")
    lines.append("")
    lines.append("## Live verification")
    for field in template.get("live_verification_fields", []):
        lines.append(f"- [LIVE-VERIFICATION: {field}]")
    return "\n".join(lines)


def render_declarations(manifest: dict, template: dict) -> str:
    decl_req = template.get("declaration_requirements", {})
    lines = ["# Declarations", ""]
    def _line(label: str, value: str, key: str) -> str:
        if value and value.strip():
            return f"- {label}: {value.strip()}"
        return f"- {label}: [LIVE-VERIFICATION: {key} — user must verify]"
    lines.append(_line("Funding", manifest.get("funding", ""), "funding"))
    lines.append(_line("Conflict of interest", manifest.get("conflicts", ""), "conflict of interest"))
    data_status = manifest.get("data_availability_status", "")
    if data_status == "ready":
        lines.append("- Data availability: ready (see FAIR package)")
    elif data_status == "not-applicable":
        lines.append("- Data availability: not applicable")
    else:
        lines.append("- Data availability: [LIVE-VERIFICATION: data availability — user must verify]")
    if decl_req.get("credit_author_statement"):
        lines.append("- CRediT author statement: [LIVE-VERIFICATION: user must fill CRediT roles]")
    if decl_req.get("ethics"):
        lines.append("- Ethics statement: [LIVE-VERIFICATION: fill if human/animal subjects involved]")
    return "\n".join(lines)


def render_source_stub(label: str, path: str, status: str) -> str:
    lines = [f"# {label} Source", ""]
    lines.append(f"Path: {path or 'not supplied'}")
    lines.append(f"Status: {status}")
    lines.append("")
    lines.append("This stub records the source path. The submission package does not copy content.")
    return "\n".join(lines)


def render_reviewer_risk(gates: dict) -> str:
    lines = ["# Reviewer-Risk Regression", ""]
    lines.append(f"G6 Reviewer Simulation: {gates.get('G6', 'not_applicable')}")
    lines.append(f"G7 Submission Fit: {gates.get('G7', 'not_applicable')}")
    lines.append("")
    if gates.get("G6") == "not_applicable":
        lines.append("Reviewer simulation has not been run. Consider running materials-reviewer before submission.")
    return "\n".join(lines)


def write_package(pkg_dir: Path, manifest: dict, template: dict, writing_state: dict, gates: dict, abstract: str) -> list[str]:
    pkg_dir.mkdir(parents=True, exist_ok=True)
    written = []
    (pkg_dir / "MANIFEST.md").write_text(render_manifest_md(manifest, template, writing_state, gates), encoding="utf-8")
    written.append("MANIFEST.md")
    (pkg_dir / "cover-letter.md").write_text(render_cover_letter_inline(manifest, template, abstract), encoding="utf-8")
    written.append("cover-letter.md")
    if template.get("highlights_required"):
        (pkg_dir / "highlights.md").write_text(render_highlights_inline(abstract, template), encoding="utf-8")
        written.append("highlights.md")
    keywords = writing_state.get("keywords") or manifest.get("keywords") or []
    (pkg_dir / "keywords.md").write_text("# Keywords\n\n" + "\n".join(f"- {k}" for k in keywords) + "\n", encoding="utf-8")
    written.append("keywords.md")
    (pkg_dir / "declarations.md").write_text(render_declarations(manifest, template), encoding="utf-8")
    written.append("declarations.md")
    (pkg_dir / "submission-checklist.md").write_text(render_checklist_inline(manifest, template), encoding="utf-8")
    written.append("submission-checklist.md")
    (pkg_dir / "manuscript").mkdir(exist_ok=True)
    (pkg_dir / "manuscript" / "SOURCE.md").write_text(render_source_stub("Manuscript", manifest.get("writing_state_path", ""), "supplied" if manifest.get("writing_state_path") else "not_supplied"), encoding="utf-8")
    written.append("manuscript/SOURCE.md")
    (pkg_dir / "figures").mkdir(exist_ok=True)
    (pkg_dir / "figures" / "SOURCE.md").write_text(render_source_stub("Figures", manifest.get("figure_package_path", ""), "supplied" if manifest.get("figure_package_path") else "not_supplied"), encoding="utf-8")
    written.append("figures/SOURCE.md")
    (pkg_dir / "data").mkdir(exist_ok=True)
    (pkg_dir / "data" / "SOURCE.md").write_text(render_source_stub("Data", manifest.get("fair_package_path", ""), "supplied" if manifest.get("fair_package_path") else "not_supplied"), encoding="utf-8")
    written.append("data/SOURCE.md")
    (pkg_dir / "reviewer-risk-regression.md").write_text(render_reviewer_risk(gates), encoding="utf-8")
    written.append("reviewer-risk-regression.md")
    return written


def render_cover_letter_inline(manifest: dict, template: dict, abstract: str) -> str:
    import datetime as _dt
    journal_name = template.get("full_name", "")
    title = manifest.get("title", "[TITLE MISSING]")
    article_type = manifest.get("article_type", "research-article")
    corresponding = manifest.get("corresponding_author", "[CORRESPONDING AUTHOR MISSING]")
    funding = manifest.get("funding", "").strip() or "[LIVE-VERIFICATION: funding — user must verify]"
    conflicts = manifest.get("conflicts", "").strip() or "[LIVE-VERIFICATION: conflict of interest — user must verify]"
    data_status = manifest.get("data_availability_status", "")
    if data_status == "ready":
        data_line = "Data availability: ready (see FAIR package)"
    elif data_status == "not-applicable":
        data_line = "Data availability: not applicable"
    else:
        data_line = "[LIVE-VERIFICATION: data availability — user must verify]"
    today = _dt.date.today().isoformat()
    lines = [
        f"# Cover Letter — {journal_name}", "",
        today, "",
        "Editorial Office", journal_name, "",
        "Dear Editor,",
        "",
        f'We wish to submit our manuscript entitled "{title}" for consideration as a {article_type} in {journal_name}.',
        "",
        "[LLM: One paragraph summarizing the problem, approach, and key finding. "
        "Use the title, abstract, and journal triage points. Do not repeat detailed methods or results.]",
        "",
    ]
    if abstract:
        lines += ["Abstract (for LLM reference):", abstract, ""]
    points = template.get("cover_letter_required_points", [])
    if points:
        lines.append("Journal triage points (for LLM reference):")
        for p in points:
            lines.append(f"- {p}")
        lines.append("")
    lines += [
        f"We believe this work aligns with the scope of {journal_name} because "
        "[LLM: one sentence explaining the specific fit].",
        "",
        "Declarations:",
        f"- Funding: {funding}",
        f"- Conflicts of interest: {conflicts}",
        f"- {data_line}",
        "- Suggested reviewers: [omitted — supply real names only if available]",
        "",
        "Thank you for your consideration.",
        "",
        "Sincerely,",
        corresponding,
    ]
    return "\n".join(lines)


def render_highlights_inline(abstract: str, template: dict) -> str:
    rules = template.get("highlights_rules", {})
    max_count = rules.get("max_count", 5)
    max_chars = rules.get("max_characters_per_item", 85)
    lines = [
        "# Highlights", "",
        f"Target: {rules.get('min_count',3)}-{max_count} items, each ≤{max_chars} characters.", "",
        "[LLM: Extract highlights from the abstract below. Each highlight must be a single line ≤85 characters. Do not invent findings absent from the abstract.]",
        "",
        "Abstract:",
        abstract or "[no abstract supplied — ask user to fill manifest or writing state]",
        "",
        "Highlights:",
    ]
    for i in range(1, max_count + 1):
        lines.append(f"{i}. [LLM: highlight {i}]")
    return "\n".join(lines)


def render_checklist_inline(manifest: dict, template: dict) -> str:
    article_type = manifest.get("article_type", "research-article")
    at = {}
    for entry in template.get("article_types", []):
        if entry.get("id") == article_type:
            at = entry
            break
    decl = template.get("declaration_requirements", {})
    lines = [
        f"# Submission Checklist — {template.get('full_name', template.get('journal_id'))}", "",
        f"Article type: {article_type}",
        f"Word limit: {at.get('word_limit', 'verify')}",
        f"Abstract words: {at.get('abstract_words', 'verify')}",
        "",
        "## Mandatory items",
        "- [ ] Title",
        "- [ ] Authors, affiliations, corresponding author",
        f"- [ ] {at.get('abstract_structure', 'structured')} abstract within {at.get('abstract_words', 'verify')} words",
        "- [ ] Keywords (3-6)",
    ]
    if template.get("highlights_required"):
        rules = template.get("highlights_rules", {})
        lines.append(f"- [ ] Highlights {rules.get('min_count',3)}-{rules.get('max_count',5)} items, ≤{rules.get('max_characters_per_item',85)} characters each")
    lines += ["", "## Declarations"]
    if decl.get("data_availability"):
        lines.append("- [ ] Data availability statement")
    if decl.get("credit_author_statement"):
        lines.append("- [ ] CRediT author statement")
    if decl.get("conflict_of_interest"):
        lines.append("- [ ] Declaration of competing interest")
    if decl.get("funding"):
        lines.append("- [ ] Funding statement")
    if decl.get("ethics"):
        lines.append("- [ ] Ethics statement (if applicable)")
    lines += ["", "## Figures and references",
              "- [ ] Figures meet resolution and format requirements",
              "- [ ] References in journal style",
              "", "## Cover letter"]
    for point in template.get("cover_letter_required_points", []):
        lines.append(f"- [ ] Cover letter states: {point}")
    lines += ["", "## Live-verification items"]
    for field in template.get("live_verification_fields", []):
        lines.append(f"- [LIVE-VERIFICATION: {field} — re-check against current Guide for Authors]")
    lines += ["", f"Official class: {template.get('official_class', 'verify')}",
              f"Submission portal: {template.get('submission_portal', 'verify')}"]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="path to submission-manifest.yaml")
    parser.add_argument("--output-dir", default="submission-package", help="output directory")
    parser.add_argument("--dry-run", action="store_true", help="validate without writing")
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"manifest not found: {manifest_path}", file=sys.stderr)
        return 1
    manifest = load_yaml(manifest_path)

    reasons = check_refusal(manifest)
    if reasons:
        print("Refusal conditions met:", file=sys.stderr)
        for r in reasons:
            print(f"  - {r}", file=sys.stderr)
        print("Emitting dry-run only.", file=sys.stderr)
        args.dry_run = True

    journal = manifest.get("target_journal", "")
    template = load_template(journal) if journal in PILOT_JOURNALS else {}
    writing_state = read_writing_state(manifest.get("writing_state_path", "")) if manifest.get("writing_state_path") else {}
    abstract = writing_state.get("abstract") or manifest.get("abstract") or ""
    rows = read_weakness_routing(manifest.get("weakness_routing_path", ""))
    gates = compute_gate_status(rows)

    if args.dry_run:
        print("=== DRY RUN ===")
        print(render_manifest_md(manifest, template, writing_state, gates))
        print("")
        print("Files that would be written:")
        for f in ["MANIFEST.md", "cover-letter.md"] + (["highlights.md"] if template.get("highlights_required") else []) + ["keywords.md", "declarations.md", "submission-checklist.md", "manuscript/SOURCE.md", "figures/SOURCE.md", "data/SOURCE.md", "reviewer-risk-regression.md"]:
            print(f"  {f}")
        return 0

    pkg_dir = Path(args.output_dir)
    written = write_package(pkg_dir, manifest, template, writing_state, gates, abstract)
    print(f"wrote {len(written)} files to {pkg_dir}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

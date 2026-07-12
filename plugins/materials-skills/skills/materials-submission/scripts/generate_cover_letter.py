"""Generate a cover letter skeleton from the submission manifest.

Reads the manifest, loads the journal template, and produces a 7-paragraph
skeleton with [LLM: ...] placeholders for the LLM to fill. Declaration
fields are filled from the manifest; empty fields become
[LIVE-VERIFICATION: ...] placeholders.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import sys
from pathlib import Path

import yaml

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
JOURNAL_TEMPLATES = PLUGIN_ROOT / "_shared" / "journal-templates"

PILOT_JOURNALS = ("cbm", "ccc", "rmpd", "jbe")


def load_template(journal_id: str) -> dict:
    path = JOURNAL_TEMPLATES / f"{journal_id}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"journal template not found: {path}")
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def _decl(value: str, label: str) -> str:
    if value and value.strip():
        return value.strip()
    return f"[LIVE-VERIFICATION: {label} — user must verify]"


def render_cover_letter(manifest: dict, template: dict, abstract: str) -> str:
    journal_name = template.get("full_name", template.get("journal_id", ""))
    title = manifest.get("title", "[TITLE MISSING]")
    article_type = manifest.get("article_type", "research-article")
    corresponding = manifest.get("corresponding_author", "[CORRESPONDING AUTHOR MISSING]")
    funding = _decl(manifest.get("funding", ""), "funding statement")
    conflicts = _decl(manifest.get("conflicts", ""), "conflict of interest declaration")
    data_status = manifest.get("data_availability_status", "")
    if data_status == "ready":
        data_line = "Data availability: ready (see FAIR package)"
    elif data_status == "not-applicable":
        data_line = "Data availability: not applicable"
    else:
        data_line = "[LIVE-VERIFICATION: data availability status — user must verify]"
    reviewers = manifest.get("suggested_reviewers") or []
    today = _dt.date.today().isoformat()

    lines = []
    lines.append(f"# Cover Letter — {journal_name}")
    lines.append("")
    lines.append(today)
    lines.append("")
    lines.append("Editorial Office")
    lines.append(journal_name)
    lines.append("")
    lines.append("Dear Editor,")
    lines.append("")
    lines.append(f'We wish to submit our manuscript entitled "{title}" for consideration as a {article_type} in {journal_name}.')
    lines.append("")
    lines.append("[LLM: One paragraph summarizing the problem, approach, and key finding. "
                 "Use the manuscript title, the abstract below, and the journal's "
                 "cover_letter_required_points. Do not repeat detailed methods or results.]")
    lines.append("")
    if abstract:
        lines.append("Abstract (for LLM reference):")
        lines.append(abstract)
        lines.append("")
    points = template.get("cover_letter_required_points", [])
    if points:
        lines.append("Journal triage points (for LLM reference):")
        for p in points:
            lines.append(f"- {p}")
        lines.append("")
    lines.append(f"We believe this work aligns with the scope of {journal_name} because "
                 "[LLM: one sentence explaining the specific fit, using the triage points above].")
    lines.append("")
    lines.append("Declarations:")
    lines.append(f"- Funding: {funding}")
    lines.append(f"- Conflicts of interest: {conflicts}")
    lines.append(f"- {data_line}")
    if reviewers:
        lines.append("- Suggested reviewers:")
        for r in reviewers:
            lines.append(f"  - {r}")
    else:
        lines.append("- Suggested reviewers: [omitted — supply real names only if available]")
    lines.append("")
    lines.append("Thank you for your consideration.")
    lines.append("")
    lines.append("Sincerely,")
    lines.append(corresponding)
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="path to submission-manifest.yaml")
    parser.add_argument("--abstract", default="", help="manuscript abstract (if writing state not available)")
    parser.add_argument("--output", default="-", help="output path or '-' for stdout")
    args = parser.parse_args(argv)

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"manifest not found: {manifest_path}", file=sys.stderr)
        return 1
    with manifest_path.open(encoding="utf-8") as fh:
        manifest = yaml.safe_load(fh) or {}

    journal = manifest.get("target_journal")
    if journal not in PILOT_JOURNALS:
        print(f"target_journal {journal!r} not in pilot journals {PILOT_JOURNALS}", file=sys.stderr)
        return 1

    template = load_template(journal)
    letter = render_cover_letter(manifest, template, args.abstract)

    if args.output == "-":
        print(letter)
    else:
        Path(args.output).write_text(letter, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

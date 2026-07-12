"""Generate a journal-specific submission checklist.

Reads the journal-formats fact sheet and the journal-templates yaml and
assembles a markdown checklist. Deterministic; no LLM call.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

PLUGIN_ROOT = Path(__file__).resolve().parents[3]
JOURNAL_FORMATS = PLUGIN_ROOT / "_shared" / "journal-formats"
JOURNAL_TEMPLATES = PLUGIN_ROOT / "_shared" / "journal-templates"

PILOT_JOURNALS = ("cbm", "ccc", "rmpd", "jbe")


def load_template(journal_id: str) -> dict:
    path = JOURNAL_TEMPLATES / f"{journal_id}.yaml"
    if not path.exists():
        raise FileNotFoundError(f"journal template not found: {path}")
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def find_article_type(template: dict, article_type: str) -> dict:
    for entry in template.get("article_types", []):
        if entry.get("id") == article_type:
            return entry
    raise KeyError(f"article_type {article_type!r} not in journal template")


def render_checklist(template: dict, article_type: str) -> str:
    at = find_article_type(template, article_type)
    decl = template.get("declaration_requirements", {})
    lines = []
    lines.append(f"# Submission Checklist — {template.get('full_name', template.get('journal_id'))}")
    lines.append("")
    lines.append(f"Article type: {article_type}")
    lines.append(f"Word limit: {at.get('word_limit', 'verify')}")
    lines.append(f"Abstract words: {at.get('abstract_words', 'verify')}")
    lines.append(f"Abstract structure: {at.get('abstract_structure', 'verify')}")
    lines.append("")
    lines.append("## Mandatory items")
    lines.append("- [ ] Title")
    lines.append("- [ ] Authors, affiliations, corresponding author")
    lines.append(f"- [ ] {at.get('abstract_structure', 'structured')} abstract within {at.get('abstract_words', 'verify')} words")
    lines.append("- [ ] Keywords (3-6)")
    if template.get("highlights_required"):
        rules = template.get("highlights_rules", {})
        lines.append(f"- [ ] Highlights {rules.get('min_count',3)}-{rules.get('max_count',5)} items, ≤{rules.get('max_characters_per_item',85)} characters each")
    lines.append("")
    lines.append("## Declarations")
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
    lines.append("")
    lines.append("## Figures and references")
    lines.append("- [ ] Figures meet resolution and format requirements")
    lines.append("- [ ] References in journal style")
    lines.append("- [ ] Panel labels lowercase in parentheses: (a), (b), (c)")
    lines.append("")
    lines.append("## Cover letter")
    for point in template.get("cover_letter_required_points", []):
        lines.append(f"- [ ] Cover letter states: {point}")
    lines.append("")
    lines.append("## Live-verification items")
    for field in template.get("live_verification_fields", []):
        lines.append(f"- [LIVE-VERIFICATION: {field} — re-check against current Guide for Authors]")
    lines.append("")
    lines.append(f"Official class: {template.get('official_class', 'verify')}")
    lines.append(f"Submission portal: {template.get('submission_portal', 'verify')}")
    lines.append(f"Official template: {template.get('official_template_url', 'verify')}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--journal", required=True, choices=PILOT_JOURNALS)
    parser.add_argument("--article-type", default="research-article")
    parser.add_argument("--output", default="-", help="output path or '-' for stdout")
    args = parser.parse_args(argv)

    template = load_template(args.journal)
    checklist = render_checklist(template, args.article_type)

    if args.output == "-":
        print(checklist)
    else:
        Path(args.output).write_text(checklist, encoding="utf-8")
        print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

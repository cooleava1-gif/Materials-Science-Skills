"""Generate a highlights skeleton with character-limit enforcement.

Produces a markdown file with [LLM: ...] placeholders and the abstract.
If the user supplies a highlights file via --highlights-file, the script
validates each line against the 85-character limit.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from template_support import SUPPORTED_JOURNALS, load_template


def render_skeleton(abstract: str, template: dict) -> str:
    rules = template.get("highlights_rules", {})
    min_count = rules.get("min_count", 3)
    max_count = rules.get("max_count", 5)
    max_chars = rules.get("max_characters_per_item", 85)
    lines = []
    lines.append("# Highlights")
    lines.append("")
    lines.append(f"Target: {min_count}-{max_count} items, each ≤{max_chars} characters.")
    lines.append("")
    lines.append("[LLM: Extract highlights from the abstract below. Each highlight")
    lines.append("must be a single line ≤85 characters. Do not invent findings")
    lines.append("absent from the abstract.]")
    lines.append("")
    lines.append("Abstract:")
    lines.append(abstract or "[no abstract supplied — ask user to fill manifest or writing state]")
    lines.append("")
    lines.append("Highlights:")
    for i in range(1, max_count + 1):
        lines.append(f"{i}. [LLM: highlight {i}]")
    return "\n".join(lines)


def validate_highlights(path: Path, max_chars: int) -> list[str]:
    import re
    text = path.read_text(encoding="utf-8")
    highlights = []
    pattern = re.compile(r"^\d+\.\s+(.+)$")
    for line in text.splitlines():
        stripped = line.strip()
        match = pattern.match(stripped)
        if match:
            highlight = match.group(1).strip()
            if highlight and not highlight.startswith("[LLM"):
                highlights.append(highlight)
    violations = [h for h in highlights if len(h) > max_chars]
    return violations


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--journal", required=True, choices=SUPPORTED_JOURNALS)
    parser.add_argument("--abstract", default="", help="manuscript abstract")
    parser.add_argument("--highlights-file", help="existing highlights file to validate")
    parser.add_argument("--output", default="-", help="output path or '-' for stdout")
    args = parser.parse_args(argv)

    template = load_template(args.journal)
    if not template.get("highlights_required"):
        print(f"{args.journal} does not require highlights; skipping.", file=sys.stderr)
        return 0

    rules = template.get("highlights_rules", {})
    max_chars = rules.get("max_characters_per_item", 85)

    if args.highlights_file:
        violations = validate_highlights(Path(args.highlights_file), max_chars)
        if violations:
            print("Highlights exceeding character limit:", file=sys.stderr)
            for h in violations:
                print(f"  ({len(h)} chars) {h}", file=sys.stderr)
            return 1
        print("all highlights within limit", file=sys.stderr)
        return 0

    skeleton = render_skeleton(args.abstract, template)
    if args.output == "-":
        print(skeleton)
    else:
        Path(args.output).write_text(skeleton, encoding="utf-8")
        print(f"wrote {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

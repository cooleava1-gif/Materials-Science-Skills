#!/usr/bin/env python3
"""Check figure_contract.md completeness as a blocking gate before plotting.

In contract-driven mode the figure contract must be filled in with substantive
content for all seven points before any plotting happens. This script returns a
list of issues; an empty list means the contract passes the gate.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

SEVEN_POINTS = [
    "Core Conclusion",
    "Evidence Chain",
    "Archetype",
    "Backend",
    "Journal/Export Contract",
    "Statistics And Image Integrity",
    "WER-EA Boundary",
]

# Patterns that indicate placeholder / unfinished content.
# "not applicable" is allowed when followed by an explanation ("because..."),
# since some sections (e.g. Statistics) may legitimately have no statistics.
PLACEHOLDER_PATTERNS = [
    r"template[- ]only",
    r"replace this",
    r"\[DRAFT",
    r"to be (checked|confirmed|determined)",
    r"placeholder",
    r"not applicable(?!\s+because)",
]

MIN_SECTION_LENGTH = 20


def check_contract(contract_path: Path) -> list[str]:
    """Return list of issues. Empty list = pass."""
    issues: list[str] = []

    if not contract_path.is_file():
        return [f"figure_contract.md not found at {contract_path}"]

    text = contract_path.read_text(encoding="utf-8")

    # 1. Every one of the seven points must be present as a ## heading.
    for point in SEVEN_POINTS:
        if f"## {point}" not in text:
            issues.append(f"missing section: {point}")

    # 2. Each present section must have substantive (non-placeholder) content.
    for point in SEVEN_POINTS:
        section = extract_section(text, point)
        if not section:
            continue
        for pattern in PLACEHOLDER_PATTERNS:
            if re.search(pattern, section, re.IGNORECASE):
                issues.append(f"{point}: contains placeholder '{pattern}'")
                break
        else:
            if len(section.strip()) < MIN_SECTION_LENGTH:
                issues.append(f"{point}: content too short (<{MIN_SECTION_LENGTH} chars)")

    return issues


def extract_section(text: str, heading: str) -> str:
    """Extract section content between ## heading and the next ## heading."""
    pattern = rf"## {re.escape(heading)}\s*\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1) if match else ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("contract_path", help="path to figure_contract.md")
    parser.add_argument("--json", action="store_true", help="emit JSON result")
    args = parser.parse_args(argv)

    issues = check_contract(Path(args.contract_path))

    if args.json:
        print(json.dumps({"status": "pass" if not issues else "blocked", "issues": issues}, ensure_ascii=False, indent=2))
    else:
        if issues:
            print("BLOCKED: figure contract incomplete")
            for issue in issues:
                print(f"  - {issue}")
        else:
            print("PASS: figure contract complete")

    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())

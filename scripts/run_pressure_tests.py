"""Automated pressure test runner for civil-materials-skills.

Parses all ``**/tests/pressure-tests/*.md`` files, extracts structured
sections (Prompt, Expected Behavior, Failure Signs), and generates a
validation report.  Does NOT invoke the LLM — it validates that each
pressure test file is structurally complete and that the project has
sufficient coverage across themes and modules.

Usage::

    python scripts/run_pressure_tests.py [--json] [--skill-root PATH]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


REQUIRED_SECTIONS = ["Theme", "Modules Covered", "Prompt", "Expected Behavior", "Failure Signs"]

# Themes that must each appear in at least one pressure test
REQUIRED_THEMES = {
    "overclaim",
    "fake citation",
    "journal mismatch",
    "missing experimental conditions",
    "literal translation",
    "weak novelty",
    "figure caption",
    "pptx missing data",
    "fair data",
    "reviewer response",
    "statistics",
    "scope creep",
}


@dataclass
class PressureTest:
    """Parsed representation of one pressure test .md file."""
    path: Path
    title: str = ""
    theme: str = ""
    modules: list[str] = field(default_factory=list)
    prompt: str = ""
    expected_behavior: str = ""
    failure_signs: list[str] = field(default_factory=list)
    missing_sections: list[str] = field(default_factory=list)
    is_valid: bool = True


def parse_pressure_test(path: Path) -> PressureTest:
    """Parse a single pressure test markdown file."""
    text = path.read_text(encoding="utf-8")
    test = PressureTest(path=path)

    # Extract title from first heading
    title_match = re.search(r"^#\s+Pressure Test:\s*(.+)", text, re.MULTILINE)
    test.title = title_match.group(1).strip() if title_match else path.stem

    # Extract sections by ## headings
    sections: dict[str, str] = {}
    current_section = None
    current_lines: list[str] = []
    for line in text.splitlines():
        heading = re.match(r"^##\s+(.+)", line)
        if heading:
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = heading.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)
    if current_section:
        sections[current_section] = "\n".join(current_lines).strip()

    # Map sections (handle alternate names)
    test.theme = (sections.get("Theme", "") or sections.get("Scenario", "")).strip().lower()
    test.prompt = (sections.get("Prompt", "") or sections.get("Scenario", "")).strip()
    test.expected_behavior = (
        sections.get("Expected Behavior", "")
        or sections.get("Required Behavior", "")
        or sections.get("Expected Polished Direction", "")
    ).strip()

    # Parse modules
    modules_text = sections.get("Modules Covered", "")
    test.modules = [
        line.strip("- ").strip()
        for line in modules_text.splitlines()
        if line.strip().startswith("-")
    ]

    # Parse failure signs
    signs_text = sections.get("Failure Signs", "")
    test.failure_signs = [
        line.strip("- ").strip()
        for line in signs_text.splitlines()
        if line.strip().startswith("-")
    ]

    # Check missing sections (accept alternate names)
    required = {
        "Theme": ["Theme", "Scenario"],
        "Modules Covered": ["Modules Covered"],
        "Prompt": ["Prompt", "Scenario"],
        "Expected Behavior": ["Expected Behavior", "Required Behavior", "Expected Polished Direction"],
        "Failure Signs": ["Failure Signs"],
    }
    test.missing_sections = []
    for canonical, alternates in required.items():
        if not any(sections.get(alt, "").strip() for alt in alternates):
            test.missing_sections.append(canonical)

    test.is_valid = len(test.missing_sections) == 0 and bool(test.prompt)
    return test


def discover_pressure_tests(root: Path) -> list[PressureTest]:
    """Find and parse all pressure test .md files under root."""
    tests = []
    for md_path in sorted(root.glob("*/tests/pressure-tests/*.md")):
        tests.append(parse_pressure_test(md_path))
    return tests


def validate_coverage(tests: list[PressureTest]) -> dict[str, Any]:
    """Check theme and module coverage across all tests."""
    found_themes = {t.theme for t in tests if t.theme}
    found_modules: set[str] = set()
    for t in tests:
        found_modules.update(t.modules)

    missing_themes = REQUIRED_THEMES - found_themes
    invalid_tests = [t for t in tests if not t.is_valid]

    return {
        "total_tests": len(tests),
        "valid_tests": len(tests) - len(invalid_tests),
        "invalid_tests": len(invalid_tests),
        "found_themes": sorted(found_themes),
        "missing_themes": sorted(missing_themes),
        "found_modules": sorted(found_modules),
        "theme_coverage_pct": round(100 * len(found_themes & REQUIRED_THEMES) / len(REQUIRED_THEMES), 1),
        "status": "pass" if not missing_themes and not invalid_tests else "incomplete",
    }


def render_markdown(tests: list[PressureTest], coverage: dict[str, Any]) -> str:
    """Render a human-readable validation report."""
    lines = [
        "# Pressure Test Validation Report",
        "",
        f"**Status:** {coverage['status'].upper()}",
        f"**Total tests:** {coverage['total_tests']}",
        f"**Valid tests:** {coverage['valid_tests']}",
        f"**Theme coverage:** {coverage['theme_coverage_pct']}%",
        "",
    ]

    if coverage["missing_themes"]:
        lines.append("## Missing Themes")
        for theme in coverage["missing_themes"]:
            lines.append(f"- {theme}")
        lines.append("")

    # Per-test details
    lines.append("## Test Details")
    lines.append("")
    for t in tests:
        status = "✅" if t.is_valid else "❌"
        lines.append(f"### {status} {t.title}")
        lines.append(f"- **Path:** `{t.path.relative_to(t.path.parents[3])}`")
        lines.append(f"- **Theme:** {t.theme or '(missing)'}")
        lines.append(f"- **Modules:** {', '.join(t.modules) or '(none)'}")
        if t.missing_sections:
            lines.append(f"- **Missing sections:** {', '.join(t.missing_sections)}")
        lines.append("")

    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate pressure test coverage.")
    parser.add_argument("--skill-root", type=Path, default=None, help="Root directory containing skills/")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of markdown")
    args = parser.parse_args(argv)

    # Ensure UTF-8 output on Windows
    import io
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    root = args.skill_root or Path(__file__).resolve().parents[1]
    skills_dir = root / "skills" if (root / "skills").is_dir() else root

    tests = discover_pressure_tests(skills_dir)
    coverage = validate_coverage(tests)

    if args.json:
        report = {
            "coverage": coverage,
            "tests": [
                {
                    "title": t.title,
                    "path": str(t.path),
                    "theme": t.theme,
                    "modules": t.modules,
                    "is_valid": t.is_valid,
                    "missing_sections": t.missing_sections,
                }
                for t in tests
            ],
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(tests, coverage))

    return 0 if coverage["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

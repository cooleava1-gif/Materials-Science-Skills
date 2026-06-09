#!/usr/bin/env python3
"""Audit civil-materials pressure tests and example library coverage."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_MODULES = [
    "civil-materials-research",
    "civil-materials-reader",
    "civil-materials-citation",
    "civil-materials-polishing",
    "civil-materials-response",
    "civil-materials-paper2ppt",
    "civil-materials-pptx",
    "civil-materials-figure",
    "civil-materials-data",
]

REQUIRED_THEMES = [
    "overclaim",
    "fake citation",
    "journal mismatch",
    "missing experimental conditions",
    "literal translation",
    "weak novelty",
    "figure caption",
    "pptx missing data",
    "FAIR data",
    "reviewer response",
    "statistics",
    "scope creep",
]


def audit(skill_root: Path) -> dict[str, object]:
    pressure_files = sorted((skill_root / "tests" / "pressure-tests").glob("*.md"))
    example_files = sorted((skill_root / "examples" / "library").glob("*.md"))
    pressure_text = "\n".join(path.read_text(encoding="utf-8") for path in pressure_files)
    examples_text = "\n".join(path.read_text(encoding="utf-8") for path in example_files)
    combined = pressure_text + "\n" + examples_text

    covered_modules = [module for module in REQUIRED_MODULES if module in pressure_text]
    example_modules = [module for module in REQUIRED_MODULES if module in examples_text]
    missing_modules = [module for module in REQUIRED_MODULES if module not in covered_modules]
    missing_example_modules = [module for module in REQUIRED_MODULES if module not in example_modules]
    missing_themes = [theme for theme in REQUIRED_THEMES if theme not in combined]

    status = "pass"
    if len(pressure_files) < 12 or len(example_files) < len(REQUIRED_MODULES) + 1:
        status = "incomplete"
    if missing_modules or missing_example_modules or missing_themes:
        status = "incomplete"

    return {
        "status": status,
        "pressure_test_count": len(pressure_files),
        "example_count": len(example_files),
        "covered_modules": covered_modules,
        "example_modules": example_modules,
        "missing_modules": missing_modules,
        "missing_example_modules": missing_example_modules,
        "missing_themes": missing_themes,
    }


def render_markdown(report: dict[str, object]) -> str:
    lines = [
        "# Civil Materials Pressure Asset Audit",
        "",
        f"- status: {report['status']}",
        f"- pressure_test_count: {report['pressure_test_count']}",
        f"- example_count: {report['example_count']}",
        "",
        "## Missing",
    ]
    for key in ("missing_modules", "missing_example_modules", "missing_themes"):
        values = report[key]
        assert isinstance(values, list)
        lines.append(f"- {key}: {', '.join(values) if values else 'none'}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skill-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    report = audit(Path(args.skill_root))
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

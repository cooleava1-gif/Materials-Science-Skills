#!/usr/bin/env python3
"""Behavioral contract test runner — semi-automated.

Loads Markdown scenario files from skills/<name>/tests/scenarios/,
presents them for manual evaluation, and records results.

Usage:
    python scripts/run_behavioral_tests.py --json
    python scripts/run_behavioral_tests.py --skill writing
    python scripts/run_behavioral_tests.py --list
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from skill_manifest import discover_skill_names

SKILLS_ROOT = Path(__file__).resolve().parents[1] / "skills"


def _discover_scenarios() -> dict[str, list[Path]]:
    """Discover all .md scenario files under skills/*/tests/scenarios/."""
    scenarios: dict[str, list[Path]] = {}
    for skill_name in discover_skill_names(SKILLS_ROOT):
        scenarios_dir = SKILLS_ROOT / skill_name / "tests" / "scenarios"
        if scenarios_dir.exists():
            files = sorted(scenarios_dir.glob("*.md"))
            if files:
                scenarios[skill_name] = files
    return scenarios


def parse_scenario(path: Path) -> dict:
    """Parse a Markdown scenario file into sections."""
    text = path.read_text(encoding="utf-8")

    sections = {}
    current_heading = None
    current_lines = []

    for line in text.split("\n"):
        heading_match = re.match(r"^## (.+)$", line)
        if heading_match:
            if current_heading:
                sections[current_heading] = "\n".join(current_lines).strip()
            current_heading = heading_match.group(1).strip()
            current_lines = []
        else:
            current_lines.append(line)

    if current_heading:
        sections[current_heading] = "\n".join(current_lines).strip()

    return {
        "path": str(path),
        "skill": sections.get("Skill", "unknown"),
        "title": text.split("\n")[0].replace("# ", "").strip(),
        "input": sections.get("Input", ""),
        "expected": sections.get("Expected behavior", ""),
        "forbidden": sections.get("Forbidden behavior", ""),
        "checklist": sections.get("Pass/fail checklist", ""),
    }


def list_scenarios() -> None:
    """List all discovered scenarios."""
    scenarios = _discover_scenarios()
    if not scenarios:
        print("No scenario files found under skills/*/tests/scenarios/")
        return

    total = 0
    for skill_name, files in sorted(scenarios.items()):
        print(f"\n{skill_name} ({len(files)} scenarios):")
        for f in files:
            scenario = parse_scenario(f)
            print(f"  - {scenario['title']}")
            total += 1
    print(f"\nTotal: {total} scenarios across {len(scenarios)} skills")


def run_scenario(path: Path, silent: bool = False) -> dict:
    """Evaluate one scenario (prints for human review, returns metadata)."""
    scenario = parse_scenario(path)

    if silent:
        return {
            "scenario": scenario["title"],
            "path": str(path),
            "skill": scenario["skill"],
            "checklist_items": [
                line.strip().lstrip("- []") for line in scenario["checklist"].split(chr(10))
                if line.strip().startswith("- [")
            ],
        }

    print()
    print("=" * 70)
    print("SCENARIO: " + scenario["title"])
    print("SKILL:    " + scenario["skill"])
    print("=" * 70)

    print()
    print("INPUT")
    print("-" * 40)
    print(scenario["input"])

    print()
    print("EXPECTED BEHAVIOR")
    print("-" * 40)
    print(scenario["expected"])

    print()
    print("FORBIDDEN BEHAVIOR")
    print("-" * 40)
    print(scenario["forbidden"])

    print()
    print("PASS/FAIL CHECKLIST")
    print("-" * 40)
    for line in scenario["checklist"].split(chr(10)):
        if line.strip().startswith("- ["):
            print("  [ ] " + line.strip()[4:])

    print()
    print("-" * 40)
    print("Run this scenario through the AI agent, then check each item above.")
    print()

    return {
        "scenario": scenario["title"],
        "path": str(path),
        "skill": scenario["skill"],
        "checklist_items": [
            line.strip().lstrip("- []") for line in scenario["checklist"].split(chr(10))
            if line.strip().startswith("- [")
        ],
    }


def run_skill(skill_name: str, silent: bool = False) -> list[dict]:
    """Run all scenarios for a skill."""
    results = []
    scenarios_dir = SKILLS_ROOT / skill_name / "tests" / "scenarios"
    if not scenarios_dir.exists():
        if not silent:
            print(f"No scenarios directory for {skill_name}")
        return results

    for f in sorted(scenarios_dir.glob("*.md")):
        result = run_scenario(f, silent=silent)
        results.append(result)

    return results


def run_all(silent: bool = True) -> dict[str, list[dict]]:
    """Run all scenarios across all skills."""
    all_results: dict[str, list[dict]] = {}
    for skill_name in discover_skill_names(SKILLS_ROOT):
        results = run_skill(skill_name, silent=silent)
        if results:
            all_results[skill_name] = results
    return all_results


def main() -> int:
    parser = argparse.ArgumentParser(description="Behavioral contract test runner")
    parser.add_argument("--skill", help="Run scenarios for one skill only")
    parser.add_argument("--list", action="store_true", help="List available scenarios")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    if args.list:
        list_scenarios()
        return 0

    if args.skill:
        skill_names = discover_skill_names(SKILLS_ROOT)
        skill_map = {s.replace('materials-', ''): s for s in skill_names}
        skill_map.update({s: s for s in skill_names})
        skill_name = skill_map.get(args.skill, args.skill)
        results = run_skill(skill_name, silent=args.json)
    else:
        results_dict = run_all()
        results = []
        for skill_results in results_dict.values():
            results.extend(skill_results)

    if args.json:
        print(json.dumps({
            "status": "info",
            "scenarios": results,
            "note": "These are semi-automated behavioral tests. "
                    "Run each scenario through the skill agent and manually check the pass/fail checklist.",
            "total": len(results),
        }, indent=2, ensure_ascii=False))
    else:
        print(f"\n\n{'=' * 70}")
        print(f"Scenarios loaded: {len(results)}")
        print("Run each through the skill agent and verify against the checklist.")
        print("Record results in tests/scenarios/results/ if desired.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

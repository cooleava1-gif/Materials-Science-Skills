#!/usr/bin/env python3
"""Validate Material Registry entries against schema and cross-references.

Checks:
  1. Every entry file is valid YAML and has required fields.
  2. Every entry's id matches its filename.
  3. Every entry's family is a valid value.
  4. Every entry's coverage_tier is a valid value.
  5. Every referenced file path actually exists in the repo.
  6. Every entry.id appears in the registry index.
  7. Registry index lists every entry file.
  8. Every cross_references.related and .parent points to an existing entry.
  9. No duplicate ids across entries.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "materials-skills"
REGISTRY_DIR = PLUGIN_ROOT / "_shared" / "material-registry"
ENTRIES_DIR = REGISTRY_DIR / "entries"
INDEX_FILE = REGISTRY_DIR / "registry-index.yaml"
SCHEMA_FILE = REGISTRY_DIR / "registry-schema.yaml"

VALID_FAMILIES = {"civil", "polymers", "metals", "ceramics", "functional", "nano"}
VALID_TIERS = {"full", "partial", "skeleton", "generic"}


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"__yaml_error__": str(exc)}
    return data if isinstance(data, dict) else {}


def validate_index() -> list[str]:
    """Validate the registry index file."""
    issues: list[str] = []
    if not INDEX_FILE.exists():
        return [f"missing index: {INDEX_FILE.as_posix()}"]
    index = _read_yaml(INDEX_FILE)
    if not index.get("materials"):
        issues.append("index has no 'materials' list")
    return issues


def validate_entry(path: Path) -> list[str]:
    """Validate a single material registry entry."""
    issues: list[str] = []
    data = _read_yaml(path)

    if "__yaml_error__" in data:
        return [f"{path.name}: YAML parse error: {data['__yaml_error__']}"]

    # Required fields
    for field in ("name", "id", "family", "coverage_tier", "description", "skill_mapping"):
        if field not in data:
            issues.append(f"{path.name}: missing required field '{field}'")

    if issues:
        return issues

    # id matches filename
    expected_id = path.stem
    if data["id"] != expected_id:
        issues.append(f"{path.name}: id '{data['id']}' does not match filename '{expected_id}'")

    # family validity
    if data["family"] not in VALID_FAMILIES:
        issues.append(f"{path.name}: invalid family '{data['family']}'")

    # coverage_tier validity
    if data["coverage_tier"] not in VALID_TIERS:
        issues.append(f"{path.name}: invalid coverage_tier '{data['coverage_tier']}'")

    # description.summary
    desc = data.get("description", {})
    if isinstance(desc, dict) and not desc.get("summary"):
        issues.append(f"{path.name}: description.summary is missing or empty")

    # skill_mapping present
    skill = data.get("skill_mapping", {})
    if not isinstance(skill, dict):
        issues.append(f"{path.name}: skill_mapping must be a dict")

    # Validate referenced file paths (relative to the plugin package)
    if isinstance(skill, dict):
        for key in ("figure_scripts", "figure_packages", "data_schemas"):
            for ref in skill.get(key, []) or []:
                if isinstance(ref, str):
                    full = PLUGIN_ROOT / ref
                    if not full.exists():
                        issues.append(f"{path.name}: skill_mapping.{key} references non-existent: {ref}")

    # Validate narrative skill_references
    narrative = data.get("narrative", {})
    if isinstance(narrative, dict):
        skill_refs = narrative.get("skill_references", {}) or {}
        if isinstance(skill_refs, dict):
            for ref_key, ref_path in skill_refs.items():
                if isinstance(ref_path, str):
                    full = PLUGIN_ROOT / ref_path
                    if not full.exists():
                        issues.append(f"{path.name}: narrative.skill_references.{ref_key} non-existent: {ref_path}")

    # Validate cross_references
    cross = data.get("cross_references", {}) or {}
    if isinstance(cross, dict):
        for ref in cross.get("related", []) or []:
            entry_path = ENTRIES_DIR / f"{ref}.yaml"
            if not entry_path.exists():
                issues.append(f"{path.name}: cross_references.related '{ref}' has no matching registry entry")
        parent = cross.get("parent")
        if parent:
            parent_path = ENTRIES_DIR / f"{parent}.yaml"
            if not parent_path.exists():
                issues.append(f"{path.name}: cross_references.parent '{parent}' has no matching registry entry")

    return issues


def validate_all(json_output: bool = False) -> dict[str, list[str]]:
    """Run all registry validations."""
    all_issues: dict[str, list[str]] = {}

    # 1. Index validation
    idx_issues = validate_index()
    if idx_issues:
        all_issues["registry-index"] = idx_issues

    # 2. Entry files
    if not ENTRIES_DIR.exists():
        all_issues["entries"] = [f"entries directory not found: {ENTRIES_DIR.as_posix()}"]
        return all_issues

    entry_files = sorted(ENTRIES_DIR.glob("*.yaml"))
    if not entry_files:
        all_issues["entries"] = ["no entry files found"]
        return all_issues

    seen_ids: set[str] = set()
    for path in entry_files:
        entry_issues = validate_entry(path)
        if entry_issues:
            all_issues.setdefault("entries", []).extend(entry_issues)

        # Check duplicate ids
        data = _read_yaml(path)
        eid = data.get("id")
        if eid:
            if eid in seen_ids:
                all_issues.setdefault("entries", []).append(f"duplicate id '{eid}' in {path.name}")
            seen_ids.add(eid)

    # 3. Index vs. entries consistency
    index = _read_yaml(INDEX_FILE)
    indexed_ids = {m["id"] for m in index.get("materials", []) if isinstance(m, dict) and m.get("id")}
    entry_ids = set(p.stem for p in entry_files if p.stem) if entry_files else set()

    missing_from_index = entry_ids - indexed_ids
    if missing_from_index:
        all_issues.setdefault("index-consistency", []).append(
            f"entries not in index: {sorted(missing_from_index)}"
        )

    extra_in_index = indexed_ids - entry_ids
    if extra_in_index:
        all_issues.setdefault("index-consistency", []).append(
            f"index references non-existent entries: {sorted(extra_in_index)}"
        )

    # 4. Schema file exists
    if not SCHEMA_FILE.exists():
        all_issues.setdefault("schema", []).append("registry-schema.yaml not found")

    return all_issues


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args(argv)

    issues = validate_all(json_output=args.json)

    if args.json:
        print(json.dumps({
            "status": "pass" if not issues else "fail",
            "issues": issues,
        }, indent=2, ensure_ascii=False))
    else:
        if issues:
            for category, category_issues in issues.items():
                for issue in category_issues:
                    print(f"[{category}] {issue}")
            print(f"\nFAIL: {sum(len(v) for v in issues.values())} issues found")
        else:
            print("PASS: all registry checks passed")

    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())

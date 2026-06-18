#!/usr/bin/env python3
"""Validate every skill's manifest.yaml for structural integrity.

Checks path existence, fragment orphans, trigger hygiene, contract references.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml
from skill_manifest import discover_skill_names

repo_root = Path(__file__).resolve().parents[1]
SKILLS_ROOT = repo_root / "skills"
CONTRACTS_DIR = repo_root / "_shared" / "contracts"

REGISTRY_DIR = repo_root / "_shared" / "material-registry" / "entries"


def _parse_yaml_text(text: str) -> dict:
    """Parse YAML text, handling encoding issues."""
    return yaml.safe_load(text)


def _load_yaml(path: Path) -> dict | None:
    if not path.exists():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return _parse_yaml_text(f.read())
    except (OSError, UnicodeDecodeError, yaml.YAMLError):
        return None


def _is_registry_referenced(skill_name: str, filename: str) -> bool:
    """Check if a file is referenced by any Material Registry entry."""
    if not REGISTRY_DIR.exists():
        return False
    for entry_path in sorted(REGISTRY_DIR.glob("*.yaml")):
        entry = _load_yaml(entry_path)
        if not entry:
            continue
        narrative = entry.get("narrative", {})
        if not isinstance(narrative, dict):
            continue
        refs = narrative.get("skill_references", {}) or {}
        for ref_key in ("domain_fragment", "narrative_guide", "reviewer_criteria"):
            ref_path = refs.get(ref_key, "")
            if isinstance(ref_path, str) and ref_path.endswith(filename) and skill_name in ref_path:
                return True
    return False


def _collect_paths_from_dict(d: dict, base: Path) -> list[Path]:
    """Recursively collect all 'path' and 'trigger_file' values from a nested dict structure."""
    paths = []
    if isinstance(d, dict):
        for k, v in d.items():
            if k in ("path", "trigger_file") and isinstance(v, str):
                full = (base / v).resolve()
                paths.append(full)
            else:
                paths.extend(_collect_paths_from_dict(v, base))
        # Also check 'contract' key
        for k, v in d.items():
            if k == "contract" and isinstance(v, str):
                full = (base / v).resolve()
                paths.append(full)
    elif isinstance(d, list):
        for item in d:
            paths.extend(_collect_paths_from_dict(item, base))
    return paths


def _collect_all_referenced_paths(manifest: dict, skill_root: Path) -> set[Path]:
    """Collect every file path referenced in manifest (always_load, axis values, on_demand, assets, scripts)."""
    referenced: set[Path] = set()

    # always_load
    for ref in manifest.get("always_load", []):
        if isinstance(ref, str):
            referenced.add((skill_root / ref).resolve())

    # axes values
    axes = manifest.get("axes", {})
    if isinstance(axes, dict):
        for axis_name, axis_def in axes.items():
            if isinstance(axis_def, dict):
                values = axis_def.get("values", {})
                if isinstance(values, dict):
                    for val_name, val_def in values.items():
                        if isinstance(val_def, dict):
                            p = val_def.get("path")
                            if p and isinstance(p, str):
                                referenced.add((skill_root / p).resolve())

    # references.on_demand  (supports both dict and list formats)
    refs = manifest.get("references", {})
    if isinstance(refs, dict):
        on_demand = refs.get("on_demand", {})
        if isinstance(on_demand, list):
            for entry in on_demand:
                if isinstance(entry, dict):
                    p = entry.get("path")
                    if p and isinstance(p, str):
                        referenced.add((skill_root / p).resolve())
        elif isinstance(on_demand, dict):
            for key, entry in on_demand.items():
                if isinstance(entry, dict):
                    p = entry.get("path")
                    if p and isinstance(p, str):
                        referenced.add((skill_root / p).resolve())
                elif isinstance(entry, str):
                    referenced.add((skill_root / entry).resolve())

    # assets
    for asset in manifest.get("assets", []):
        if isinstance(asset, str):
            p = skill_root / asset
            if p.exists():
                referenced.add(p.resolve())

    # scripts
    for script in manifest.get("scripts", []):
        if isinstance(script, str):
            p = skill_root / script
            if p.exists():
                referenced.add(p.resolve())

    # handoffs.provides.*.contract
    handoffs = manifest.get("handoffs", {})
    if isinstance(handoffs, dict):
        provides = handoffs.get("provides", {})
        if isinstance(provides, dict):
            for name, hdef in provides.items():
                if isinstance(hdef, dict):
                    c = hdef.get("contract")
                    if c and isinstance(c, str):
                        referenced.add((skill_root / c).resolve())

    return referenced


def validate_skill(skill_name: str) -> list[str]:
    """Validate a single skill's manifest.yaml. Returns list of issues (empty = clean)."""
    issues: list[str] = []
    skill_root = SKILLS_ROOT / skill_name
    manifest_path = skill_root / "manifest.yaml"

    if not manifest_path.exists():
        return [f"manifest.yaml not found"]

    manifest = _load_yaml(manifest_path)
    if manifest is None:
        return [f"could not parse manifest.yaml"]

    # 1. Path existence — collect all paths and check they exist
    all_refs = _collect_all_referenced_paths(manifest, skill_root)
    for ref_path in sorted(all_refs):
        if not ref_path.exists():
            rel = ref_path.relative_to(SKILLS_ROOT.parent) if ref_path.is_relative_to(SKILLS_ROOT.parent) else ref_path
            issues.append(f"path not found: {rel}")

    # 2. No orphan fragments
    fragments_dir = skill_root / "static" / "fragments"
    if fragments_dir.exists():
        orphan_fragments = []
        for fpath in sorted(fragments_dir.rglob("*.md")):
            resolved = fpath.resolve()
            if resolved not in all_refs:
                rel = resolved.relative_to(skill_root)
                orphan_fragments.append(str(rel))
        if orphan_fragments:
            issues.append(f"orphan fragments (not referenced by any axis): {', '.join(orphan_fragments[:5])}")

    # 3. Trigger non-empty and 4. Trigger collision
    axes = manifest.get("axes", {})
    if isinstance(axes, dict):
        for axis_name, axis_def in axes.items():
            if not isinstance(axis_def, dict):
                continue
            values = axis_def.get("values", {})
            if not isinstance(values, dict):
                continue
            seen_triggers: dict[str, str] = {}  # trigger -> value_name
            for val_name, val_def in values.items():
                if not isinstance(val_def, dict):
                    continue
                # Load triggers from inline list or external trigger_file
                triggers = val_def.get("triggers", [])
                trigger_file_ref = val_def.get("trigger_file")
                if trigger_file_ref and isinstance(trigger_file_ref, str):
                    # Load external trigger file
                    tf_path = (skill_root / trigger_file_ref).resolve()
                    if tf_path.exists():
                        tf_data = _load_yaml(tf_path)
                        if tf_data and isinstance(tf_data, dict) and "triggers" in tf_data:
                            triggers = tf_data["triggers"]
                    else:
                        issues.append(f"trigger_file not found: {trigger_file_ref} (axis '{axis_name}.{val_name}')")
                if not isinstance(triggers, list) or len(triggers) < 2:
                    issues.append(
                        f"axis '{axis_name}.{val_name}' has {len(triggers) if isinstance(triggers, list) else 0} triggers (need >=2)"
                    )
                # Check collision
                if isinstance(triggers, list):
                    for t in triggers:
                        if isinstance(t, str) and t.strip():
                            lower = t.strip().lower()
                            if lower in seen_triggers:
                                issues.append(
                                    f"trigger collision in axis '{axis_name}': "
                                    f"'{t}' used in both '{seen_triggers[lower]}' and '{val_name}'"
                                )
                            else:
                                seen_triggers[lower] = val_name

    # 5. Contract reference existence
    handoffs = manifest.get("handoffs", {})
    if isinstance(handoffs, dict):
        provides = handoffs.get("provides", {})
        if isinstance(provides, dict):
            for name, hdef in provides.items():
                if isinstance(hdef, dict):
                    c = hdef.get("contract")
                    if c and isinstance(c, str):
                        contract_path = (skill_root / c).resolve()
                        if not contract_path.exists():
                            issues.append(f"contract not found: {c} (referenced by handoff '{name}')")

    # 6. Template existence (from handoff contracts)
    if isinstance(handoffs, dict):
        provides = handoffs.get("provides", {})
        if isinstance(provides, dict):
            for name, hdef in provides.items():
                if isinstance(hdef, dict):
                    c = hdef.get("contract")
                    if c and isinstance(c, str):
                        contract_path = (skill_root / c).resolve()
                        if contract_path.exists():
                            contract = _load_yaml(contract_path)
                            if contract:
                                templates = contract.get("templates", [])
                                if isinstance(templates, list):
                                    for tpl_ref in templates:
                                        if isinstance(tpl_ref, str):
                                            tpl_path = (skill_root / tpl_ref).resolve()
                                            if not tpl_path.exists():
                                                # Try relative to contracts dir
                                                alt_path = (CONTRACTS_DIR.parent.parent / skill_name / tpl_ref).resolve()
                                                if not alt_path.exists():
                                                    issues.append(
                                                        f"template not found: {tpl_ref} (referenced by contract '{name}')"
                                                    )

    # 7. No dangling references (every file in references/ is referenced somewhere)
    refs_dir = skill_root / "references"
    if refs_dir.exists():
        for ref_file in sorted(refs_dir.iterdir()):
            if ref_file.suffix == ".md" and ref_file.is_file():
                resolved = ref_file.resolve()
                if resolved not in all_refs:
                    # Check if it's referenced through the Material Registry
                    if _is_registry_referenced(skill_name, ref_file.name):
                        continue
                    rel = resolved.relative_to(skill_root)
                    issues.append(f"dangling reference (not referenced by manifest): {rel}")

    return issues


def validate_all(skill_names: list[str] | None = None) -> dict[str, list[str]]:
    """Validate all (or specific) skills. Returns {skill_name: [issues]}."""
    if skill_names is None:
        skill_names = discover_skill_names(SKILLS_ROOT)

    all_issues: dict[str, list[str]] = {}
    for name in skill_names:
        skill_issues = validate_skill(name)
        if skill_issues:
            all_issues[name] = skill_issues
    return all_issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate skill manifest.yaml integrity")
    parser.add_argument("--skill", help="Validate one skill only")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    skills = [args.skill] if args.skill else discover_skill_names(SKILLS_ROOT)
    issues = validate_all(skills)

    if args.json:
        print(json.dumps({
            "status": "pass" if not issues else "fail",
            "issues": issues,
        }, indent=2, ensure_ascii=False))
    else:
        if issues:
            for skill, skill_issues in issues.items():
                for issue in skill_issues:
                    print(f"[{skill}] {issue}")
            total = sum(len(v) for v in issues.values())
            print(f"\nFAIL: {total} manifest issues found")
        else:
            print("PASS: all manifests valid")

    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())

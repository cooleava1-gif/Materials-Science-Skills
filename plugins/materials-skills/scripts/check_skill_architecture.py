"""Inspect materials skill architecture contracts.

The checker is intentionally diagnostic-first: missing router files and broken
manifest routes are hard issues, while standardization gaps that are still being
rolled out are reported as warnings for the first architecture pass.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import yaml


REQUIRED_CORE_FILES = ("static/core/contract.md", "static/core/workflow.md")
REQUIRED_ROUTER_FILES = ("SKILL.md", "manifest.yaml", "agents/openai.yaml")
VALID_MATURITY_STATUSES = {"stable", "beta", "draft"}
STANDARD_MANIFEST_BLOCKS = (
    "assets",
    "scripts",
    "quality_gates",
    "handoffs",
    "release_checks",
)
MOJIBAKE_MARKERS = (
    "閺",
    "缁",
    "閸",
    "鐠",
    "娴",
    "鈧",
    "鏂",
    "绮",
    "鍏",
    "寮",
    "璇",
    "姘存",
)


def _read_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - exact parser errors vary
        return {"__yaml_error__": str(exc)}
    return data if isinstance(data, dict) else {}


def _read_skill_frontmatter(skill_md_path: Path) -> dict[str, Any]:
    """Parse YAML frontmatter from SKILL.md if present."""
    if not skill_md_path.exists():
        return {}
    text = skill_md_path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    try:
        data = yaml.safe_load(text[3:end])
    except Exception as exc:
        return {"__yaml_error__": str(exc)}
    return data if isinstance(data, dict) else {}


def _as_posix(path: Path) -> str:
    return path.as_posix()


def _is_probable_path(value: str) -> bool:
    if not value or "\n" in value:
        return False
    if value.startswith(("http://", "https://", "#")):
        return False
    return "/" in value or "\\" in value or "." in Path(value).name


def _iter_axis_values(manifest: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    values: list[tuple[str, dict[str, Any]]] = []
    axes = manifest.get("axes", {})
    if not isinstance(axes, dict):
        return values
    for axis_name, axis in axes.items():
        if not isinstance(axis, dict):
            continue
        axis_values = axis.get("values", {})
        if not isinstance(axis_values, dict):
            continue
        for value_name, value_data in axis_values.items():
            if isinstance(value_data, dict):
                values.append((f"axes.{axis_name}.values.{value_name}", value_data))
    return values


def _collect_declared_paths(value: Any) -> list[str]:
    paths: list[str] = []
    if isinstance(value, str):
        if _is_probable_path(value):
            paths.append(value)
    elif isinstance(value, list):
        for item in value:
            paths.extend(_collect_declared_paths(item))
    elif isinstance(value, dict):
        for key, item in value.items():
            if key in {"path", "paths", "file", "files", "script", "scripts", "test", "tests"}:
                paths.extend(_collect_declared_paths(item))
            elif isinstance(item, (dict, list)):
                paths.extend(_collect_declared_paths(item))
    return paths


def _collect_triggers(value: Any, prefix: str = "") -> list[tuple[str, str]]:
    triggers: list[tuple[str, str]] = []
    if isinstance(value, dict):
        for key, item in value.items():
            next_prefix = f"{prefix}.{key}" if prefix else str(key)
            if key == "triggers" and isinstance(item, list):
                for idx, trigger in enumerate(item):
                    if isinstance(trigger, str):
                        triggers.append((f"{next_prefix}[{idx}]", trigger))
            else:
                triggers.extend(_collect_triggers(item, next_prefix))
    elif isinstance(value, list):
        for idx, item in enumerate(value):
            triggers.extend(_collect_triggers(item, f"{prefix}[{idx}]"))
    return triggers


def _iter_trigger_files(manifest: dict[str, Any]) -> list[tuple[str, str]]:
    """Yield (location, trigger_file_path) for all axis values with trigger_file."""
    results: list[tuple[str, str]] = []
    axes = manifest.get("axes", {})
    if not isinstance(axes, dict):
        return results
    for axis_name, axis in axes.items():
        if not isinstance(axis, dict):
            continue
        values = axis.get("values", {})
        if not isinstance(values, dict):
            continue
        for value_name, value_data in values.items():
            if isinstance(value_data, dict):
                tf = value_data.get("trigger_file")
                if isinstance(tf, str) and tf:
                    results.append((f"axes.{axis_name}.values.{value_name}.trigger_file", tf))
    return results


def _iter_reference_paths(manifest: dict[str, Any]) -> list[tuple[str, str]]:
    """Yield (location, path) for all references.on_demand entries."""
    results: list[tuple[str, str]] = []
    refs = manifest.get("references", {})
    if not isinstance(refs, dict):
        return results
    on_demand = refs.get("on_demand", {})
    if isinstance(on_demand, list):
        for idx, entry in enumerate(on_demand):
            if isinstance(entry, dict):
                p = entry.get("path")
                if isinstance(p, str) and p:
                    results.append((f"references.on_demand[{idx}].path", p))
    elif isinstance(on_demand, dict):
        for key, entry in on_demand.items():
            if isinstance(entry, dict):
                p = entry.get("path")
                if isinstance(p, str) and p:
                    results.append((f"references.on_demand.{key}.path", p))
            elif isinstance(entry, str) and entry:
                results.append((f"references.on_demand.{key}", entry))
    return results


def _check_consistency(skill_dir: Path, manifest: dict[str, Any]) -> dict[str, Any]:
    """Return standardization warnings for a single skill."""
    skill_md_path = skill_dir / "SKILL.md"
    readme_path = skill_dir / "README.md"
    front = _read_skill_frontmatter(skill_md_path)

    version = manifest.get("version")
    skill_version = front.get("version") if isinstance(front, dict) else None
    version_mismatch = None
    if version is not None and skill_version is not None and version != skill_version:
        version_mismatch = f"manifest version {version!r} != SKILL.md version {skill_version!r}"

    readme_missing_version = None
    if version is not None and readme_path.exists():
        readme_text = readme_path.read_text(encoding="utf-8")
        if version not in readme_text:
            readme_missing_version = f"README.md does not mention version {version!r}"

    missing_references_block = None
    if "references" not in manifest:
        missing_references_block = "manifest missing 'references' block"

    skill_missing_router_terms = None
    if skill_md_path.exists():
        body = skill_md_path.read_text(encoding="utf-8").lower()
        if "manifest" not in body or "axes" not in body:
            skill_missing_router_terms = "SKILL.md does not mention both 'manifest' and 'axes'"

    return {
        "version_mismatch": version_mismatch,
        "readme_missing_version": readme_missing_version,
        "missing_references_block": missing_references_block,
        "skill_missing_router_terms": skill_missing_router_terms,
    }


def _path_exists(skill_dir: Path, path_text: str) -> bool:
    return (skill_dir / path_text).resolve().exists()


def _core_status(skill_dir: Path) -> dict[str, list[str]]:
    static_core = skill_dir / "static" / "core"
    existing_core = {path.name for path in static_core.glob("*.md")} if static_core.exists() else set()
    missing = [path for path in REQUIRED_CORE_FILES if not (skill_dir / path).exists()]
    compatible = []
    if missing and "workflow.md" in existing_core and (
        any(name.endswith("contract.md") for name in existing_core) or any(name.endswith("stance.md") for name in existing_core)
    ):
        compatible = sorted(f"static/core/{name}" for name in existing_core)
    return {"missing_exact": missing, "compatible_core_files": compatible}


def inspect_skill(skill_dir: Path) -> dict[str, object]:
    """Return missing files, missing manifest paths, and invalid trigger encodings."""

    skill_dir = Path(skill_dir)
    manifest_path = skill_dir / "manifest.yaml"
    manifest = _read_yaml(manifest_path) if manifest_path.exists() else {}
    yaml_errors = []
    if "__yaml_error__" in manifest:
        yaml_errors.append(str(manifest["__yaml_error__"]))
        manifest = {}

    missing_router_files = [path for path in REQUIRED_ROUTER_FILES if not (skill_dir / path).exists()]
    core = _core_status(skill_dir)
    missing_manifest_blocks = [block for block in STANDARD_MANIFEST_BLOCKS if block not in manifest]

    status = manifest.get("status")
    status_issue = None
    if not status:
        status_issue = "manifest missing 'status' field"
    elif str(status).lower() not in VALID_MATURITY_STATUSES:
        status_issue = f"manifest status {status!r} not in {sorted(VALID_MATURITY_STATUSES)}"

    missing_manifest_paths: list[str] = []
    checked_manifest_paths: list[str] = []
    for path_text in manifest.get("always_load", []) if isinstance(manifest.get("always_load"), list) else []:
        checked_manifest_paths.append(path_text)
        if not _path_exists(skill_dir, path_text):
            missing_manifest_paths.append(path_text)

    for _, value_data in _iter_axis_values(manifest):
        path_text = value_data.get("path")
        if isinstance(path_text, str):
            checked_manifest_paths.append(path_text)
            if not _path_exists(skill_dir, path_text):
                missing_manifest_paths.append(path_text)

    missing_declared_paths: list[str] = []
    for block in ("assets", "scripts"):
        for path_text in _collect_declared_paths(manifest.get(block)):
            checked_manifest_paths.append(path_text)
            if not _path_exists(skill_dir, path_text):
                missing_declared_paths.append(path_text)

    missing_trigger_files: list[str] = []
    for location, path_text in _iter_trigger_files(manifest):
        checked_manifest_paths.append(path_text)
        if not _path_exists(skill_dir, path_text):
            missing_trigger_files.append(f"{location}: {path_text}")

    missing_reference_paths: list[str] = []
    for location, path_text in _iter_reference_paths(manifest):
        checked_manifest_paths.append(path_text)
        if not _path_exists(skill_dir, path_text):
            missing_reference_paths.append(f"{location}: {path_text}")

    mojibake_triggers = [
        {"location": location, "trigger": trigger}
        for location, trigger in _collect_triggers(manifest)
        if any(marker in trigger for marker in MOJIBAKE_MARKERS)
    ]

    hard_issues = (
        missing_router_files
        + yaml_errors
        + ([status_issue] if status_issue else [])
        + missing_manifest_paths
        + missing_declared_paths
        + missing_trigger_files
        + missing_reference_paths
    )
    consistency = _check_consistency(skill_dir, manifest)
    consistency_issues = [v for v in consistency.values() if v is not None]

    return {
        "skill": skill_dir.name,
        "path": _as_posix(skill_dir),
        "status": "fail" if hard_issues else "pass",
        "missing_router_files": missing_router_files,
        "missing_core_files": core["missing_exact"],
        "compatible_core_files": core["compatible_core_files"],
        "missing_manifest_blocks": missing_manifest_blocks,
        "manifest_status": status,
        "manifest_status_issue": status_issue,
        "missing_manifest_paths": sorted(set(missing_manifest_paths)),
        "missing_declared_paths": sorted(set(missing_declared_paths)),
        "missing_trigger_files": sorted(set(missing_trigger_files)),
        "missing_reference_paths": sorted(set(missing_reference_paths)),
        "checked_manifest_paths": sorted(set(checked_manifest_paths)),
        "mojibake_triggers": mojibake_triggers,
        "yaml_errors": yaml_errors,
        "consistency": consistency,
        "warnings": {
            "missing_exact_core_files": core["missing_exact"],
            "missing_standard_manifest_blocks": missing_manifest_blocks,
            "mojibake_triggers": mojibake_triggers,
            "consistency_issues": consistency_issues,
        },
    }


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_ROOT = PLUGIN_ROOT / "skills"


def inspect_all(root: Path | None = None) -> dict[str, object]:
    """Inspect every materials-* skill and return a JSON-safe report."""

    root = Path(root) if root is not None else DEFAULT_SKILLS_ROOT
    skills = [path for path in sorted(root.glob("materials-*")) if path.is_dir()]
    skill_reports = [inspect_skill(skill_dir) for skill_dir in skills]
    hard_failures = [report["skill"] for report in skill_reports if report["status"] != "pass"]
    if not skill_reports:
        hard_failures.append(f"no skills found under {root}")

    warnings = {
        "skills_with_missing_exact_core_files": [
            report["skill"] for report in skill_reports if report["missing_core_files"]
        ],
        "skills_with_missing_standard_manifest_blocks": [
            report["skill"] for report in skill_reports if report["missing_manifest_blocks"]
        ],
        "skills_with_mojibake_triggers": [
            report["skill"] for report in skill_reports if report["mojibake_triggers"]
        ],
        "skills_with_consistency_issues": [
            report["skill"]
            for report in skill_reports
            if report["warnings"].get("consistency_issues")
        ],
    }
    return {
        "status": "fail" if hard_failures else "pass",
        "summary": {
            "skills_checked": len(skill_reports),
            "hard_failures": hard_failures,
            "warning_buckets": {key: len(value) if isinstance(value, list) else value for key, value in warnings.items()},
        },
        "skills": skill_reports,
        "warnings": warnings,
    }


def main(argv: list[str] | None = None) -> int:
    """Print JSON. Exit 0 only when every required architecture check passes."""

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=None, help="Skills root directory (default: plugin skills dir)")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args(argv)

    report = inspect_all(args.root)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

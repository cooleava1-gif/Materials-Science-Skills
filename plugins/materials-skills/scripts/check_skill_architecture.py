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
CONTEXT_BUDGET_FIELDS = (
    "target_activation_bytes",
    "max_activation_bytes",
    "max_always_load",
    "max_skill_lines",
    "max_workflow_lines",
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


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _manifest_allowed_roots(skills_root: Path) -> list[Path]:
    root = skills_root.resolve()
    roots = [root]
    plugin_shared = (root.parent / "_shared").resolve()
    if plugin_shared.is_dir():
        roots.append(plugin_shared)
    return roots


def _resolve_manifest_path(skills_root: Path, skill_dir: Path, path_text: str) -> Path | None:
    path = Path(path_text)
    if path.is_absolute():
        return None
    resolved = (skill_dir / path).resolve()
    if not any(_is_relative_to(resolved, root) for root in _manifest_allowed_roots(skills_root)):
        return None
    return resolved


def _resolve_cli_skill(root: Path, skill: str) -> Path:
    skill_path = Path(skill)
    if skill_path.is_absolute():
        raise ValueError("--skill must be a single skill directory name under --root")
    root = root.resolve()
    resolved = (root / skill_path).resolve()
    if not _is_relative_to(resolved, root):
        raise ValueError("--skill must stay under --root")
    relative = resolved.relative_to(root)
    if len(relative.parts) != 1:
        raise ValueError("--skill must be one directory name, not a path")
    return resolved


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


def _path_exists(
    skills_root: Path, skill_dir: Path, path_text: str, *, require_file: bool = False
) -> bool:
    path = _resolve_manifest_path(skills_root, skill_dir, path_text)
    if not path:
        return False
    return path.is_file() if require_file else path.exists()


def _line_count(path: Path) -> int:
    if not path.exists():
        return 0
    return len(path.read_text(encoding="utf-8").splitlines())


def _context_size(path: Path) -> int:
    """Return platform-independent UTF-8 context bytes, with a binary fallback."""
    try:
        return len(path.read_text(encoding="utf-8").encode("utf-8"))
    except UnicodeDecodeError:
        return path.stat().st_size


def _budget_ints(budget: dict[str, Any]) -> tuple[dict[str, int], list[str]]:
    values: dict[str, int] = {}
    hard_failures: list[str] = []
    for field in CONTEXT_BUDGET_FIELDS:
        if field not in budget:
            hard_failures.append(f"context_budget.{field} is required")
            continue
        value = budget[field]
        if isinstance(value, bool) or not isinstance(value, int) or value < 0:
            hard_failures.append(f"context_budget.{field} must be a non-negative integer")
            continue
        values[field] = value
    target = values.get("target_activation_bytes")
    maximum = values.get("max_activation_bytes")
    if target is not None and maximum is not None and target > maximum:
        hard_failures.append(
            "context_budget.target_activation_bytes must be <= context_budget.max_activation_bytes"
        )
    return values, hard_failures


def _route_on_demand_path(
    manifest: dict[str, Any], selector: str
) -> str | None:
    references = manifest.get("references", {})
    if not isinstance(references, dict):
        return None
    on_demand = references.get("on_demand", {})
    if isinstance(on_demand, dict):
        entry = on_demand.get(selector)
        if isinstance(entry, str):
            return entry
        if isinstance(entry, dict) and isinstance(entry.get("path"), str):
            return entry["path"]
    elif isinstance(on_demand, list):
        for entry in on_demand:
            if not isinstance(entry, dict):
                continue
            path_text = entry.get("path")
            if selector == path_text and isinstance(path_text, str):
                return path_text
    return None


def _route_skill_payload(
    skills_root: Path,
    skill_name: str,
    axes: Any,
    on_demand: Any,
) -> tuple[list[Path], list[str]]:
    failures: list[str] = []
    skill_dir = (skills_root / skill_name).resolve()
    if not _is_relative_to(skill_dir, skills_root.resolve()) or not skill_dir.is_dir():
        return [], [f"route skill {skill_name!r} does not exist under skills root"]

    manifest_path = skill_dir / "manifest.yaml"
    manifest = _read_yaml(manifest_path)
    files = [skill_dir / "SKILL.md", manifest_path]
    for path_text in manifest.get("always_load", []):
        if not isinstance(path_text, str):
            continue
        resolved = _resolve_manifest_path(skills_root, skill_dir, path_text)
        if resolved and resolved.is_file():
            files.append(resolved)
        else:
            failures.append(f"{skill_name}: always_load path {path_text!r} is invalid")

    if not isinstance(axes, dict):
        failures.append(f"{skill_name}: route axes must be a mapping")
        axes = {}
    manifest_axes = manifest.get("axes", {})
    if not isinstance(manifest_axes, dict):
        manifest_axes = {}
    for axis_name, value_name in axes.items():
        if not isinstance(axis_name, str) or not isinstance(value_name, str):
            failures.append(
                f"{skill_name}: route axis names and values must be strings"
            )
            continue
        axis = manifest_axes.get(axis_name)
        if not isinstance(axis, dict):
            failures.append(f"{skill_name}: route axis {axis_name!r} is not declared")
            continue
        values = axis.get("values", {})
        value = values.get(value_name) if isinstance(values, dict) else None
        if not isinstance(value, dict) or not isinstance(value.get("path"), str):
            failures.append(
                f"{skill_name}: route value {value_name!r} is not declared for axis {axis_name!r}"
            )
            continue
        path_text = value["path"]
        resolved = _resolve_manifest_path(skills_root, skill_dir, path_text)
        if resolved and resolved.is_file():
            files.append(resolved)
        else:
            failures.append(
                f"{skill_name}: route path {path_text!r} for {axis_name}.{value_name} is invalid"
            )

    if not isinstance(on_demand, list):
        failures.append(f"{skill_name}: route on_demand must be a list")
        on_demand = []
    for selector in on_demand:
        if not isinstance(selector, str):
            failures.append(f"{skill_name}: on_demand selectors must be strings")
            continue
        path_text = _route_on_demand_path(manifest, selector)
        if path_text is None:
            failures.append(f"{skill_name}: on_demand selector {selector!r} is not declared")
            continue
        resolved = _resolve_manifest_path(skills_root, skill_dir, path_text)
        if resolved and resolved.is_file():
            files.append(resolved)
        else:
            failures.append(
                f"{skill_name}: on_demand path {path_text!r} for {selector!r} is invalid"
            )
    return files, failures


def _route_scenario_reports(
    skills_root: Path, skill_dir: Path, budget: dict[str, Any]
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    contract_failures: list[str] = []
    required_names = budget.get("required_route_scenarios", [])
    required_axes = budget.get("required_route_axes", [])
    for field, value in (
        ("required_route_scenarios", required_names),
        ("required_route_axes", required_axes),
    ):
        if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
            contract_failures.append(f"context_budget.{field} must be a list of strings")
    if contract_failures:
        return [], [], contract_failures

    scenarios = budget.get("route_scenarios", [])
    scenarios_file = budget.get("route_scenarios_file")
    if scenarios_file is not None:
        if not isinstance(scenarios_file, str):
            return [], [], contract_failures + [
                "context_budget.route_scenarios_file must be a string"
            ]
        resolved = _resolve_manifest_path(skills_root, skill_dir, scenarios_file)
        if not resolved or not resolved.is_file():
            return [], [], contract_failures + [
                f"context_budget.route_scenarios_file {scenarios_file!r} is invalid"
            ]
        scenario_data = _read_yaml(resolved)
        if "__yaml_error__" in scenario_data:
            return [], [], contract_failures + [
                f"context_budget.route_scenarios_file: {scenario_data['__yaml_error__']}"
            ]
        scenarios = scenario_data.get("route_scenarios", [])
    if scenarios == []:
        missing = ", ".join(required_names)
        if missing:
            contract_failures.append(f"required route scenarios are missing: {missing}")
        return [], [], contract_failures
    if not isinstance(scenarios, list):
        return [], [], contract_failures + [
            "context_budget.route_scenarios must be a list"
        ]

    reports: list[dict[str, Any]] = []
    warnings: list[str] = []
    hard_failures: list[str] = list(contract_failures)
    seen_names: set[str] = set()
    for index, scenario in enumerate(scenarios):
        prefix = f"context_budget.route_scenarios[{index}]"
        scenario_failures: list[str] = []
        if not isinstance(scenario, dict):
            hard_failures.append(f"{prefix} must be a mapping")
            continue
        name = scenario.get("name")
        if not isinstance(name, str) or not name.strip():
            name = f"route-{index}"
            scenario_failures.append(f"{prefix}.name must be a non-empty string")
        elif name in seen_names:
            scenario_failures.append(f"{prefix}.name {name!r} must be unique")
        seen_names.add(name)

        primary_axes = scenario.get("axes", {})
        if isinstance(primary_axes, dict):
            missing_axes = [axis for axis in required_axes if axis not in primary_axes]
            if missing_axes:
                scenario_failures.append(
                    f"{prefix}.axes missing required axes: {', '.join(missing_axes)}"
                )

        target = scenario.get("target_bytes")
        maximum = scenario.get("max_bytes")
        for field, value in (("target_bytes", target), ("max_bytes", maximum)):
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                scenario_failures.append(f"{prefix}.{field} must be a non-negative integer")
        if isinstance(target, int) and isinstance(maximum, int) and target > maximum:
            scenario_failures.append(f"{prefix}.target_bytes must be <= max_bytes")

        selections = [
            {
                "skill": skill_dir.name,
                "axes": scenario.get("axes", {}),
                "on_demand": scenario.get("on_demand", []),
            }
        ]
        companions = scenario.get("companions", [])
        if not isinstance(companions, list):
            scenario_failures.append(f"{prefix}.companions must be a list")
            companions = []
        selections.extend(companion for companion in companions if isinstance(companion, dict))
        if len(selections) != len(companions) + 1:
            scenario_failures.append(f"{prefix}.companions entries must be mappings")
        selected_skills: set[str] = set()
        for selection in selections:
            selected_skill = selection.get("skill")
            if isinstance(selected_skill, str) and selected_skill in selected_skills:
                scenario_failures.append(
                    f"{prefix}: skill {selected_skill!r} is selected more than once"
                )
            elif isinstance(selected_skill, str):
                selected_skills.add(selected_skill)
            selection_axes = selection.get("axes", {})
            selection_required_axes = selection.get("required_axes", [])
            if not isinstance(selection_required_axes, list) or any(
                not isinstance(axis, str) for axis in selection_required_axes
            ):
                scenario_failures.append(
                    f"{prefix}: required_axes must be a list of strings"
                )
            elif isinstance(selection_axes, dict):
                missing_selection_axes = [
                    axis for axis in selection_required_axes if axis not in selection_axes
                ]
                if missing_selection_axes:
                    scenario_failures.append(
                        f"{prefix}: {selected_skill} missing required axes: "
                        + ", ".join(missing_selection_axes)
                    )

        unique_files: dict[Path, None] = {}
        skill_bytes: dict[str, int] = {}
        for selection in selections:
            selected_skill = selection.get("skill")
            if not isinstance(selected_skill, str) or not selected_skill:
                scenario_failures.append(f"{prefix}: each skill selection needs a skill name")
                continue
            files, failures = _route_skill_payload(
                skills_root,
                selected_skill,
                selection.get("axes", {}),
                selection.get("on_demand", []),
            )
            scenario_failures.extend(failures)
            before = set(unique_files)
            for path in files:
                if path.is_file():
                    unique_files[path.resolve()] = None
            skill_bytes[selected_skill] = sum(
                _context_size(path) for path in unique_files if path not in before
            )

        activation_bytes = sum(_context_size(path) for path in unique_files)
        route_warnings: list[str] = []
        if isinstance(target, int) and activation_bytes > target:
            route_warnings.append(
                f"route {name!r} bytes {activation_bytes} exceed target {target}"
            )
        if isinstance(maximum, int) and activation_bytes > maximum:
            scenario_failures.append(
                f"route {name!r} bytes {activation_bytes} exceed maximum {maximum}"
            )
        warnings.extend(route_warnings)
        hard_failures.extend(scenario_failures)
        reports.append(
            {
                "name": name,
                "activation_bytes": activation_bytes,
                "files": sorted(path.as_posix() for path in unique_files),
                "file_count": len(unique_files),
                "skill_bytes": skill_bytes,
                "warnings": route_warnings,
                "hard_failures": scenario_failures,
            }
        )
    missing_names = [name for name in required_names if name not in seen_names]
    unexpected_names = [name for name in seen_names if name not in required_names]
    if required_names and missing_names:
        hard_failures.append(
            "required route scenarios are missing: " + ", ".join(missing_names)
        )
    if required_names and unexpected_names:
        hard_failures.append(
            "undeclared route scenarios are present: " + ", ".join(sorted(unexpected_names))
        )
    return reports, warnings, hard_failures


def _context_budget_report(
    skills_root: Path, skill_dir: Path, manifest: dict[str, Any]
) -> dict[str, Any]:
    if "context_budget" not in manifest:
        return {
            "declared": False,
            "metrics": {},
            "warnings": [],
            "hard_failures": [],
        }
    budget = manifest.get("context_budget")
    schema_failures: list[str] = []
    budget_values: dict[str, int] = {}
    if isinstance(budget, dict):
        budget_values, schema_failures = _budget_ints(budget)
    else:
        schema_failures.append("context_budget must be a mapping")

    skill_path = skill_dir / "SKILL.md"
    manifest_path = skill_dir / "manifest.yaml"
    workflow_path = skill_dir / "static" / "core" / "workflow.md"
    always_load = manifest.get("always_load", [])
    if not isinstance(always_load, list):
        always_load = []

    always_load_bytes = 0
    for path_text in always_load:
        if not isinstance(path_text, str):
            continue
        path = _resolve_manifest_path(skills_root, skill_dir, path_text)
        if path and path.exists() and path.is_file():
            always_load_bytes += _context_size(path)

    skill_bytes = _context_size(skill_path) if skill_path.exists() else 0
    manifest_bytes = _context_size(manifest_path) if manifest_path.exists() else 0
    activation_bytes = skill_bytes + manifest_bytes + always_load_bytes
    metrics = {
        "activation_bytes": activation_bytes,
        "skill_bytes": skill_bytes,
        "manifest_bytes": manifest_bytes,
        "always_load_bytes": always_load_bytes,
        "always_load_count": len(always_load),
        "skill_lines": _line_count(skill_path),
        "workflow_lines": _line_count(workflow_path),
    }

    routes, route_warnings, route_failures = _route_scenario_reports(
        skills_root, skill_dir, budget if isinstance(budget, dict) else {}
    )
    warnings: list[str] = list(route_warnings)
    hard_failures: list[str] = list(schema_failures) + route_failures

    target = budget_values.get("target_activation_bytes")
    if target is not None and activation_bytes > target:
        warnings.append(f"activation bytes {activation_bytes} exceed target {target}")

    maximum = budget_values.get("max_activation_bytes")
    if maximum is not None and activation_bytes > maximum:
        hard_failures.append(f"activation bytes {activation_bytes} exceed maximum {maximum}")

    max_always = budget_values.get("max_always_load")
    if max_always is not None and len(always_load) > max_always:
        hard_failures.append(f"always_load count {len(always_load)} exceeds maximum {max_always}")

    max_skill_lines = budget_values.get("max_skill_lines")
    if max_skill_lines is not None and metrics["skill_lines"] > max_skill_lines:
        hard_failures.append(f"SKILL.md lines {metrics['skill_lines']} exceed maximum {max_skill_lines}")

    max_workflow_lines = budget_values.get("max_workflow_lines")
    if max_workflow_lines is not None and metrics["workflow_lines"] > max_workflow_lines:
        hard_failures.append(
            f"workflow lines {metrics['workflow_lines']} exceed maximum {max_workflow_lines}"
        )

    return {
        "declared": True,
        "metrics": metrics,
        "routes": routes,
        "warnings": warnings,
        "hard_failures": hard_failures,
    }


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


def inspect_skill(skill_dir: Path, skills_root: Path | None = None) -> dict[str, object]:
    """Return missing files, missing manifest paths, and invalid trigger encodings."""

    skill_dir = Path(skill_dir)
    skills_root = Path(skills_root) if skills_root is not None else skill_dir.parent
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
        if not isinstance(path_text, str) or not _path_exists(
            skills_root, skill_dir, path_text, require_file=True
        ):
            missing_manifest_paths.append(path_text)

    for _, value_data in _iter_axis_values(manifest):
        path_text = value_data.get("path")
        if isinstance(path_text, str):
            checked_manifest_paths.append(path_text)
            if not _path_exists(skills_root, skill_dir, path_text, require_file=True):
                missing_manifest_paths.append(path_text)

    missing_declared_paths: list[str] = []
    for block in ("assets", "scripts"):
        for path_text in _collect_declared_paths(manifest.get(block)):
            checked_manifest_paths.append(path_text)
            if not _path_exists(skills_root, skill_dir, path_text):
                missing_declared_paths.append(path_text)

    missing_trigger_files: list[str] = []
    for location, path_text in _iter_trigger_files(manifest):
        checked_manifest_paths.append(path_text)
        if not _path_exists(skills_root, skill_dir, path_text, require_file=True):
            missing_trigger_files.append(f"{location}: {path_text}")

    missing_reference_paths: list[str] = []
    for location, path_text in _iter_reference_paths(manifest):
        checked_manifest_paths.append(path_text)
        if not _path_exists(skills_root, skill_dir, path_text, require_file=True):
            missing_reference_paths.append(f"{location}: {path_text}")

    mojibake_triggers = [
        {"location": location, "trigger": trigger}
        for location, trigger in _collect_triggers(manifest)
        if any(marker in trigger for marker in MOJIBAKE_MARKERS)
    ]
    context_budget = _context_budget_report(skills_root, skill_dir, manifest)

    hard_issues = (
        missing_router_files
        + yaml_errors
        + ([status_issue] if status_issue else [])
        + missing_manifest_paths
        + missing_declared_paths
        + missing_trigger_files
        + missing_reference_paths
        + context_budget["hard_failures"]
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
        "context_budget": context_budget,
        "yaml_errors": yaml_errors,
        "consistency": consistency,
        "warnings": {
            "missing_exact_core_files": core["missing_exact"],
            "missing_standard_manifest_blocks": missing_manifest_blocks,
            "mojibake_triggers": mojibake_triggers,
            "context_budget_warnings": context_budget["warnings"],
            "consistency_issues": consistency_issues,
        },
    }


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_ROOT = PLUGIN_ROOT / "skills"


def inspect_all(root: Path | None = None) -> dict[str, object]:
    """Inspect every materials-* skill and return a JSON-safe report."""

    root = Path(root) if root is not None else DEFAULT_SKILLS_ROOT
    skills = [path for path in sorted(root.glob("materials-*")) if path.is_dir()]
    skill_reports = [inspect_skill(skill_dir, root) for skill_dir in skills]
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
        "skills_over_context_target": [
            report["skill"] for report in skill_reports if report["context_budget"]["warnings"]
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
    parser.add_argument("--skill", help="Inspect one skill directory by name.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args(argv)

    root = Path(args.root) if args.root is not None else DEFAULT_SKILLS_ROOT
    if args.skill:
        try:
            skill_dir = _resolve_cli_skill(root, args.skill)
        except ValueError as exc:
            parser.error(str(exc))
        report = inspect_skill(skill_dir, root)
    else:
        report = inspect_all(root)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

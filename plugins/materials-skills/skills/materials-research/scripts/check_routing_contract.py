#!/usr/bin/env python3
"""Run deterministic checks for the materials-research routing contract."""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterator

import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = SKILL_ROOT.parent
MANIFEST_PATH = SKILL_ROOT / "manifest.yaml"
REQUIRED_ROUTING_AXES = ("task", "domain", "journal")


class ContractError(ValueError):
    """Raised when a manifest or selected fragment violates the contract."""


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def _manifest_allowed_roots(skills_root: Path) -> tuple[Path, ...]:
    root = skills_root.resolve()
    return (root, (root.parent / "_shared").resolve())


def load_manifest(manifest_path: Path = MANIFEST_PATH) -> dict[str, Any]:
    try:
        document = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        raise ContractError(f"could not load manifest: {exc}") from exc
    if not isinstance(document, dict):
        raise ContractError("manifest must contain a mapping at the document root")
    return document


def _resolve_declared_file(
    path_ref: object,
    *,
    skill_root: Path,
    allowed_roots: tuple[Path, ...],
    label: str,
    boundary_label: str,
) -> Path:
    if not isinstance(path_ref, str) or not path_ref.strip():
        raise ContractError(f"{label} must be a non-empty path")

    path = Path(path_ref)
    if path.is_absolute():
        raise ContractError(f"{label} must be relative: {path_ref}")

    resolved = (skill_root / path).resolve()
    if not any(_is_within(resolved, root) for root in allowed_roots):
        raise ContractError(f"{label} escapes {boundary_label}: {path_ref}")
    if not resolved.is_file():
        raise ContractError(f"{label} does not resolve to a file: {path_ref}")
    try:
        resolved.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise ContractError(f"{label} is not loadable: {path_ref}") from exc
    return resolved


def select_fragment(
    manifest: dict[str, Any],
    *,
    axis: str,
    selection: str,
    skill_root: Path = SKILL_ROOT,
    skills_root: Path = SKILLS_ROOT,
) -> tuple[str, Path]:
    axes = manifest.get("axes")
    if not isinstance(axes, dict):
        raise ContractError("manifest axes must be a mapping")

    axis_definition = axes.get(axis)
    if not isinstance(axis_definition, dict):
        raise ContractError(f"unknown axis: {axis}")

    values = axis_definition.get("values")
    if not isinstance(values, dict):
        raise ContractError(f"axis has no selectable values: {axis}")
    if selection not in values:
        raise ContractError(f"unknown selection: {axis}.{selection}")

    value_definition = values[selection]
    if not isinstance(value_definition, dict):
        raise ContractError(f"selection is not a mapping: {axis}.{selection}")

    path_ref = value_definition.get("path")
    path = _resolve_declared_file(
        path_ref,
        skill_root=skill_root,
        allowed_roots=_manifest_allowed_roots(skills_root),
        label=f"axes.{axis}.values.{selection}.path",
        boundary_label="manifest allowed roots",
    )
    assert isinstance(path_ref, str)
    return path_ref, path


def _required_axes(manifest: dict[str, Any]) -> dict[str, Any]:
    axes = manifest.get("axes")
    if not isinstance(axes, dict):
        raise ContractError("manifest axes must be a mapping")
    missing = [axis for axis in REQUIRED_ROUTING_AXES if axis not in axes]
    if missing:
        raise ContractError(
            "manifest missing required routing axes: " + ", ".join(missing)
        )
    return axes


def _iter_manifest_paths(manifest: dict[str, Any]) -> Iterator[tuple[str, object]]:
    always_load = manifest.get("always_load")
    if not isinstance(always_load, list):
        raise ContractError("manifest always_load must be a list")
    for index, path_ref in enumerate(always_load):
        yield f"always_load[{index}]", path_ref

    axes = _required_axes(manifest)
    for axis in sorted(axes):
        axis_definition = axes[axis]
        if not isinstance(axis_definition, dict):
            raise ContractError(f"axis is not a mapping: {axis}")
        values = axis_definition.get("values")
        if not isinstance(values, dict):
            raise ContractError(f"axis has no selectable values: {axis}")
        for selection in sorted(values):
            value_definition = values[selection]
            if not isinstance(value_definition, dict):
                raise ContractError(f"selection is not a mapping: {axis}.{selection}")
            prefix = f"axes.{axis}.values.{selection}"
            yield f"{prefix}.path", value_definition.get("path")
            if "trigger_file" in value_definition:
                yield f"{prefix}.trigger_file", value_definition["trigger_file"]

    references = manifest.get("references")
    if not isinstance(references, dict):
        raise ContractError("manifest references must be a mapping")
    on_demand = references.get("on_demand")
    if not isinstance(on_demand, dict):
        raise ContractError("manifest references.on_demand must be a mapping")
    for name in sorted(on_demand):
        entry = on_demand[name]
        if not isinstance(entry, dict):
            raise ContractError(f"on-demand reference is not a mapping: {name}")
        yield f"references.on_demand.{name}.path", entry.get("path")

    handoffs = manifest.get("handoffs")
    if not isinstance(handoffs, dict):
        raise ContractError("manifest handoffs must be a mapping")
    provides = handoffs.get("provides")
    if not isinstance(provides, dict):
        raise ContractError("manifest handoffs.provides must be a mapping")
    for name in sorted(provides):
        entry = provides[name]
        if not isinstance(entry, dict):
            raise ContractError(f"handoff is not a mapping: {name}")
        if "contract" in entry:
            yield f"handoffs.provides.{name}.contract", entry["contract"]


def validate_manifest_files(
    manifest: dict[str, Any],
    *,
    skill_root: Path = SKILL_ROOT,
    skills_root: Path = SKILLS_ROOT,
) -> int:
    checked = 0
    issues: list[str] = []
    for label, path_ref in _iter_manifest_paths(manifest):
        try:
            _resolve_declared_file(
                path_ref,
                skill_root=skill_root,
                allowed_roots=_manifest_allowed_roots(skills_root),
                label=label,
                boundary_label="manifest allowed roots",
            )
        except ContractError as exc:
            issues.append(str(exc))
        checked += 1

    if issues:
        raise ContractError("; ".join(issues))
    return checked


def _selection_snapshot(manifest: dict[str, Any]) -> list[dict[str, str]]:
    axes = _required_axes(manifest)

    snapshot: list[dict[str, str]] = []
    for axis in sorted(axes):
        axis_definition = axes[axis]
        if not isinstance(axis_definition, dict):
            raise ContractError(f"axis is not a mapping: {axis}")
        values = axis_definition.get("values")
        if not isinstance(values, dict):
            raise ContractError(f"axis has no selectable values: {axis}")
        for selection in sorted(values):
            path_ref, _ = select_fragment(
                manifest,
                axis=axis,
                selection=selection,
            )
            snapshot.append(
                {
                    "axis": axis,
                    "selection": selection,
                    "path": path_ref,
                }
            )
    return snapshot


def _capture_error(operation: Any) -> str:
    try:
        operation()
    except ContractError as exc:
        return str(exc)
    raise ContractError("expected operation to raise ContractError")


def _expect_error(operation: Any, expected: str) -> None:
    actual = _capture_error(operation)
    if actual != expected:
        raise ContractError(f"expected error {expected!r}, got {actual!r}")


def _expect_error_contains(operation: Any, expected: str) -> None:
    actual = _capture_error(operation)
    if expected not in actual:
        raise ContractError(f"expected error to contain {expected!r}, got {actual!r}")


def _run_valid_selections(manifest: dict[str, Any]) -> str:
    snapshot = _selection_snapshot(manifest)
    return f"PASS valid-selections count={len(snapshot)}"


def _run_manifest_files(manifest: dict[str, Any]) -> str:
    checked = validate_manifest_files(manifest)
    return f"PASS manifest-files count={checked}"


def _run_path_errors() -> str:
    with tempfile.TemporaryDirectory() as directory:
        temporary_root = Path(directory)
        skills_root = temporary_root / "skills"
        skill_root = skills_root / "materials-research"
        existing = skill_root / "static" / "fragments" / "existing.md"
        existing.parent.mkdir(parents=True)
        existing.write_text("existing fragment\n", encoding="utf-8")
        manifest = {
            "axes": {
                "task": {
                    "values": {
                        "missing": {"path": "static/fragments/missing.md"},
                        "escape": {"path": "../../outside.md"},
                        "absolute": {"path": str(existing.resolve())},
                    }
                }
            }
        }

        _expect_error(
            lambda: select_fragment(
                manifest,
                axis="task",
                selection="missing",
                skill_root=skill_root,
                skills_root=skills_root,
            ),
            "axes.task.values.missing.path does not resolve to a file: "
            "static/fragments/missing.md",
        )
        _expect_error(
            lambda: select_fragment(
                manifest,
                axis="task",
                selection="escape",
                skill_root=skill_root,
                skills_root=skills_root,
            ),
            "axes.task.values.escape.path escapes manifest allowed roots: "
            "../../outside.md",
        )
        _expect_error_contains(
            lambda: select_fragment(
                manifest,
                axis="task",
                selection="absolute",
                skill_root=skill_root,
                skills_root=skills_root,
            ),
            "axes.task.values.absolute.path must be relative",
        )
    return "PASS path-errors"


def _reordered_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    reordered = dict(manifest)
    axes = manifest["axes"]
    assert isinstance(axes, dict)
    reordered_axes: dict[str, Any] = {}
    for axis in reversed(list(axes)):
        axis_definition = dict(axes[axis])
        values = axis_definition.get("values")
        if isinstance(values, dict):
            axis_definition["values"] = {
                name: values[name] for name in reversed(list(values))
            }
        reordered_axes[axis] = axis_definition
    reordered["axes"] = reordered_axes
    return reordered


def _snapshot_json(manifest: dict[str, Any]) -> str:
    return json.dumps(
        _selection_snapshot(manifest),
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )


def _run_deterministic_output(manifest: dict[str, Any]) -> str:
    first = _snapshot_json(manifest)
    second = _snapshot_json(_reordered_manifest(manifest))
    if first != second:
        raise ContractError("selected-fragment output is not deterministic")

    operation = lambda: select_fragment(
        manifest,
        axis="task",
        selection="missing-value",
    )
    if _capture_error(operation) != _capture_error(operation):
        raise ContractError("selected-fragment error output is not deterministic")
    return "PASS deterministic-output"


def _run_case(case: str, manifest: dict[str, Any]) -> str:
    if case == "valid-selections":
        return _run_valid_selections(manifest)
    if case == "manifest-files":
        return _run_manifest_files(manifest)
    if case == "path-errors":
        return _run_path_errors()
    if case == "deterministic-output":
        return _run_deterministic_output(manifest)
    raise ContractError(f"unknown case: {case}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--case",
        choices=(
            "valid-selections",
            "manifest-files",
            "path-errors",
            "deterministic-output",
        ),
    )
    parser.add_argument("--axis")
    parser.add_argument("--selection")
    args = parser.parse_args()

    if (args.axis is None) != (args.selection is None):
        parser.error("--axis and --selection must be provided together")
    if args.case is None and args.axis is None:
        parser.error("provide --case or both --axis and --selection")
    if args.case is not None and args.axis is not None:
        parser.error("--case cannot be combined with --axis or --selection")

    try:
        manifest = load_manifest()
        if args.axis is not None and args.selection is not None:
            path_ref, _ = select_fragment(
                manifest,
                axis=args.axis,
                selection=args.selection,
            )
            print(path_ref)
        else:
            print(_run_case(args.case, manifest))
    except ContractError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

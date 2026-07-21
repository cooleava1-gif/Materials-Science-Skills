"""Snapshot and finalize per-skill Phase 3 evidence records."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SKILLS_ROOT = Path(__file__).resolve().parent.parent / "skills"


def _within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def snapshot_skill(skill: str, skills_root: Path = DEFAULT_SKILLS_ROOT) -> dict[str, Any]:
    skill_dir = (Path(skills_root) / skill).resolve()
    package_root = skill_dir.parent.parent.resolve()
    manifest_path = skill_dir / "manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    requested = [skill_dir / "SKILL.md", manifest_path]
    always_load = manifest.get("always_load", [])
    if isinstance(always_load, list):
        requested.extend(skill_dir / str(path) for path in always_load)
    files: list[dict[str, Any]] = []
    seen: set[Path] = set()
    for path in requested:
        resolved = path.resolve()
        if resolved in seen or not _within(resolved, package_root) or not resolved.is_file():
            continue
        seen.add(resolved)
        data = resolved.read_bytes()
        role = "skill" if resolved.name == "SKILL.md" else "manifest" if resolved.name == "manifest.yaml" else "always_load"
        files.append(
            {
                "path": resolved.relative_to(REPO_ROOT).as_posix(),
                "role": role,
                "bytes": len(data),
                "lines": len(data.decode("utf-8").splitlines()),
                "sha256": hashlib.sha256(data).hexdigest(),
            }
        )
    skill_file = next(item for item in files if item["role"] == "skill")
    manifest_file = next(item for item in files if item["role"] == "manifest")
    return {
        "skill": skill,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "files": files,
        "skill_bytes": skill_file["bytes"],
        "manifest_bytes": manifest_file["bytes"],
        "always_load_bytes_unique": sum(item["bytes"] for item in files if item["role"] == "always_load"),
        "default_activation_bytes": sum(item["bytes"] for item in files),
    }


def write_snapshot(skill: str, output: Path, skills_root: Path = DEFAULT_SKILLS_ROOT) -> dict[str, Any]:
    snapshot = snapshot_skill(skill, skills_root)
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return snapshot


def finalize_record(
    *,
    skill: str,
    before_path: Path,
    output: Path,
    skills_root: Path = DEFAULT_SKILLS_ROOT,
    status: str,
    decision: str,
    reason: str,
    a_status: str,
    b_status: str,
    c_status: str,
    modifications: list[str],
    verification: list[str],
    notes: list[str],
) -> dict[str, Any]:
    before = json.loads(Path(before_path).read_text(encoding="utf-8"))
    after = snapshot_skill(skill, skills_root)
    record = {
        "version": 1,
        "skill": skill,
        "status": status,
        "decision": decision,
        "reason": reason,
        "modifications": modifications,
        "verification": verification,
        "notes": notes,
        "behavior": {"A_current": a_status, "B_no_skill": b_status, "C_candidate": c_status},
        "before": before,
        "after": after,
        "delta": {
            "default_activation_bytes": after["default_activation_bytes"] - before["default_activation_bytes"],
            "skill_bytes": after["skill_bytes"] - before["skill_bytes"],
            "manifest_bytes": after["manifest_bytes"] - before["manifest_bytes"],
        },
        "recorded_at": datetime.now(timezone.utc).isoformat(),
    }
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return record


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True)
    parser.add_argument("--skills-root", type=Path, default=DEFAULT_SKILLS_ROOT)
    parser.add_argument("--phase", choices=("snapshot", "finalize"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--before", type=Path)
    parser.add_argument("--status", default="complete")
    parser.add_argument("--decision", default="retain")
    parser.add_argument("--reason", default="")
    parser.add_argument("--a-status", default="blocked_auth")
    parser.add_argument("--b-status", default="blocked_auth")
    parser.add_argument("--c-status", default="not_run")
    parser.add_argument("--modification", action="append", default=[])
    parser.add_argument("--verification", action="append", default=[])
    parser.add_argument("--note", action="append", default=[])
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.phase == "snapshot":
        write_snapshot(args.skill, args.output, args.skills_root)
        return 0
    if not args.before:
        raise SystemExit("--before is required for finalize")
    finalize_record(
        skill=args.skill,
        before_path=args.before,
        output=args.output,
        skills_root=args.skills_root,
        status=args.status,
        decision=args.decision,
        reason=args.reason,
        a_status=args.a_status,
        b_status=args.b_status,
        c_status=args.c_status,
        modifications=args.modification,
        verification=args.verification,
        notes=args.note,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

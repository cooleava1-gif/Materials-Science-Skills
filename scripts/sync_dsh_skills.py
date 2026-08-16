#!/usr/bin/env python3
"""Sync the materials skills into a deepseek-harness (dsh) skills root.

dsh discovers skills one level deep at ``<root>/<name>/SKILL.md``; the
materials bundle already matches that layout. This script mirrors the plugin
skills tree (``materials-*`` plus ``_shared``) into the target root, removing
stale skill directories first so old files do not survive an update — the
same contract as ``scripts/install.ps1`` for the Codex manual install.

Default target: ``<repo>/.dsh/skills`` (project scope, dsh rank 100).
Use ``--user`` for ``<dshHome>/skills`` (user scope, rank 400) or
``--target <path>`` for any explicit root.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_SKILLS = REPO_ROOT / "plugins" / "materials-skills" / "skills"
DEFAULT_PROJECT_TARGET = REPO_ROOT / ".dsh" / "skills"


def _dsh_home() -> Path:
    env = os.environ.get("DSH_HOME")
    if env:
        return Path(env)
    return Path.home() / ".dsh"


def resolve_target(args: argparse.Namespace) -> Path:
    if args.target:
        return Path(args.target).expanduser()
    if args.user:
        return _dsh_home() / "skills"
    return DEFAULT_PROJECT_TARGET


def _inside(target: Path, root: Path) -> bool:
    try:
        target.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def remove_stale(source_root: Path, target_root: Path) -> None:
    for child in target_root.iterdir() if target_root.is_dir() else []:
        if not child.is_dir():
            continue
        if not _inside(child, target_root):
            print(f"refusing to remove outside target root: {child}")
            continue
        if not (source_root / child.name).is_dir():
            shutil.rmtree(child, ignore_errors=True)
            print(f"removed stale skill: {child.name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", action="store_true", help="Sync to <dshHome>/skills instead of the project root")
    parser.add_argument("--target", help="Explicit target skills root (overrides --user)")
    parser.add_argument("--dry-run", action="store_true", help="Report what would change without writing")
    args = parser.parse_args()

    if not SOURCE_SKILLS.is_dir():
        print(f"source skills directory not found: {SOURCE_SKILLS}", file=sys.stderr)
        return 1

    entries = sorted(
        path
        for path in SOURCE_SKILLS.iterdir()
        if path.is_dir() and (path.name == "_shared" or path.name.startswith("materials-"))
    )
    if not entries:
        print(f"no materials-* skill directories found in: {SOURCE_SKILLS}", file=sys.stderr)
        return 1

    target = resolve_target(args)
    print(f"source: {SOURCE_SKILLS}")
    print(f"target: {target}")
    if args.dry_run:
        print(f"would sync {len(entries)} directories")
        for entry in entries:
            print(f"  {entry.name}")
        return 0

    target.mkdir(parents=True, exist_ok=True)
    remove_stale(SOURCE_SKILLS, target)
    for entry in entries:
        destination = target / entry.name
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(entry, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        print(f"synced {entry.name}")

    print(f"synced {len(entries)} directories into {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

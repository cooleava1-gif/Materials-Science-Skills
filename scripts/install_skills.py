#!/usr/bin/env python3
"""Cross-platform installer for the Materials Science Skills bundle.

Single canonical source: ``plugins/materials-skills/skills/``.

Targets
-------
claude       personal skills   -> ~/.claude/skills/
opencode     global skills     -> ~/.config/opencode/skills/
antigravity  global skills     -> ~/.gemini/config/skills/
codex        Codex home        -> $CODEX_HOME/skills/ (+ $CODEX_HOME/_shared)
generic      --dest directory  -> self-contained copy anywhere

Self-containment (materialization)
----------------------------------
In the canonical source, skills reference shared content with relative paths:
``_shared/...`` (skill-local), ``../_shared/...`` (skill-level shared dir) and
``../../_shared/...`` (plugin-level shared dir; the Codex layout keeps both
``skills/_shared`` and ``plugins/materials-skills/_shared`` as siblings).
OpenCode / Claude personal / Antigravity do not guarantee cross-directory
reads, so for every non-codex target each skill is *materialized*: both shared
trees are merged into ``<skill>/_shared/`` and every ``(../)+_shared/...``
reference is rewritten to ``_shared/...``. The Codex-only ``agents/`` dir is
dropped for non-codex targets.

MCP
---
The ``materials-academic-search`` server (Python stdio, shipped inside
``materials-citation``) is registered per platform with an absolute path:
claude  -> merge into ``--mcp-dest`` (default ``<cwd>/.mcp.json``, mcpServers)
opencode-> merge into ``~/.config/opencode/opencode.json`` (mcp field)
codex   -> merge into ``--mcp-dest`` (default ``<cwd>/.mcp.json``, mcpServers)
antigravity/generic -> informational only (mechanism not yet standardized)
Pass ``--no-mcp`` to skip MCP registration entirely.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SKILL_PREFIX = "materials-"
PLUGIN_REL = Path("plugins") / "materials-skills"

# Entry files/dirs inside the shared trees that must NOT be merged into each
# skill's materialized `_shared/` (they are skill entry points, not content).
SHARED_ENTRY_FILES = {"SKILL.md", "README.md"}
SHARED_ENTRY_DIRS = {"agents"}

TEXT_SUFFIXES = {".md", ".yaml", ".yml", ".txt"}
REF_RE = re.compile(r"(?:\.\./)+_shared/")
# References inside a materialized shared tree (files under <skill>/_shared/)
# that still point at the canonical layout (e.g. `_shared/core/x`,
# `../../_shared/x`, `../../skills/_shared/x`) are rewritten relative to the
# merged shared root: files live one level deep, so the root is `../`.
SHARED_TREE_REF_RE = re.compile(r"(?:\.\./)*(?:skills/)?_shared/")
REF_SCAN_RE = re.compile(r"(?:\.\./)*_shared/([^\s`\"'(),;\]\}\)>]+)")

# Precise string fixes applied to Python scripts inside a materialized skill.
# The canonical layout resolves shared content via a *sibling* `_shared` dir
# (e.g. `SKILL_ROOT.parent / "_shared"`), which does not exist after
# materialization; the merged shared tree lives at `<skill>/_shared`.
PY_REF_FIXES = (
    ('SKILL_ROOT.parent / "_shared"', 'SKILL_ROOT / "_shared"'),
    ('DOE_ROOT.parent / "_shared"', 'DOE_ROOT / "_shared"'),
    ('SKILL_DIR.parents[1] / "_shared"', 'SKILL_DIR / "_shared"'),
    ('PLUGIN_ROOT / "_shared" / "journal-templates"',
     'Path(__file__).resolve().parents[1] / "_shared" / "journal-templates"'),
    ('parents[3] / "_shared" / "journal-templates"',
     'parents[1] / "_shared" / "journal-templates"'),
)

MCP_NAME = "materials-academic-search"
MCP_SERVER_REL = (
    Path("skills") / "materials-citation" / "mcp" / "academic_search" / "server.py"
)


def default_target_dir(target: str) -> Path:
    home = Path.home()
    if target == "claude":
        return home / ".claude" / "skills"
    if target == "opencode":
        return home / ".config" / "opencode" / "skills"
    if target == "antigravity":
        return home / ".gemini" / "config" / "skills"
    if target == "codex":
        base = Path(os.environ.get("CODEX_HOME", str(home / ".codex")))
        return base / "skills"
    raise ValueError(f"{target} has no default target dir; pass --dest")


# ---------------------------------------------------------------------------
# Shared-tree helpers
# ---------------------------------------------------------------------------


def locate_shared_sources(repo_root: Path) -> tuple[Path, list[Path]]:
    """Return (skills_root, [skill-level shared, plugin-level shared])."""
    skills_root = repo_root / PLUGIN_REL / "skills"
    skill_shared = skills_root / "_shared"
    package_shared = repo_root / PLUGIN_REL / "_shared"
    for p in (skills_root, skill_shared, package_shared):
        if not p.is_dir():
            raise FileNotFoundError(f"Required source directory missing: {p}")
    return skills_root, [skill_shared, package_shared]


def copy_tree(src: Path, dst: Path, exclude: set[str] | None = None) -> None:
    """Copy a directory tree, skipping top-level entries in ``exclude``."""
    dst.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if exclude and item.name in exclude:
            continue
        target = dst / item.name
        if target.exists():
            if target.is_dir() and not target.is_symlink():
                shutil.rmtree(target)
            else:
                target.unlink()
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def merge_shared_into(skill_dst: Path, shared_sources: list[Path]) -> None:
    """Merge both shared trees into ``<skill>/_shared/`` (no entry files)."""
    dst_shared = skill_dst / "_shared"
    dst_shared.mkdir(parents=True, exist_ok=True)
    for src in shared_sources:
        for item in src.iterdir():
            if item.name in SHARED_ENTRY_FILES or item.name in SHARED_ENTRY_DIRS:
                continue
            target = dst_shared / item.name
            if target.exists():
                if target.is_dir() and not target.is_symlink():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            if item.is_dir():
                shutil.copytree(item, target)
            else:
                shutil.copy2(item, target)


def rewrite_shared_refs(root: Path) -> int:
    """Rewrite shared-content references so every skill is self-contained.

    - Files outside ``<root>/_shared/``: ``(../)+_shared/X`` -> ``_shared/X``
      (relative to the skill root).
    - Files inside ``<root>/_shared/``: any ``(../)*(skills/)?_shared/X``
      form (including bare ``_shared/X`` conventions and ``../../skills/``
      escapes) -> ``../X`` (relative to the merged shared root).
    """
    changed = 0
    for f in root.rglob("*"):
        if not f.is_file() or f.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        in_shared_tree = f.relative_to(root).parts[0] == "_shared"
        pattern = SHARED_TREE_REF_RE if in_shared_tree else REF_RE
        new_text = pattern.sub("../" if in_shared_tree else "_shared/", text)
        if new_text != text:
            f.write_text(new_text, encoding="utf-8")
            changed += 1
    return changed


def _ref_resolves(f: Path, root: Path, rel: str) -> bool:
    """Multi-basis resolution for a shared reference.

    a) literal path relative to the referencing file;
    b) convention ``_shared/X`` relative to the skill root
       (``<skill>/_shared/X``), after stripping ``../`` prefixes;
    c) same as (b) but relative to the merged shared root
       (``<skill>/_shared/X``).
    """
    if (f.parent / rel).exists():
        return True
    base = rel
    while base.startswith("../"):
        base = base[3:]
    if base.startswith("_shared/"):
        if (root / base).exists():
            return True
        if (root / "_shared" / base[len("_shared/"):]).exists():
            return True
    return False


def verify_materialized_refs(root: Path) -> list[str]:
    """Every shared-content reference must resolve inside ``root``.

    Returns a list of human-readable problems (empty == OK).
    """
    problems: list[str] = []
    for f in sorted(root.rglob("*")):
        if not f.is_file() or f.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for m in REF_SCAN_RE.finditer(text):
            rel = m.group(0).rstrip(".")
            if "#" in rel:
                rel = rel.split("#", 1)[0]
            if not rel:
                continue
            # template placeholders such as `<journal>.yaml` are not literal
            # paths and cannot be validated against the filesystem
            if "<" in rel or ">" in rel:
                continue
            if not _ref_resolves(f, root, rel):
                problems.append(f"{f.relative_to(root)} -> {rel}")
    return problems


def fix_py_shared_refs(root: Path) -> int:
    """Apply PY_REF_FIXES to Python scripts under root (string replaces only)."""
    changed = 0
    for f in root.rglob("*.py"):
        if not f.is_file():
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        new = text
        for old, rep in PY_REF_FIXES:
            new = new.replace(old, rep)
        if new != text:
            f.write_text(new, encoding="utf-8")
            changed += 1
    return changed


def materialize_skill(src_skill: Path, dst_skill: Path, shared_sources: list[Path]) -> int:
    """Install one skill as a self-contained copy. Returns changed-file count."""
    copy_tree(src_skill, dst_skill, exclude={"agents"})
    merge_shared_into(dst_skill, shared_sources)
    return rewrite_shared_refs(dst_skill) + fix_py_shared_refs(dst_skill)


# ---------------------------------------------------------------------------
# MCP registration
# ---------------------------------------------------------------------------


def mcp_entry(repo_root: Path) -> dict:
    """Absolute-path server entry shared by claude/codex (.mcp.json style)."""
    server = repo_root / PLUGIN_REL / MCP_SERVER_REL
    return {
        MCP_NAME: {
            "command": "python",
            "args": [str(server.resolve())],
            "cwd": str(server.resolve().parent),
        }
    }


def _load_json_safe(path: Path) -> tuple[dict | None, str | None]:
    """Load JSON, tolerating missing file. Returns (data, error_message).

    Config files such as opencode.json may be JSONC (comments / trailing
    commas); if parsing fails we refuse to overwrite the user's file.
    """
    if not path.exists():
        return {}, None
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except (json.JSONDecodeError, OSError, UnicodeDecodeError) as exc:
        return None, f"cannot parse {path} ({exc}); skipping merge to avoid overwriting user config"


def merge_into_mcp_json(path: Path, entry: dict, dry_run: bool) -> list[str]:
    """Merge ``{mcpServers: entry}`` into an existing/new .mcp.json."""
    data, err = _load_json_safe(path)
    if err is not None:
        return [f"mcp: WARNING {err}"]
    servers = data.setdefault("mcpServers", {})
    overwritten = MCP_NAME in servers
    servers.update(entry)
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    note = "; replacing existing entry" if overwritten else ""
    return [f"mcp: merge {MCP_NAME} into {path}{note}"]


def merge_into_opencode_config(path: Path, entry: dict, dry_run: bool) -> list[str]:
    """Merge ``{mcp: entry}`` into opencode.json (OpenCode ``mcp`` field)."""
    data, err = _load_json_safe(path)
    if err is not None:
        return [f"mcp: WARNING {err}"]
    mcp = data.setdefault("mcp", {})
    overwritten = MCP_NAME in mcp
    mcp.update({name: {"type": "local", "command": ["python", *cfg["args"]],
                       "environment": {}, "enabled": True}
                for name, cfg in entry.items()})
    if not dry_run:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    note = "; replacing existing entry" if overwritten else ""
    return [f"mcp: merge {MCP_NAME} into {path}{note}"]


def register_mcp(target: str, repo_root: Path, mcp_dest: Path | None,
                 dry_run: bool) -> list[str]:
    """Register the MCP server for the given target. Returns action log."""
    if target == "antigravity" or target == "generic":
        return [
            "mcp: skipped for antigravity/generic (no standardized global config); "
            "register the server manually, see adapters/README.md"
        ]
    entry = mcp_entry(repo_root)
    if target == "opencode":
        path = mcp_dest or (Path.home() / ".config" / "opencode" / "opencode.json")
        return merge_into_opencode_config(path, entry, dry_run)
    path = mcp_dest or (Path.cwd() / ".mcp.json")
    return merge_into_mcp_json(path, entry, dry_run)


# ---------------------------------------------------------------------------
# Installers
# ---------------------------------------------------------------------------


def install_self_contained(target: str, repo_root: Path, dest: Path,
                           force: bool, dry_run: bool) -> tuple[list[str], list[str]]:
    """Install all skills as self-contained materialized copies."""
    skills_root, shared_sources = locate_shared_sources(repo_root)
    actions: list[str] = []
    problems: list[str] = []
    if not dry_run:
        dest.mkdir(parents=True, exist_ok=True)
    for skill_dir in sorted(skills_root.iterdir()):
        if not (skill_dir.is_dir() and skill_dir.name.startswith(SKILL_PREFIX)):
            continue
        dst = dest / skill_dir.name
        if dst.exists():
            if not force:
                actions.append(f"skip (exists, use --force to replace): {dst}")
                continue
            shutil.rmtree(dst)
        actions.append(f"materialize {skill_dir.name} -> {dst}")
        if not dry_run:
            materialize_skill(skill_dir, dst, shared_sources)
            problems.extend(
                f"{skill_dir.name}: {p}" for p in verify_materialized_refs(dst)
            )
    return actions, problems


def install_codex(repo_root: Path, dest: Path, force: bool,
                  dry_run: bool) -> tuple[list[str], list[str]]:
    """Codex layout: skills/_shared and plugin _shared stay as siblings."""
    skills_root, shared_sources = locate_shared_sources(repo_root)
    actions: list[str] = []
    problems: list[str] = []
    if not dry_run:
        dest.mkdir(parents=True, exist_ok=True)
    for skill_dir in sorted(skills_root.iterdir()):
        if not (skill_dir.is_dir() and skill_dir.name.startswith(SKILL_PREFIX)):
            continue
        dst = dest / skill_dir.name
        if dst.exists() and not force:
            actions.append(f"skip (exists, use --force to replace): {dst}")
            continue
        actions.append(f"copy {skill_dir.name} -> {dst}")
        if not dry_run:
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(skill_dir, dst)
    # skill-level _shared -> dest/_shared (sibling of the skills)
    dst_shared = dest / "_shared"
    if dst_shared.exists() and not force:
        actions.append(f"skip skills/_shared (exists, use --force to replace): {dst_shared}")
    else:
        actions.append(f"copy skills/_shared -> {dst_shared}")
        if not dry_run:
            if dst_shared.exists():
                shutil.rmtree(dst_shared)
            shutil.copytree(shared_sources[0], dst_shared)
    # plugin-level _shared -> parent(dest)/_shared
    # Only valid when dest is the platform "skills" directory directly under
    # the Codex home (e.g. $CODEX_HOME/skills); otherwise the parent could be
    # an arbitrary user directory and --force would delete an unrelated
    # `_shared` there.
    pkg_shared = shared_sources[1]
    dst_pkg = dest.parent / "_shared"
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))).resolve()
    if dest.resolve().parent != codex_home:
        actions.append(
            f"skip plugin-level _shared: dest is not <CODEX_HOME>/skills "
            f"(would touch {dst_pkg}); reference it manually or install to "
            f"<CODEX_HOME>/skills"
        )
    elif dst_pkg.exists() and not force:
        actions.append(f"skip plugin _shared (exists, use --force to replace): {dst_pkg}")
    else:
        actions.append(f"copy plugin _shared -> {dst_pkg}")
        if not dry_run:
            if dst_pkg.exists():
                shutil.rmtree(dst_pkg)
            shutil.copytree(pkg_shared, dst_pkg)
    return actions, problems


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Install the Materials Science Skills bundle for any agent.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    p.add_argument("--target", required=True,
                   choices=["claude", "opencode", "antigravity", "codex", "generic"],
                   help="Agent platform to install for.")
    p.add_argument("--dest", type=Path, default=None,
                   help="Install destination (overrides the platform default).")
    p.add_argument("--mcp-dest", type=Path, default=None,
                   help="MCP config file to write (claude/codex: .mcp.json; "
                        "opencode: opencode.json).")
    p.add_argument("--no-mcp", action="store_true",
                   help="Skip MCP registration.")
    p.add_argument("--force", action="store_true",
                   help="Replace existing skill directories.")
    p.add_argument("--dry-run", action="store_true",
                   help="Print the plan without changing anything.")
    p.add_argument("--repo-root", type=Path, default=None,
                   help="Path to the repository root (default: repo of this script).")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    repo_root = (args.repo_root or Path(__file__).resolve().parent.parent).resolve()
    dest = args.dest or default_target_dir(args.target)
    dest = dest.expanduser().resolve()

    print(f"target : {args.target}")
    print(f"source : {repo_root}")
    print(f"dest   : {dest}")
    if args.dry_run:
        print("mode   : dry-run (no changes)")

    if args.target == "codex":
        actions, problems = install_codex(repo_root, dest, args.force, args.dry_run)
    else:
        actions, problems = install_self_contained(
            args.target, repo_root, dest, args.force, args.dry_run
        )

    for a in actions:
        print("  -", a)

    if not args.no_mcp:
        for a in register_mcp(args.target, repo_root, args.mcp_dest, args.dry_run):
            print("  -", a)

    if problems:
        print("\nREFERENCE INTEGRITY PROBLEMS:")
        for p in problems:
            print("  -", p)
        return 1
    if actions and not args.dry_run:
        print("\nInstall OK. Restart/reload your agent to pick up the skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

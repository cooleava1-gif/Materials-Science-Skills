#!/usr/bin/env python3
"""Cross-host packaging validation for the materials-skills plugin.

Checks the Claude Code plugin manifest, the repository marketplace entry, and
the SKILL.md frontmatter compatibility envelope shared by Claude Code and
ZCode. The Codex packaging itself remains covered by the other gate checks.

Paths are validated statically: every declared path must resolve inside the
repository tree, and MCP arguments using ``$CLAUDE_PLUGIN_ROOT`` must point at
files that exist relative to the plugin root.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = PLUGIN_ROOT.parent.parent
SKILLS_ROOT = PLUGIN_ROOT / "skills"

HOST_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}$")
MAX_DESCRIPTION_CHARS = 1024
MIN_BUNDLE_SKILLS = 14


def _read_json(path: Path) -> tuple[object, str | None]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except OSError as exc:
        return None, f"{path.relative_to(REPO_ROOT)}: unreadable: {exc}"
    except json.JSONDecodeError as exc:
        return None, f"{path.relative_to(REPO_ROOT)}: invalid JSON: {exc}"


def _manifest_of(plugin_dir: Path) -> Path | None:
    for name in (".claude-plugin", ".codex-plugin", ".zcode-plugin"):
        candidate = plugin_dir / name / "plugin.json"
        if candidate.exists():
            return candidate
    return None


def collect_claude_manifest_issues() -> list[str]:
    manifest_path = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"
    if not manifest_path.exists():
        return [f"missing {manifest_path.relative_to(REPO_ROOT)}"]

    manifest, error = _read_json(manifest_path)
    if error is not None:
        return [error]
    if not isinstance(manifest, dict):
        return [f"{manifest_path.relative_to(REPO_ROOT)}: manifest must be a JSON object"]

    issues: list[str] = []

    for field in ("name", "version", "description"):
        value = manifest.get(field)
        if not isinstance(value, str) or not value.strip():
            issues.append(f"claude plugin.json: missing or empty {field!r}")

    name = manifest.get("name")
    if isinstance(name, str) and not HOST_NAME_RE.match(name):
        issues.append(f"claude plugin.json: name {name!r} violates host name pattern")

    skills = manifest.get("skills")
    if isinstance(skills, str):
        skills_paths = [skills]
    elif isinstance(skills, list) and all(isinstance(p, str) for p in skills):
        skills_paths = skills
    else:
        skills_paths = []
        issues.append("claude plugin.json: 'skills' must be a path string or array of path strings")

    for rel_path in skills_paths:
        target = (PLUGIN_ROOT / rel_path).resolve()
        try:
            target.relative_to(PLUGIN_ROOT)
        except ValueError:
            issues.append(f"claude plugin.json: skills path escapes plugin root: {rel_path}")
            continue
        if not target.is_dir():
            issues.append(f"claude plugin.json: skills path not found: {rel_path}")
            continue
        skill_dirs = [
            child
            for child in target.glob("materials-*")
            if child.is_dir() and (child / "SKILL.md").exists()
        ]
        if len(skill_dirs) < MIN_BUNDLE_SKILLS:
            issues.append(
                f"claude plugin.json: skills path {rel_path} exposes "
                f"{len(skill_dirs)} materials skills, expected at least {MIN_BUNDLE_SKILLS}"
            )

    mcp_servers = manifest.get("mcpServers")
    if mcp_servers is not None:
        if not isinstance(mcp_servers, dict):
            issues.append("claude plugin.json: 'mcpServers' must be an object")
        else:
            for server_name, server in mcp_servers.items():
                if not isinstance(server, dict) or not isinstance(server.get("command"), str):
                    issues.append(f"claude plugin.json: mcp server {server_name!r} missing 'command'")
                    continue
                for arg in server.get("args", []) or []:
                    if not isinstance(arg, str):
                        continue
                    if "$CLAUDE_PLUGIN_ROOT" not in arg:
                        continue
                    remainder = arg.split("$CLAUDE_PLUGIN_ROOT", 1)[1]
                    target = (PLUGIN_ROOT / remainder.lstrip("/\\")).resolve()
                    if not target.exists():
                        issues.append(
                            f"claude plugin.json: MCP arg path not found relative to "
                            f"plugin root: {arg}"
                        )
    return issues


def collect_marketplace_issues() -> list[str]:
    """Validate the marketplace entries every host reads.

    Claude Code expects ``.claude-plugin/marketplace.json`` at the repository
    root; ZCode expects a root ``marketplace.json``. Both files are shipped
    and must carry identical content.
    """
    paths = [REPO_ROOT / "marketplace.json", REPO_ROOT / ".claude-plugin" / "marketplace.json"]
    payloads: list[object | None] = []
    for marketplace_path in paths:
        if not marketplace_path.exists():
            return [f"missing {marketplace_path.relative_to(REPO_ROOT)}"]
        marketplace, error = _read_json(marketplace_path)
        if error is not None:
            return [error]
        if not isinstance(marketplace, dict):
            return [f"{marketplace_path.relative_to(REPO_ROOT)}: must be a JSON object"]
        payloads.append(marketplace)

    if payloads[0] != payloads[1]:
        return ["marketplace.json and .claude-plugin/marketplace.json differ; keep them identical"]

    marketplace = payloads[0]
    issues: list[str] = []
    if not isinstance(marketplace.get("name"), str) or not marketplace["name"].strip():
        issues.append("marketplace.json: missing or empty 'name'")

    plugins = marketplace.get("plugins")
    if not isinstance(plugins, list) or not plugins:
        issues.append("marketplace.json: 'plugins' must be a non-empty array")
        return issues

    for index, plugin in enumerate(plugins):
        if not isinstance(plugin, dict):
            issues.append(f"marketplace.json: plugins[{index}] must be an object")
            continue
        plugin_name = plugin.get("name")
        if not isinstance(plugin_name, str) or not HOST_NAME_RE.match(plugin_name):
            issues.append(f"marketplace.json: plugins[{index}] has invalid name")
        source = plugin.get("source")
        if isinstance(source, str):
            target = (REPO_ROOT / source).resolve()
            try:
                target.relative_to(REPO_ROOT)
            except ValueError:
                issues.append(f"marketplace.json: plugins[{index}] source escapes repo: {source}")
                continue
            if not target.is_dir():
                issues.append(f"marketplace.json: plugins[{index}] source not found: {source}")
                continue
            if _manifest_of(target) is None:
                issues.append(
                    f"marketplace.json: plugins[{index}] source has no recognized plugin manifest: {source}"
                )
        elif isinstance(source, dict):
            if not isinstance(source.get("source"), str):
                issues.append(f"marketplace.json: plugins[{index}] source object missing 'source' kind")
        else:
            issues.append(f"marketplace.json: plugins[{index}] source must be a path string or object")
    return issues


def collect_zcode_manifest_issues() -> list[str]:
    """ZCode probes .zcode-plugin first, so this manifest must stand alone.

    ZCode drops MCP servers with unknown keys (strict schema), so the check
    also pins the allowed stdio fields.
    """
    manifest_path = PLUGIN_ROOT / ".zcode-plugin" / "plugin.json"
    if not manifest_path.exists():
        return [f"missing {manifest_path.relative_to(REPO_ROOT)}"]

    manifest, error = _read_json(manifest_path)
    if error is not None:
        return [error]
    if not isinstance(manifest, dict):
        return [f"{manifest_path.relative_to(REPO_ROOT)}: manifest must be a JSON object"]

    issues: list[str] = []
    name = manifest.get("name")
    if not isinstance(name, str) or not HOST_NAME_RE.match(name):
        issues.append(f"zcode plugin.json: name {name!r} violates host name pattern")

    skills = manifest.get("skills")
    if isinstance(skills, str):
        target = (PLUGIN_ROOT / skills).resolve()
        if not target.is_dir():
            issues.append(f"zcode plugin.json: skills path not found: {skills}")
    elif skills is not None:
        issues.append("zcode plugin.json: 'skills' must be a directory path string")

    allowed_stdio_keys = {"command", "args", "cwd", "env", "enabled", "timeoutMs", "type"}
    mcp_servers = manifest.get("mcpServers")
    if mcp_servers is None:
        return issues
    if not isinstance(mcp_servers, dict):
        issues.append("zcode plugin.json: 'mcpServers' must be an object")
        return issues
    for server_name, server in mcp_servers.items():
        if not isinstance(server, dict):
            issues.append(f"zcode plugin.json: mcp server {server_name!r} must be an object")
            continue
        unknown_keys = set(server) - allowed_stdio_keys
        if unknown_keys:
            issues.append(
                f"zcode plugin.json: mcp server {server_name!r} has unknown keys "
                f"that ZCode drops: {sorted(unknown_keys)}"
            )
        if not isinstance(server.get("command"), str):
            issues.append(f"zcode plugin.json: mcp server {server_name!r} missing 'command'")
        for arg in server.get("args", []) or []:
            if not isinstance(arg, str):
                continue
            if "${ZCODE_PLUGIN_ROOT}" not in arg:
                continue
            remainder = arg.split("${ZCODE_PLUGIN_ROOT}", 1)[1]
            target = (PLUGIN_ROOT / remainder.lstrip("/\\")).resolve()
            if not target.exists():
                issues.append(
                    f"zcode plugin.json: MCP arg path not found relative to "
                    f"plugin root: {arg}"
                )
    return issues


def collect_dsh_compat_issues() -> list[str]:
    """deepseek-harness compatibility checks.

    dsh requires kebab-case frontmatter names and honours
    ``disable-model-invocation`` / ``user-invocable`` policies; the shared
    support skill must stay hidden from both surfaces. The sync script and
    the zero-copy patch overlay must exist for installation.
    """
    issues: list[str] = []
    kebab_re = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
    for skill_md in sorted(SKILLS_ROOT.glob("*/SKILL.md")):
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        try:
            frontmatter = yaml.safe_load(parts[1]) or {}
        except yaml.YAMLError:
            continue
        if not isinstance(frontmatter, dict):
            continue
        name = frontmatter.get("name")
        rel = skill_md.relative_to(PLUGIN_ROOT)
        if isinstance(name, str) and not kebab_re.match(name):
            issues.append(f"{rel}: dsh requires kebab-case name, got {name!r}")

    shared_md = SKILLS_ROOT / "_shared" / "SKILL.md"
    if shared_md.exists():
        text = shared_md.read_text(encoding="utf-8", errors="replace")
        parts = text.split("---", 2) if text.startswith("---") else []
        if len(parts) >= 3:
            try:
                shared_fm = yaml.safe_load(parts[1]) or {}
            except yaml.YAMLError:
                shared_fm = {}
            if isinstance(shared_fm, dict) and (
                shared_fm.get("disable-model-invocation") is not True
                or shared_fm.get("user-invocable") is not False
            ):
                issues.append(
                    "skills/_shared/SKILL.md: dsh requires "
                    "disable-model-invocation: true and user-invocable: false"
                )

    sync_script = REPO_ROOT / "scripts" / "sync_dsh_skills.py"
    if not sync_script.exists():
        issues.append(f"missing {sync_script.relative_to(REPO_ROOT)}")

    patch_overlay = REPO_ROOT / "dsh" / "cordis.patch.yml"
    if not patch_overlay.exists():
        issues.append(f"missing {patch_overlay.relative_to(REPO_ROOT)}")
    else:
        try:
            overlay = yaml.safe_load(patch_overlay.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            issues.append(f"{patch_overlay.relative_to(REPO_ROOT)}: YAML error: {exc}")
            overlay = None
        if overlay is not None and not isinstance(overlay, list):
            issues.append(f"{patch_overlay.relative_to(REPO_ROOT)}: overlay must be a YAML list")
    return issues


def collect_frontmatter_compat_issues() -> list[str]:
    issues: list[str] = []
    for skill_md in sorted(SKILLS_ROOT.glob("**/SKILL.md")):
        text = skill_md.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            issues.append(f"{skill_md.relative_to(PLUGIN_ROOT)}: missing YAML frontmatter")
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            issues.append(f"{skill_md.relative_to(PLUGIN_ROOT)}: unterminated frontmatter")
            continue
        try:
            frontmatter = yaml.safe_load(parts[1]) or {}
        except yaml.YAMLError as exc:
            issues.append(f"{skill_md.relative_to(PLUGIN_ROOT)}: frontmatter YAML error: {exc}")
            continue
        if not isinstance(frontmatter, dict):
            issues.append(f"{skill_md.relative_to(PLUGIN_ROOT)}: frontmatter is not a mapping")
            continue
        name = frontmatter.get("name")
        description = frontmatter.get("description")
        rel = skill_md.relative_to(PLUGIN_ROOT)
        if not isinstance(name, str) or not name.strip():
            issues.append(f"{rel}: missing 'name' in frontmatter")
        elif not HOST_NAME_RE.match(name):
            issues.append(f"{rel}: name {name!r} violates host name pattern")
        if not isinstance(description, str) or not description.strip():
            issues.append(f"{rel}: missing 'description' in frontmatter")
        elif len(description) > MAX_DESCRIPTION_CHARS:
            issues.append(
                f"{rel}: description is {len(description)} chars, "
                f"over the {MAX_DESCRIPTION_CHARS}-char host limit"
            )
    return issues


def validate_host_packaging() -> dict[str, list[str]]:
    """Return issues keyed by check name; empty lists mean a clean check."""
    return {
        "claude_plugin_manifest": collect_claude_manifest_issues(),
        "zcode_plugin_manifest": collect_zcode_manifest_issues(),
        "marketplace": collect_marketplace_issues(),
        "skill_frontmatter_compat": collect_frontmatter_compat_issues(),
        "dsh_compat": collect_dsh_compat_issues(),
    }


def main() -> int:
    report = validate_host_packaging()
    total = sum(len(issues) for issues in report.values())
    print(json.dumps({"status": "pass" if total == 0 else "fail", "issues": report}, indent=2))
    return 0 if total == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

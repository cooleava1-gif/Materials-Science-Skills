"""Tests for the cross-platform installer (scripts/install_skills.py)."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

import install_skills as inst  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def short_tmp():
    """A short-path temp dir: pytest's tmp_path is too deep on Windows and
    overflows MAX_PATH once the bundle's long example paths are appended."""
    base = Path(tempfile.gettempdir()) / f"msskills-t-{os.getpid()}"
    base.mkdir(parents=True, exist_ok=True)
    yield base
    shutil.rmtree(base, ignore_errors=True)


def _count_skills() -> int:
    skills_root, _ = inst.locate_shared_sources(REPO_ROOT)
    return sum(1 for d in skills_root.iterdir()
               if d.is_dir() and d.name.startswith(inst.SKILL_PREFIX))


def test_locate_shared_sources_finds_both_trees() -> None:
    skills_root, shared = inst.locate_shared_sources(REPO_ROOT)
    assert skills_root.is_dir()
    assert len(shared) == 2
    assert all(s.is_dir() for s in shared)
    # both trees must merge without top-level name collisions
    names = [s.name for s in shared[0].iterdir()] + [s.name for s in shared[1].iterdir()]
    assert len(names) == len(set(names))


def test_materialize_rewrites_and_resolves(short_tmp: Path) -> None:
    skills_root, shared = inst.locate_shared_sources(REPO_ROOT)
    src = skills_root / "materials-research"
    dst = short_tmp / "materials-research"
    inst.materialize_skill(src, dst, shared)

    # shared content is merged into the skill directory
    assert (dst / "_shared" / "core" / "evidence-contract.md").is_file()
    assert (dst / "_shared" / "contracts").is_dir()  # plugin-level merged too

    # no relative escape references remain
    for f in dst.rglob("*"):
        if not f.is_file() or f.suffix not in inst.TEXT_SUFFIXES:
            continue
        text = f.read_text(encoding="utf-8")
        assert "../../_shared" not in text
        assert "../_shared" not in text

    # every reference resolves inside the materialized skill
    assert inst.verify_materialized_refs(dst) == []

    # Codex-only agents/ dir is dropped for self-contained installs
    assert not (dst / "agents").exists()


def test_all_skills_materialize_cleanly(short_tmp: Path) -> None:
    skills_root, shared = inst.locate_shared_sources(REPO_ROOT)
    problems: list[str] = []
    count = 0
    for skill_dir in sorted(skills_root.iterdir()):
        if not (skill_dir.is_dir() and skill_dir.name.startswith(inst.SKILL_PREFIX)):
            continue
        dst = short_tmp / skill_dir.name
        inst.materialize_skill(skill_dir, dst, shared)
        problems += [f"{skill_dir.name}: {p}"
                     for p in inst.verify_materialized_refs(dst)]
        count += 1
    assert count == _count_skills() >= 14
    assert problems == []


def test_cli_generic_dry_run_makes_no_changes(short_tmp: Path) -> None:
    dest = short_tmp / "skills-out"
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "install_skills.py"),
         "--target", "generic", "--dest", str(dest), "--dry-run",
         "--repo-root", str(REPO_ROOT)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert not dest.exists()


def test_cli_generic_full_install(short_tmp: Path) -> None:
    dest = short_tmp / "skills-out"
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "install_skills.py"),
         "--target", "generic", "--dest", str(dest), "--no-mcp",
         "--repo-root", str(REPO_ROOT)],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    installed = [d for d in dest.iterdir() if d.is_dir()]
    assert len(installed) == _count_skills()
    for skill in installed:
        assert (skill / "SKILL.md").is_file()
        assert (skill / "_shared").is_dir()
        assert inst.verify_materialized_refs(skill) == []


def test_cli_codex_layout(short_tmp: Path) -> None:
    dest = short_tmp / ".codex" / "skills"
    env = {**os.environ, "CODEX_HOME": str(short_tmp / ".codex")}
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "install_skills.py"),
         "--target", "codex", "--dest", str(dest), "--no-mcp",
         "--repo-root", str(REPO_ROOT)],
        capture_output=True, text=True, env=env,
    )
    assert result.returncode == 0, result.stderr
    # sibling shared trees, no materialization
    assert (dest / "_shared").is_dir()
    assert (dest.parent / "_shared").is_dir()
    skill = dest / "materials-research"
    assert (skill / "SKILL.md").is_file()
    assert (skill / "agents" / "openai.yaml").is_file()


def test_py_shared_refs_rewritten_everywhere(short_tmp: Path) -> None:
    """Every known hard-coded Python shared-path pattern must be rewritten and
    point at an existing file inside the materialized skill."""
    skills_root, shared = inst.locate_shared_sources(REPO_ROOT)
    targets = [
        ("materials-data", "scripts/build_fair_package.py",
         'SKILL_ROOT.parent / "_shared"', 'SKILL_ROOT / "_shared"'),
        ("materials-doe", "scripts/doe_plan_to_experiment_record.py",
         'DOE_ROOT.parent / "_shared"', 'DOE_ROOT / "_shared"'),
        ("materials-submission", "scripts/build_submission_package.py",
         'SKILL_DIR.parents[1] / "_shared"', 'SKILL_DIR / "_shared"'),
        ("materials-submission", "scripts/test_template_driven_outputs.py",
         'SKILL_DIR.parents[1] / "_shared"', 'SKILL_DIR / "_shared"'),
        ("materials-submission", "scripts/template_support.py",
         'PLUGIN_ROOT / "_shared" / "journal-templates"',
         'parents[1] / "_shared" / "journal-templates"'),
        ("materials-writing", "scripts/check_manuscript_structure.py",
         'parents[3] / "_shared" / "journal-templates"',
         'parents[1] / "_shared" / "journal-templates"'),
    ]
    for skill_name, rel, old, new in targets:
        dst = short_tmp / skill_name
        inst.materialize_skill(skills_root / skill_name, dst, shared)
        text = (dst / rel).read_text(encoding="utf-8")
        assert old not in text, f"{rel}: {old} not rewritten"
        assert new in text, f"{rel}: {new} missing"


def test_codex_non_skills_dest_skips_parent_shared(short_tmp: Path) -> None:
    """--target codex with a dest outside CODEX_HOME must not touch parent/_shared."""
    dest = short_tmp / "not-skills"
    actions, _ = inst.install_codex(REPO_ROOT, dest, force=True, dry_run=True)
    joined = "\n".join(actions)
    assert "skip plugin-level _shared" in joined
    assert "not <CODEX_HOME>/skills" in joined
    assert not (dest.parent / "_shared").exists()


def test_codex_real_skills_dest_plans_parent_shared(short_tmp: Path) -> None:
    """A dest literally under CODEX_HOME/skills passes the guard (dry-run)."""
    import os
    codex_home = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    dest = codex_home / "skills"
    if dest.resolve().parent != codex_home.resolve():
        return  # environment-dependent; guard is about exact location
    actions, _ = inst.install_codex(REPO_ROOT, dest, force=True, dry_run=True)
    assert any("copy plugin _shared" in a for a in actions)


def test_codex_skip_log_matches_behavior(short_tmp: Path) -> None:
    """Existing _shared without --force must log a skip, not a copy."""
    dest = short_tmp / ".codex" / "skills"
    dest.mkdir(parents=True)
    (dest / "_shared").mkdir()
    actions, _ = inst.install_codex(REPO_ROOT, dest, force=False, dry_run=True)
    joined = "\n".join(actions)
    assert "skip skills/_shared" in joined
    assert "skip plugin-level _shared" in joined
    assert "copy skills/_shared ->" not in joined
    assert "copy plugin _shared ->" not in joined


def test_mcp_merge_tolerates_jsonc(short_tmp: Path) -> None:
    """opencode.json may be JSONC; a broken parse must not clobber the file."""
    path = short_tmp / "opencode.json"
    path.write_text('{\n  // comment\n  "mcp": {},\n}', encoding="utf-8")
    before = path.read_text(encoding="utf-8")
    actions = inst.merge_into_opencode_config(path, inst.mcp_entry(REPO_ROOT),
                                              dry_run=False)
    assert any("WARNING" in a for a in actions)
    assert path.read_text(encoding="utf-8") == before  # untouched


def test_platform_manifests_are_valid_json() -> None:
    """The new adapter manifests must parse as JSON and carry required keys."""
    marketplace = REPO_ROOT / ".claude-plugin" / "marketplace.json"
    plugin = REPO_ROOT / "plugins" / "materials-skills" / ".claude-plugin" / "plugin.json"
    for path in (marketplace, plugin):
        data = json.loads(path.read_text(encoding="utf-8"))
        assert data["name"]
    mkt = json.loads(marketplace.read_text(encoding="utf-8"))
    assert mkt["owner"]["name"]
    assert mkt["plugins"][0]["name"] == "materials-skills"
    assert mkt["plugins"][0]["source"] == "./plugins/materials-skills"


def test_mcp_json_merge(short_tmp: Path) -> None:
    path = short_tmp / ".mcp.json"
    path.write_text(json.dumps({"mcpServers": {"existing": {"command": "x"}}}),
                    encoding="utf-8")
    entry = inst.mcp_entry(REPO_ROOT)
    actions = inst.merge_into_mcp_json(path, entry, dry_run=False)
    assert actions
    data = json.loads(path.read_text(encoding="utf-8"))
    assert "existing" in data["mcpServers"]
    srv = data["mcpServers"][inst.MCP_NAME]
    assert srv["command"] == "python"
    assert srv["args"][0].endswith("server.py")
    assert Path(srv["args"][0]).is_absolute()


def test_mcp_opencode_merge(short_tmp: Path) -> None:
    path = short_tmp / "opencode.json"
    path.write_text(json.dumps({"mcp": {"other": {"type": "local"}}}), encoding="utf-8")
    entry = inst.mcp_entry(REPO_ROOT)
    actions = inst.merge_into_opencode_config(path, entry, dry_run=False)
    assert actions
    data = json.loads(path.read_text(encoding="utf-8"))
    assert "other" in data["mcp"]
    cfg = data["mcp"][inst.MCP_NAME]
    assert cfg["type"] == "local"
    assert cfg["command"][0] == "python"
    assert cfg["enabled"] is True

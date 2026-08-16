from __future__ import annotations

import importlib.util
import time
from pathlib import Path

import pytest

REPO_SCRIPTS = Path(__file__).resolve().parent
MODULE_PATH = REPO_SCRIPTS / "autoupdate_skills.py"


def _load(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("MATERIALS_AUTOUPDATE_STATE", str(tmp_path / "state"))
    spec = importlib.util.spec_from_file_location("autoupdate_skills", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_throttle_skips_recent_check(tmp_path, monkeypatch):
    mod = _load(tmp_path, monkeypatch)
    state = tmp_path / "state" / "claude-x"
    state.mkdir(parents=True)
    (state / "last-check").write_text(str(time.time()), encoding="utf-8")
    assert mod.should_check_upstream(state, throttle=3600, force=False) is False


def test_throttle_allows_stale_or_missing_check(tmp_path, monkeypatch):
    mod = _load(tmp_path, monkeypatch)
    state = tmp_path / "state" / "claude-x"
    state.mkdir(parents=True)
    (state / "last-check").write_text(str(time.time() - 7200), encoding="utf-8")
    assert mod.should_check_upstream(state, throttle=3600, force=False) is True
    (state / "last-check").write_text("garbage", encoding="utf-8")
    assert mod.should_check_upstream(state, throttle=3600, force=False) is True
    (state / "last-check").unlink()
    assert mod.should_check_upstream(state, throttle=3600, force=False) is True
    assert mod.should_check_upstream(state, throttle=3600, force=True) is True


def test_corrupt_stamp_is_treated_as_stale(tmp_path, monkeypatch):
    mod = _load(tmp_path, monkeypatch)
    state = tmp_path / "state" / "claude-x"
    state.mkdir(parents=True)
    (state / "last-check").write_text("not-a-number", encoding="utf-8")
    assert mod.should_check_upstream(state, throttle=3600, force=False) is True


def test_destination_drift_detects_missing_skill(tmp_path, monkeypatch):
    mod = _load(tmp_path, monkeypatch)
    dest = tmp_path / "dest"
    dest.mkdir()
    names = sorted(
        p.name for p in (mod.REPO_ROOT / "plugins" / "materials-skills" / "skills").iterdir()
        if p.is_dir() and p.name.startswith("materials-")
    )
    assert len(names) >= mod.MIN_SKILLS
    # missing one skill directory -> drift
    for name in names[:-1]:
        (dest / name).mkdir()
    assert mod.destination_drift("claude", dest) is True
    (dest / names[-1]).mkdir()
    assert mod.destination_drift("claude", dest) is False
    # nonexistent destination -> drift
    assert mod.destination_drift("claude", tmp_path / "missing") is True


def test_repo_is_clean_rejects_dirty_tree(tmp_path, monkeypatch):
    mod = _load(tmp_path, monkeypatch)
    repo = tmp_path / "repo"
    repo.mkdir()
    import subprocess

    def git(*args: str, check: bool = True):
        return subprocess.run(["git", *args], cwd=repo, check=check, capture_output=True, text=True)

    git("init", "-q")
    git("config", "user.email", "t@example.com")
    git("config", "user.name", "t")
    (repo / "file.txt").write_text("hello", encoding="utf-8")
    git("add", ".")
    git("commit", "-qm", "init")
    clean, _ = mod.repo_is_clean(repo)
    assert clean is True
    (repo / "file.txt").write_text("dirty", encoding="utf-8")
    clean, reason = mod.repo_is_clean(repo)
    assert clean is False
    assert "dirty" in reason


def test_fast_forward_tolerates_network_failure(tmp_path, monkeypatch):
    mod = _load(tmp_path, monkeypatch)
    repo = tmp_path / "repo"
    repo.mkdir()
    # Not a git repository at all: fetch fails -> offline-safe path.
    moved, ok, error = mod.fast_forward(repo)
    assert moved is False
    assert ok is False
    assert error


def test_lock_is_exclusive_and_released(tmp_path, monkeypatch):
    mod = _load(tmp_path, monkeypatch)
    state = tmp_path / "state" / "claude-x"
    state.mkdir(parents=True)
    assert mod.acquire_lock(state) is True
    assert mod.acquire_lock(state) is False
    mod.release_lock(state)
    assert mod.acquire_lock(state) is True


def test_update_target_offline_returns_zero(tmp_path, monkeypatch):
    mod = _load(tmp_path, monkeypatch)
    repo = tmp_path / "repo"  # not a git repo -> tolerated offline path
    repo.mkdir()
    # claude destination exists with all skills -> no drift; upstream check
    # fails gracefully and the run still exits 0.
    names = [
        p.name for p in (mod.REPO_ROOT / "plugins" / "materials-skills" / "skills").iterdir()
        if p.is_dir() and p.name.startswith("materials-")
    ]
    full = tmp_path / "full-dest"
    full.mkdir()
    for name in names:
        (full / name).mkdir()
    monkeypatch.setitem(mod.TARGET_DESTS, "claude", full)
    assert mod.update_target("claude", repo, throttle=0, force=True) == 0

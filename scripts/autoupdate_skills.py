#!/usr/bin/env python3
"""Keep an installed copy of the skills in sync with upstream, cheaply.

Python port of nature-skills' autoupdate-skills.sh idea (Apache-2.0),
adapted to the materials-skills multi-host installer. Run from a dedicated
clone of this repository (not your dev checkout); on each run it:

1. throttles upstream checks (default 1 h per destination, --force ignores),
2. fast-forwards the clone only (refuses dirty trees or local commits),
3. re-runs install_skills.py --force for each target when upstream moved or
   the installed destination drifted (missing skill directories),
4. stays offline-safe: any network/git failure is logged and the run still
   exits 0 so a session-start hook never blocks.

Usage:
  python scripts/autoupdate_skills.py                          # claude (default)
  python scripts/autoupdate_skills.py --target zcode --target codex
  python scripts/autoupdate_skills.py --target dsh             # project .dsh/skills
  python scripts/autoupdate_skills.py --throttle 3600 --force

Environment:
  MATERIALS_AUTOUPDATE_STATE   base state dir (default: platform state dir)
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
INSTALLER = REPO_ROOT / "scripts" / "install_skills.py"
DSH_SYNC = REPO_ROOT / "scripts" / "sync_dsh_skills.py"
MIN_SKILLS = 15  # must match validate_host_packaging.MIN_BUNDLE_SKILLS

TARGET_DESTS = {
    "claude": Path.home() / ".claude" / "skills",
    "opencode": Path.home() / ".config" / "opencode" / "skills",
    "antigravity": Path.home() / ".gemini" / "config" / "skills",
    "zcode": Path.home() / ".zcode" / "skills",
    "codex": Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")) / "skills",
}
LOCK_STALE_SECONDS = 600


def state_base() -> Path:
    env = os.environ.get("MATERIALS_AUTOUPDATE_STATE")
    if env:
        return Path(env)
    xdg = os.environ.get("XDG_STATE_HOME") or str(Path.home() / ".local" / "state")
    return Path(xdg) / "materials-skills"


def dest_key(target: str, dest: Path) -> str:
    return f"{target}-{str(dest.resolve())}".replace(":", "").replace("\\", "_").replace("/", "_")


def log_line(state_dir: Path, message: str) -> None:
    stamp = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    line = f"{stamp} {message}"
    print(line)
    try:
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / "autoupdate.log").open("a", encoding="utf-8").write(line + "\n")
    except OSError:
        pass


def should_check_upstream(state_dir: Path, throttle: int, force: bool) -> bool:
    if force or throttle <= 0:
        return True
    stamp = state_dir / "last-check"
    if not stamp.is_file():
        return True
    try:
        return (time.time() - float(stamp.read_text(encoding="utf-8").strip())) >= throttle
    except (OSError, ValueError):
        return True


def touch_last_check(state_dir: Path) -> None:
    try:
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / "last-check").write_text(str(time.time()), encoding="utf-8")
    except OSError:
        pass


def acquire_lock(state_dir: Path) -> bool:
    """True if acquired; stale locks (age > LOCK_STALE_SECONDS) are broken."""
    import platform

    lock = state_dir / "update.lock"
    state_dir.mkdir(parents=True, exist_ok=True)
    if lock.exists():
        try:
            if time.time() - lock.stat().st_mtime > LOCK_STALE_SECONDS:
                lock.unlink()
            else:
                return False
        except OSError:
            return False
    try:
        lock.write_text(f"{platform.node()}:{os.getpid()}\n", encoding="utf-8")
        return True
    except OSError:
        return False


def release_lock(state_dir: Path) -> None:
    try:
        (state_dir / "update.lock").unlink(missing_ok=True)
    except OSError:
        pass


def repo_is_clean(repo: Path) -> tuple[bool, str]:
    """True when the clone has no local edits and no unpushed local commits."""
    def git(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=repo, check=False, text=True,
            capture_output=True,
        ).stdout.strip()

    status = git("status", "--porcelain")
    if status:
        return False, "working tree dirty; refusing to update a dev checkout"
    ahead = git("rev-list", "--count", "@{u}..HEAD") if git("rev-parse", "@{u}") else "0"
    if ahead not in ("", "0"):
        return False, f"clone has {ahead} local commit(s); refusing non-fast-forward"
    return True, ""


def fast_forward(repo: Path) -> tuple[bool, bool, str]:
    """Fetch + fast-forward. Returns (upstream_moved, ok, error)."""
    fetch = subprocess.run(
        ["git", "fetch", "--quiet"], cwd=repo, check=False,
        capture_output=True, text=True,
    )
    if fetch.returncode != 0:
        return False, False, (fetch.stderr or "fetch failed").strip()
    ahead_behind = subprocess.run(
        ["git", "rev-list", "--left-right", "--count", "HEAD...@{u}"],
        cwd=repo, check=False, capture_output=True, text=True,
    )
    if ahead_behind.returncode != 0:
        return False, False, (ahead_behind.stderr or "rev-list failed").strip()
    parts = ahead_behind.stdout.split()
    if len(parts) == 2 and parts[0] == "0" and parts[1] == "0":
        return False, True, ""
    if len(parts) == 2 and parts[0] != "0":
        return False, False, "local commits ahead; refusing non-fast-forward"
    merge = subprocess.run(
        ["git", "merge", "--ff-only", "--quiet"], cwd=repo, check=False,
        capture_output=True, text=True,
    )
    if merge.returncode != 0:
        return False, False, (merge.stderr or "ff merge failed").strip()
    return True, True, ""


def destination_drift(target: str, dest: Path) -> bool:
    """Cheap drift check: every materials-* skill must exist in the dest."""
    names = sorted(
        p.name for p in (REPO_ROOT / "plugins" / "materials-skills" / "skills").iterdir()
        if p.is_dir() and p.name.startswith("materials-")
    )
    if len(names) < MIN_SKILLS:
        return True
    if not dest.is_dir():
        return True
    return any(not (dest / name).is_dir() for name in names)


def sync_target(target: str, repo: Path) -> bool:
    if target == "dsh":
        result = subprocess.run(
            [sys.executable, str(DSH_SYNC)], cwd=repo, check=False,
            capture_output=True, text=True,
        )
        return result.returncode == 0
    dest = TARGET_DESTS[target]
    cmd = [sys.executable, str(INSTALLER), "--target", target, "--force"]
    result = subprocess.run(cmd, cwd=repo, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        print((result.stdout or "") + (result.stderr or ""))
        return False
    return True


def update_target(target: str, repo: Path, throttle: int, force: bool) -> int:
    dest = TARGET_DESTS.get(target)
    state_dir = state_base() / dest_key(target, dest or repo)
    if not acquire_lock(state_dir):
        log_line(state_dir, f"{target}: another update is running; skipping")
        return 0

    try:
        drift = destination_drift(target, dest) if dest else True
        if drift:
            log_line(state_dir, f"{target}: destination drift detected; re-syncing")
            ok = sync_target(target, repo)
            log_line(state_dir, f"{target}: repair sync {'ok' if ok else 'FAILED'}")
            if not ok:
                return 1
        if not should_check_upstream(state_dir, throttle, force):
            log_line(state_dir, f"{target}: throttled; destination verified")
            return 0
        clean, reason = repo_is_clean(repo)
        if not clean:
            log_line(state_dir, f"{target}: {reason}")
            return 0
        moved, ok, error = fast_forward(repo)
        if not ok:
            log_line(state_dir, f"{target}: offline/error tolerated ({error})")
            return 0  # offline-safe: never block a session start
        touch_last_check(state_dir)
        if moved:
            log_line(state_dir, f"{target}: upstream moved; re-syncing")
            if not sync_target(target, repo):
                log_line(state_dir, f"{target}: sync FAILED")
                return 1
            log_line(state_dir, f"{target}: sync ok")
        else:
            log_line(state_dir, f"{target}: up to date")
        return 0
    finally:
        release_lock(state_dir)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--target", action="append", choices=[*TARGET_DESTS, "dsh"],
                        help="destination(s) to update (repeatable; default claude)")
    parser.add_argument("--throttle", type=int, default=3600,
                        help="min seconds between upstream checks (0 = always)")
    parser.add_argument("--force", action="store_true", help="ignore throttle")
    parser.add_argument("--repo", default=str(REPO_ROOT), help="dedicated clone of this repository")
    args = parser.parse_args(argv)

    repo = Path(args.repo).resolve()
    targets = args.target or ["claude"]
    exit_code = 0
    for target in targets:
        exit_code |= update_target(target, repo, args.throttle, args.force)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

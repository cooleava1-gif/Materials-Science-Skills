# Automatic updates / 自动更新

`scripts/autoupdate_skills.py` keeps installed skills in sync with upstream —
cheaply enough to run at every session start. It is a Python port of the
[nature-skills](https://github.com/Yuan1z0825/nature-skills) autoupdate idea,
adapted to our multi-host installer.

`scripts/autoupdate_skills.py` 让已安装技能与上游保持同步，代价足够低，可在
每次会话启动时运行。设计移植自 nature-skills（Apache-2.0），适配本仓库的
多宿主安装器。

## Safety properties 安全特性

- **Throttled** — upstream checks at most once per hour per destination
  (`--throttle`, default 3600 s; `--force` ignores).
- **Offline-safe** — any git/network failure is logged and the run exits 0;
  a session-start hook never blocks on a flaky link.
- **Non-destructive** — only ever fast-forwards the dedicated clone; refuses
  to run on a dirty tree or local commits (keep it on a skills-only clone,
  not your dev checkout).
- **Per-destination state** — independent throttle, log, and lock per target
  under `$XDG_STATE_HOME/materials-skills/` (override:
  `MATERIALS_AUTOUPDATE_STATE`).
- **Drift repair** — every invocation verifies the destination still holds
  all `materials-*` skills and re-syncs if any went missing.

## Setup 准备

```bash
mkdir -p ~/ai-skills && cd ~/ai-skills
git clone https://github.com/cooleava1-gif/Materials-Science-Skills.git
```

Run manually 手动运行：

```bash
python scripts/autoupdate_skills.py --target claude
python scripts/autoupdate_skills.py --target zcode --target codex
python scripts/autoupdate_skills.py --target dsh   # project .dsh/skills
```

## Session-start hooks 会话启动钩子

### Claude Code (`~/.claude/settings.json`)

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python ~/ai-skills/Materials-Science-Skills/scripts/autoupdate_skills.py --target claude"
          }
        ]
      }
    ]
  }
}
```

### Codex (`~/.codex/hooks.json`)

```json
{
  "hooks": {
    "session_start": [
      {
        "type": "command",
        "command": "python ~/ai-skills/Materials-Science-Skills/scripts/autoupdate_skills.py --target codex"
      }
    ]
  }
}
```

### ZCode / OpenCode / Antigravity / any agent with a startup hook

Run the same one-liner with the right `--target`
(`zcode` / `opencode` / `antigravity`) through the host's hook or startup
mechanism; a shell profile or scheduled task works equally well:

```bash
python ~/ai-skills/Materials-Science-Skills/scripts/autoupdate_skills.py --target zcode
```

## Logs and troubleshooting 日志与排障

- Per-destination logs: `<state>/materials-skills/<target>-<dest>/autoupdate.log`
- `update.lock` appears only while an update runs; stale locks (>10 min)
  are broken automatically.
- "working tree dirty" — you pointed `--repo` at a dev checkout; clone again
  into a skills-only directory.
- No updates happening — check the throttle stamp (`last-check`) and git
  remotes; every run still repairs destination drift.

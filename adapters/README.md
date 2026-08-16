# Adapters — install the bundle on any agent

The canonical source stays platform-neutral (`plugins/materials-skills/skills/`:
SKILL.md + manifest.yaml + fragments + references + `_shared/` protocol layer).
Adapters add thin platform shells on top; the installer
(`scripts/install_skills.py`) is the single entry point.

## Platform matrix

| Platform | Install command | Skills location | MCP registration | Distribution |
|---|---|---|---|---|
| Claude Code | `--target claude` | `~/.claude/skills/` | `.mcp.json` (`mcpServers`) | `.claude-plugin/` marketplace (Option B) |
| OpenCode | `--target opencode` | `~/.config/opencode/skills/` | `opencode.json` `mcp` field | none (skills dir only) |
| Antigravity | `--target antigravity` | `~/.gemini/config/skills/` | manual (not yet standardized) | experimental `plugin.json` |
| ZCode | `--target zcode` | `~/.zcode/skills/` | plugin manifest (`${ZCODE_PLUGIN_ROOT}` MCP) | `.zcode-plugin/` plugin |
| Codex (original) | `--target codex` (or `scripts/install.ps1`) | `$CODEX_HOME/skills/` | `.mcp.json` / `config.toml` | `.codex-plugin/` plugin |
| deepseek-harness (dsh) | `scripts/sync_dsh_skills.py` | project `.dsh/skills/` or `<dshHome>/skills` | cordis patch overlay (`dsh/cordis.patch.yml`) | none (developer preview) |
| Any SKILL.md agent | `--target generic --dest <dir>` | anywhere | manual | none |

## How the installer makes skills portable

1. **Materialization**: skills reference shared content via `../_shared/...`
   and `../../_shared/...` (the Codex layout keeps two sibling `_shared`
   trees). OpenCode / Claude personal / Antigravity do not guarantee
   cross-directory reads, so non-codex targets merge both trees into each
   skill's `_shared/` and rewrite every reference to `_shared/...`.
2. **Integrity check**: after materialization every shared reference is
   re-validated against the installed tree (multi-basis resolution;
   placeholder patterns such as `<journal>.yaml` are skipped).
3. **Platform hygiene**: the Codex-only `agents/` directory is dropped for
   non-codex targets; MCP servers are registered with absolute paths.

## Usage

```bash
python scripts/install_skills.py --target claude --dry-run    # preview only
python scripts/install_skills.py --target claude              # real install
python scripts/install_skills.py --target opencode --force    # replace existing
python scripts/install_skills.py --target zcode               # ~/.zcode/skills/
python scripts/install_skills.py --target generic --dest ./vendor/skills --no-mcp
python scripts/sync_dsh_skills.py                             # dsh: project .dsh/skills/
```

Options: `--dest PATH` (override location), `--mcp-dest PATH` (MCP config
file), `--no-mcp`, `--force`, `--dry-run`, `--repo-root PATH`.

See `claude/`, `opencode/`, `antigravity/`, `zcode/`, `dsh/` for per-platform
notes and troubleshooting.

## Compatibility notes

- Frontmatter is limited to `name`/`description`/`version`/`stability`; the
  supported non-Codex platforms tolerate unknown fields (OpenCode ignores
  them by spec), and `description` is the shared trigger mechanism
  everywhere. deepseek-harness additionally honors `disable-model-invocation`
  and `user-invocable` policies (set on `_shared`).
- Behavioral contracts (`manifest.yaml` routing, stage gates, handoffs) are
  executed by the model reading the files, not by any platform — agent
  capability determines how strictly they are followed.
- Known limitation: a few in-skill Python tools hard-code sibling-`_shared`
  paths (e.g. `check_routing_contract.py`). The installer rewrites the known
  patterns (`SKILL_ROOT.parent`-style and `parents[3]`-style references) to
  the merged in-skill `_shared/`; any remaining dynamic-path references must
  be adapted manually when those scripts are run inside a materialized
  install. Text references (SKILL.md / manifest.yaml / fragments) are fully
  verified after install.

# deepseek-harness (dsh) adapter

[deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) (`dsh`,
npm `@deepseek-ai/dsh`) discovers skills one level deep at
`<root>/<name>/SKILL.md`, with these roots (rank order): project
`.dsh/skills` (100), project `.agents/skills` (200), `customSkillDirs` (300),
`<dshHome>/skills` (400), `~/.agents/skills` (500). Frontmatter requires
kebab-case `name` + `description`; unknown keys are ignored, and
`disable-model-invocation` / `user-invocable` control catalog visibility
(both set on `_shared`, which is support-only).

## Option A — Sync into the project skills root (recommended)

Works for both the `web` and `headless` profiles:

```bash
python scripts/sync_dsh_skills.py            # project .dsh/skills/ (rank 100)
python scripts/sync_dsh_skills.py --user     # <dshHome>/skills (rank 400)
```

The script mirrors `materials-*` plus `_shared` (layout preserved, so the
skills' `../_shared/` references keep resolving) and removes stale skill
directories first. Rerun after skill updates.

## Option B — Zero-copy overlay (headless/CLI profiles)

No copy at all: the overlay points dsh at the plugin skills tree and inserts
the academic-search MCP client row. Launch dsh from the repository root:

```bash
dsh --profile headless --patch ./dsh/cordis.patch.yml "<task>"
```

- `skill-filesystem.customSkillDirs` → `./plugins/materials-skills/skills`.
- `@deepseek-ai/dsh-mcp-client` row → tools appear as
  `mcp__materials-academic-search__*`.
- Web profile note: `dsh-web-app` disables the host skill rows because agent
  presets own local skill discovery there; use Option A for the web UI.

## Notes

- dsh is a developer preview (`0.1.0-rc.x`) with planned
  compatibility-breaking changes; pin the rc version you validated against.
- Verified end-to-end on `0.1.0-rc.6`: all 14 `materials-*` skills listed in
  the model catalog, `materials-shared` hidden by policy, and MCP tools
  registered.
- The MCP server needs its Python dependencies:
  `python -m pip install -r plugins/materials-skills/skills/materials-citation/mcp/academic_search/requirements.txt`

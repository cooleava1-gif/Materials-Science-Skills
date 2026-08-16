# Claude Code adapter

Claude Code loads the bundle through **two independent paths**; pick one.

## Option A — Personal skills (self-contained, recommended)

Every skill is *materialized* (both `_shared` trees are merged into each skill
directory and all relative references are rewritten), so the install has no
cross-directory dependencies — required because Claude Code copies plugins to a
cache and cannot resolve `../_shared` paths outside a plugin.

```bash
python scripts/install_skills.py --target claude --dry-run   # preview
python scripts/install_skills.py --target claude             # ~/.claude/skills/
```

- Skills land in `~/.claude/skills/<skill>/SKILL.md` and are discovered on
  session start.
- MCP: the installer merges `materials-academic-search` into `.mcp.json`
  (`--mcp-dest` to redirect, `--no-mcp` to skip). Alternatively run
  `claude mcp add materials-academic-search -- python <abs path to server.py>`
  (see `--dry-run` output for the resolved absolute path).

## Option B — Plugin marketplace (shared source of truth, no materialization)

The plugin lives at `plugins/materials-skills/` with a Claude manifest at
`.claude-plugin/plugin.json` and the catalog at `.claude-plugin/marketplace.json`.
Both `_shared` trees sit *inside* the plugin directory, so their sibling
relative references survive the cache copy.

```bash
claude plugin marketplace add . --scope user     # from the repo root
claude plugin install materials-skills@materials-skills-marketplace
```

- Plugin skills are namespaced: `/materials-skills:materials-research`.
- MCP: the manifest declares `materials-academic-search` inline in
  `mcpServers` with args resolved through `$CLAUDE_PLUGIN_ROOT`; the
  plugin-root `.mcp.json` remains the Codex configuration and is not used
  here.
- `claude plugin validate ./plugins/materials-skills` to sanity-check the
  manifest and skill frontmatter.

## Notes

- Frontmatter is intentionally limited to `name`/`description`/`version`/
  `stability`; Claude ignores unknown fields, and `name` matches each
  directory name (kebab-case), so all 14 skills are valid.
- The Codex-only `agents/` directory is dropped by the installer
  (Option A) and ignored by Claude (Option B).

# ZCode adapter

ZCode discovers `SKILL.md` directories under `~/.zcode/skills/`,
`~/.agents/skills/`, workspace `.zcode/skills` / `.agents/skills`, and plugin
roots. Two install paths are supported; pick one.

## Option A — Personal skills (materialized)

```bash
python scripts/install_skills.py --target zcode --dry-run   # preview
python scripts/install_skills.py --target zcode             # ~/.zcode/skills/
```

Every skill is materialized (both `_shared` trees merged into the skill
directory, references rewritten), so the install is self-contained. MCP is
not registered by this path; use Option B or a workspace-level MCP config for
the academic-search server.

## Option B — Plugin (shared source of truth)

The plugin lives at `plugins/materials-skills/` with a ZCode manifest at
`.zcode-plugin/plugin.json` (ZCode probes `.zcode-plugin/` before the
`.claude-plugin/` and `.codex-plugin/` compatibility names). In the client,
open **Settings → Plugin Management → Discover**, add the repository as a
marketplace with the `+` button
(`https://github.com/cooleava1-gif/Materials-Science-Skills.git`, ref `main`),
then install `materials-skills`.

- Skills come from the plugin's `skills/` component, `_shared` stays a
  sibling, so relative references survive.
- MCP: the manifest declares `materials-academic-search` inline with args
  resolved through `${ZCODE_PLUGIN_ROOT}` (template expansion works only for
  plugin-scoped MCP servers); it auto-connects as
  `plugin:materials-skills:materials-academic-search`.

## Notes

- Frontmatter is limited to `name`/`description`/`version`/`stability`;
  ZCode recognizes `name`, `description` (≤1024 chars), `when_to_use`,
  `license`, and `metadata`; other flat keys are skipped, not fatal.
- The MCP server needs its Python dependencies:
  `python -m pip install -r plugins/materials-skills/skills/materials-citation/mcp/academic_search/requirements.txt`

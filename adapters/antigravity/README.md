# Google Antigravity adapter

Antigravity 2.0 (desktop, CLI `agy`, IDE, SDK) follows the Agent Skills open
standard: skills live at `<workspace>/.agents/skills/<folder>/SKILL.md`
(project) or `~/.gemini/config/skills/<folder>/` (global).

The installer targets the global location:

```bash
python scripts/install_skills.py --target antigravity --dry-run   # preview
python scripts/install_skills.py --target antigravity             # ~/.gemini/config/skills/
```

- Each skill is **materialized** (self-contained `_shared/`), so no
  cross-directory references are needed.
- The Codex-only `agents/` directory is dropped.
- MCP: not auto-registered — Antigravity's global MCP configuration mechanism
  is not yet standardized in public docs. Register the server manually per the
  current Antigravity MCP docs, pointing at:
  `<skills-dir>/materials-citation/mcp/academic_search/server.py`
  (run `--dry-run` first to see the resolved install path).

## Notes

- Antigravity documents `name` (optional, defaults to folder name) and
  `description` (required) only; the bundle's extra `version`/`stability`
  fields are conservative metadata and have not been observed to cause issues,
  but if a future Antigravity release enforces strict frontmatter, strip them
  before installing.
- Antigravity CLI also supports *flat* `.md` slash-command skills under
  `.agents/skills/` (a single `foo.md`, not a folder); this bundle uses the
  folder + `SKILL.md` form, which both Antigravity 2.0 and the CLI accept.
- `adapters/antigravity/plugin.json` is an experimental plugin distribution
  manifest. Antigravity validates `plugin.json` against a strict schema
  (`additionalProperties: false`); verify against the current official schema
  before distributing it.

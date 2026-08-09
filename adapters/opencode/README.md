# OpenCode adapter

OpenCode (opencode.ai) natively discovers `SKILL.md` directories in six
locations: `.opencode/skills/`, `~/.config/opencode/skills/`,
`.claude/skills/`, `~/.claude/skills/`, `.agents/skills/`, `~/.agents/skills/`.

The installer targets the global location:

```bash
python scripts/install_skills.py --target opencode --dry-run   # preview
python scripts/install_skills.py --target opencode             # ~/.config/opencode/skills/
```

## What the installer does

- **Materializes** every skill: both `_shared` trees are merged into
  `<skill>/_shared/` and all `(../)+_shared/` references are rewritten to
  `_shared/`, because OpenCode only guarantees reads inside the skill
  directory.
- **Drops** the Codex-only `agents/` directory.
- **Registers the MCP server** by merging into
  `~/.config/opencode/opencode.json`:

```json
{
  "mcp": {
    "materials-academic-search": {
      "type": "local",
      "command": ["python", "<abs path to>/materials-citation/mcp/academic_search/server.py"],
      "environment": {},
      "enabled": true
    }
  }
}
```

## OpenCode-specific notes

- Only these frontmatter fields are read: `name`, `description`, `license`,
  `compatibility`, `metadata`; everything else (including `version` and
  `stability`) is ignored — that is intentional and harmless.
- The `manifest.yaml` routing and handoff contracts are executed by the model
  reading the files, not by the platform; OpenCode does not package skills via
  its plugin system (plugin.ts is a separate mechanism).
- Permissions: if you want to gate skill invocation, set
  `permission.skill` in `opencode.json`.

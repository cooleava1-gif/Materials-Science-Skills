# Install Materials Science Skills

This guide is for the polished, day-to-day use of the bundle: install it, run a
five-minute workflow, verify the installed state, and avoid stale-skill drift
between the plugin source and the local installation.

## Cross-platform installer (recommended)

The one installer covers every supported agent and *materializes* each skill
into a self-contained directory (both `_shared` trees merged in, references
rewritten, Codex-only `agents/` dropped), then registers the
`materials-academic-search` MCP server for the platform.

```bash
# preview first — prints the full plan, changes nothing
python scripts/install_skills.py --target claude --dry-run

# real installs
python scripts/install_skills.py --target claude        # ~/.claude/skills/
python scripts/install_skills.py --target opencode      # ~/.config/opencode/skills/
python scripts/install_skills.py --target antigravity   # ~/.gemini/config/skills/
python scripts/install_skills.py --target zcode         # ~/.zcode/skills/
python scripts/install_skills.py --target codex         # $CODEX_HOME/skills/ (no materialization)
python scripts/install_skills.py --target generic --dest ./vendor/skills --no-mcp

# deepseek-harness (dsh): layout-preserving sync instead of materialization
python scripts/sync_dsh_skills.py                       # project .dsh/skills/
```

Useful flags: `--dest PATH` (override location), `--mcp-dest PATH` (MCP config
file), `--no-mcp`, `--force` (replace existing), `--repo-root PATH`. See
`adapters/README.md` for per-platform notes.

## Option 1: Codex Plugin

Add the local marketplace entry and install the plugin:

```powershell
codex plugin marketplace add https://github.com/cooleava1-gif/Materials-Science-Skills.git --ref main
codex plugin add materials-skills@materials-skills
```

What this gives you:

- the `materials-*` skill bundle
- the required `_shared` support folder
- the academic-search MCP configuration included with the plugin

## Option 2: Manual Skills Install

From the repository root, run:

```powershell
.\scripts\install.ps1
```

The installer copies all `materials-*` skills plus `_shared` into
`$CODEX_HOME\skills` if `CODEX_HOME` is set, or into `~\.codex\skills`
otherwise. It also removes stale target directories before reinstalling so old
files do not survive an update.

If you need the manual fallback commands:

```powershell
$skillsDir = if ($env:CODEX_HOME) { Join-Path $env:CODEX_HOME "skills" } else { Join-Path $HOME ".codex\skills" }
$codexHome = Split-Path -Parent $skillsDir
New-Item -ItemType Directory -Force $skillsDir | Out-Null
Copy-Item -Recurse -Force .\plugins\materials-skills\skills\materials-* $skillsDir
Copy-Item -Recurse -Force .\plugins\materials-skills\skills\_shared $skillsDir
Copy-Item -Recurse -Force .\plugins\materials-skills\_shared $codexHome
```

## Option 3: ZCode Plugin

ZCode probes `.zcode-plugin/plugin.json` before the Codex and Claude
manifests, and the repository ships one at
`plugins/materials-skills/.zcode-plugin/plugin.json`. In the client, open
**Settings → Plugin Management → Discover**, add a marketplace with the `+`
button pointing at the repository
(`https://github.com/cooleava1-gif/Materials-Science-Skills.git`, ref `main`),
then install `materials-skills`. A local checkout directory works as a
marketplace source too.

What this gives you:

- the `materials-*` skill bundle and the `_shared` support folder
- the academic-search MCP server, launched via `${ZCODE_PLUGIN_ROOT}` and
  auto-connected as `plugin:materials-skills:materials-academic-search`

## Option 4: DeepSeek Harness (dsh)

Sync the bundle into the project skills root (works for the `web` and
`headless` profiles):

```powershell
python .\scripts\sync_dsh_skills.py
```

Use `--user` for the user-level `<dshHome>\skills` root. Alternatively, for
headless/CLI profiles only, boot with the zero-copy overlay from the
repository root:

```powershell
dsh --profile headless --patch .\dsh\cordis.patch.yml "<task>"
```

The overlay points dsh at the plugin skills tree and registers the
academic-search MCP server (`mcp__materials-academic-search__*` tools). dsh is
a developer preview (`0.1.0-rc.x`); pin the rc version you validated against.
See `adapters/dsh/README.md` for details.

## Optional Academic Search MCP

If you want the local academic-search MCP, install the Python dependencies
first:
```powershell
python -m pip install -r .\plugins\materials-skills\skills\materials-citation\mcp\academic_search\requirements.txt
```

Example Codex MCP configuration:

```toml
[mcp_servers."materials-academic-search"]
command = "python"
args = ["./skills/materials-citation/mcp/academic_search/server.py"]
cwd = "plugins/materials-skills"
```

Optional environment variables:

- `OPENALEX_API_KEY`
- `SEMANTIC_SCHOLAR_API_KEY`
- `MATERIALS_CONTACT_EMAIL`
- `NCBI_API_KEY`

## Verify The Install

If you kept the repository validation scripts locally, run:

```powershell
python .\scripts\run_release_checks.py --json
```

Judge the release by the final JSON `status`. If any skill files under
`plugins/materials-skills/skills/` changed, rerun `.\scripts\install.ps1`.

## Five-Minute Walkthrough

Use one of these paths immediately after install.

### Path A: WER-EA Mini-Review

Prompt:

```text
Help me run a WER-EA mini-review workflow from screening to figure planning.
```

Expected shape:

1. `materials-research` routes the workflow.
2. `materials-citation` plans the search and screening matrix.
3. `materials-reader` builds evidence-chain handoffs.
4. `materials-writing` builds the outline.
5. `materials-figure` plans the review figures.

### Path B: Experimental Manuscript

Prompt:

```text
Audit this experimental manuscript for evidence gaps before I draft the discussion.
```

Expected shape:

1. `materials-research` frames stage, evidence level, and route.
2. `materials-data` and `materials-figure` tighten supporting data.
3. `materials-writing` and `materials-polishing` rebuild bounded text.
4. `materials-reviewer` checks the revised package.

### Path C: Paper To Presentation

Prompt:

```text
Turn this paper package into a journal-club outline and verified HTML academic deck.
```

Expected shape:

1. `materials-html-deck` creates the slide story, speaker notes, and retained HTML deck.
2. `materials-figure` supports figure placement or redrawing when needed.

### Path D: Paper To Chinese Invention Patent

Prompt:

```text
Convert this materials paper into an evidence-grounded Chinese invention patent
application draft.
```

Expected shape:

1. `materials-research` resolves `source_format` / `task_mode` /
   `invention_type` (default: `process-material`).
2. `materials-paper-to-patent` builds the source map, terminology ledger,
   and evidence ledger.
3. `materials-paper-to-patent` drafts claims with the
   claim-feature → source-id map.
4. `validate_patent_claims.py` runs the 7-rule civil content check; the
   `validate_patent_draft.py` runs the structural check.
5. `build_patent_package.py` renders the DOCX (description + claims +
   abstract + cover letter) and the `flowchart.svg`.

Notes: figure notes are produced as text; the actual figures are generated
by `materials-figure`. The default `invention_type` is `process-material`;
switch via `manifest.yaml` for `apparatus-system` / `algorithm-software` /
`mixed`.

## Guided Demo Routes

To see the visual proof side first, open [docs/gallery/README.md](docs/gallery/README.md).

## Showcase Shortcuts

- Workflow demos: [docs/workflows/README.md](docs/workflows/README.md)
- Outcome showcases: [docs/showcases/README.md](docs/showcases/README.md)
- Coverage dashboard: [docs/coverage-dashboard.md](docs/coverage-dashboard.md)
- Skills index: [docs/skills-index.md](docs/skills-index.md)

## Recommended Reading Order

If this is your first time with the bundle, open these in order:

1. [README.md](README.md)
2. `plugins/materials-skills/skills/materials-research/README.md`
3. the README for the production skill you actually need
4. if you plan to convert papers to patents,
   `plugins/materials-skills/skills/materials-paper-to-patent/README.md`

## Troubleshooting

- Installed skill seems stale:
  rerun `.\scripts\install.ps1`, then run the release checks again.
- Repo tests pass but Codex behaves like an older version:
  compare the skills under `plugins/materials-skills/skills/` with the installed
  skills.
- Journal facts are old:
  live-check official journal pages before submission advice.
- Search results look strong but claims still feel weak:
  treat search outputs as screening inputs, then rebuild the evidence chain with
  the reader skill before writing.

## npx skills compatibility / npx skills 兼容性

The [skills.sh](https://skills.sh) CLI discovers and installs this bundle
out of the box (verified with `skills` CLI on Node 24):

```bash
npx skills add cooleava1-gif/Materials-Science-Skills --list
npx skills add cooleava1-gif/Materials-Science-Skills   --agent claude-code --skill '*' --yes --copy
# valid agents include claude-code, codex, zcode, opencode, cursor, ...
```

**Boundary** 边界：`npx skills` copies raw skill directories; the two
`_shared` trees stay referenced as `../_shared/...` /
`../../_shared/...`, which do not resolve in that flat layout. Full
self-contained installs (shared trees merged into each skill, references
rewritten, MCP registered) come from `scripts/install_skills.py` — prefer
it. A single-shared-tree restructure that would make raw copies
self-contained is on the roadmap (203 cross-references affected).

## Auto-update 自动更新

Keep a dedicated clone and wire `scripts/autoupdate_skills.py` into a
session-start hook (throttled, offline-safe, fast-forward only). Hooks for
Claude Code, Codex, and other hosts: [docs/autoupdate.md](docs/autoupdate.md).

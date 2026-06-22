# Install Materials Science Skills

This guide is for the polished, day-to-day use of the bundle: install it, run a
five-minute workflow, verify the installed state, and avoid stale-skill drift
between the plugin source and the local Codex installation.

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
cwd = "."
```

Optional environment variables:

- `OPENALEX_API_KEY`
- `SEMANTIC_SCHOLAR_API_KEY`
- `CIVIL_MATERIALS_CONTACT_EMAIL`
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
Turn this paper package into a journal-club slide outline and then a real PPTX.
```

Expected shape:

1. `materials-paper2ppt` creates slide-ready Markdown.
2. `materials-pptx` turns the outline into a real PowerPoint deck.

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

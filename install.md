# Install Materials Science Skills

This guide is for the polished, day-to-day use of the bundle: install it, run a
five-minute workflow, verify the installed state, and avoid stale-skill drift
between the source repo, plugin mirror, and local Codex installation.

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
New-Item -ItemType Directory -Force $skillsDir | Out-Null
Copy-Item -Recurse -Force .\skills\materials-* $skillsDir
Copy-Item -Recurse -Force .\skills\_shared $skillsDir
```

## Optional Academic Search MCP

If you want the citation skill's local academic-search MCP, install the Python
dependencies first:

```powershell
python -m pip install -r .\requirements.txt
```

Example Codex MCP configuration:

```toml
[mcp_servers."materials-academic-search"]
command = "python"
args = ["$CODEX_HOME/skills/materials-citation/mcp/academic_search/server.py"]
```

Optional environment variables:

- `OPENALEX_API_KEY`
- `SEMANTIC_SCHOLAR_API_KEY`
- `CIVIL_MATERIALS_CONTACT_EMAIL`
- `NCBI_API_KEY`

## Verify The Install

Run the main release verification:

```powershell
python .\scripts\run_release_checks.py --json
```

Then check that the installed state is not stale:

1. If you changed root skill files, rerun `.\scripts\install.ps1`.
2. Confirm the plugin mirror under `plugins/materials-skills/skills/`
   still matches the source skills you edited.
3. Judge the release by the final JSON `status`, not by expected negative-test
   lines such as `source PDF not found: ...missing.pdf`.

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

## Guided Demo Routes

If you want a curated first-use path instead of jumping in cold, start here:

1. [WER-EA mini-review](docs/workflows/wer-ea-mini-review.md)
2. [Experimental manuscript](docs/workflows/experimental-manuscript.md)
3. [Revision loop](docs/workflows/revision-loop.md)
4. [Paper to presentation](docs/workflows/paper-to-presentation.md)

To see the visual proof side first, open [docs/gallery/README.md](docs/gallery/README.md).

## Showcase Shortcuts

If you already know the outcome you want, jump straight to:

1. [Submission package](docs/showcases/submission-package.md)
2. [Reviewer response](docs/showcases/reviewer-response.md)
3. [FAIR data package](docs/showcases/fair-data-package.md)

## Recommended Reading Order

If this is your first time with the bundle, open these in order:

1. [README.md](README.md)
2. [docs/skills-index.md](docs/skills-index.md)
3. `skills/materials-research/README.md`
4. the README for the production skill you actually need

## Troubleshooting

- Installed skill seems stale:
  rerun `.\scripts\install.ps1`, then run the release checks again.
- Repo tests pass but Codex behaves like an older version:
  compare source skills, plugin mirror skills, and installed skills.
- Journal facts are old:
  live-check official journal pages before submission advice.
- Search results look strong but claims still feel weak:
  treat search outputs as screening inputs, then rebuild the evidence chain with
  the reader skill before writing.

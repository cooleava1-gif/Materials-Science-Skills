# Materials Science Skills

A full-cycle Codex skill bundle for materials science research. It connects
routing, reading, citation, writing, figure production, data packaging,
reviewer simulation, response drafting, and PPTX generation into one workflow
instead of leaving each step as a separate prompt.

The bundle currently covers **29 material systems** across civil/construction,
polymers, metals, ceramics, and functional/nano materials. Each system carries
a narrative arc, figure scripts, reviewer criteria, and worked example packages
where the coverage tier has reached `full`.

![WER-EA figure proof board](plugins/materials-skills/skills/materials-figure/assets/showcase-proof/wer_ea_figure_proof_board.png)

## What the bundle does

1. **Routes** your request to the right material domain and production skill.
2. **Reads** papers into source-anchored evidence packages.
3. **Searches** literature through an MCP-backed academic search server.
4. **Writes** manuscript sections, review outlines, and argument chains.
5. **Polishes** prose with claim-strength calibration.
6. **Draws** journal-ready figures from CSV data and reader handoffs.
7. **Packages** data with FAIR checks and data-availability statements.
8. **Reviews** drafts like a peer reviewer before submission.
9. **Responds** to reviewer comments with point-by-point replies.
10. **Presents** papers as Chinese journal-club slide outlines or real `.pptx` decks.

## Quick Start

```powershell
codex plugin marketplace add https://github.com/cooleava1-gif/Materials-Science-Skills.git --ref main
codex plugin add materials-skills@materials-skills
```

Then start a Codex session and ask naturally:

- `Help me run a WER-EA mini-review from screening to figure planning.`
- `Audit this experimental manuscript for evidence gaps before the discussion.`
- `Turn this paper package into a journal-club slide outline and then a real PPTX.`

For manual install or MCP setup, see [install.md](install.md).

## The 12 skills

| Skill | What it produces |
|---|---|
| `materials-research` | Domain routing, topic angle, workflow plan, risk map |
| `materials-reader` | Source-anchored reader package, evidence-chain matrix |
| `materials-citation` | Screened citation matrix, normalized IDs, reference gaps |
| `materials-writing` | Manuscript sections, review outlines, argument chains |
| `materials-polishing` | Polished text, claim-strength audit, overclaim flags |
| `materials-figure` | Journal-ready SVG/PNG/PDF/TIFF figures from data |
| `materials-data` | FAIR package, data availability statement, metadata |
| `materials-doe` | Experiment plan, methods paragraph, analysis naming |
| `materials-reviewer` | Simulated peer review, desk-reject risk report |
| `materials-response` | Point-by-point response letter, rebuttal package |
| `materials-paper2ppt` | Slide-ready Markdown, talk structure |
| `materials-pptx` | Real `.pptx` deck |

More detail: [docs/skills-index.md](docs/skills-index.md).

## Material Coverage

| Tier | Count | Description |
|---|---|---|
| 🟢 **full** | 29 | Narrative guide + figure scripts + reviewer criteria + example packages |
| 🟡 **partial** | 0 | Narrative guide + at least one support resource |
| 🔵 **skeleton** | 0 | Domain fragment + auto-generated narrative |
| ⚪ **generic** | 0 | Family-level guidance only |

The 29 full systems span civil/construction, polymers, metals, ceramics, and
functional/nano materials. Full dashboard: [docs/coverage-dashboard.md](docs/coverage-dashboard.md).

## Guided demos

- [WER-EA mini-review](docs/workflows/wer-ea-mini-review.md)
- [Experimental manuscript](docs/workflows/experimental-manuscript.md)
- [Revision loop](docs/workflows/revision-loop.md)
- [Paper to presentation](docs/workflows/paper-to-presentation.md)

## Showcases

Ready-to-inspect result shapes:

- [Submission package](docs/showcases/submission-package.md)
- [Reviewer response](docs/showcases/reviewer-response.md)
- [FAIR data package](docs/showcases/fair-data-package.md)
- [Thermal insulation demo](docs/showcases/thermal-insulation-demo.md)
- [Polymer composites demo](docs/showcases/polymer-composites-demo.md)

## Four Workflow Entry Points

| Entry | Best for |
|---|---|
| WER-EA mini-review | Systematic review + figure planning for asphalt emulsion materials |
| Experimental manuscript | Evidence-gap audit before discussion drafting |
| Revision loop | Post-review response + rebuttal package |
| Paper to presentation | Journal-club PPT from a paper package |

## Installation Paths

```powershell
codex plugin marketplace add https://github.com/cooleava1-gif/Materials-Science-Skills.git --ref main
codex plugin add materials-skills@materials-skills
```

For manual install, see [install.md](install.md).

## Skills

See [docs/skills-index.md](docs/skills-index.md).

## Guided Demos

- [WER-EA mini-review](docs/workflows/wer-ea-mini-review.md)
- [Experimental manuscript](docs/workflows/experimental-manuscript.md)
- [Revision loop](docs/workflows/revision-loop.md)
- [Paper to presentation](docs/workflows/paper-to-presentation.md)

## Visual Gallery

See [docs/gallery/README.md](docs/gallery/README.md).

## Outcome Showcases

- [Submission package](docs/showcases/submission-package.md)
- [Reviewer response](docs/showcases/reviewer-response.md)
- [FAIR data package](docs/showcases/fair-data-package.md)
- [Thermal insulation demo](docs/showcases/thermal-insulation-demo.md)
- [Polymer composites demo](docs/showcases/polymer-composites-demo.md)

## Scope

This bundle structures materials research work with stronger evidence, routing,
and packaging discipline. It does not replace deep reading, real experimental
evidence, supervisor judgment, official journal instructions, or institutional
requirements.

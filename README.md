# Materials Science Skills

A full-cycle Codex skill bundle for materials science research. It connects
routing, reading, citation, writing, figure production, data packaging,
experiment design, reviewer simulation, response drafting, and PPTX generation
into one workflow instead of leaving each step as a separate prompt.

材料科学研究的全流程 Codex 技能包。把路由、阅读、引文检索、写作、配图、数据打包、
实验设计、审稿模拟、回复信撰写、PPT 生成串成一条工作流，而不是让每一步都成为孤立的提示。

The bundle currently covers **29 material systems** across civil/construction,
polymers, metals, ceramics, and functional/nano materials. Each system carries
a narrative arc, figure scripts, reviewer criteria, and worked example packages
where the coverage tier has reached `full`.

本技能包当前覆盖 **29 个材料体系**，涵盖土木/建筑、聚合物、金属、陶瓷、功能/纳米材料。
每个体系都带有叙事主线、配图脚本、审稿标准和完整示例包（`full` 覆盖等级）。

<table>
  <tr>
    <td align="center">
      <b>Chart-Type Atlas — 6 figure families</b><br/>
      <img width="720" alt="Chart-Type Atlas" src="docs/gallery/gallery_chart_atlas.png" />
    </td>
  </tr>
  <tr>
    <td align="center">
      <b>WER-EA Figures — dosage window, durability retention, evidence heatmap</b><br/>
      <img width="720" alt="WER-EA Research Workflow" src="docs/gallery/gallery_wer_ea_workflow.png" />
    </td>
  </tr>
  <tr>
    <td align="center">
      <b>Cross-Material-System Figures — ceramics characterization + thermal performance</b><br/>
      <img width="720" alt="Cross-Material-System Figures" src="docs/gallery/gallery_material_systems.png" />
    </td>
  </tr>
</table>

## What the bundle does

1. **Routes** your request to the right material domain and production skill.
2. **Reads** papers into source-anchored evidence packages.
3. **Searches** literature through an MCP-backed academic search server.
4. **Writes** manuscript sections, review outlines, and argument chains.
5. **Polishes** prose with claim-strength calibration.
6. **Draws** journal-ready figures from CSV data and reader handoffs.
7. **Packages** data with FAIR checks and data-availability statements.
8. **Designs** experiments with factorial, Taguchi, and mixture matrices.
9. **Reviews** drafts like a peer reviewer before submission.
10. **Responds** to reviewer comments with point-by-point replies.
11. **Presents** papers as Chinese journal-club slide outlines or real `.pptx` decks.

## Installation

### 1. Codex Plugin (recommended)

This repository includes Codex plugin packaging at `plugins/materials-skills/`,
so Codex users can install the complete bundle from the plugin marketplace
instead of copying each skill folder manually.

CLI installation:

```powershell
codex plugin marketplace add https://github.com/cooleava1-gif/Materials-Science-Skills.git --ref main
codex plugin add materials-skills@materials-skills
```

Codex Desktop users can add the same repository as a custom plugin marketplace:

- Marketplace source: `https://github.com/cooleava1-gif/Materials-Science-Skills.git`
- Branch/ref: `main`
- Plugin: `materials-skills`

After installation, all `materials-*` skills are available through the plugin
as a complete bundle, together with the shared support directory. If the skills
do not appear immediately, refresh the plugin page or start a new Codex session.

### 2. Manual Skills Install

Clone the repo and run the installer:

```powershell
git clone https://github.com/cooleava1-gif/Materials-Science-Skills.git
cd Materials-Science-Skills
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

### 3. Optional Academic Search MCP

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
- `CIVIL_MATERIALS_CONTACT_EMAIL`
- `NCBI_API_KEY`

For the full walkthrough, see [install.md](install.md).

## Skill index

| Skill | Status | Purpose | Trigger keywords |
|---|---|---|---|
| [`materials-research`](plugins/materials-skills/skills/materials-research/README.md) | Stable | Domain routing, topic angle, workflow plan, risk map | "materials research", "topic routing", "workflow plan" |
| [`materials-reader`](plugins/materials-skills/skills/materials-reader/README.md) | Stable | Source-anchored reader package, evidence-chain matrix | "reader package", "evidence chain", "paper notes" |
| [`materials-citation`](plugins/materials-skills/skills/materials-citation/README.md) | Stable | Screened citation matrix, normalized IDs, reference gaps | "citation matrix", "literature screening", "reference gap" |
| [`materials-writing`](plugins/materials-skills/skills/materials-writing/README.md) | Stable | Manuscript sections, review outlines, argument chains | "manuscript draft", "review outline", "argument chain" |
| [`materials-polishing`](plugins/materials-skills/skills/materials-polishing/README.md) | Stable | Polished text, claim-strength audit, overclaim flags | "polish", "claim strength", "academic tone" |
| [`materials-figure`](plugins/materials-skills/skills/materials-figure/README.md) | Stable | Journal-ready SVG/PNG/PDF/TIFF figures from data | "figure", "publication plot", "mechanism map" |
| [`materials-data`](plugins/materials-skills/skills/materials-data/README.md) | Stable | FAIR package, data availability statement, metadata | "FAIR package", "data availability", "dataset" |
| [`materials-doe`](plugins/materials-skills/skills/materials-doe/README.md) | Stable | Experiment plan, methods paragraph, analysis naming | "DOE", "experiment design", "orthogonal array" |
| [`materials-reviewer`](plugins/materials-skills/skills/materials-reviewer/README.md) | Stable | Simulated peer review, desk-reject risk report | "peer review", "desk-reject risk", "reviewer report" |
| [`materials-response`](plugins/materials-skills/skills/materials-response/README.md) | Stable | Point-by-point response letter, rebuttal package | "response letter", "rebuttal", "reviewer comment" |
| [`materials-paper2ppt`](plugins/materials-skills/skills/materials-paper2ppt/README.md) | Stable | Slide-ready Markdown, talk structure | "paper to slides", "journal club", "slide outline" |
| [`materials-pptx`](plugins/materials-skills/skills/materials-pptx/README.md) | Stable | Real `.pptx` deck | "pptx", "powerpoint", "slide deck" |

---

## materials-figure

**What it does** — Generates journal-ready multi-panel figures for materials
manuscripts: mechanism maps, evidence heatmaps, dosage-window plots,
characterization panels, review figures, and full figure packages with source
data, caption boundaries, and export QA. Python-only backend, SVG-first
output, with PNG/PDF/TIFF export bundles.

**Chart-type atlas** — The skill ships a chart-type atlas covering 6 chart
families: bar charts, line trends, heatmaps, radar/polar, scatter/bubble, and
distributions. Each family has bundled CSV data and a generated preview.

| ![Bar charts](plugins/materials-skills/skills/materials-figure/assets/chart-atlas/generated/atlas-bar-charts.png) | ![Line trends](plugins/materials-skills/skills/materials-figure/assets/chart-atlas/generated/atlas-line-trends.png) | ![Heatmaps](plugins/materials-skills/skills/materials-figure/assets/chart-atlas/generated/atlas-heatmaps.png) |
|---|---|---|
| ![Radar/polar](plugins/materials-skills/skills/materials-figure/assets/chart-atlas/generated/atlas-radar-polar.png) | ![Scatter/bubble](plugins/materials-skills/skills/materials-figure/assets/chart-atlas/generated/atlas-scatter-bubble.png) | ![Distributions](plugins/materials-skills/skills/materials-figure/assets/chart-atlas/generated/atlas-distributions.png) |

**WER-EA atlas** — A 20-panel atlas for waterborne epoxy resin modified
emulsified asphalt research, from screening flow and evidence heatmap to
mechanism map, dosage window, graphical abstract, and research gap. SVG
templates carry the full panel structure, certainty-tier legend, and claim
boundary; GitHub renders them inline.

| ![Screening flow](plugins/materials-skills/skills/materials-figure/assets/wer-ea-atlas/generated/wer_ea_screening_flow.svg) | ![Evidence heatmap](plugins/materials-skills/skills/materials-figure/assets/wer-ea-atlas/generated/wer_ea_evidence_heatmap.svg) | ![Mechanism map](plugins/materials-skills/skills/materials-figure/assets/wer-ea-atlas/generated/wer_ea_mechanism_map.svg) |
|---|---|---|
| ![Dosage window](plugins/materials-skills/skills/materials-figure/assets/wer-ea-atlas/generated/wer_ea_dosage_window.svg) | ![Graphical abstract](plugins/materials-skills/skills/materials-figure/assets/wer-ea-atlas/generated/wer_ea_graphical_abstract.svg) | ![Research gap](plugins/materials-skills/skills/materials-figure/assets/wer-ea-atlas/generated/wer_ea_research_gap.svg) |

**Ceramics atlas** — Characterization figures for structural/functional
ceramics: XRD patterns, stress-strain curves, TGA/DSC, thermal expansion,
Weibull plots, grain-size distributions, EIS Nyquist plots, and sintering
curves.

| ![XRD pattern](plugins/materials-skills/skills/materials-figure/assets/ceramics-atlas/generated/ceramics_xrd_pattern.png) | ![Stress-strain](plugins/materials-skills/skills/materials-figure/assets/ceramics-atlas/generated/ceramics_stress_strain.png) | ![TGA/DSC](plugins/materials-skills/skills/materials-figure/assets/ceramics-atlas/generated/ceramics_tga_dsc.png) |
|---|---|---|
| ![Thermal expansion](plugins/materials-skills/skills/materials-figure/assets/ceramics-atlas/generated/ceramics_thermal_expansion.png) | ![Weibull plot](plugins/materials-skills/skills/materials-figure/assets/ceramics-atlas/generated/ceramics_weibull_plot.png) | ![Grain size](plugins/materials-skills/skills/materials-figure/assets/ceramics-atlas/generated/ceramics_grain_size_dist.png) |

**Figure package structure** — Every serious output is delivered as a figure
package, not a loose image:

```text
figure-package/
  figure_contract.md
  source_data.csv
  plot.py
  figure.svg
  figure.pdf
  figure.png
  figure.tiff
  caption.md
  qa_report.md
  asset_manifest.md
```

**Key rules enforced**

- Python-only plotting backend; no silent fallback to another stack.
- Figure contract written before plotting: core conclusion, evidence chain,
  panel map, target journal, statistics/units/scale bars, claim boundary.
- Caption boundaries separate measured from inferred claims.
- Export bundle includes SVG, PDF, PNG, and TIFF when possible.
- QA report covers Python backend exclusivity, export checks, and caption
  boundary.

---

## materials-writing

**What it does** — Turns claims, results, notes, and outlines into argument
chains, abstracts, introductions, results/discussion sections, conclusions, or
review outlines while keeping missing evidence visible. Built for materials
science manuscripts across civil/construction, polymers, metals, ceramics, and
functional/nano materials.

**Key rules enforced**

- Argument chain before prose: claim → evidence → mechanism → boundary.
- Missing evidence stays visible as explicit gaps, not hidden hedging.
- Section-aware tense and hedging: past tense for results, present for
  established knowledge, hedged for inferred mechanisms.
- Review outlines separate synthesis structure from borrowed structure.

---

## materials-doe

**What it does** — Design-of-experiments planning and matrix generation for
civil engineering and construction materials research. Supports classical
factorial, Taguchi orthogonal array, and mixture/simplex designs with factor
screening and response surface extensions.

**Outputs**

| Output | Description |
|---|---|
| Test matrix | Factor-level table in CSV or markdown |
| Analysis strategy | Notes on ANOVA, S/N ratio, or RSM approach |
| DOE handoff | Structured handoff for downstream skills |
| Methods paragraph | Ready-to-paste experimental methods section |

**Usage examples**

- "Design an L9 orthogonal array for asphalt modifier dosage, curing time, and temperature"
- "Generate a mix design matrix for three-component mortar system"
- "Plan a factorial experiment for concrete durability factors"

**Boundaries** — This skill plans experiments and generates matrices. It does
not execute tests, analyze collected data, or produce manuscript text. For
data analysis or figure production, hand off to `materials-data` or
`materials-figure`.

---

## materials-citation

**What it does** — Literature search strategy, source screening, citation
matrices, reference-gap audits, ID normalization, and claim-source alignment.
Its MCP-backed search tools query academic sources and export structured
citation evidence with evidence layer, source role, source quality, reader
anchor, figure handoff, and reviewer-risk fields.

**MCP academic search** — The bundled MCP server queries Crossref, OpenAlex,
Semantic Scholar, PubMed, arXiv, Scopus, and ScienceDirect, with domain
classification for materials science. Exports BibTeX, CSL-JSON, RIS, and JSONL.

---

## materials-reviewer

**What it does** — Simulates peer review before submission or resubmission.
Checks novelty and evidence sufficiency, flags figure/statistics gaps, and
produces reviewer-style reports with editorial criteria for the material
domain. Outputs a desk-reject risk report so weak packages get routed back to
reader, citation, writing, or figure work before submission.

---

## materials-response

**What it does** — After reviewer comments arrive, separates response tone
from manuscript action, drafts point-by-point replies, and prevents
unsupported promises such as claiming new experiments were completed. Outputs
a response letter plus a rebuttal package with action items and risk flags.

---

## materials-data

**What it does** — Raw/processed dataset organization, metadata, FAIR checks,
supplementary data packaging, and data availability statements. Outputs a FAIR
package with audit report, dataset README, metadata template, and
journal-ready data availability statement.

---

## materials-reader

**What it does** — Use when the raw material is a paper, PDF, abstract,
figure caption, or pasted text. Produces standard reader packages,
source-grounded notes, figure/table evidence maps,
claim-evidence-mechanism-boundary matrices, and handoff rows for citation and
figure skills.

---

## materials-polishing

**What it does** — Use after text exists. Handles English polishing,
Chinese-to-English academic rewriting, claim-strength control, overclaim
reduction, and journal-tone tightening. Outputs polished text plus a
claim-strength audit that flags overclaims and unsupported hedging.

---

## materials-paper2ppt & materials-pptx

**What it does** — `materials-paper2ppt` converts papers, reading notes,
review matrices, and research outlines into slide-ready Markdown. It is the
handoff layer before real PowerPoint generation. `materials-pptx` then turns
structured Markdown or JSON slide specs into a real `.pptx` deck with notes
and image placement.

---

## materials-research

**What it does** — Front door for broad materials work. Detects task type,
material domain, and journal family, then hands off to the right companion
skill. Best for topic positioning, journal fit, paper strategy, reviewer-risk
framing, and combined workflows such as mini-review plus figure planning.

---

## Visual Gallery

See [docs/gallery/README.md](docs/gallery/README.md) for editorial proof boards
and figure-package previews.

## Four Workflow Entry Points

| Entry | Best for |
|---|---|
| WER-EA mini-review | Systematic review + figure planning for asphalt emulsion materials |
| Experimental manuscript | Evidence-gap audit before discussion drafting |
| Revision loop | Post-review response + rebuttal package |
| Paper to presentation | Journal-club PPT from a paper package |

## Scope

This bundle structures materials research work with stronger evidence, routing,
and packaging discipline. It does not replace deep reading, real experimental
evidence, supervisor judgment, official journal instructions, or institutional
requirements.

## Acknowledgements

The repository structure, skill-bundle packaging approach, and README layout
of this project are inspired by [nature-skills](https://github.com/Yuan1z0825/nature-skills)
by Yizhe Yuan. The Codex plugin marketplace distribution pattern, the
per-skill detail section format, and the chart-type atlas concept in
`materials-figure` draw on the design patterns established by nature-skills.
We thank the nature-skills project for demonstrating a clean, reusable model
for shipping academic skill bundles as Codex plugins.

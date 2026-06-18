# Skills Index

Pick a skill by deliverable. Start with `materials-research` when the task is
broad, the material domain is unclear, or you need a multi-skill workflow.
Jump straight to a production skill when the output is already defined.

## Status

All 12 skills are now at **Stable**. The bundle has moved past early draft
stages into daily-use production tooling.

| Skill | Typical input | Typical product |
|---|---|---|
| `materials-research` | Research idea, journal target, manuscript task | Route, topic angle, risk map, workflow plan |
| `materials-reader` | PDF, paper notes, figure captions | Reader package, evidence-chain matrix |
| `materials-citation` | Topic, claim list, candidate sources | Search plan, screened citation matrix, ID conversion |
| `materials-writing` | Claims, results, outline, Chinese draft | Manuscript section, review outline, argument chain |
| `materials-polishing` | English draft, Chinese academic paragraph | Polished text, claim-strength audit |
| `materials-figure` | Data table, handoff row, figure idea | SVG/PNG/PDF/TIFF figure, caption boundary |
| `materials-data` | Raw/processed data, metadata needs | FAIR package, data availability statement |
| `materials-doe` | Experiment factors, responses | Methods paragraph, analysis script |
| `materials-reviewer` | Manuscript draft, abstract, figures | Simulated review, desk-reject risk report |
| `materials-response` | Reviewer comments, revision notes | Point-by-point response, rebuttal package |
| `materials-paper2ppt` | Paper notes, review matrix, outline | Slide-ready Markdown, talk structure |
| `materials-pptx` | PPTX-ready Markdown or JSON | Real `.pptx` deck |

## How routing works

`materials-research` uses two axes:

1. **Material family**: civil, ceramics, metals, polymers, functional, nano.
2. **Domain**: one of 52 specific material systems such as `thermal-insulation`,
   `cement-concrete`, `polymer-composites`, or `2d-materials`.

If your domain is registered, the skill loads the matching narrative arc,
figure archetypes, and reviewer criteria. If not, it falls back to family-level
guidance.

## Skill notes

### `materials-research`

Front door for broad materials work. Detects task type, material domain, and
journal family, then hands off to the right companion skill. Best for topic
positioning, journal fit, paper strategy, reviewer-risk framing, and combined
workflows such as mini-review plus figure planning.

### `materials-reader`

Use when the raw material is a paper, PDF, abstract, figure caption, or pasted
text. Produces standard reader packages, source-grounded notes, figure/table
evidence maps, claim-evidence-mechanism-boundary matrices, and handoff rows for
citation and figure skills.

### `materials-citation`

Use for literature search strategy, source screening, citation matrices,
reference-gap audits, ID normalization, and claim-source alignment. Its
MCP-backed search tools query academic sources and export structured citation
evidence with evidence layer, source role, source quality, reader anchor, figure
handoff, and reviewer-risk fields.

### `materials-writing`

Use when the deliverable is manuscript text or a review-paper structure. Turns
claims, results, notes, and outlines into argument chains, abstracts,
introductions, results/discussion sections, conclusions, or review outlines while
keeping missing evidence visible.

### `materials-polishing`

Use after text exists. Handles English polishing, Chinese-to-English academic
rewriting, claim-strength control, overclaim reduction, and journal-tone
tightening.

### `materials-figure`

Use for figure planning, chart design, review-figure intake, figure-package
audits, SVG/PNG/PDF/TIFF generation, caption boundaries, and visual evidence
checks. Includes dedicated figure scripts for 29 material systems and WER-EA
atlas templates that separate measured, inferred, speculative, and missing
evidence.

### `materials-data`

Use for raw/processed dataset organization, metadata, FAIR checks,
supplementary data packaging, and data availability statements.

### `materials-doe`

Use for experiment design, methods paragraph drafting, factor-level naming, and
response-variable description.

### `materials-reviewer`

Use before submission or resubmission. Simulates peer review, checks novelty and
evidence sufficiency, flags figure/statistics gaps, and produces reviewer-style
reports with editorial criteria for the material domain.

### `materials-response`

Use after reviewer comments arrive. Separates response tone from manuscript
action, drafts point-by-point replies, and prevents unsupported promises such as
claiming new experiments were completed.

### `materials-paper2ppt`

Use to convert papers, reading notes, review matrices, and research outlines
into slide-ready Markdown. The handoff layer before real PowerPoint generation.

### `materials-pptx`

Use when a real `.pptx` file is needed. Converts structured Markdown or JSON
slide specs into PowerPoint decks with notes and image placement.

## WER-EA mini-review route

For waterborne epoxy resin modified emulsified asphalt, the cross-skill route
is:

1. `materials-research`: define the review question, scope, inclusion/exclusion
   boundary, and submission route.
2. `materials-citation`: run expanded literature screening and build a
   claim-source matrix.
3. `materials-reader`: extract mechanism evidence chains into a standard reader
   package, separating bonding, rheology, emulsion stability, microstructure,
   durability, and field/service evidence.
4. `materials-writing`: convert the evidence matrix into a review outline,
   section argument chain, and bounded draft.
5. `materials-figure`: plan mechanism maps, evidence heatmaps, study-selection
   flow, graphical abstracts, and performance-mechanism boundary figures.
6. `materials-polishing` and `materials-reviewer`: tighten claim strength and
   audit submission risk before journal targeting.

Typical product: a source-grounded mini-review package with screened literature,
mechanism evidence chain, review outline, figure planning notes, and submission
route.

## Coverage tiers

| Tier | Meaning |
|---|---|
| `full` | Narrative guide + figure scripts + reviewer criteria + example packages |
| `partial` | Narrative guide + at least one support resource |
| `skeleton` | Domain fragment + auto-generated narrative |
| `generic` | Family-level guidance only |

All 29 registered systems are currently at `full`. The dashboard is at
[coverage-dashboard.md](coverage-dashboard.md).

# Human-Readable Skills Index

This index is for people deciding which materials skill to use before invoking Codex. The short rule is: start with `materials-research` when the task needs routing or research judgment, then hand off to the production skill that owns the deliverable.

## Status Table

| Module | Maturity | Scripts | Tests | Typical input | Typical product |
|---|---|---|---|---|---|
| `materials-research` | Stable router | Yes | Yes | Research idea, journal target, manuscript task | Route, topic angle, risk map, workflow plan |
| `materials-reader` | Stable production skill | Yes | Yes | PDF/text, paper notes, figure caption | Standard reader package, evidence-chain matrix, citation/figure handoff |
| `materials-citation` | Stable MCP-backed skill | Yes | Yes | Topic, claim list, candidate sources | Search plan, screened citation matrix, reference gaps, ID/citation conversion |
| `materials-writing` | Stable production skill | Yes | Yes | Claims, results, outline, Chinese draft | Manuscript section, review outline, argument chain |
| `materials-polishing` | Stable production skill | Yes | Yes | English draft, Chinese academic paragraph | Polished text, claim-strength audit |
| `materials-response` | Stable production skill | Yes | Yes | Reviewer comments, revision notes | Point-by-point response, rebuttal package |
| `materials-reviewer` | Stable audit skill | Yes | Yes | Manuscript draft, abstract, figures | Simulated review, desk-reject risk report |
| `materials-paper2ppt` | Stable handoff skill | Yes | Yes | Paper notes, review matrix, outline | Slide-ready Markdown, talk structure |
| `materials-pptx` | Stable generation skill | Yes | Yes | PPTX-ready Markdown or JSON | Real `.pptx` deck |
| `materials-figure` | Stable production skill | Yes | Yes | Data table, reader/citation handoff, figure idea | Figure plan, review-figure intake, WER-EA atlas, SVG/PNG package, caption boundary |
| `materials-data` | Stable FAIR skill | Yes | Yes | Raw/processed data, metadata needs | FAIR package, data availability statement |

## Material Coverage Tiers

When you start research with `materials-research`, the router checks your
material domain's **coverage tier**. This determines what the AI can offer:

| Tier | Icon | What the AI knows |
|---|---|---|
| **full** | 🟢 | Deep narrative guide, dedicated figure scripts, reviewer criteria, worked examples |
| **partial** | 🟡 | Narrative guide + at least one support resource (figures or reviewer criteria) |
| **skeleton** | 🔵 | Domain fragment + auto-generated narrative template |
| **generic** | ⚪ | General materials science guidance only |

The full coverage dashboard is at [docs/coverage-dashboard.md](docs/coverage-dashboard.md).

## Module Notes

### `materials-research`

Use this as the front door for broad materials research work. It detects task, material domain, and journal family, then routes to the correct companion skill. It is best for topic positioning, journal fit, paper strategy, reviewer-risk framing, and combined workflows such as literature review plus figure planning.

### `materials-reader`

Use this when the raw material is a paper, PDF, abstract, figure caption, or pasted source text. It produces standard reader packages, source-grounded notes, figure/table evidence maps, claim-evidence-mechanism-boundary matrices, citation handoff rows, figure handoff rows, and review-ready reading artifacts.

### `materials-citation`

Use this for literature search strategy, WER-EA source screening, citation matrices, reference-gap audits, ID normalization, citation-file conversion, and claim-source alignment. Its MCP-backed search tools can query academic sources and export structured citation evidence with evidence layer, source role, source quality, reader anchor, figure handoff, and reviewer-risk fields.

### `materials-writing`

Use this when the deliverable is manuscript text or a review-paper structure. It turns claims, results, notes, and outlines into argument chains, abstracts, introductions, results/discussion sections, conclusions, or review outlines while keeping missing evidence visible.

### `materials-polishing`

Use this after text exists. It handles English polishing, Chinese-to-English academic rewriting, claim-strength control, overclaim reduction, and journal-tone tightening.

### `materials-response`

Use this after reviewer comments arrive. It separates response tone from manuscript action, drafts point-by-point replies, and prevents unsupported promises such as claiming new experiments were completed.

### `materials-reviewer`

Use this before submission or resubmission. It simulates peer review, checks novelty and evidence sufficiency, flags figure/statistics gaps, and produces reviewer-style reports.

### `materials-paper2ppt`

Use this to convert papers, reading notes, review matrices, and research outlines into slide-ready Markdown. It is the handoff layer before real PowerPoint generation.

### `materials-pptx`

Use this when a real `.pptx` file is needed. It converts structured Markdown or JSON slide specs into PowerPoint decks with notes and image placement.

### `materials-figure`

Use this for figure planning, chart design, review-figure intake, WER-EA atlas templates, figure-package audits, SVG/PNG generation examples, caption boundaries, and visual evidence checks. For WER-EA review figures, it separates measured, inferred, speculative, and missing evidence.

### `materials-data`

Use this for raw/processed dataset organization, metadata, FAIR checks, supplementary data packaging, and data availability statements.

## WER-EA Mini-Review Route

For waterborne epoxy resin modified emulsified asphalt, use this cross-skill route:

1. `materials-research`: define the WER-EA review question, scope, inclusion/exclusion boundary, and submission route.
2. `materials-citation`: run expanded literature screening and build a claim-source matrix with evidence layer, source role, source quality, normalized IDs, reader anchor, figure handoff, and reviewer-risk fields.
3. `materials-reader`: extract the mechanism evidence chain from each paper into a standard reader package, separating bonding, rheology, emulsion stability, microstructure, durability, and field/service evidence, then produce citation and figure handoff rows.
4. `materials-writing`: convert the evidence matrix into a review outline, section argument chain, and bounded draft.
5. `materials-figure`: intake reader/citation handoff rows, then use the WER-EA atlas to plan mechanism maps, evidence heatmaps, study-selection flow, graphical abstracts, and performance-mechanism boundary figures with measured/inferred/speculative/missing evidence visibly separated.
6. `materials-polishing` and `materials-reviewer`: tighten claim strength and audit submission risk before journal targeting.

Typical product: a source-grounded mini-review package with screened literature, mechanism evidence chain, review outline, figure planning notes, and submission route.

# Human-Readable Skills Index

This index is for people deciding which civil-materials skill to use before invoking Codex. The short rule is: start with `civil-materials-research` when the task needs routing or research judgment, then hand off to the production skill that owns the deliverable.

## Status Table

| Module | Maturity | Scripts | Tests | Typical input | Typical product |
|---|---|---|---|---|---|
| `civil-materials-research` | Stable router | Yes | Yes | Research idea, journal target, manuscript task | Route, topic angle, risk map, workflow plan |
| `civil-materials-reader` | Stable production skill | Yes | Yes | PDF/text, paper notes, figure caption | Source-grounded reader, evidence-chain matrix |
| `civil-materials-citation` | Stable MCP-backed skill | Yes | Yes | Topic, claim list, candidate sources | Search plan, citation matrix, reference gaps |
| `civil-materials-writing` | Stable production skill | Yes | Yes | Claims, results, outline, Chinese draft | Manuscript section, review outline, argument chain |
| `civil-materials-polishing` | Stable production skill | Yes | Yes | English draft, Chinese academic paragraph | Polished text, claim-strength audit |
| `civil-materials-response` | Stable production skill | Yes | Yes | Reviewer comments, revision notes | Point-by-point response, rebuttal package |
| `civil-materials-reviewer` | Stable audit skill | Yes | Yes | Manuscript draft, abstract, figures | Simulated review, desk-reject risk report |
| `civil-materials-paper2ppt` | Stable handoff skill | Yes | No | Paper notes, review matrix, outline | Slide-ready Markdown, talk structure |
| `civil-materials-pptx` | Stable generation skill | Yes | No | PPTX-ready Markdown or JSON | Real `.pptx` deck |
| `civil-materials-figure` | Stable production skill | Yes | Yes | Data table, figure idea, caption | Figure plan, SVG/PNG examples, caption boundary |
| `civil-materials-data` | Stable FAIR skill | Yes | Yes | Raw/processed data, metadata needs | FAIR package, data availability statement |

## Module Notes

### `civil-materials-research`

Use this as the front door for broad civil-materials research work. It detects task, material domain, and journal family, then routes to the correct companion skill. It is best for topic positioning, journal fit, paper strategy, reviewer-risk framing, and combined workflows such as literature review plus figure planning.

### `civil-materials-reader`

Use this when the raw material is a paper, PDF, abstract, figure caption, or pasted source text. It produces source-grounded notes, figure/table evidence maps, claim-evidence-mechanism-boundary matrices, and review-ready reading artifacts.

### `civil-materials-citation`

Use this for literature search strategy, source screening, citation matrices, reference-gap audits, and claim-source alignment. Its MCP-backed search tools can query academic sources and export structured citation evidence.

### `civil-materials-writing`

Use this when the deliverable is manuscript text or a review-paper structure. It turns claims, results, notes, and outlines into argument chains, abstracts, introductions, results/discussion sections, conclusions, or review outlines while keeping missing evidence visible.

### `civil-materials-polishing`

Use this after text exists. It handles English polishing, Chinese-to-English academic rewriting, claim-strength control, overclaim reduction, and journal-tone tightening.

### `civil-materials-response`

Use this after reviewer comments arrive. It separates response tone from manuscript action, drafts point-by-point replies, and prevents unsupported promises such as claiming new experiments were completed.

### `civil-materials-reviewer`

Use this before submission or resubmission. It simulates peer review, checks novelty and evidence sufficiency, flags figure/statistics gaps, and produces reviewer-style reports.

### `civil-materials-paper2ppt`

Use this to convert papers, reading notes, review matrices, and research outlines into slide-ready Markdown. It is the handoff layer before real PowerPoint generation.

### `civil-materials-pptx`

Use this when a real `.pptx` file is needed. It converts structured Markdown or JSON slide specs into PowerPoint decks with notes and image placement.

### `civil-materials-figure`

Use this for figure planning, chart design, figure-package audits, SVG/PNG generation examples, caption boundaries, and visual evidence checks.

### `civil-materials-data`

Use this for raw/processed dataset organization, metadata, FAIR checks, supplementary data packaging, and data availability statements.

## WER-EA Mini-Review Route

For waterborne epoxy resin modified emulsified asphalt, use this cross-skill route:

1. `civil-materials-research`: define the WER-EA review question, scope, inclusion/exclusion boundary, and submission route.
2. `civil-materials-citation`: run literature screening and build a claim-source matrix.
3. `civil-materials-reader`: extract the mechanism evidence chain from each paper, separating bonding, rheology, emulsion stability, microstructure, durability, and field/service evidence.
4. `civil-materials-writing`: convert the evidence matrix into a review outline, section argument chain, and bounded draft.
5. `civil-materials-figure`: plan mechanism maps, evidence heatmaps, study-selection flow, and performance-mechanism boundary figures.
6. `civil-materials-polishing` and `civil-materials-reviewer`: tighten claim strength and audit submission risk before journal targeting.

Typical product: a source-grounded mini-review package with screened literature, mechanism evidence chain, review outline, figure planning notes, and submission route.

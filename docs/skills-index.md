# Skills Index

This index lists all 16 installable `materials-*` skills, their key rules and
output structures. 本页收录全部 16 个技能的定位、关键规则与输出结构。

| Skill | Primary role | Typical handoff |
|---|---|---|
| `materials-research` | Router and paper-production orchestrator | All companion skills |
| `materials-reader` | Source-grounded reader package | citation, writing, figure |
| `materials-citation` | Search strategy and citation matrix | reader, writing |
| `materials-literature-pipeline` | Recurring discovery and source-depth triage | research, reader, citation |
| `materials-paper-card` | Fixed 16-section deep-reading card | reader, citation, research |
| `materials-writing` | Stateful manuscript sections and argument chains | polishing, reviewer |
| `materials-polishing` | Claim-strength and language tightening | reviewer, response |
| `materials-figure` | Figure contracts and publication plots | writing, data |
| `materials-data` | FAIR dataset package | writing, figure |
| `materials-doe` | Experiment design matrices | data, writing |
| `materials-statistics` | Statistical reporting audit and drafting | doe, reviewer, polishing, response |
| `materials-reviewer` | Simulated peer review and risk report | response, writing |
| `materials-response` | Point-by-point rebuttal package | writing, polishing |
| `materials-html-deck` | Slide-ready outline and verified HTML academic deck | figure |
| `materials-paper-to-patent` | Chinese invention-patent draft | figure, data |
| `materials-submission` | Route C assembly for 10 supported journal templates | research, writing, figure, data |

## Profile-first routing

The bundle follows a **profile-first routing** protocol defined in
`_shared/core/direction-profile.md`. On first use, the router asks the user
once for their current materials research direction, saves it to a user-local
file `.materials/profile.yaml` (not tracked by git), and uses it to set
defaults for `material_family` and `domain` across all 16 skills.

| Layer | Source | Behaviour |
|---|---|---|
| 1 | Explicit direction in the current user request | Used immediately |
| 2 | `.materials/profile.yaml` saved locally | Default fallback |
| 3 | Neutral / general materials support | Last-resort fallback |

## Skill details

### materials-research — the router

- Front door of the bundle: detects task type, material domain, and journal
  family, then hands off to the right companion skill.
- **Fragment system** (manifest-defined): `task` (17), `domain` (**36**),
  `journal` (20) axes drive routing decisions.
- Every output is a **6-stage gated plan** (positioning → reading → citation →
  writing → polishing → reviewer/response) with explicit handoff rows plus a
  `coverage_tier` report (`full` / `partial` / `skeleton` / `generic`).

### materials-reader

- Raw material: a paper, PDF, abstract, figure caption, or pasted text.
- Produces standard reader packages, source-grounded notes, figure/table
  evidence maps, claim-evidence-mechanism-boundary matrices, and handoff rows
  for citation and figure skills. Has its own `evals.json`.
- **Interactive bilingual HTML reading page** (1.4.0): for full-paper
  translation requests ("生成中文版", "全文翻译", "可交互双语网页") it emits a
  Chinese-first page built from `assets/templates/bilingual-reader-template.html`
  following `references/bilingual-html-reader.md` — sentence-level English-Chinese
  alignment with hover/focus to reveal the English source, figures/tables/
  captions/hierarchy preserved. It is an output format of the reader, reusing
  the same `source_map.json` and terminology ledger, not a separate skill.

### materials-citation — search, screen, structure

- Literature search strategy, source screening, citation matrices,
  reference-gap audits, ID normalisation, and claim-source alignment.
- **Reference verification** (1.2.0): field-by-field multi-source cross-check
  via the academic-search MCP — volume-year vs DOI-year conflicts,
  hallucinated first authors, order anomalies, page drift — with a
  structured OK/WARN/ERROR report and Zotero-style fix suggestions.
- **MCP academic search**: queries Crossref, OpenAlex, Semantic Scholar,
  PubMed, arXiv, Scopus, and ScienceDirect with materials-domain
  classification; exports BibTeX, CSL-JSON, RIS, and JSONL. A 13-test unit
  suite covers MCP adapters, search-plan generators, and fallback paths.

### materials-literature-pipeline

- Recurring literature discovery with materials-specific candidate scoring,
  source-depth triage, deduplication, digest delivery, degradation handling,
  and next-reading actions.

### materials-writing — the 8-axis stateful manuscript engine

- Turns claims, results, notes, and outlines into argument chains, abstracts,
  introductions, results/discussion, conclusions, or review outlines while
  keeping missing evidence visible.
- **Eight axes**: `writing_mode` (compose/revise/hybrid/qa), `paper_type`,
  `section`, `language` (zh/en), `journal_family`, `material_family`, `domain`,
  `input_source` (manual/experiment-record).
- Reference corpus: narrative references, state-machine references, 5 section
  arcs, domain phrase banks, domain paragraph patterns.
- Key rules: argument chain before prose; `state.json` tracks mode/round/
  scores/technical debts/stop status; revision loops stop on round limit, low
  score gain, missing key evidence, unresolved specialist conflict, or target
  reached; past tense for results, present for established knowledge, hedged
  for inferred mechanisms.

### materials-polishing

- English polishing, Chinese-to-English academic rewriting, claim-strength
  control, overclaim reduction, journal-tone tightening.
- Outputs polished text plus a claim-strength audit; ships 22 references
  including the `claim-strength-ladder` (causal / associative / correlative /
  speculative) and domain language rulebooks. Has its own `evals.json`.

### materials-figure — the flagship

- LLM-driven figure creation: validates a **figure contract** and source-data
  anchor first, then the LLM writes `plot.py` from the contract, data,
  chart-atlas reference, legend rules, and reviewer-risk notes.
- Pipeline: `figure_contract.md → source_data.csv → LLM writes plot.py →
  figure.svg/pdf/png/tiff → caption.md + qa_report.md + asset_manifest.md`.
- Key rules: exclusive plotting backend per package (Python default, R
  opt-in with persisted preference) for data plots; **conceptual/schematic
  figures default to R hybrid composition** (2.6.0) — a user-provided AI
  image model (GPT Image 2, nanobanana, or self-generated assets) generates
  watermark-stripped, transparent decoration assets only, while R draws
  every text, border, arrow, and annotation as editable vector
  (`asset_manifest.yaml` placement map + text-vector + watermark QA); a
  standalone AI draft is produced only on explicit request (OpenRouter/GPT
  Image 2 AI-schematic route, provenance-tracked, never data panels); with
  no AI tool the skill explains and falls back to R/Python-only drawing
  with procedural decorations; contract written before plotting
  (core conclusion, evidence chain, panel map, target journal,
  statistics/units/scale bars, claim boundary); caption boundaries separate
  measured from inferred claims; QA report covers backend exclusivity, export
  checks, and caption boundary.
- Lightweight preview boards ship in `docs/gallery/`; the generated
  atlas/gallery/showcase image corpus is not part of the installable bundle.

### materials-data — FAIR packaging with 9 domain schemas

- Raw/processed dataset organisation, metadata, FAIR checks, supplementary
  packaging, journal-ready data-availability statements.
- **Nine domain schemas**: `asphalt`, `cement-concrete`, `ceramics`, `civil`,
  `functional`, `metals`, `nano`, `polymers`, `thermal-insulation` — each with
  canonical CSV column order, FAIR metadata fields, and a
  data-availability statement template adapted to common target journals.

### materials-doe

- Design-of-experiments planning: classical factorial, Taguchi orthogonal
  array, and mixture/simplex designs with factor screening and response
  surface extensions.
- Outputs: test matrix (CSV/markdown), analysis strategy (ANOVA / S/N / RSM),
  structured DOE handoff, and a ready-to-paste methods paragraph.
- Boundary: plans experiments and generates matrices; does not execute tests,
  analyse data, or produce manuscript text (hand off to `materials-data` /
  `materials-figure`).

### materials-statistics — statistical reporting gate

- Audits, revises, and drafts statistical reporting for materials
  manuscripts: replicate and `n` definitions, design-matched tests
  (factorial ANOVA with interactions, Taguchi S/N with a stated error term,
  RSM with lack-of-fit, Scheffé mixture models), multiple-comparison
  corrections, effect sizes with uncertainty, and figure-statistics
  alignment (SD/SEM/CI declared, per-panel n, named corrections).
- **Three blocking gates**: replication-gate (never infer n from reading,
  image, or scan counts), invention-gate (never invent p-values, dfs, CIs,
  software versions), boundary-gate (computation only on user-supplied data
  with an explicit request).
- Materials replication contexts: specimens vs repeated readings vs nested
  batch subspecimens, durability repeated measures, semi-quantitative
  microanalysis (XRD RIR / EDS), standards (ASTM / ISO / GB) that prescribe
  replicate counts.
- Outputs the core format (scope, P0/P1/P2 issues, ready-to-paste revision,
  AUTHOR_INPUT_NEEDED, reviewer-risk note); hands design work to
  `materials-doe`, re-plotting to `materials-figure`, wording to
  `materials-polishing`, reply assembly to `materials-response`.

### materials-paper-card — the 16-section deep-reading card

- Turns one materials paper (PDF, DOI page, pasted text, or a
  `materials-reader` package) into a source-grounded reading card with
  fixed Sections 01-16: bibliographic position, research question,
  background route, pain point, core insight, material system and
  processing route, method logic, essential formulas,
  experiment-to-claim evidence chain, characterization-chain reading,
  conclusion boundaries, author-stated limitations, critical analysis,
  learned knowledge, knowledge connections, gated research ideas.
- **Three locator modes** (page-grounded / structure-grounded /
  source-limited) plus context modes (paper-only / targeted external
  check / externally verified) keep citations honest; unsupported
  sections are `Not assessable`, never invented.
- Materials-first: Section 06 (material system, mix design, processing)
  and Section 10 (XRD / FTIR / SEM / TG chain, reported-not-verified).
- Section 16 ideas pass gap / testability / boundary / reuse gates and
  hand off to `materials-research`. Has its own `evals.json`.

### materials-reviewer — peer review with 22 domain criteria

- Simulates peer review before submission: checks novelty and evidence
  sufficiency, flags figure/statistics gaps, produces reviewer-style reports
  and a desk-reject risk report.
- **Five review axes**: originality / importance / interdisciplinary /
  technical validity / readability.
- **Twenty-two domain criteria** covering the typical reviewer concerns per
  material sub-direction (asphalt, cement, ceramics, construction-materials,
  civil-generic, waterproofing-sealants, timber-masonry, steel, geotechnical,
  nano, nano-thin-films, 2d-materials, nanocomposites, nanoparticles,
  photonic-optoelectronic, dielectrics-piezoelectrics, semiconductors,
  polymers, metals, insulation, functional, sustainability-durability).

### materials-response

- After reviewer comments arrive, separates response tone from manuscript
  action, drafts point-by-point replies, and prevents unsupported promises.
  Outputs a response letter plus a rebuttal package with action items and
  risk flags. Has its own `evals.json`.

### materials-html-deck

- Converts papers, reading notes, review matrices, and research outlines into
  browser-native HTML academic decks: retained `index.html`, per-slide HTML
  files, shared design tokens, Playwright screenshots, QA reports, speaker
  notes, and an asset manifest.

### materials-paper-to-patent — Chinese invention-patent conversion

- Turns a materials research paper into an evidence-grounded Chinese
  invention-patent application draft. Default `invention_type` is
  `process-material` (配方/工艺/材料类发明专利).
- **Three-axis routing**: `source_format` (pdf-text / scanned-pdf /
  pasted-text / mixed-project), `task_mode` (full-draft / claim-set /
  disclosure-analysis / paper-patent-audit), `invention_type`
  (process-material / device / system / mixture-formula).
- Civil patent knowledge base: `patent_kb.yaml` covering Chinese Patent Law
  articles 22 / 26.3 / 26.4 / 31.1 / 33, CNIPA guidelines, 4 invention-type
  verb patterns, 9 claim anti-patterns, 7 unit-alias groups, 6 material-domain
  links.
- Claim-validation engine: `validate_patent_claims.py` runs 7 rule functions
  (independent-claim technical features, dependent-claim references,
  specification support, anti-patterns, unit consistency, invention-type
  alignment, claim-count limits) with ERROR / WARNING / INFO severities.
- 9 scripts total; outputs `draft.json`, a complete DOCX application
  (description + claims + abstract + cover letter), and `flowchart.svg`;
  figures are produced by `materials-figure`.

### materials-submission

- Route C package assembly for 10 supported journal templates: submission
  package, cover letter, and highlights.

## Shared core — `_shared/`

All 16 skills share a small set of protocol files under
`plugins/materials-skills/skills/_shared/` — single-purpose authorities rather
than a default encyclopedia; skills load only the profile protocol and their
declared core by default.

| File | Purpose |
|---|---|
| `core/direction-profile.md` | Profile-first routing protocol (first-use question, `.materials/profile.yaml` storage) |
| `core/claim-strength-ladder.md` | Quantitative claim-strength calibration (causal → associative → correlative → speculative) |
| `core/evidence-contract.md` | Required fields for any claim evidence tuple (claim-id, source-id, evidence-layer, source-quality, …) |
| `core/source-basis.md` | Source taxonomy and reliability tiers |
| `core/stance.md` | How to handle disagreements, hedges, and uncertainty |
| `core/terminology-ledger.md` | Canonical term normalisation across skills |
| `core/ethics.md` | Ethics, attribution, and "do not fabricate" guardrails |
| `journal-formats/` | **17 journal format guides** (CBM, CCC, RMPD, JBE, nature-materials, acs-nano, acta-materialia, advanced-materials, advanced-functional-materials, ceramics-international, energy-buildings, building-environment, jacers, jmca, nano-letters, progress-polymer-science, thermal-sciences) |

## Quantitative summary

- **16** `materials-*` skills plus shared contracts under `_shared`
- **29** material systems in the material registry
- **17** journal format guides · **22** reviewer-criteria documents ·
  **9** domain data schemas
- Public verification: `python .\scripts\run_release_checks.py --json`
- The public repository does not ship the internal Python regression suite or
  the full generated visual asset pack (maintainer-side assets).

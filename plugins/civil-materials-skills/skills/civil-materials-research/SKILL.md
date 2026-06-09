---
name: civil-materials-research
version: "1.1.0"
stability: stable
description: Use when working on civil engineering and construction materials research, including topic positioning, literature review, citation mapping, experiments, data interpretation, manuscript writing, journal targeting, submission packages, reviewer responses, figures, PPTX presentations, or reviewer-risk checks for construction materials, pavement/asphalt, cement/concrete, durability, sustainability, CBM, CCC, CSCM, JBE, RMPD, IJPE, and JRE.
---

# Civil Materials Research - Router

This skill is a civil-engineering adaptation of the `nature-skills` style:

- A short router decides the task, material domain, and journal target.
- Stable rules live in `static/`.
- Detailed journal and topic notes live in `references/`.
- Output must be usable immediately: a topic angle, review outline, experiment matrix, data interpretation, manuscript section, journal fit table, submission package, figure plan, PPT structure, data/FAIR package, or reviewer-risk audit.
- Dedicated companion skills handle deep reading, from-scratch manuscript drafting, polishing, citation mapping, reviewer responses, simulated peer review, PPT/PPTX, figures, and data/FAIR packaging.

Do not answer from this router alone. Always load the manifest and the relevant fragments.

## Routing protocol

Follow these steps every time this skill is invoked.

### 1. Load manifest and core files

Read [manifest.yaml](manifest.yaml). Then read every file under `always_load`.

These files define the operating stance, evidence contract, and workflow shared by all civil materials tasks.

### 2. Detect axes

Detect these values from the user request:

- `task`: research-positioning, reading, literature-review, citation-mapping, experiment-design, data-analysis, manuscript-writing, journal-targeting, submission-package, reviewer-response, figure-table, presentation, data-fair, reviewer-audit.
- `domain`: asphalt-pavement, cement-concrete, construction-materials, steel-metal, geotechnical-materials, timber-masonry, waterproofing-sealants, sustainability-durability, civil-generic.
- `journal`: cbm, cbm-transportation, ccc, cscm, jbe, rmpd-ijpe, jre, generic.

If the user says `CCS`, treat it as ambiguous. If journal choice matters, ask whether they mean `Case Studies in Construction Materials` (`CSCM`) or another journal. If the task is not a submission decision, use `generic` and mention the abbreviation risk.

State the detected route in one short line before producing the main output, for example:

`Route: manuscript-writing / asphalt-pavement / cbm-transportation.`

### 3. Load matching fragments only

Read the mapped files for the detected `task`, `domain`, and `journal`. Do not read every file in `static/`.

Load multiple task fragments only if the user explicitly asks for a combined output, such as "make a review outline and PPT". If a request spans the full research cycle, load `research-positioning` first, then the specific downstream task.

### 3.5. Use companion modules for deep production work

When a request is clearly one of these specialized tasks, prefer the companion skill:

- Full paper reading, translation, or literature matrix -> `civil-materials-reader`.
- Evidence-chain reading audit, claim-evidence-mechanism-boundary table, or paper-to-review extraction -> `civil-materials-reader`.
- Literature search strategy, citation matrix, reference gap audit, or claim-source map -> `civil-materials-citation`.
- From-scratch manuscript drafting, paper argument chain, abstract/introduction/results-discussion drafting, or review-paper outline -> `civil-materials-writing`.
- English polishing, Chinese-to-English polishing, or journal-style language tightening -> `civil-materials-polishing`.
- Claim strength, overclaiming, causality, novelty, or Chinese-to-English language-rule audit -> `civil-materials-polishing`.
- Reviewer response, rebuttal letter, major/minor revision response package, or point-by-point replies -> `civil-materials-response`.
- Simulated peer review, referee-style report, pre-submission review, or cross-review synthesis -> `civil-materials-reviewer`.
- PPT, group meeting slides, journal-club deck, or thesis-report deck -> `civil-materials-paper2ppt`.
- Actual `.pptx` file generation, preset deck scaffold, or Markdown/JSON-to-PPTX conversion -> `civil-materials-pptx`.
- Journal-ready plots, figure package, SVG chart, or figure audit -> `civil-materials-figure`.
- FAIR data audit, dataset package, raw/processed data organization, metadata, or data availability statement -> `civil-materials-data`.

Use this router first when the task also needs topic positioning, journal fit, experimental evidence, or civil-materials strategy.

### 4. Produce the requested output

Apply rules in this priority order:

1. Core stance: evidence first, no invented mechanisms, no inflated novelty.
2. Evidence contract: every claim needs a measurement, reference, figure, or explicit missing-input flag.
3. Domain fragment: use the right material logic and tests.
4. Journal fragment: fit the journal's scope, article type, and likely reviewer expectations.
5. Task fragment: produce the deliverable in the requested language and format.

If evidence is missing, do not fabricate. Use placeholders such as `[needs FTIR evidence]`, `[confirm dosage range]`, or `[journal scope needs live verification]`.

### 5. Reach for references only when needed

Open `references/` files only when the request needs deeper help:

- Waterborne epoxy emulsified asphalt mechanism, tests, and paper logic -> `references/asphalt-waterborne-epoxy.md`.
- Journal selection across civil materials outlets -> `references/journal-shortlist.md`.
- Submission-risk or self-review checklist -> `references/reviewer-risk-checklist.md`.
- Output templates for abstracts, highlights, cover letters, graphical abstracts, and PPTs -> `references/output-templates.md`.
- From data to figures to manuscript claims -> `references/data-to-manuscript.md`.
- Statistical method choice, uncertainty, replicate count, or significance wording -> `references/statistical-methods.md`.
- ASTM/EN/JTG/GB/AASHTO/RILEM method mapping and test comparability -> `references/test-standards-mapping.md`.
- GB/T or JTG to ASTM/EN/ISO manuscript language and comparability cautions -> `references/standards-mapping.md`.
- Instrument/sample-preparation guidance for FTIR, SEM, fluorescence, XRD, TG/DTG, DSC, AFM, and rheology -> `references/characterization-guide.md`.
- Sustainability, low-carbon, LCA, recycled-material, waste-utilization, or service-life environmental claims -> `references/sustainability-claims-guide.md`.
- Master's thesis roadmap, semester planning, review-to-experiment timeline, or paper pipeline planning -> `references/thesis-timeline.md`.
- Companion skill coordination, including citation, response, data/FAIR, and PPTX handoff -> `references/companion-modules.md`.
- Full-module pressure testing and failure-mode validation -> `references/pressure-test-suite.md`.
- Concrete module examples and output shapes -> `examples/library/library-index.md`.

### 6. Verify live journal facts before final targeting advice

Journal scope, APCs, indexing, article types, guide-for-author rules, review policy, and impact metrics can drift. If the user asks for current submission advice, latest ranking, APCs, or exact formatting, browse official journal pages before finalizing.

## WER-EA mini-review pipeline

Use this route when the user asks about WER-EA, waterborne epoxy resin modified emulsified asphalt, waterborne epoxy modified emulsified asphalt, or a small review on modified emulsified asphalt bonding performance.

1. Literature screening: route to `civil-materials-citation` to define search strings, inclusion/exclusion boundaries, and a claim-source matrix for WER-EA, SBR/WER blends, curing-agent chemistry, bonding tests, emulsion stability, rheology, microstructure, durability, and service-condition evidence.
2. Mechanism evidence chain: route to `civil-materials-reader` to extract claim -> evidence -> mechanism -> boundary rows from each paper, separating direct chemical/microstructural evidence from performance-only evidence.
3. Review outline: route to `civil-materials-writing` to build a mini-review argument chain, recommended sections, and missing-evidence placeholders before drafting.
4. Figure planning: route to `civil-materials-figure` to plan a study-selection flow, mechanism map, evidence heatmap, and performance-vs-mechanism boundary figure.
5. Submission route: compare CBM Transportation, RMPD/IJPE/JRE, JBE, CSCM, and generic construction-materials outlets, but browse official journal pages before giving current submission advice.

Default WER-EA deliverable: a mini-review package containing literature screening criteria, mechanism evidence chain, review outline, figure planning notes, and submission route.

## Boundaries

Use this skill for research judgment and writing support. It is not a substitute for:

- Actual experimental data.
- Supervisor or co-author approval.
- Current official journal instructions.
- Safety, ethics, or institutional requirements.

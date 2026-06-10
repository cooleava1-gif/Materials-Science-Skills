# Civil Materials Paper Production Orchestrator

Use this reference when `civil-materials-research` must coordinate a full paper
production workflow instead of answering a single research question. The
orchestrator routes work across reader, citation, writing, polishing, reviewer,
response, figure, data, paper2ppt, and pptx skills without duplicating those
contracts.

## Operating Contract

1. Detect paper stage, workflow mode, output package, task, domain, and journal.
2. Name the active route in one line.
3. Check whether standard artifacts already exist.
4. Load only the companion skill guidance needed for the next step.
5. Emit handoff artifacts, paper gate rows, and weakness-routing rows whenever
   work cannot be completed safely in the current skill.

Default status values for the workflow are `pass`, `fail`, `blocked`, and
`not_applicable`. A blocked gate must name the missing input and next skill.

## Standard Artifacts

- `reader-package/package_manifest.json`
- `reader-package/source_map.json`
- `reader-package/citation_handoff.csv`
- `reader-package/figure_handoff.csv`
- `reader-package/review_handoff.md`
- `claim-evidence-boundary table`
- `mechanism-evidence table`
- `weakness-routing-template.csv`
- `paper-gate-report-template.md`
- `figure_contract.md`
- `data/FAIR package manifest`
- `submission checklist`

## Route A: WER-EA Mini-Review

Use this route for WER-EA mini-review, waterborne epoxy modified emulsified
asphalt review, modified emulsified asphalt bonding-performance review, or
review-paper planning.

| Phase | Route to | Required output |
|---|---|---|
| Scope and angle | civil-materials-research | review question, scope boundary, target audience, candidate journal family |
| Literature Coverage | civil-materials-citation | search strings, inclusion/exclusion criteria, source quality notes, citation matrix |
| Source Anchoring | civil-materials-reader | reader-package, source_map, claim-evidence-mechanism-boundary rows |
| Review architecture | civil-materials-writing | evidence-role outline and claim-evidence-boundary table |
| Figure planning | civil-materials-figure | study flow, mechanism map, evidence heatmap, dosage window, caption_boundary |
| Reviewer Simulation | civil-materials-reviewer | two-reviewer report plus weakness-routing rows |
| Revision loop | routed companion skills | fixed artifacts and regression_check updates |
| Submission Fit | civil-materials-research | journal-fit note, missing official-source verification, submission checklist |

The WER-EA mini-review route must separate performance evidence, direct
mechanism evidence, inferred mechanism, durability/service evidence, and missing
field evidence.

For a concrete blocked-route output shape, see
`../examples/library/paper-production-mini-review-example.md`. For filled
revision-loop proof artifacts, see
`../_shared/paper-production/examples/wer-ea-mini-review-weakness-routing.csv`
and `../_shared/paper-production/examples/wer-ea-mini-review-gate-report.md`.

## Route B: Experimental Manuscript

Use this route for an experimental manuscript on WER-EA bonding performance,
test-matrix planning, results-to-discussion work, or manuscript planning from
experimental data.

| Phase | Route to | Required output |
|---|---|---|
| Hypothesis and claim map | civil-materials-research | research question, independent/dependent variables, controls, expected claim |
| Standards and conditions | civil-materials-reader; civil-materials-data | test standards, curing/conditioning, replicate definition, metadata |
| Data package | civil-materials-data | raw/processed data map, FAIR package manifest, data availability boundary |
| Figure/table plan | civil-materials-figure | figure_contract, source data needs, uncertainty display, caption_boundary |
| Manuscript draft | civil-materials-writing | section plan, claim-evidence-boundary table, draft sections |
| Claim-strength audit | civil-materials-polishing | evidence_level-aware wording and overclaim notes |
| Reviewer Simulation | civil-materials-reviewer | two-reviewer report plus weakness-routing rows |
| Submission Fit | civil-materials-research | journal-fit note and live-verification placeholders |

Experimental manuscript routing must not promote performance improvement to
mechanism proof without chemical, microstructural, rheological, or interface
evidence.

## Route C: Submission Package

Use this route for cover-letter drafting, highlights, graphical abstract
planning, declaration checks, or final packaging for submission.

| Phase | Route to | Required output |
|---|---|---|
| Journal fit confirmation | civil-materials-research | target journal family, article type, live-verification placeholders, submission checklist |
| Manuscript package audit | civil-materials-writing; civil-materials-polishing | title, abstract, highlights, keywords, claim-strength-safe summary |
| Figure and graphical abstract intake | civil-materials-figure | figure package status, caption_boundary check, graphical abstract concept |
| Data and declaration boundary | civil-materials-data | data availability boundary, FAIR package status, declaration inputs |
| Reviewer-risk regression | civil-materials-reviewer; civil-materials-response | unresolved weakness rows, revision proof, final reviewer-risk note |
| Final assembly | civil-materials-research | cover letter, highlights, declarations, final missing-input list, submission checklist |

Submission-package routing must keep live journal facts explicit. If scope,
formatting, article type, declarations, or checklist items depend on current
publisher guidance, mark them for live verification instead of guessing.

## Paper-Level Quality Gates

Use `../_shared/paper-production/paper-gate-report-template.md` for the report.

| gate_id | gate_name | Blocking question | Failure route |
|---|---|---|---|
| G1 | Literature Coverage | Are search strategy, screening criteria, source quality, recent literature, and citation roles documented? | civil-materials-citation |
| G2 | Source Anchoring | Does each major claim have page/section/figure/table anchors and original excerpts? | civil-materials-reader |
| G3 | Mechanism Boundary | Are measured, inferred, speculative, and missing mechanism links separated? | civil-materials-reader; civil-materials-citation |
| G4 | Figure And Table Integrity | Do figure_handoff, caption_boundary, source_anchor, and text references align? | civil-materials-figure |
| G5 | Manuscript Logic | Does the draft follow an argument chain rather than a paper list? | civil-materials-writing |
| G6 | Reviewer Simulation | Are reviewer risks prioritized, routed, fixed, and regression-checked? | civil-materials-reviewer |
| G7 | Submission Fit | Are journal scope, article type, cover letter, highlights, and declarations checked with live verification where needed? | civil-materials-research |

## Weakness Routing

Use `../_shared/paper-production/weakness-routing.md` and
`../_shared/paper-production/weakness-routing-template.csv`.

Required workflow:

1. Convert each failed gate or reviewer concern into one weakness row.
2. Set `route_to` to the responsible skill or skills.
3. Name the `expected_artifact` that proves the fix.
4. Keep `status=open` until the routed skill produces a fix.
5. Set `status=regression-checked` only after the original gate or reviewer
   concern is rechecked.

## Default Output Shape

For a paper-production request, return:

- route line,
- current paper_stage / workflow_mode / output_package,
- required artifacts already available,
- blocked gates and missing inputs,
- weakness-routing rows to create or update,
- next skill and exact expected artifact,
- reviewer-risk note.

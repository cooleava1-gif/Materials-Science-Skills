# WER-EA mini-review

## Route Summary

Use this route when the goal is a source-grounded WER-EA mini-review package,
not just a loose literature summary. The ideal flow is research routing first,
then citation screening, reader-package extraction, review architecture, figure
planning, and finally reviewer-risk control.

## Demo Prompt

```text
Help me run a WER-EA mini-review workflow from screening to figure planning.
```

## Workflow Steps

1. Start with `civil-materials-research` and frame the review question, scope,
   target journal family, and `paper_stage=screening`.
2. Hand off to `civil-materials-citation` to build the search logic, screening
   criteria, and a reviewer-safe citation matrix.
3. Send the screened paper set into `civil-materials-reader` to generate
   `source_map.json`, `citation_handoff.csv`, `figure_handoff.csv`, and
   evidence-boundary notes.
4. Use `civil-materials-writing` to turn those artifacts into a review outline
   organized by evidence roles rather than paper titles.
5. Use `civil-materials-figure` to plan the mechanism map, evidence heatmap,
   screening flow, dosage window, and caption boundaries.
6. Before treating the package as ready, run `civil-materials-reviewer` or
   `civil-materials-polishing` on the outline and figure logic to downgrade
   overclaims and expose missing evidence.

## Expected Artifacts

- screened citation matrix with source-role and evidence-layer fields
- reader package files such as `source_map.json`, `review_handoff.md`, and
  `figure_handoff.csv`
- review outline with gap, contribution, and missing-evidence markers
- figure-planning notes for WER-EA review figures
- reviewer-risk notes before journal targeting

## What Good Looks Like

- the review has a clear angle instead of a paper-by-paper list
- performance evidence is kept separate from mechanism evidence
- recent WER-EA and adjacent emulsified-asphalt literature is screened
- figures are planned from actual source anchors, not guessed from memory
- the output can hand off cleanly into drafting or submission planning

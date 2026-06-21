# Experimental manuscript

## Route Summary

Audits an experimental materials manuscript before discussion drafting, with
emphasis on evidence gaps, data structure, figures, and reviewer risk.

## Demo Prompt

```text
Audit this experimental manuscript for evidence gaps before I draft the discussion.
```

## Workflow Steps

1. `materials-research` identifies paper stage, domain, and evidence level.
2. `materials-data` checks raw/processed data, metadata, and availability.
3. `materials-figure` checks figure contracts and caption boundaries.
4. `materials-writing` rebuilds bounded results/discussion logic.
5. `materials-reviewer` produces desk-reject and must-fix risk notes.

## Expected Artifacts

- Evidence-gap table.
- FAIR data audit notes.
- Figure QA handoff.
- Revised argument chain for the discussion.
- Reviewer-risk report.

## What Good Looks Like

Every performance claim points to data, every mechanism claim points to
characterization evidence, and unresolved missing measurements remain visible.

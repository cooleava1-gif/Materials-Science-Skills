# Experimental manuscript

## Route Summary

Use this route when the user already has an experiment or draft manuscript and
needs a tighter evidence chain before writing or revising the paper. This flow
prioritizes stage control, data support, figure integrity, and bounded results
discussion.

## Demo Prompt

```text
Audit this experimental manuscript for evidence gaps before I draft the discussion.
```

## Workflow Steps

1. Start with `civil-materials-research` and detect the manuscript stage,
   claimed contribution, and missing-support hotspots.
2. If data organization is weak, route to `civil-materials-data` to clarify
   variables, controls, raw/processed structure, and FAIR-facing gaps.
3. Send result figures or tables to `civil-materials-figure` to tighten figure
   contracts, source-data anchors, export QA, and caption boundaries.
4. Use `civil-materials-writing` to rebuild the argument chain in the results
   and discussion around actual measurements and stated boundaries.
5. Use `civil-materials-polishing` to reduce literal translation or
   mechanism-overreach after the technical content is stable.
6. Run `civil-materials-reviewer` before submission framing to see which claims,
   figures, or methods still look vulnerable.

## Expected Artifacts

- staged workflow note showing where the manuscript is blocked
- data or metadata repair list when variables are unclear
- figure contract and figure-package QA notes
- revised discussion or outline with bounded claims
- reviewer-risk summary for the next revision step

## What Good Looks Like

- every major claim can be traced to data, figure panels, or explicit limits
- test conditions and comparison baselines are visible
- figures support the paper logic instead of simply decorating it
- the discussion stops short of mechanism claims the data cannot support
- the next authoring step is obvious after the audit

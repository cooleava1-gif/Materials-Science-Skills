# Revision loop

## Route Summary

Use this route when reviewer comments already exist and the goal is not only to
draft a reply, but to route each weakness to the right repair module before the
response letter is finalized.

## Demo Prompt

```text
Take these reviewer comments, route the weaknesses to the right skills, and build a revision-ready response package.
```

## Workflow Steps

1. Start with `civil-materials-reviewer` or directly with
   `civil-materials-response` if comments are already structured.
2. Convert major concerns into weakness routes: reader for source-grounding,
   citation for coverage, writing for argument chain, figure for caption or
   panel risk, data for variables and metadata, polishing for overclaim control.
3. Repair the technical content in the owning module before polishing the reply
   text.
4. Return to `civil-materials-response` to build point-by-point replies with
   proof of change, manuscript location, and bounded commitments.
5. Re-run `civil-materials-reviewer` if the revision is substantial and you need
   a regression check before resubmission.

## Expected Artifacts

- weakness-routing list mapped to responsible skills
- repaired manuscript or figure notes before the response letter is finalized
- point-by-point response package with evidence of change
- optional regression review before resubmission

## What Good Looks Like

- the response letter does not promise work that the manuscript still lacks
- each reviewer concern has an owner, a fix, and a proof location
- tone is calm and specific rather than defensive
- revised claims are more supportable than the original version
- resubmission risk is lower after the regression pass

# Paper Production Mini-Review Example

Module: civil-materials-research paper-production orchestrator

## Use Case

Coordinate a WER-EA mini-review when literature screening has been completed
but source anchoring and mechanism-safe drafting are still blocked.

## Example Output Shape

Route: literature-review / asphalt-pavement / generic.

- `paper_stage`: screening
- `workflow_mode`: paper-production
- `output_package`: reader-package

## Available Artifacts

- `citation_handoff.csv`
- `review_handoff.md`
- `weakness-routing-template.csv`

## Blocked Gates

- `G2 Source Anchoring` -> next skill `civil-materials-reader` -> expected
  artifact `reader-package/source_map.json`
- `G3 Mechanism Boundary` -> next skill `civil-materials-reader` ->
  expected artifact `claim-evidence-boundary table`

## Weakness Routing Rows To Update

- `W-G2-001`
- `W-G3-001`

## Reviewer-Risk Note

Mechanism wording is blocked until page-level anchors are restored and the
performance-only papers are separated from direct mechanism evidence.

## Quality Bar

Do not treat the route as draft-ready until each blocked gate is paired with a
named next skill, a concrete expected artifact, and weakness rows that can be
rechecked after revision.

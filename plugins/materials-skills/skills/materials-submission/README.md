# materials-submission

Version: 1.1.0

`materials-submission` assembles evidence-grounded journal submission packages
for supported materials journals. It produces cover-letter, checklist,
declarations, conditional keyword, and source-tracing artifacts without
fabricating manuscript content or declarations.

## Supported journals

- CBM, CCC, RMPD, and JBE.
- Building and Environment, Energy and Buildings, and Ceramics International.
- Acta Materialia, Journal of Materials Chemistry A, and Nature Materials.

Each journal's YAML template is the executable source of article types,
official display labels, highlights, declarations, and required artifacts.

## Supported article routes

`research-article`, `review-article`, `short-communication`, `technical-note`,
`letter`, `comment-and-opinion`, and `perspective` are routed only when the
selected journal supports them. The package builder rejects unavailable routes.

## Core outputs

- `cover-letter.md` with publisher-facing article labels.
- `highlights.md` only when the template requires highlights.
- `submission-checklist.md` with declarations and stage-specific artifacts.
- `keywords.md` only when the selected article route requires keywords.
- `declarations.md` only when the selected article route requires declarations,
  with non-fabricated data and code-availability placeholders.
- Source-tracing stubs for manuscript, figures, and FAIR data.

## Boundaries

- The skill does not submit files to publisher portals.
- The skill does not provide publisher Word or LaTeX files.
- Empty declarations and live facts remain explicit verification placeholders.
- Publisher guides remain authoritative for all live-verification fields.

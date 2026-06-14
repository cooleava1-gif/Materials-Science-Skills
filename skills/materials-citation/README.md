# materials-citation

The citation skill is the literature-screening and claim-source mapping layer
for materials manuscripts. Use it when you need more than a few references
and want a reviewer-safe citation matrix with explicit evidence roles.

## When To Use

Use this skill when the deliverable is a search strategy, screened citation
matrix, reference-gap audit, normalized scholarly identifiers package, or
claim-source alignment table for CBM, CCC, JBE, RMPD, IJPE, WER-EA, asphalt
pavement materials, cement/concrete, durability, or mechanism-heavy topics.

## Inputs

- review question, manuscript claim list, or topic angle
- inclusion and exclusion boundaries
- candidate DOI, PMID, RIS, BibTeX, CSV, or mixed citation records
- journal family when scope or recency standards matter

## Outputs

- search strategy with database and keyword logic
- screened citation matrix with fields such as evidence layer, source role,
  source quality, reviewer risk, and reader anchor
- normalized IDs and converted citation exports
- reference-gap notes that can be handed to reader or writing workflows

## Example

- Template:
  `skills/materials-citation/assets/templates/citation-matrix-template.csv`
- Companion example:
  `skills/materials-research/examples/library/citation-matrix-example.md`
- WER-EA source-quality reference:
  `references/wer-ea-screening-and-source-quality.md`

## Validation

- MCP and service tests live under
  `skills/materials-citation/mcp/academic_search/tests/`
- Release checks verify citation handoff files and academic-search assets
- The bundle-level verification entrypoint is
  `python .\scripts\run_release_checks.py --json`

## Boundaries

This skill does not replace deep paper reading. Search hits, abstract-level
matches, and identifier-normalized records are still screening outputs until the
reader skill or the human researcher confirms the actual evidence inside the
paper.

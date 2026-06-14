# materials-reader

The reader skill is the source-grounded reading engine for the bundle. It turns
papers into evidence-chain artifacts that later writing, figure, and reviewer
work can actually trust.

## When To Use

Use this skill when the raw material is a paper, PDF, abstract, figure caption,
or pasted source text and you need structured notes, source anchors, or
claim-evidence-mechanism-boundary extraction.

## Inputs

- PDF or text of a materials paper
- reading target such as mechanism extraction, figure planning, or review
  synthesis
- domain cues such as WER-EA, asphalt pavement materials, cement/concrete, or
  durability
- whether translation notes, figure cards, or review handoffs are needed

## Outputs

- reader package with `package_manifest.json`, `source_map.json`,
  `citation_handoff.csv`, `figure_handoff.csv`, and `review_handoff.md`
- claim-evidence-mechanism-boundary rows
- figure/table-aware notes and anchored excerpts
- reviewer-safer inputs for writing and figure workflows

## Example

- Example:
  `skills/materials-reader/examples/waterborne-epoxy-evidence-chain-example.md`
- Reader-package protocol:
  `references/wer-ea-intensive-reading-package.md`

## Validation

- Contract tests live under `skills/materials-reader/tests/`
- Important checks include `test_reader_package_contract.py`,
  `test_reader_handoff.py`, and `test_validate_reader_package.py`
- Bundle verification:
  `python .\scripts\run_release_checks.py --json`

## Boundaries

This skill structures and audits reading outputs, but it does not certify that
your interpretation is publication-ready. Final research judgment still belongs
to the researcher and, when needed, later reviewer or polishing loops.

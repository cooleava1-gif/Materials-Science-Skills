# materials-polishing

The polishing skill is the language and claim-strength control layer for
materials prose. It is where rough English, literal translation, and
overstated mechanism claims get tightened into reviewer-safer manuscript text.

## When To Use

Use this skill after draft text already exists and you need polishing,
Chinese-to-English academic rewriting, journal-tone tightening, or overclaim
auditing for abstracts, introductions, discussions, conclusions, highlights, or
cover letters.

## Inputs

- English draft or Chinese source paragraph
- target journal or style constraints when relevant
- evidence level or reviewer concern that should bound the wording
- nearby claims, figures, or source anchors when risk is high

## Outputs

- polished manuscript prose
- claim-strength adjustments and overclaim warnings
- cleaner journal tone with missing-evidence markers preserved
- revision-safe wording that can be handed back to writing or response workflows

## Example

- Example:
  `plugins/materials-skills/skills/materials-polishing/examples/claim-strength-polishing-example.md`
- Related library example:
  `plugins/materials-skills/skills/materials-research/examples/library/polishing-claim-strength-example.md`

## Validation

- Core regression test:
  `plugins/materials-skills/skills/materials-polishing/tests/test_polishing_references.py`
- Pressure test:
  `plugins/materials-skills/skills/materials-polishing/tests/pressure-tests/overclaim-and-literal-translation.md`
- Bundle verification:
  `python .\scripts\run_release_checks.py --json`

## Boundaries

This skill improves wording and claim discipline, but it does not create new
evidence. If the underlying mechanism support is weak, the fix is often to
downgrade the claim or route back to reader, citation, figure, or data work.

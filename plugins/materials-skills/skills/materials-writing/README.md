# materials-writing

The writing skill turns evidence and structure into manuscript text. It is the
production layer for review outlines, argument chains, and bounded manuscript
drafting.

## When To Use

Use this skill when the deliverable is manuscript prose or section structure:
abstracts, introductions, methods, results/discussion, conclusions, review
outlines, or experimental-paper logic built from claims, notes, results, and
figures.

## Inputs

- claim list, results, reader-package artifacts, or Chinese source draft
- section target such as abstract, introduction, discussion, or full review
  architecture
- journal family or tone requirements when relevant
- evidence boundaries that must stay visible in the output

## Outputs

- review outline or manuscript section draft
- argument chain with gap and contribution logic
- bounded claim wording that keeps missing evidence explicit
- cleaner handoff to polishing, reviewer, or response loops

## Example

- Example:
  `plugins/materials-skills/skills/materials-writing/examples/review-outline-example.md`
- Additional example:
  `plugins/materials-skills/skills/materials-writing/examples/waterborne-epoxy-abstract-example.md`

## Validation

- Core regression test:
  `plugins/materials-skills/skills/materials-writing/tests/test_writing_skill.py`
- Pressure test:
  `plugins/materials-skills/skills/materials-writing/tests/pressure-tests/missing-data-writing.md`
- Bundle verification:
  `python .\scripts\run_release_checks.py --json`

## Boundaries

This skill drafts from available evidence; it should not be used to hide
missing data, invent mechanism support, or blur the difference between measured
results and interpretation.

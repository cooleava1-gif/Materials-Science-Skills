# Tests

This directory holds behavior test scenarios for the `materials-writing` skill.

## Layout

- `scenarios/*.md` — one file per scenario, describing the input, expected axis detection, expected workflow gate behavior, and expected output shape.

## Status

Currently empty. Scenarios will be added in later release stages to cover:

- axis detection across all six axes (paper_type, section, language, journal_family, material_family, domain)
- the confirmation gate (step 5 of `static/core/workflow.md`)
- the targeted revision loop (step 11)
- placeholder behavior when evidence is missing

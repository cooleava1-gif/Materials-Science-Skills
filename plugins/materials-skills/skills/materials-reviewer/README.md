# materials-reviewer

The reviewer skill simulates a tough but useful referee. It is the bundle's
main pre-submission and pre-resubmission risk screen.

## When To Use

Use this skill when you want a peer-review style audit for novelty, evidence
sufficiency, figure integrity, logic flow, journal fit, or desk-reject risk
before submission or revision.

## Inputs

- abstract, section draft, full manuscript, or figure package
- target journal or journal family when fit matters
- review goal such as desk-reject risk, novelty pressure test, or revision
  regression check
- any known weak spots you want prioritized

## Outputs

- reviewer-style report with major and minor concerns
- risk prioritization that can be routed into fixes
- weakness routing guidance for companion skills
- a stronger basis for revision planning or final gating

## Example

- Example:
  `plugins/materials-skills/skills/materials-reviewer/examples/cbm-review-simulation.md`
- Additional example:
  `plugins/materials-skills/skills/materials-reviewer/examples/ccc-review-simulation.md`

## Validation

- Core regression test:
  `plugins/materials-skills/skills/materials-reviewer/tests/test_reviewer_skill.py`
- Pressure test:
  `plugins/materials-skills/skills/materials-reviewer/tests/pressure-tests/weak-manuscript-review.md`
- Bundle verification:
  `python .\scripts\run_release_checks.py --json`

## Boundaries

This skill simulates reviewer pressure, but it is not a real editor or journal.
Current journal facts, APCs, and submission rules should still be checked live
on official pages when the decision is time-sensitive.

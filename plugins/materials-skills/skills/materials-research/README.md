# materials-research

The research skill is the front door and paper-production orchestrator for the
bundle. Start here when the user need is broad, multi-stage, or not yet pinned
to one companion skill.

## When To Use

Use this skill for topic positioning, paper angle design, literature-review
planning, journal targeting, experimental manuscript routing, submission
strategy, PPT planning, or any cross-skill workflow that needs paper-stage and
evidence-level judgment.

## Inputs

- rough research question, manuscript draft, or review goal
- domain and journal hints when available
- workflow intent such as mini-review, experimental manuscript, revision loop,
  or presentation
- current stage such as idea, screening, reading, drafting, revision, or
  submission

## Outputs

- routed workflow package with next-step ownership
- stage-aware and evidence-aware task framing
- journal-fit, reviewer-risk, or gate-oriented guidance
- handoff recommendations to reader, citation, writing, figure, reviewer,
  response, paper2ppt, pptx, or data modules

## Example

- Example library:
  `plugins/materials-skills/skills/materials-research/examples/library/library-index.md`
- Paper-production orchestrator:
  `references/paper-production-orchestrator.md`

## Validation

- Core regression tests:
  `plugins/materials-skills/skills/materials-research/tests/test_paper_production_orchestrator.py`
  and `test_pressure_examples_library.py`
- Pressure tests live under
  `plugins/materials-skills/skills/materials-research/tests/pressure-tests/`
- Bundle verification:
  `python .\scripts\run_release_checks.py --json`

## Boundaries

This skill routes and judges workflow shape, but it should not duplicate the
full procedures of every companion skill. Once the deliverable is clear, the
actual deep production work belongs to the specialized module.

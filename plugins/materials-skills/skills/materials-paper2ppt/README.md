# materials-paper2ppt

The paper-to-PPT skill converts paper notes, review matrices, and manuscript
logic into a presentation story. It is the fastest path from evidence package
to slide-ready Markdown.

## When To Use

Use this skill when you need a Chinese group-meeting deck, journal-club
structure, thesis-progress report, or paper summary outline before generating a
real PowerPoint file.

## Inputs

- paper notes, review outlines, reader-package artifacts, or manuscript drafts
- meeting context such as journal club, group meeting, thesis report, or
  submission rehearsal
- preferred audience focus such as mechanism, novelty, methods, or results

## Outputs

- slide-by-slide Markdown outline
- section pacing and talk logic
- figure placement suggestions and speaking-point structure
- handoff-ready content for `materials-pptx`

## Example

- Library example:
  `plugins/materials-skills/skills/materials-research/examples/library/paper2ppt-group-meeting-example.md`
- Companion real deck handoff:
  `plugins/materials-skills/skills/materials-research/examples/library/pptx-outline-json-example.md`

## Validation

- Core regression test:
  `plugins/materials-skills/skills/materials-paper2ppt/tests/test_presentation_handoff.py`
- Bundle verification:
  `python .\scripts\run_release_checks.py --json`

## Boundaries

This skill structures the talk; it does not by itself generate a `.pptx` file.
Use `materials-pptx` for the actual PowerPoint output when the outline is
ready.

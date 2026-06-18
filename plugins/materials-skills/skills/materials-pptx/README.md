# materials-pptx

The PPTX skill turns structured slide content into a real PowerPoint file. It
is the generation layer after the story and slide logic are already decided.

## When To Use

Use this skill when you already have PPTX-ready Markdown or JSON and need an
actual `.pptx` deck for journal club, group meeting, thesis report, or paper
presentation.

## Inputs

- slide-ready Markdown or JSON outline
- image paths, figure crops, and notes where needed
- speaker-note expectations and audience context
- deck scope such as paper summary, review talk, or experiment update

## Outputs

- real `.pptx` slide deck
- image placement and note-bearing slides
- a cleaner final package than plain Markdown alone

## Example

- Outline example:
  `plugins/materials-skills/skills/materials-research/examples/library/pptx-outline-json-example.md`
- Upstream slide-outline companion:
  `plugins/materials-skills/skills/materials-research/examples/library/paper2ppt-group-meeting-example.md`

## Validation

- Core regression test:
  `plugins/materials-skills/skills/materials-pptx/tests/test_pptx_generation.py`
- Bundle verification:
  `python .\scripts\run_release_checks.py --json`

## Boundaries

This skill generates the file, but it does not replace the logic design step.
If the talk structure is not ready yet, start with `materials-paper2ppt`
or with the research router.

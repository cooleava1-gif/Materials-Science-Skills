# materials-response

The response skill builds reviewer replies that are specific, structured, and
provable. It keeps the response letter tied to actual manuscript changes instead
of vague promises.

## When To Use

Use this skill when reviewer comments have arrived and the deliverable is a
point-by-point response package, rebuttal letter, revision summary, or
resubmission note set for a materials manuscript.

## Inputs

- reviewer comments or editor decision letter
- current manuscript revision notes
- figure, data, or text changes that can prove what was fixed
- target journal and revision severity when relevant

## Outputs

- point-by-point response structure
- proof-of-change language with locations and revision evidence
- routed weakness list for writing, polishing, figure, data, or reader fixes
- cleaner separation between tone management and technical repair

## Example

- Example:
  `plugins/materials-skills/skills/materials-response/examples/cbm-major-revision-response-example.md`
- Additional examples:
  `plugins/materials-skills/skills/materials-response/examples/ccc-methodology-critique-response-example.md`
  and `plugins/materials-skills/skills/materials-response/examples/rmpd-minor-revision-response-example.md`

## Validation

- Core regression test:
  `plugins/materials-skills/skills/materials-response/tests/test_response_examples.py`
- Pressure test:
  `plugins/materials-skills/skills/materials-response/tests/pressure-tests/aggressive-reviewer-mechanism-request.md`
- Bundle verification:
  `python .\scripts\run_release_checks.py --json`

## Boundaries

This skill improves the response package, but it does not magically resolve the
underlying technical problem. If a reviewer asks for stronger mechanism support
or clearer figures, the real fix may need reader, citation, figure, or writing
work before the reply is honest.

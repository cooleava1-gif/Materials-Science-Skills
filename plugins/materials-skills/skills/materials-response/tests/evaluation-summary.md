# Evaluation summary

`materials-response` is evaluated with synthetic Markdown fixtures. These tests are not executable
unit tests; they are behavior contracts for manual and agent review.

## Status rationale

Recommended status: `Stable`.

Rationale:

- The core rules are defined in `SKILL.md` and modular references.
- The skill has synthetic fixtures covering aggressive mechanism requests, conflicting reviewers,
  major revision with missing evidence, impossible experiments, and defensive draft auditing.
- Each fixture includes expected behavior, forbidden behavior, and pass/fail criteria.
- The examples show expected output shape without using real confidential reviewer comments.
- The rubric (`tests/rubric.md`) defines 6 evaluation dimensions with pass/fail criteria.

## Fixture coverage

| Fixture | Coverage | Key failure prevented |
|---|---|---|
| `aggressive-reviewer-mechanism-request.md` | hostile tone, missing SEM/FTIR, no additional experiments | emotional rebuttal, fabricated data |
| `conflicting-reviewers.md` | incompatible reviewer requests, editor priority | contradictory promises, ignoring conflict |
| `major-revision-missing-evidence.md` | missing DSC/TG, n=3 statistics, absent durability data | invented statistics, fabricated experiments |
| `impossible-experiment.md` | field trial limitations, LCCA requirements | false promises, time/funding excuses |
| `defensive-draft-audit.md` | hostile draft language, dismissive tone | accusatory language, retaining defensiveness |
| `third-round-reviewer-insists.md` | reviewer repeats same request across rounds, final revision | fabricating DSC data, false promises |
| `reviewer-demands-new-theory.md` | reviewer requests theoretical framework authors cannot provide | inventing mathematical models |
| `statistical-methods-disagreement.md` | wrong statistical test, n=3 limitations, missing p-values | fabricated p-values, inappropriate tests |
| `scope-creep-out-of-scope-requests.md` | field trials, LCCA, LCA outside study scope | fabricated field data, invented cost/LCA |
| `reviewer-misreads-paper.md` | reviewer misquotes data, misunderstands claims | confrontational tone, changing correct claims |

## Rubric dimensions

| Dimension | Focus |
|---|---|
| Completeness | Every comment has an ID; nothing is skipped |
| Traceability | Every claimed change has a location or explicit placeholder |
| Factuality | No invented data, statistics, or experiments |
| Tone | Cooperative, evidence-forward, not defensive |
| Actionability | Author knows exactly what to change |
| Domain-fit | Mechanism/performance claims respect materials evidence boundary |

## Manual evaluation checklist

- [x] Every fixture has input, expected behavior, forbidden behavior, and pass/fail checklist.
- [x] No fixture uses real reviewer comments.
- [x] Examples are synthetic and do not contain confidential review content.
- [x] Rubric covers 6 dimensions with materials domain specificity.
- [x] All fixtures are consistent with `SKILL.md` rules and `tests/rubric.md` standards.

## Promotion path

The skill is at `Stable`. Maintain stability by:

- testing new fixtures before adding response patterns;
- validating that rubric dimensions remain sufficient as new journal families are added;
- reviewing real anonymized revision packages when available to expand fixture coverage.

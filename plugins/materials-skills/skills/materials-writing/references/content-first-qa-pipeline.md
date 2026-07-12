# Content-First QA Pipeline

Use this reference for QA, auditing, or polishing after an initial draft.
The operating rule is **content before language**: scientific logic is checked
before style polishing.

## Gate Order

### Gate 2: Content Expert Review

- Check whether the argument matches the evidence.
- Check methods, DOE choices, material systems, and test conditions.
- Check alternative explanations, novelty boundaries, and missing evidence.

### Gate 1: Language And Style Review

Run language cleanup only after Gate 2. Check terminology, paragraph focus,
translation residue, vague AI phrasing, inflated verbs, and unsupported certainty.

### Gate 3: Auto-Validation

- Every factual claim has a citation, dataset, figure, table, or explicit placeholder.
- Methods, units, abbreviations, and figure/table numbering are consistent.
- Conclusions stay inside the evidence boundary.

### Gate 4: Score Threshold

Score the dimensions in `state-machine/evaluation-rubric.md`, route revision by
the lowest score, and apply `state-machine/stopping-rules.md` before proposing
another full revision round.

## QA Output

Return:

1. Gate summary: pass, revise, or stop.
2. Highest-risk content issue.
3. Language issues after content issues.
4. Auto-validation gaps.
5. Dimension scores and the targeted next revision.
6. Current artifact, score/status, remaining risks, stop-or-continue reason,
   and one next action.

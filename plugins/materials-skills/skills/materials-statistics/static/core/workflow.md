# Statistics Workflow

1. **Classify the task.** audit / rewrite / draft / reviewer-response support /
   figure-statistics alignment / data-backed check. Partial input means a
   bounded audit; say which parts cannot be assessed.
2. **Extract the design.** Groups, factors, levels, blocks, replicates,
   repeats, randomisation, exclusions, invoked standards (ASTM / ISO / GB),
   and the inference each result claims.
3. **Define `n` and replication.** Identify the independent unit per the
   contract; split independent specimens from repeated readings, fields,
   scans, and model runs. Mark unknowns `AUTHOR_INPUT_NEEDED`.
4. **Map claims to analyses.** For each claim record the comparison or model,
   test family, assumption checks, correction strategy, effect estimate,
   uncertainty, and exact p-value policy.
5. **Check failure modes.** Load `references/common-failure-modes.md` for
   nested data, many comparisons, small samples, interaction claims,
   curve regressions, or significance-only reasoning.
6. **Check DOE-specific reporting.** For factorial / Taguchi / RSM / mixture
   designs load `references/doe-statistics.md` and align with the
   `materials-doe` handoff (matrix, S/N columns, pooling rules).
7. **Check reporting completeness.** Load
   `references/statistical-reporting.md`; ensure Methods give test, `n`,
   unit, correction, assumption handling, and software with versions, and
   Results give effect estimates with uncertainty, not only p.
8. **Align figure statistics.** Load `references/figure-statistics.md` when
   captions, error bars, box plots, or significance markers are involved;
   check SD vs SEM declarations and per-panel `n`.
9. **Draft or revise.** Produce conservative ready-to-paste text. Keep claims
   inside the supplied design. Do not upgrade association to mechanism.
10. **Final QA.** Load `references/reviewer-checklist.md`; attach severity
    labels (P0 / P1 / P2), unresolved author questions, and reviewer-risk
    notes in the output format.

## Handoff boundaries

- New or extended design matrices → `materials-doe`.
- Dataset packaging and availability statements → `materials-data`.
- Re-plotting figures with corrected statistics → `materials-figure`.
- Language tightening of the statistics text → `materials-polishing`.
- Reviewer-response assembly → `materials-response`.

---
name: materials-statistics
version: 1.0.0
stability: beta
description: >-
  Use when auditing, revising, or drafting statistical reporting for
  materials-science manuscripts: sample-size and replicate definitions
  (specimens vs repeated measurements), ANOVA for factorial and Taguchi
  designs, response-surface regression, multiple-comparison corrections,
  effect sizes and uncertainty, error-bar and figure-statistics alignment,
  and reviewer comments about statistics. Trigger for statistics review,
  statistical analysis section, p-values, replicate counts, 统计审查、统计分析、
  统计方法、方差分析、多重比较、样本量、重复数、置信区间、效应量、图注统计、
  审稿人统计意见. Do not use for full raw-data reanalysis unless the user
  supplies data and explicitly asks for computation, for figure rendering,
  or for experiment planning without a reporting question.
---

# Materials Statistics Reporting Router

Read `manifest.yaml` and its `always_load` files. Apply explicit direction >
saved `.materials/profile.yaml` > neutral fallback, then resolve the task and
study-design axes before loading any reference.

## Blocking gates

- **replication-gate** — if the independent experimental unit (`n`) cannot be
  determined from the supplied text, mark it `AUTHOR_INPUT_NEEDED`; never
  infer `n` from cell, image, spectrum, or reading counts.
- **invention-gate** — never invent or silently repair p-values, degrees of
  freedom, confidence intervals, software versions, or correction methods.
- **boundary-gate** — reporting and wording skill only; computation happens
  only on user-supplied data with an explicit request.

## Routing protocol

1. Classify the task (audit / rewrite / draft / reviewer-response support /
   figure-statistics alignment / data-backed check).
2. Extract the design: groups, factors, levels, blocks, repeats, standards
   invoked (ASTM / ISO / GB), and the claimed inference.
3. Resolve `study_design` from the manifest axis and load its fragment.
4. Load `references/statistical-reporting.md` before drafting any Statistical
   analysis subsection.
5. Check `references/common-failure-modes.md` when nested measurements,
   many comparisons, small samples, or curve regressions appear.
6. Align figure statistics with `references/figure-statistics.md` when
   captions, error bars, or significance markers are involved.
7. Run `references/reviewer-checklist.md` before final delivery.

Hand off experiment planning to `materials-doe`, dataset packaging to
`materials-data`, plotting to `materials-figure`, and wording control to
`materials-polishing`. This skill owns only the statistical reporting layer.

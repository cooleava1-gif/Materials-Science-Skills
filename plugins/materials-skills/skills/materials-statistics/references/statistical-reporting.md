# Statistical Reporting Reference

What a materials journal expects from the Statistical analysis subsection and
from statistics in Results, and how to audit or draft it.

## Methods (Statistical analysis) checklist

Every element below must appear, be marked as not applicable with a reason,
or be flagged `AUTHOR_INPUT_NEEDED`:

1. **Independent unit and n.** "Three replicate specimens per mix were tested;
   each specimen was measured once" — explicit, per comparison.
2. **Replicate structure.** Independent specimens vs repeated readings vs
   nested subspecimens, and which entered the test.
3. **Tests and models.** Named test (t-test, one-way / two-way ANOVA,
   Welch, Kruskal–Wallis, Tukey HSD, Dunnett, regression family) with
   one-line justification tied to the design.
4. **Assumption handling.** Normality and variance-homogeneity checks (and
   the nonparametric or robust fallback when they fail), or why they were
   unnecessary for the design.
5. **Multiple-comparison strategy.** Named correction (Tukey, Dunnett,
   Bonferroni, Holm, FDR) whenever more than one pairwise comparison is
   reported. "p < 0.05 was considered significant" alone is incomplete.
6. **Effect and uncertainty reporting policy.** Means ± SD or ± SEM (state
   which), confidence intervals for key differences, and where exact p-values
   appear.
7. **Software and versions.** Origin 2024, SPSS 26, R 4.3 with package names,
   Python scipy 1.11 — with version, never bare names.
8. **Standards invoked.** When an ASTM / ISO / GB method prescribes replicate
   counts or precision statements, cite it and follow it.

## Results checklist

- Report effect sizes and uncertainty, not only p: "28-day compressive
  strength increased by 8.4 MPa (95% CI 5.9–10.9; n = 3 per group)".
- Exact p-values to the precision computed (p = 0.0031), except p < 0.001.
- "Significant" only means the test rejected; importance needs magnitude.
- Do not describe overlapping error bars as outperformance.
- Keep the same statistics in text, tables, and captions (consistency sweep
  with `materials-polishing` / shared terminology ledger).

## Common wording fixes

| Weak | Preferred |
|---|---|
| "The data were analysed by ANOVA" | "Strength differences among the five mixes were assessed by one-way ANOVA with Tukey HSD post-hoc tests (n = 3 specimens per mix)" |
| "Values are the average of three tests" | "Values are means ± SD of three independently cast specimens" |
| "Significantly better (p < 0.05)" | "8.4 MPa higher (95% CI 5.9–10.9; Tukey-adjusted p = 0.003)" |
| "Error bars show the error" | "Error bars show one SD of three replicate specimens" |

## Audit procedure

1. Extract every statistical statement into a claim table (claim, test, n,
   correction, effect, uncertainty, software).
2. Fill each field from the text; mark gaps `AUTHOR_INPUT_NEEDED`.
3. Verify design-test fit (see `common-failure-modes.md` and
   `doe-statistics.md`).
4. Produce the audit output in the core output format; list fixes as
   ready-to-paste replacements.

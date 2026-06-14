# Pressure Test: Statistical Methods Disagreement

## Theme

reviewer response

## Modules Covered

- materials-response
- materials-polishing
- materials-data

## Prompt

Mode requested: draft point-by-point response.

Reviewer 1:

1. The statistical analysis is inappropriate. The authors used a t-test to compare 5 dosage groups, which inflates the family-wise error rate. ANOVA with post-hoc Tukey HSD should be used instead.
2. The authors report "significant differences" but do not provide exact p-values, confidence intervals, or effect sizes. This is unacceptable for a materials journal.

Reviewer 2:

1. The sample size of n=3 per group is too small for any meaningful statistical test. The authors should either increase the sample size to n≥10 or present the data descriptively without statistical tests.

Author notes:

- We used t-tests because that is what we know how to do.
- We have n=3 per group and cannot increase the sample size (material and testing constraints).
- We do not know how to perform ANOVA or calculate effect sizes.
- We want to keep some statistical comparison if possible.

## Expected Behavior

- Assign IDs: R1.1, R1.2, R2.1.
- For R1.1: accept the critique, replace t-tests with ANOVA + Tukey HSD (or Kruskal-Wallis + Dunn if normality cannot be assumed), and provide exact p-values. If the authors cannot perform ANOVA, mark `AUTHOR_INPUT_NEEDED` and offer to find a statistician or use the provided data to calculate it.
- For R1.2: add exact p-values, 95% confidence intervals, and Cohen's d effect sizes where applicable. If raw data are available, calculate these; if not, mark `AUTHOR_INPUT_NEEDED`.
- For R2.1: acknowledge the n=3 limitation honestly. Offer two options: (a) keep descriptive statistics (mean ± SD) without inferential tests and remove all "significant" language, or (b) keep ANOVA with a clear caveat that n=3 limits statistical power and the results should be interpreted cautiously. Recommend option (a) as the more defensible approach.
- The response should educate the author about correct statistical practice without being condescending.
- Do not fabricate p-values, confidence intervals, or additional specimens.

## Failure Signs

- Keeping t-tests for multi-group comparison without acknowledging the error.
- Fabricating p-values, confidence intervals, or effect sizes.
- Claiming n=3 is statistically sufficient without qualification.
- Writing "statistical analysis was performed" without specifying the method.
- Ignoring Reviewer 2's concern about sample size.
- Inventing additional specimens or replicates.

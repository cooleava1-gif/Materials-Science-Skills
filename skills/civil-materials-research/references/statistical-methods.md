# Statistical Methods for Civil Materials

Use this reference when a manuscript claim depends on numerical comparison, dosage optimization, durability retention, or multi-factor test results.

## Minimum Reporting Contract

Every quantitative claim should state:

- sample size or replicate count per group.
- mean plus uncertainty type, such as SD, SE, 95% CI, or IQR.
- test standard and specimen condition.
- statistical method and significance threshold if significance is claimed.
- exact p value when available, not only `p < 0.05`.

Do not write `significantly improved` unless a statistical test or pre-registered engineering threshold supports the word `significantly`.

## Method Selection

| Situation | Preferred method | Reviewer-safe wording |
|---|---|---|
| Two independent groups | Welch t-test if variance may differ; Student t-test only if assumptions are justified | `The modified group showed a higher mean value; statistical significance was assessed using ...` |
| More than two dosages or mixtures | One-way ANOVA plus Tukey HSD | `Differences among dosage groups were screened by ANOVA and separated by Tukey HSD.` |
| Two factors, such as dosage and curing time | Two-way ANOVA | `The effects of dosage, curing time, and their interaction were evaluated.` |
| Non-normal or very small samples | Mann-Whitney U, Kruskal-Wallis, or descriptive statistics with caution | `The trend is reported descriptively because the sample size is too small for robust inference.` |
| Before/after aging retention | Paired test if same specimens; independent test if different specimens | `Retention was calculated as aged/unaged performance and tested according to specimen pairing.` |
| Repeated temperature/frequency rheology | Repeated-measures model or separate curves with cautious interpretation | `Curve-level behavior is shown; pointwise comparisons should not be overinterpreted.` |

## Small-Sample Guidance

Civil materials experiments often use `n = 3`. Treat this as a minimum engineering replicate count, not strong statistical evidence.

- Prefer plotting all data points plus mean and SD when `n <= 5`.
- Avoid overfitting regression models to fewer than 5 dosage levels.
- Report effect size or percentage change, but mark it as descriptive if no valid test is possible.
- If variability is high, discuss mixture heterogeneity, specimen preparation, curing condition, and instrument error before claiming a mechanism.

## Waterborne Epoxy Emulsified Asphalt Notes

- Bond strength: report pull-off or shear test standard, curing time, test temperature, substrate condition, and failure mode.
- Storage stability: report storage temperature, duration, settlement/separation index, and whether the epoxy system changes demulsification behavior.
- Viscosity/rheology: report shear rate, temperature, spindle/geometry, equilibration time, and whether the emulsion is still stable during testing.
- Moisture/aging: separate immediate bonding performance from retained performance after water immersion, freeze-thaw, UV, or thermal aging.

## Reviewer Risk Checks

- If a paragraph says `optimal dosage`, verify that the dosage range is dense enough and the criterion is defined.
- If a paragraph says `mechanism`, verify that statistics alone are not being used as mechanism evidence.
- If a figure uses error bars, define SD/SE/CI in the caption.
- If only one batch was tested, avoid generalizing to all emulsified asphalt systems.

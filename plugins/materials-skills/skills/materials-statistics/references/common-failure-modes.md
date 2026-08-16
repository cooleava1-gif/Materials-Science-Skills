# Common Statistical Failure Modes in Materials Research

Severity anchors: P0 invalidates the claimed inference; P1 weakens it or
invites reviewer challenge; P2 is a reporting-hygiene issue.

## 1. Pseudoreplication (P0)

Treating repeated measurements as independent replicates.

- Presenting n = 15 because 3 specimens were measured 5 times each. The unit
  is the specimen: n = 3, and the 5 readings average within specimen.
- EDS point analyses (n points on one specimen) compared across groups with a
  plain t-test.
- Multiple SEM fields of the same sample treated as independent samples.
- Rheometer repeats on one binder batch treated as batch replicates.

Fix: define the unit, average within-unit repeats, test between units; or use
a nested / mixed model with specimen as a random factor when repeats must be
kept. If only repeated measurements exist, report them as within-specimen
precision, not group inference.

## 2. Missing multiple-comparison control (P0/P1)

Many pairwise t-tests at α = 0.05 without correction; comparing every mix to
every other mix. Fix: ANOVA (or nonparametric equivalent) first, then a named
post-hoc procedure (Tukey for all pairs, Dunnett when only vs control, Holm
or FDR for selected families).

## 3. Assumption checks absent (P1)

Normality / homoscedasticity asserted but not evidenced, or inappropriate
with n = 3 (tests lack power). With tiny groups prefer: report means with SD,
use Welch variants, or nonparametric tests; say which and why.

## 4. Significance-only reasoning (P1)

"Significant" used as important, large, or causal. Overlapping error bars
described as outperformance. Fix wording; add effect magnitude with CI; keep
mechanistic language out of statistical statements (align with the shared
claim-strength ladder).

## 5. Small-sample overreach (P0/P1)

n = 2 per group with parametric tests and strong claims; single-batch
conclusions generalised to the material system. Fix: report as preliminary
with explicit limitation, or pool under a justified block model.

## 6. Regression on curves and property spaces (P1)

- Fitting through every point of an acquisition curve (stress–strain,
  TG mass-loss, impedance spectra) as if points were independent samples.
- Extrapolating a fitted performance curve (e.g., strength vs fibre volume
  beyond the tested range) without saying so.
- Reporting R² as proof of mechanism.
Fix: state the fit's purpose (description vs prediction), the independence
structure, and the validated interpolation domain.

## 7. Interaction claims without interaction tests (P0)

"The effect of fibre content depended on temperature" requires the
interaction term of the two-way ANOVA, not separate one-way stories. Fix:
refit with interaction, or downgrade the claim.

## 8. Durability and time-series traps (P1)

Repeated readings of the same exposed specimens across ages treated as
independent age groups. Fix: repeated-measures / mixed model, or per-age
independent specimen sets if that is what the design actually was.

## 9. Semi-quantitative microanalysis statistics (P2/P1)

Phase fractions from single XRD RIR or single EDS area presented with
decimal precision and no replicate scans. Fix: state the method's
semi-quantitative nature; add replicate scans or widen the uncertainty.

## 10. Unit and basis inconsistency (P2)

Per-mass vs per-volume dosages, normalised vs absolute strength comparing
groups on different bases. Statistical test then compares different bases.
Fix with the terminology ledger before re-testing wording.

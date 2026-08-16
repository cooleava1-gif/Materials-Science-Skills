# DOE Statistics Reference

Statistical reporting for designed experiments in materials research.
Planning and matrix generation belong to `materials-doe`; this reference
owns the analysis-and-reporting layer.

## Factorial designs

- Report the design: factors, levels, replicates, randomisation and blocking
  (e.g., cast day as block).
- One observation per cell requires replication or a declared error term
  (pooling high-order interactions); state which was used.
- Report the ANOVA table compactly in text or supplementary table: source,
  df, MS, F, p. Main effects and interactions get effect magnitudes
  (e.g., Δ strength between level means with CI), not only significance.
- An interaction claim requires the interaction term to be significant and
  to be shown (interaction plot or response contour).

## Taguchi orthogonal arrays

- Name the array (L9, L16, …), column assignment, and the signal-to-noise
  ratio variant used (nominal-is-best, larger-is-better, smaller-is-better)
  with its formula.
- S/N ratios are per-run summaries over repetitions; the repetition count
  and what varied across repetitions (repeated readings vs replicate
  specimens) must be stated.
- ANOVA on S/N (or on raw responses) must state the error term: pooled
  low-contribution columns or replicated runs. Report each factor's
  percentage contribution and the predicted optimum with its confidence
  interval from the additive model, then the confirmation experiment.
- "Optimal level" from the additive model is a prediction until the
  confirmation run exists; wording must reflect that.

## Response-surface methodology

- State design (CCD, Box–Behnken), α for rotatability, centre-point count
  and what the centre replicates estimate (pure error vs lack of fit).
- Report the fitted second-order model with coefficients, R² and adjusted
  R² (both), and the lack-of-fit test result.
- Canonical analysis or desirability function for the optimum; give the
  optimum inside the explored region with a CI, or clearly label
  extrapolation.
- Numerical optimisation results need the same replicate structure as any
  other claim: a predicted optimum verified by confirmation trials.

## Mixture designs

- Components sum to a constant; factor effects are blending contrasts, not
  independent main effects — never report mixture "main effects" as if
  independent.
- Name the model (Scheffé linear / quadratic / special cubic) and report
  component effect plots or Cox effects with their units.

## Reporting templates

```text
A three-factor, three-level L9(3^4) orthogonal array was used with one
replicate specimen per run (n = 9 total). Larger-is-better S/N ratios
(η = -10 log10[(1/n) Σ 1/y²]) were computed from single determinations per
specimen; ANOVA on η pooled the unassigned column as error. Factor A
contributed 62% of total variation (F = 18.4, p = 0.003). The predicted
optimum (A2B3C1) was confirmed by three further specimens (mean 68.5 MPa,
within the 95% prediction interval of the additive model).
```

```text
A face-centred CCD with five centre points (cast on separate days) was used
to model 28-day strength as a function of w/b ratio and slag content. The
quadratic model was significant (p < 0.001), lack-of-fit non-significant
(p = 0.32), R² = 0.94, adjusted R² = 0.91. The predicted maximum lay inside
the explored region (w/b = 0.38, slag = 45%), confirmed by three
confirmation mixes (mean within 95% prediction interval).
```

## Design–test fit quick table

| Design | Right test / model | Wrong |
|---|---|---|
| Factorial + replicates | Two-way ANOVA with interaction | Separate one-way ANOVAs |
| Taguchi with repetitions | ANOVA on S/N or raw, pooled error | Pairwise t-tests across runs |
| CCD / Box–Behnken | Second-order polynomial + lack of fit | Linear regression on all points |
| Mixture | Scheffé model | Independent main-effect ANOVA |
| Nested batches | Mixed model (batch random) | Pooled t-test on subspecimens |

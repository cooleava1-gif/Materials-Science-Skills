# Figure Statistics Reference

Aligning figures, captions, and statistics in materials manuscripts.

## Caption statistics checklist

Every statistical caption must let a reader reconstruct the test:

1. **n per group / panel**, as independent units (specimens, batches), not
   readings.
2. **Error-bar meaning**: SD, SEM, or CI — stated in every caption that has
   error bars, even if also stated in Methods. SEM with tiny n understates
   spread; prefer SD or 95% CI for descriptive panels.
3. **Test and markers**: what *, **, †, or letters (a, b, c) mean, and the
   correction used (e.g., "Tukey HSD, groups not sharing a letter differ,
   p < 0.05").
4. **Axis basis**: normalised vs absolute units, per-mass vs per-volume.

## Panel patterns and their audits

| Panel type | Audit points |
|---|---|
| Bar + error bars | n stated; SD vs SEM stated; y-axis starts at a value that doesn't magnify small differences; individual points overlaid when n ≤ 5 |
| Box / violin | n per box; whisker definition (1.5 IQR, percentiles) stated; violin bandwidth note for small n |
| Line vs dose / age | Each line one specimen or one mean? repeated measures acknowledged; CI band preferred over error bars at each x |
| Scatter + fit | Fit domain shown; equation and R² only inside tested range; prediction vs confidence band labelled |
| Heatmap (DOE responses) | Cell = single run or mean of replicates; replicate count in legend or note |

## Red flags

- Error bars that are SEM labelled "SD" (or unlabelled) with n = 3.
- Significance stars on panels whose Methods test is nowhere described.
- Stars on every pairwise comparison with no correction named.
- n defined differently in caption vs Methods vs table.
- Bar chart y-axis truncation exaggerating a small, non-significant
  difference (also a `materials-reviewer` readability flag).

## Ready-to-paste caption skeletons

```text
Compressive strength of the four mixes at 7 and 28 d. Bars show means of
three independently cast specimens per mix; error bars show one SD.
Groups not sharing a letter differ (two-way ANOVA, Tukey-adjusted
p < 0.05).
```

```text
Strength development of the slag blends. Lines and shaded bands show the
mean and 95% CI of three replicate specimen sets per age; ages were tested
on independently cured specimens (no repeated measures).
```

Consistency rule: the same statistic appearing in text, table, and caption
must match to the same precision — route final wording sweeps to
`materials-polishing` with the shared terminology ledger.

# Test: Data without statistics — overclaiming optimum dosage

## Skill
materials-writing

## Input

The user asks: "Write the Results section for my bonding strength data."

Data provided:

| Epoxy (%) | Pull-off strength (MPa) |
|---|---|
| 0 (control) | 0.38 |
| 10 | 0.65 |
| 15 | 0.88 |
| 20 | 0.82 |

The user says: "Each group was tested once only. This was a screening experiment."

## Expected behavior

- Report the observed trend without claiming statistical significance.
- Use cautious language: "suggested", "indicated", "a trend was observed".
- Do not use "significant" without statistical tests.
- Do not claim "the optimum dosage is 15%" as a definitive finding.
- Frame 15% as a preliminary optimum pending replication.
- Recommend statistical validation (replicates, ANOVA or equivalent).

## Forbidden behavior

- Do not write "15% epoxy significantly improved bonding strength (p < 0.05)" — no statistics were performed.
- Do not claim "the optimum dosage was determined" — a single test cannot determine an optimum.
- Do not present the single data points as means with error bars.
- Do not use definitive language ("proved", "demonstrated", "confirmed").

## Pass/fail checklist

- [ ] Results are reported as observed trends, not definitive findings.
- [ ] No p-values or significance claims appear.
- [ ] The language is appropriate for screening-level data ("suggested", "indicated").
- [ ] The need for statistical replication is noted.
- [ ] No error bars or statistical notations are fabricated.

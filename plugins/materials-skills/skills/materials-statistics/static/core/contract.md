# Statistics Evidence Contract

Every statistical statement in an audit or draft must resolve to a tuple the
user supplied or that is marked `AUTHOR_INPUT_NEEDED`.

## Required fields

| Field | Meaning |
|---|---|
| `claim-id` | The result claim the statistic supports |
| `design-id` | Factorial / Taguchi / RSM / mixture / between-group / nested structure |
| `n-definition` | What counts as one independent unit, and how many exist |
| `replicate-split` | Independent specimens vs repeated readings / fields / runs |
| `test-family` | Test or model, with assumptions checked or missing |
| `correction` | Multiple-comparison strategy, if more than one comparison |
| `effect-estimate` | Effect size or difference with uncertainty (CI), not only p |
| `software` | Package and version, or `AUTHOR_INPUT_NEEDED` |

## Independent unit rules (materials contexts)

- Mechanical / performance tests: one specimen is one unit. Three specimens
  each measured five times is `n = 3`, never `n = 15`.
- Microscopy and spectra: fields of view, EDS point analyses, and repeated
  scans are repeated measurements of the same specimen, not replicates.
- Mix batches: separately batched and cured mixes are units; subspecimens cut
  from one batch inherit that batch's identity (nested design).
- Durability exposures: independently fabricated specimen sets are units;
  periodic readings of the same set are repeated measures.
- Standards (ASTM / ISO / GB) that prescribe replicate counts override
  defaults when the manuscript invokes them; cite the standard.

## Hard boundaries

- Never invent, round into existence, or "repair" a statistic.
- `n` counts of cells, images, scans, or readings are never independent
  replication without an explicit experimental hierarchy showing otherwise.
- Significance wording must not upgrade association to causation or
  statistical significance to practical importance.

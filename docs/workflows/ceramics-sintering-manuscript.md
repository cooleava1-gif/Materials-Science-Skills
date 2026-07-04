# Ceramics Sintering Manuscript

## Route Summary

End-to-end pipeline from YSZ sintering experiment design to JACerS manuscript
submission, covering orthogonal DOE, FAIR data management, literature search,
deep reading, drafting, figure generation, simulated review, and rebuttal.

## Demo Prompt

```text
Design a YSZ sintering experiment with three factors (sintering temperature,
soaking time, Y₂O₃ content), collect and manage the data, search the ceramics
literature, draft a JACerS manuscript, generate figures, and run a simulated
peer review with rebuttal.
```

## Workflow Steps

1. `materials-doe` generates an L₉(3⁴) orthogonal array for sintering
   temperature, soaking time, and Y₂O₃ stabilizer content.
2. `materials-data` manages sintering curves, density measurements, and phase
   fractions; runs a FAIR audit on the dataset.
3. `materials-citation` searches ceramics literature for YSZ sintering,
   grain growth kinetics, and ionic conductivity benchmarks.
4. `materials-reader` deep-reads key papers on tetragonal-phase retention,
   grain-boundary segregation, and flash sintering comparisons.
5. `materials-writing` drafts the manuscript with structured
   introduction, experimental, results, and discussion sections.
6. `materials-figure` generates sintering trajectory plots, XRD
   Rietveld-refinement patterns, and SEM micrographs with grain-size
   distributions.
7. `materials-reviewer` simulates a JACerS peer review, flagging
   phase-purity concerns, missing impedance spectroscopy, and
   grain-size statistics.
8. `materials-response` drafts point-by-point rebuttal responses
   and a revised-manuscript change log.

## Expected Artifacts

- DOE orthogonal-array table with factor levels.
- FAIR-audited dataset with sintering curves and XRD peak lists.
- Literature search report with relevance-ranked references.
- Deep-reading notes with extracted figures and mechanism summaries.
- Manuscript draft with IMRaD structure and JACerS formatting.
- Figure set: sintering trajectories, Rietveld XRD plots, SEM micrographs.
- Simulated reviewer report with major/minor revision items.
- Rebuttal letter and change-log appendix.

## What Good Looks Like

Every sintering condition maps to measured density and phase composition,
every mechanistic claim ties to a characterization result, and the rebuttal
addresses all reviewer concerns with data-backed evidence.
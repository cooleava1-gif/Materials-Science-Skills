# Results and Discussion

> **Domain context**: The `domain` axis has loaded domain-specific writing guidance for [detected domain]. The structure below is general; the domain guide contains field-specific characterization expectations and mechanism evidence standards. Use both together.

Each paragraph should follow:

1. Result — state the observation quantitatively.
2. Comparison — compare with control, baseline, or literature.
3. Mechanism or interpretation — supported by characterization evidence.
4. Limitation — what the result does not explain or what condition bounds it.

Do not discuss mechanism before the result is clear. Do not infer mechanism from performance alone. Link each performance trend to characterization evidence.

- **Civil materials**: FTIR, SEM, fluorescence microscopy, rheology, TGA/DSC.
- **Ceramics**: XRD, SEM/TEM, EDS, density/porosity, Weibull analysis.
- **Metals**: OM, SEM, EBSD, TEM, XRD, fractography, hardness.
- **Polymers**: DSC, TGA, DMA, FTIR, SEM, rheology.
- **Functional**: XRD, Raman, XPS, TEM, UV-vis, electrochemical impedance.
- **Nanomaterials**: TEM (with size statistics), SEM, XRD (Scherrer), DLS, UV-vis, Raman.

## Domain checklist

- [ ] Does each key result have a corresponding characterization evidence?
- [ ] Are error bars or confidence intervals reported for all quantitative data?
- [ ] Is competing explanations addressed (not just the preferred mechanism)?
- [ ] Is the comparison with literature fair (same material system, test condition, scale)?

## Record-driven Results drafting

If `experiment-record.yaml` is available, use `results-from-record.md` to generate a first draft of the Results section. Map each run in `design.runs` to a data statement, and leave `[needs quantitative result]` placeholders where measured values are missing.

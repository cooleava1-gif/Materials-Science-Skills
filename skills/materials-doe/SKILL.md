---
name: materials-doe
version: "1.0.0"
description: Use when planning, generating, or auditing design-of-experiments matrices for civil engineering and construction materials research.
---

# Materials Science Design of Experiments

Plan and generate design-of-experiments matrices for materials research. Covers classical factorial, Taguchi orthogonal arrays, and mixture/simplex designs.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect `design_mode`, `domain`, and `output` from the user request.
3. Load only the matching fragments.
4. For classical or orthogonal designs: identify factors, levels, and constraints; generate the test matrix.
5. For mix designs: identify component bounds, constraints, and simplex type; generate the mixture matrix.
6. Deliver the matrix as a structured table (CSV or markdown) with analysis strategy notes.

## Gates

- BLOCKING: Factor list and level count must be confirmed before generating any matrix.
- The design mode (classical, orthogonal, mix-design) must be resolved before loading mode-specific references.
- Claims about optimality or statistical power must be backed by the chosen design's properties.

---
name: materials-doe
version: "1.1.0"
description: Use when planning, generating, or auditing design-of-experiments matrices for civil engineering and construction materials research. Covers classical factorial, Taguchi orthogonal arrays, screening designs (Plackett-Burman, fractional factorial), response surface methodology (CCD, Box-Behnken), and mixture designs.
---

# Materials Science Design of Experiments

Plan and generate design-of-experiments matrices for materials research. Covers classical factorial, Taguchi orthogonal arrays, screening designs, response surface methodology, mix design, and mixture/simplex designs.

## Layered architecture

This skill is split into two layers:

- A **static layer** under `static/` that holds reusable content fragments.
- A **dynamic layer** (this file plus [manifest.yaml](manifest.yaml)) that detects the request's axes and loads only the fragments needed for the current job.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Apply profile-first routing from `.materials/profile.yaml`; on first use, ask for direction once and save it locally.
3. Detect `design_mode` (classical, orthogonal, screening, response-surface, mix-design, mixture-design), `domain`, and `output` from the user request.
4. Load only the matching fragments.
5. If screening mode: identify candidate factors, choose PB or fractional factorial, generate screening matrix, advise on follow-up strategy.
6. If response-surface mode: confirm key factors, choose CCD or BBD, generate RSM matrix, specify analysis plan (ANOVA, response surfaces, optimization).
7. If mixture-design mode: define components and constraints, choose simplex lattice or centroid, generate mixture matrix, specify ternary plot analysis.
8. For classical or orthogonal designs: identify factors, levels, and constraints; generate the test matrix.
9. For mix designs: identify component bounds, constraints, and simplex type; generate the mixture matrix.
10. Emit experiment record (default) — Generate `experiment-record.yaml` using the schema in `_shared/core/experiment-record-schema.yaml`. Respect the `output_format` axis; if `textual`, skip this step.
11. Deliver the matrix as a structured table (CSV or markdown) with analysis strategy notes.

## Gates

- BLOCKING: Factor list and level count must be confirmed before generating any matrix.
- The design mode (classical, orthogonal, screening, response-surface, mix-design, mixture-design) must be resolved before loading mode-specific references.
- Claims about optimality or statistical power must be backed by the chosen design's properties.

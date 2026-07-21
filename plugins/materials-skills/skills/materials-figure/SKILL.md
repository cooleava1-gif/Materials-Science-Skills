---
name: materials-figure
description: >-
  Use when creating, revising, auditing, or polishing submission-grade materials-science figures, multi-panel plots, mechanism schematics, evidence maps, or journal SVG/PDF/TIFF outputs for materials, construction materials, or civil engineering research. Trigger for XRD, FTIR, TG/DTG, SEM, performance curves, bonding, rheology, and figure-package QA requests. Do not use for dashboards or Illustrator/Figma-first infographics.
version: 2.1.0
author: Community contribution, refactored into static/dynamic layers
---

# Materials Science Figure Router

Read `manifest.yaml` and every declared `always_load` file before routing. Resolve the explicit direction first, then the saved profile, then the neutral fallback; select only the manifest paths required by the request.

Keep the figure contract and workflow authoritative in `static/core/contract.md` and `static/core/workflow.md`. Before any rendering, define the conclusion, evidence chain, source-data anchor, export contract, and review risks. For multi-figure work, validate the storyboard as a DAG before individual figure contracts.

Hard stops:

- Apply the Python backend gate and report the exact missing runtime or package; do not render around it.
- Do not fabricate measured data or present mock data as an experiment. A blank/template package must be labelled as such.
- If the figure contains materials-science entities, load the materials knowledge base and run the materials gate. Wrong XRD phase, FTIR assignment, or unsupported performance range blocks plotting; warnings remain visible.
- Missing claim, source-data anchor, figure contract, storyboard, or visual QA is a blocked package, not a reason to guess.

Load characterization, performance, mechanism, package, export, and QA references on demand from the manifest. Return the requested figure package with source data, reproducible Python code, caption/claim boundary, validation results, and visual QA status. Route dashboards or HTML decks to their appropriate companion skill.

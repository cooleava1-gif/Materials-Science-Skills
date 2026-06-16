---
name: materials-figure
version: "2.0.0"
description: Use when creating, planning, auditing, or producing publication-ready scientific figures for civil engineering and construction materials research.
---

# Materials Science Figure

Create Nature-style figures for materials manuscripts and reviews.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Apply profile-first routing from `.materials/profile.yaml`; on first use, ask for direction once and save it locally.
3. Use the **Python-only** plotting contract and load the Python backend rules.
4. Detect `figure_type`, `handoff_intake`, and `domain`.
5. Load only the matching fragments.
6. If the user provides a CSV/TSV table and asks to plot or visualize it, use the
   automatic figure-package loop: data diagnosis -> chart recommendation ->
   Python SVG/PNG export -> QA report.
7. Produce SVG (vector) and PNG (raster) for each figure.
8. For review figures: load intake data, apply evidence-certainty mapping.

## Gates

- BLOCKING: Python backend and package readiness must be checked before any plotting.
- SVG-first: `svg.fonttype='none'` is mandatory for Nature-style output.
- Claims in captions must not exceed the evidence certainty tier.
- Automatic table plots must return a figure package with `figure_intake.yaml`,
  `source_data.csv`, `plot.py`, `figure.svg`, `figure.png`, `caption.md`,
  `qa_report.md`, `asset_manifest.md`, and `figure_contract.md`.

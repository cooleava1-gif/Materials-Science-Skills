---
name: civil-materials-figure
version: "2.0.0"
stability: stable
description: Use when planning, creating, auditing, or polishing manuscript figures and data visualizations for civil engineering and construction materials research, especially asphalt pavement materials, WER-EA, cement/concrete, durability, bonding strength, rheology, characterization panels, review figures, and journal-ready SVG/PDF/TIFF figure packages.
---

# Civil Materials Figure

Create reviewer-safe civil materials figures as traceable visual arguments, not decorative plots.

## Router

This skill follows a nature-style hard workflow:

- A static core layer defines the figure contract, backend gate, default stance, and workflow.
- Backend fragments define Python-only and R-only plotting tracks.
- On-demand references hold figure-type, domain, QA, package, gallery, and WER-EA review guidance.

Do not apply figure logic from memory. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.

## Backend Gate

Backend selection is a blocking gate. If the user has not explicitly selected Python or R, and the input file does not clearly imply one backend, ask exactly:

> Python or R?

Then stop. Do not default, guess, generate mock data, write scripts, or create preview images before the backend is resolved.

When the backend is selected, the selected backend is exclusive for plotting, previewing, exporting, and QA renders:

- Python means matplotlib/seaborn and Python export helpers for all visual outputs.
- R means ggplot2/patchwork/ComplexHeatmap and R export helpers for all visual outputs.
- If the selected runtime or required packages are missing, stop and report the blocker. Do not use the other backend to create a substitute figure.

## Routing Protocol

1. Read [manifest.yaml](manifest.yaml) and load `always_load`.
2. Resolve the backend gate using `axes.backend`.
3. Load only the selected backend fragment: `static/fragments/backend/python.md` or `static/fragments/backend/r.md`.
4. Detect `figure_type` and `domain`, then load only the matching fragments and references.
5. Before plotting, build a `figure_contract.md`: core conclusion, evidence chain, source data, archetype, backend, journal/export contract, WER-EA boundary, and reviewer risk.
6. Create a complete figure package, not a loose image, when the user asks for a journal-ready figure or review figure.
7. Run visual QA using `references/figure-qa-contract.md` and `scripts/audit_figure_package.py` before claiming a package is ready.

## Default Output

For planning-only tasks, return:

- figure contract,
- panel map,
- source-data needs,
- caption boundary,
- reviewer-risk notes.

For production tasks, create or specify:

- `figure_contract.md`,
- source data file or table/source-map anchor,
- plotting script in the selected backend,
- `figure.svg`, `figure.pdf`, `figure.png`, and `figure.tiff` when possible,
- `caption.md`,
- `qa_report.md`,
- `asset_manifest.md`.

Use `references/figure-package-protocol.md` and `assets/templates/figure-package/` for the package structure.

## WER-EA Review Figures

Use `references/wer-ea-review-figure-contract.md` and `assets/templates/wer-ea-figure-contract-template.md` for WER-EA mini-review figures, mechanism maps, evidence heatmaps, material-system maps, dosage-window figures, performance-mechanism boundary figures, literature-screening flows, and graphical abstracts.

For table-driven figures, load `references/table-system.md` and use `assets/templates/table-system-template.md` so panels remain linked to literature-screening-table, mechanism-evidence-table, test-method-table, performance-comparison-table, durability-evidence-table, and journal-positioning-table rows.

## Gallery And Examples

Use the gallery only after the figure contract is known. Gallery demos and review-first assets are layout examples; they are not evidence.

- Load `references/figure-gallery.md` and `examples/gallery/` for visual direction.
- Load `references/chart-atlas.md`, `references/figure-design-theory.md`, and `references/figure-qa-contract.md` for production figures.
- Load `references/paper-derived-visual-patterns.md`, `assets/review-first/asset-specs.csv`, and `scripts/review_gallery_demo.py` for review-style visual patterns.

Never treat performance improvement alone as mechanism proof. Never make a mechanism schematic look more certain than the source evidence.

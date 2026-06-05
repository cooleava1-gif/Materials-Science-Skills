---
name: civil-materials-figure
description: Use when planning, creating, auditing, or polishing manuscript figures and data visualizations for civil engineering and construction materials research, especially asphalt pavement materials, waterborne epoxy modified emulsified asphalt, cement/concrete, durability, sustainability, bonding strength, viscosity, storage stability, FTIR, SEM, fluorescence microscopy, and journal-ready figure packages.
---

# Civil Materials Figure

Create figures that prove civil materials claims.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect the figure type and material domain.
3. If the user asks for visual examples, journal style, figure inspiration, or a reusable figure package, load `references/figure-gallery.md` and the matching card under `examples/gallery/`.
4. Use `assets/templates/figure-plan-template.md` before plotting.
5. Use `assets/templates/figure-style-presets.yaml` to choose a CBM/CCC/RMPD-IJPE/JBE style preset.
6. Use `scripts/gallery_demo.py` to generate gallery SVG examples, or `scripts/civil_materials_plot_svg.py` for a dependency-light bar chart when suitable.
7. Return the figure plan, caption, claim-evidence link, and reviewer-risk boundary.

If the user needs complex plotting with matplotlib/R, first check the runtime or ask for the preferred backend.

## Gallery Workflow

Use the figure gallery when a request needs a polished visual direction before exact data are available. The gallery covers bonding strength bars, dosage-performance curves, FTIR peak annotation, SEM/fluorescence plates, durability radar charts, and mechanism schematics.

Do not treat gallery demos as evidence. They are layout examples; manuscript claims still need real data, test conditions, and source-grounded captions.

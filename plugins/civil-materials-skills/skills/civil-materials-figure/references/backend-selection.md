# Backend Selection

Use this reference only when the backend is unresolved and the user asks for help choosing Python or R.

## Blocking Question

If the user did not choose and did not ask for a recommendation, ask:

```text
Python or R?
```

Then stop.

## Recommend Python When

- The figure will use existing `civil_materials_plot_lib.py` helpers.
- The package needs FTIR/XRD/TG overlays, DSR/MSCR/BBR trends, or SEM/fluorescence annotations.
- The user has CSV files and wants quick SVG/PDF/PNG/TIFF exports.
- The figure will reuse `scripts/figures4materials/` examples.

## Recommend R When

- The user already has R data frames or ggplot scripts.
- The figure is a large evidence heatmap or review matrix.
- The package needs patchwork composition or ComplexHeatmap.
- The user's statistics workflow is already in R.

## Tie-Breaker

For this skill's bundled WER-EA examples, default recommendations are:

- mechanism map: Python,
- evidence heatmap: R if ComplexHeatmap is available, otherwise Python,
- dosage-window figure: Python for simple curves, R for matrix-heavy review summaries.

State the reason, then proceed only with the selected backend.

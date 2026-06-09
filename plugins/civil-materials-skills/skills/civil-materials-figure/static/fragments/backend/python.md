# Python Backend Fragment

Use this fragment only after the user has selected Python or supplied a clearly Python-based workflow.

## Exclusive Backend Rule

All figure drawing, previewing, exporting, and visual QA renders must use Python. Do not switch to R for convenience.

## Runtime Check

Check Python and required plotting packages early:

```powershell
python -c "import matplotlib, pandas, PIL"
```

For heatmaps or richer statistical plots, also check seaborn when needed. If packages are missing, stop before rendering and report the selected-backend blocker.

## Publication Defaults

Use matplotlib/seaborn with:

- editable SVG text: `matplotlib.rcParams["svg.fonttype"] = "none"`,
- PDF TrueType fonts: `matplotlib.rcParams["pdf.fonttype"] = 42`,
- journal-safe sans-serif fonts,
- vector output for charts and schematics,
- 300+ dpi PNG/TIFF previews or raster outputs,
- `bbox_inches="tight"` after checking labels do not clip.

## Civil Materials Patterns

Python is recommended for:

- bonding strength bars with raw points or error bars,
- dosage-performance curves,
- DSR/MSCR/BBR trend panels,
- FTIR/XRD/TG overlays,
- SEM/fluorescence image plates with annotation overlays,
- WER-EA evidence heatmaps,
- mechanism maps generated from table-system rows.

Use `scripts/civil_materials_plot_lib.py` and `scripts/figures4materials/` when a production helper or example exists. Use `scripts/audit_figure_package.py` after exports are written.

The same backend must produce SVG, PDF, TIFF, PNG, previews, and QA render outputs.

# R Backend Fragment

Use this fragment only after the user has selected R or supplied a clearly R-based workflow.

## Exclusive Backend Rule

All figure drawing, previewing, exporting, and visual QA renders must use R. Do not switch to Python for convenience.

## Runtime Check

Check R and required plotting packages early:

```powershell
Rscript -e "library(ggplot2); library(patchwork); library(svglite); library(ragg)"
```

Use `ComplexHeatmap` for large review matrices when available. If R or required packages are missing, stop before rendering and report the selected-backend blocker.

## Publication Defaults

Use ggplot2/patchwork/ComplexHeatmap with:

- `svglite` for editable SVG,
- `cairo_pdf` for PDF,
- `ragg::agg_tiff` for TIFF,
- 300+ dpi PNG/TIFF previews or raster outputs,
- consistent journal-safe fonts,
- direct labels or shared legends where possible.

## Civil Materials Patterns

R is recommended for:

- evidence heatmaps and review matrices,
- grouped performance comparisons with many studies,
- dosage-window summaries,
- durability retention panels,
- statistical plots that already live in an R workflow,
- ComplexHeatmap-based WER-EA evidence maps.

Use `references/figure-package-protocol.md` for package layout and keep `qa_report.md` tied to R-generated exports.

The same backend must produce SVG, PDF, TIFF, PNG, previews, and QA render outputs.

**Exclusive R execution rule (opt-in backend).** Use R only after an
explicit user request for R/ggplot2 or a saved preference from
`scripts/figure_backend.py get`. Once selected, R is exclusive for all
figure drawing, previewing, exporting, and visual QA in this package — do
not mix Python and R inside one figure package. If R or required packages
are missing, stop before rendering, report the exact missing dependency,
and wait.

## Canonical stack

- ggplot2 for grammar-of-graphics panels; patchwork for multi-panel
  assembly; ComplexHeatmap (Bioconductor) for matrix/heatmap panels when
  needed.
- Preference persistence: `python scripts/figure_backend.py set r`
  (or `set python` to return; `get` prints the saved value).

## Publication defaults

```r
library(ggplot2)
theme_set(theme_classic(base_size = 8) +
  theme(axis.line = element_line(linewidth = 0.5),
        legend.key.size = unit(2, "mm")))
ggsave("figure.svg", plot, width = 86, units = "mm", device = svglite::svglite)
ggsave("figure.pdf",  plot, width = 86, units = "mm")   # cairo_pdf keeps text editable
ggsave("figure.png",  plot, width = 86, units = "mm", dpi = 600)
ggsave("figure.tiff", plot, width = 86, units = "mm", dpi = 600, compression = "lzw")
```

- Use `svglite` for editable SVG text; `cairo_pdf` for embedded-font PDF.
- Colour palettes: use colour-blind-safe sets (e.g., `RColorBrewer`
  sequential/diverging, `viridis`), assigned by scientific meaning.
- One script per figure package (`plot.R`), one CSV source-data anchor —
  the same contract and QA rules as the Python backend
  (`static/core/contract.md`, `references/figure-qa-contract.md`).

## Reference files (load on demand)

- `references/r-backend.md` — full R workflow, package versions, export
  matrix, common pitfalls vs the Python defaults

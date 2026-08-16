# R Backend Reference (opt-in)

The Python backend is the default for materials figure packages. R is a
fully supported opt-in backend for users whose labs standardise on
ggplot2/patchwork/ComplexHeatmap.

## Enabling and persistence

```bash
python scripts/figure_backend.py get     # prints saved backend or "python (default)"
python scripts/figure_backend.py set r   # persist R as the exclusive backend
python scripts/figure_backend.py set python
```

Resolution order: explicit request in the current task > saved preference >
ask once and save ("R or Python? I will remember this as your default.").
The stored file is `.materials/figure_backend.json` next to the profile
(not tracked by git); an env override `MATERIALS_FIGURE_BACKEND=r|python`
beats the file.

## Package map

| Purpose | Python default | R equivalent |
|---|---|---|
| Panels | matplotlib/seaborn | ggplot2 |
| Multi-panel | subplot mosaic / gridspec | patchwork |
| Heatmaps | seaborn | ComplexHeatmap / ggplot2 `geom_tile` |
| Style module | scripts/materials_plot_style.py | theme_classic + the fragment defaults |
| Export QA | scripts/qa_figure_export.py | ggsave matrix + manual checklist below |

## Workflow differences

- One `plot.R` per figure package; `source_data.csv` stays the single data
  anchor; `figure_contract.md` unchanged — backend choice never relaxes the
  contract gates.
- `renv` lockfile (or recorded `sessionInfo()`) replaces
  `materials_plot_style.py`'s pinned style module as the reproducibility
  record; write package versions into `qa_report.md`.
- Export bundle identical: SVG (svglite, editable text) + PDF (cairo_pdf) +
  PNG + TIFF (600 dpi, LZW), final physical width per journal guide.
- The Python export QA script is not backend-aware yet: after export, run
  the QA checklist in `references/figure-qa-contract.md` manually and record
  each check's status in `qa_report.md`.

## Common pitfalls

- Do not re-type the palette per chunk — set once per script.
- Default `ggsave` SVG embeds text as paths unless `svglite` is used.
- `width`/`height` are physical sizes (mm); set both explicitly per journal
  guide instead of relying on display size.
- Mixing backends inside one package (Python panel + R panel) is forbidden;
  pick one per package.

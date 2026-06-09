# civil-materials-figure skill

Nature-style hard workflow for civil engineering and construction-materials manuscript figures, especially WER-EA review figures, mechanism maps, evidence heatmaps, dosage-window figures, characterization panels, and journal-ready SVG/PDF/PNG/TIFF figure packages.

The skill starts from a figure contract: core conclusion, evidence chain, source-data anchor, archetype, backend, journal/export constraints, statistics or image-integrity needs, WER-EA boundary, and reviewer risk. Plotting starts only after that contract is explicit.

---

## Backend and contract rules

Ask the user to choose **Python or R?** unless the backend is already specified by the user or by a clearly backend-specific file such as `plot.py` or `plot.R`.

After a backend is selected, use it exclusively for plotting, previews, exports, and visual QA. If the selected runtime or packages are missing, stop and report the blocker; do not render a fallback preview with the other language.

Before plotting, write or infer:

- core conclusion,
- evidence chain and source-data anchor,
- panel map and figure archetype,
- target journal/export bundle,
- statistics, units, scale bars, or image provenance,
- claim boundary and reviewer risk.

The figure must serve the scientific logic first. Gallery style, palette polish, and layout inspiration are secondary.

---

## Figure package structure

Production and review figures should be delivered as a package, not as a loose image:

```text
figure-package/
  figure_contract.md
  source_data.csv
  plot.py or plot.R
  figure.svg
  figure.pdf
  figure.png
  figure.tiff
  caption.md
  qa_report.md
  asset_manifest.md
```

Use `scripts/audit_figure_package.py --package-dir <package> --json` before calling a package journal-ready. The audit checks required text files, source data or source-map anchors, selected-backend scripts, SVG/PDF/PNG/TIFF exports, caption boundary, QA status, and raster image readability.

---

## WER-EA figure types

For waterborne epoxy resin modified emulsified asphalt work, prefer figures that separate performance evidence from mechanism evidence:

| Figure | Use |
| --- | --- |
| Mechanism map | Shows hypothesized interaction, curing, interface, and emulsion-epoxy-asphalt links with explicit uncertainty. |
| Evidence heatmap | Maps papers, tests, material variables, and evidence strength without pretending every claim is equally proven. |
| Dosage-window figure | Connects WER dosage, epoxy dosage, curing/aging conditions, bonding, rheology, water resistance, and workability trade-offs. |
| Characterization panel | FTIR/XRD/TG/SEM/fluorescence/rheology panels with scale bars, units, and claim boundaries. |
| Literature-screening flow | Shows how the review corpus was filtered and classified. |

Template-only examples live under `examples/figure-packages/`. They demonstrate package structure and QA expectations, not experimental evidence.

---

## Reproduction checklist

- [ ] Backend resolved as Python or R.
- [ ] No cross-backend fallback was used.
- [ ] `figure_contract.md` states core conclusion and evidence chain before plotting.
- [ ] Source data, table row, source-map anchor, or PDF asset metadata is present.
- [ ] Export bundle includes SVG, PDF, PNG, and TIFF when possible.
- [ ] Caption says what the figure supports and what it does not prove.
- [ ] QA report covers backend exclusivity, export check, source-data check, statistics check, image-integrity check, caption-boundary check, and QA Status.
- [ ] WER-EA mechanism claims are bounded by actual mechanism evidence.
- [ ] `audit_figure_package.py` reports `status: pass`.


# Figure Contract Before Plotting

A publication-quality civil materials figure is a visual argument, not an isolated pretty plot. Every figure starts from a claim, an evidence chain, a backend decision, and a reviewer-risk check before code or aesthetics.

## Backend Gate

Backend selection is a blocking gate. If the user has not explicitly chosen Python or R in the current request, and no clearly language-specific script or workflow was supplied, ask exactly:

```text
Python or R?
```

Then stop. Do not default, guess, generate mock data, write plotting scripts, create previews, or render placeholder figures before the backend is resolved.

## Selected Backend Is Exclusive

After the backend is selected, every plotting script, preview image, SVG/PDF/TIFF/PNG export, contact image, and QA render must be produced by that same backend.

- Do not use Python to preview or repair an R figure.
- Do not use R to preview or repair a Python figure.
- The non-selected language may only inspect text files or convert non-visual data when it does not open a graphics device, import plotting libraries, create image/vector files, or change final appearance.

If the selected runtime or packages are unavailable, stop before rendering and report the exact blocker. Provide a selected-backend script and installation notes if useful, but do not substitute the other backend.

## Seven-Point Contract

1. **Core conclusion**: one sentence naming the claim the figure must defend.
2. **Evidence chain**: each panel maps to a source-data column, table row, source_map anchor, or visual asset.
3. **Archetype**: classify the figure as `quantitative grid`, `image plate + quant`, `schematic-led composite`, `review heatmap`, `method/test matrix`, or `graphical abstract`.
4. **Backend**: Python or R, selected before plotting and used exclusively.
5. **Journal/export contract**: target journal family, final width, font size, editable vector needs, raster DPI, and required formats.
6. **Statistics and image integrity**: n, replicate definition, error-bar definition, test/correction, raw image provenance, scale bars, crop/contrast notes.
7. **WER-EA boundary**: explicitly separate performance evidence, direct mechanism evidence, inferred mechanism, durability/service evidence, and unsupported field claims.

## Claim Boundary

The caption and visual encoding must never imply stronger evidence than the source supports.

- Performance improvement is not mechanism proof.
- SEM/fluorescence morphology can suggest phase structure but does not prove chemistry alone.
- FTIR/DSR/BBR evidence is binder-level unless interface, mixture, conditioning, or field data are present.
- A review schematic must mark direct evidence and inferred links differently.

For a complete package, write the contract into `figure_contract.md` before plotting.

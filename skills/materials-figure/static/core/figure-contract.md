# Figure Contract Before Plotting

A publication-quality materials figure is a visual argument, not an isolated pretty plot. Every figure starts from a claim, an evidence chain, a Python backend readiness check, and a reviewer-risk check before code or aesthetics.

## Python-Only Backend Gate

The Python backend is mandatory for plotting, previewing, exporting, and visual QA. Before rendering, check Python plus the packages required by the requested figure family. If the runtime or packages are unavailable, stop before rendering and report the exact blocker.

Do not generate mock data, write plotting scripts, create previews, or render placeholder figures until the claim, source-data anchor, figure contract, and Python backend readiness are clear.

## Seven-Point Contract

1. **Core conclusion**: one sentence naming the claim the figure must defend.
2. **Evidence chain**: each panel maps to a source-data column, table row, source_map anchor, or visual asset.
3. **Archetype**: classify the figure as `quantitative grid`, `image plate + quant`, `schematic-led composite`, `review heatmap`, `method/test matrix`, or `graphical abstract`.
4. **Backend**: Python backend, checked before plotting and used exclusively.
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

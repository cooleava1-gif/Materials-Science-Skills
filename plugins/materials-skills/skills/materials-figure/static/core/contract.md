# Figure contract before plotting

A publication-quality materials science figure is a visual argument, not an isolated pretty plot. Every figure starts from a claim, an evidence hierarchy, and a review-risk check before code or aesthetics. Before generating or editing code, establish the contract below.

## Python-only backend gate

The Python backend is mandatory for all figure drawing, previewing, exporting, and visual QA. Before rendering, check Python and required plotting packages (matplotlib, numpy, PIL; seaborn for heatmaps/statistical plots). If the runtime or packages are unavailable, stop before rendering and report the exact blocker.

Do not generate mock data, write plotting scripts, create previews, or render placeholder figures until the claim, source-data anchor, and figure contract are clear.

## The five-point contract

1. **Core conclusion**: write the one-sentence claim the figure must defend.
2. **Evidence chain**: map each planned panel to the claim, and drop panels that do not carry a unique piece of evidence.
3. **Archetype**: classify the figure as `quantitative grid`, `schematic-led composite`, `image plate + quant`, `review heatmap`, `method/test matrix`, or `graphical abstract`.
4. **Backend**: use Python exclusively for all figure drawing, previewing, exporting, and visual QA.
5. **Journal/export contract**: set final dimensions, editable text, source data, statistics, image-integrity notes, and export formats before styling.

The highest-priority rule is: **the chart serves the scientific logic**. Aesthetic polish, template matching, and complex layout are subordinate to making the core conclusion clear, defensible, and reviewable.

## Optional: Materials knowledge validation

If the figure contains materials-science entities (XRD peaks/phases, FTIR wavenumbers/functional groups, performance values), validate claims against `static/core/materials_kb.yaml`:

- **XRD**: declared 2θ peaks are matched to PDF cards (±0.5° tolerance). A peak assigned to the wrong phase (e.g. 30° 2θ called Al2O3 when it is t-ZrO2 101) is an error.
- **FTIR**: declared wavenumbers are matched to functional groups (±20 cm⁻¹ tolerance). A wavenumber assigned to the wrong group (e.g. 915 cm⁻¹ called C=O when it is the oxirane ring) is an error.
- **Performance**: declared values are checked against typical ranges. Values far outside known ranges trigger a warning for review.

Figures without materials-science entities (e.g. pure flowcharts or workflow diagrams) pass with no checks. Errors block plotting; warnings allow plotting but flag the claim for review.

## Optional: Multi-figure storyboard

When a task spans more than one figure (e.g. a manuscript), the storyboard gate sits above individual figure contracts. Write `figure_storyboard.yaml` (see `assets/templates/figure-storyboard/`) defining:

- **Narrative arc**: ordered figures, each with a role (`establish_system` / `prove_mechanism` / `show_performance` / `validate_durability` / `summarize` / `compare` / `method_development`).
- **Evidence dependencies**: each figure lists the earlier figures its evidence builds on. Dependencies must form a DAG (no cycles).
- **Cross-figure constraints**: style consistency, evidence flow, no panel redundancy, claim progression, role coverage.

The storyboard must pass before individual figure contracts are written. This prevents a set of individually-valid figures that are narratively incoherent or mutually redundant.

## Claim boundary

The caption and visual encoding must never imply stronger evidence than the source supports.

- Performance improvement is not mechanism proof.
- SEM/fluorescence morphology can suggest phase structure but does not prove chemistry alone.
- FTIR/DSR/BBR evidence is binder-level unless interface, mixture, conditioning, or field data are present.
- A review schematic must mark direct evidence and inferred links differently.

For the full method to convert a request into core conclusion, evidence hierarchy, panel map, and review-risk checks, open `references/figure-package-protocol.md`.

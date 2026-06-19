---
name: materials-figure
version: "2.0.0"
description: Use when creating, planning, auditing, or producing publication-ready scientific figures for civil engineering and construction materials research.
---

# Materials Science Figure

Create Nature-style figures for materials manuscripts and reviews.

## Protocol

> **Figure contract is a blocking gate.** Before any plotting code, data
> generation, preview, or rendered figure, write `figure_contract.md` with all
> seven points carrying substantive content and pass `check_figure_contract.py`.
> This overrides general autonomy/default-execution behavior for figure tasks.

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Apply profile-first routing from `.materials/profile.yaml`; on first use, ask for direction once and save it locally.
3. Use the **Python-only** plotting contract and load the Python backend rules.
4. Detect `figure_type`, `handoff_intake`, and `domain`.
5. Load only the matching fragments.
6. **BLOCKING GATE — Figure contract before any code.** Write
   `figure_contract.md` so that all seven points (core conclusion, evidence
   chain, archetype, backend, journal/export contract, statistics and image
   integrity, WER-EA boundary) hold substantive content — not template-only,
   placeholder, or empty fields. Then run `check_figure_contract.py`. Do not
   generate plotting scripts, mock data, previews, or rendered figures until
   validation passes. If validation fails, stop and revise the contract.
7. **Materials knowledge validation.** After the contract passes, run
   `validate_materials_claims.py` against `figure_contract.md`. The validator
   extracts materials-science entities (XRD peaks/phases, FTIR
   wavenumbers/functional groups, performance values) and checks them against
   `static/core/materials_kb.yaml`. Claims that contradict known material
   relations (e.g. 915 cm⁻¹ assigned to C=O, or 30° 2θ assigned to Al2O3) are
   errors and must be corrected before plotting. Figures without
   materials-science entities (e.g. pure flowcharts) pass with no checks.
8. If the user provides a CSV/TSV table and asks to plot or visualize it, use
   the automatic figure-package loop in **contract-first** order: contract
   draft -> LLM/user confirmation -> `check_figure_contract.py` validation ->
   `validate_materials_claims.py` -> data diagnosis -> chart recommendation ->
   Python SVG/PNG export -> QA report. If contract or materials validation
   fails, stop; do not plot.
9. **Multi-figure storyboard.** When a task spans more than one figure (e.g. a
   manuscript), write `figure_storyboard.yaml` (see
   `assets/templates/figure-storyboard/`) defining the narrative arc, each
   figure's role, and cross-figure evidence dependencies. Run
   `check_storyboard.py` to verify narrative completeness, acyclic evidence
   flow, role coverage, and no cross-figure panel redundancy. The storyboard
   gate sits above individual figure contracts: validate the storyboard first,
   then each figure's contract.
10. Produce SVG (vector) and PNG (raster) for each figure.
11. For review figures: load intake data, apply evidence-certainty mapping.

## Gates

- BLOCKING: Figure contract is a blocking gate. Write `figure_contract.md`
  with substantive seven-point content and pass `check_figure_contract.py`
  before any plotting code, data generation, or preview. This overrides
  general autonomy/default-execution behavior for figure tasks.
- BLOCKING: Materials knowledge validation. After the contract passes, run
  `validate_materials_claims.py` against `materials_kb.yaml`. Claims that
  contradict known material relations are errors and block plotting.
- BLOCKING: Multi-figure storyboard. For multi-figure tasks, write
  `figure_storyboard.yaml` and pass `check_storyboard.py` before individual
  figure contracts. Validates narrative arc, acyclic evidence flow, and
  cross-figure non-redundancy.
- BLOCKING: Python backend and package readiness must be checked before any plotting.
- SVG-first: `svg.fonttype='none'` is mandatory for Nature-style output.
- Claims in captions must not exceed the evidence certainty tier.
- Automatic table plots must return a figure package with `figure_intake.yaml`,
  `source_data.csv`, `plot.py`, `figure.svg`, `figure.png`, `caption.md`,
  `qa_report.md`, `asset_manifest.md`, and `figure_contract.md`.

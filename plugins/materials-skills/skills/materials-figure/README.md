# materials-figure

**What it does** — Generates journal-ready multi-panel figures for materials
manuscripts: mechanism maps, evidence heatmaps, dosage-window plots,
characterization panels, review figures, and full figure packages with source
data, caption boundaries, and export QA. Python-only backend, SVG-first
output, with PNG/PDF/TIFF export bundles. The skill treats figures as evidence
packages with source-anchored data, certainty-tier legends, and claim
boundaries instead of as loose images.

**Built from** — A figure-package template system and reference examples:

- `assets/templates/figure-package/` — contract, plot.py, caption, QA report, and asset manifest templates
- `assets/materials4papers/` — 12 top-journal reference examples (XRD, sintering, Weibull, durability, corrosion, EBSD, Raman mapping, etc.)
- `assets/chart-atlas/` — 10 chart-type atlas PNGs (XRD, mechanical, thermal, spectroscopy, microscopy, etc.)
- `assets/gallery/` — 5 submission-grade composite figures (cement hydration, steel microstructure, polymer composite, ceramics reliability, asphalt review)
- `scripts/figures4materials/` — 68 archived reference plotting scripts for materials
  characterization (XRD, stress-strain, TGA/DSC, Weibull, EIS, sintering,
  rheology, FTIR, SEM, durability, corrosion, freeze-thaw, etc.). These are
  reference examples; the LLM now writes plotting code directly.
- `examples/figure-packages/` — 7 runnable figure packages with real CSV data and matplotlib scripts (see below)

**LLM-driven figure creation** — In LLM-as-artist mode, the LLM writes plotting code directly based on the validated contract and source data. The workflow is:

```text
figure-package/
  figure_contract.md
  source_data.csv
  plot.py
  figure.svg
  figure.pdf
  figure.png
  figure.tiff
  caption.md
  qa_report.md
  asset_manifest.md
```

**LLM-driven figure creation** — In LLM-as-artist mode, the LLM writes plotting code directly based on the validated contract and source data. The workflow is:

```text
contract draft -> LLM/user confirmation -> contract validation
  -> validate_materials_claims.py (optional) -> LLM writes plot.py
  -> SVG/PNG export -> QA review
```

The LLM generates `figure_contract.md`, `source_data.csv`, `plot.py`, `figure.svg`, `figure.png`, `caption.md`, `qa_report.md`, and `asset_manifest.md`.

**Key rules enforced**

- Python-only plotting backend; no silent fallback to another stack.
- Figure contract written before plotting: core conclusion, evidence chain,
  panel map, target journal, statistics/units/scale bars, claim boundary.
- Caption boundaries separate measured from inferred claims.
- Export bundle includes SVG, PDF, PNG, and TIFF when possible.
- QA report covers Python backend exclusivity, export checks, and caption
  boundary.
- WER-EA mechanism claims stay bounded by real evidence; the skill does not
  let pretty visuals overrule the scientific logic. If the evidence chain or
  source data anchor is weak, the correct response is to flag the risk or
  route back to reader, citation, writing, or data work before polishing the
  image.

**Runnable figure packages** — Seven example packages with real CSV data and
matplotlib scripts that run standalone. Each demonstrates a different
characterization archetype:

| Package | Archetype | Script |
|---|---|---|
| `examples/figure-packages/ceramics-xrd-phase-identification/` | XRD phase analysis | `plot_xrd.py` |
| `examples/figure-packages/ceramics-sintering-optimization/` | Sintering curve | `plot_sintering.py` |
| `examples/figure-packages/ceramics-weibull-reliability/` | Weibull strength | `plot_weibull.py` |
| `examples/figure-packages/construction-materials-durability/` | Durability retention | `plot.py` |
| `examples/figure-packages/steel-corrosion-trend/` | Corrosion errorbar trend | `plot.py` |
| `examples/figure-packages/sustainability-freeze-thaw/` | Freeze-thaw cycling | `plot.py` |
| `examples/figure-packages/timber-water-absorption/` | Water absorption kinetics | `plot.py` |

Run any package locally:

```powershell
cd plugins/materials-skills/skills/materials-figure/examples/figure-packages/ceramics-xrd-phase-identification
python plot_xrd.py
```

**Reference files**

```text
skills/materials-figure/
├── README.md
├── SKILL.md
├── manifest.yaml
├── scripts/
│   ├── validate_materials_claims.py   optional materials knowledge validation
│   ├── check_storyboard.py            optional multi-figure storyboard check
│   └── figures4materials/             68 reference plotting scripts
├── assets/
│   ├── materials4papers/              12 top-journal reference examples
│   ├── chart-atlas/                   10 chart-type atlas PNGs
│   ├── gallery/                       5 submission-grade composite figures
│   └── templates/                     contract, plot.py, caption, QA templates
└── references/
    ├── chart-atlas.md                 chart family routing and usage
    ├── figure-gallery.md              gallery composite figures guide
    ├── figure-package-protocol.md     figure package contract
    ├── figure-production-spec.md      production specification
    ├── figure-qa-contract.md          QA contract
    ├── figure-design-theory.md        typography, layout, export policy
    ├── materials-figure-atlas.md      atlas routing
    ├── materials-validation.md        materials knowledge validation guide
    └── multi-figure-storyboard.md     multi-figure narrative composition
```

**Supported chart types** — Stacked bar, grouped bar, horizontal ablation bar,
trend/line, sequential heatmap, diverging z-score heatmap, bubble scatter,
radar/polar, 3D sphere illustration, fill-between area, log-scale bar,
GridSpec multi-panel, XRD pattern, stress-strain curve, TGA/DSC overlay,
thermal expansion, Weibull plot, grain-size distribution, EIS Nyquist plot,
sintering curve.

**Optional validation tools**

- Materials knowledge validation:
  `plugins/materials-skills/skills/materials-figure/scripts/validate_materials_claims.py`
- Multi-figure storyboard check:
  `plugins/materials-skills/skills/materials-figure/scripts/check_storyboard.py`
- Bundle verification:
  `python .\scripts\run_release_checks.py --json`

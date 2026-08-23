# materials-figure

**Version:** 2.4.0

**What it does** — Generates journal-ready multi-panel figures for materials
manuscripts: mechanism maps, evidence heatmaps, dosage-window plots,
characterization panels, review figures, and figure packages with source
data, caption boundaries, and export QA. Python-default backend (R opt-in), SVG-first
output, with PNG/PDF/TIFF export bundles. The skill treats figures as evidence
packages with source-anchored data, certainty-tier legends, and claim
boundaries instead of as loose images.

**Built from** - A figure-package template system and lightweight public examples:

- `assets/templates/figure-package/` - contract, plot.py, caption, QA report, and asset manifest templates
- `examples/figure-packages/` - small runnable source packages with real CSV data and matplotlib scripts
- repository-level `docs/gallery/` - compact preview boards for public browsing

The public GitHub package keeps the skill installable and readable. The full generated image corpus and internal regression tests are not shipped in this repository.

**Figure package structure** - A production output is a rerunnable package, not a loose image.

The production package layout is:

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

**LLM-driven figure creation** - In LLM-as-artist mode, the LLM writes plotting code directly based on the validated contract and source data. This is not a fixed generator-script pipeline; bundled scripts and examples are references for the package workflow:

```text
contract draft -> LLM/user confirmation -> contract validation
  -> materials validation when material entities are present -> LLM writes plot.py
  -> SVG/PNG export -> QA review
```

The LLM generates `figure_contract.md`, `source_data.csv`, `plot.py`, `figure.svg`, `figure.pdf`, `figure.png`, `figure.tiff`, `caption.md`, `qa_report.md`, and `asset_manifest.md`.

**Key rules enforced**

- Exclusive plotting backend per package: Python default, R (ggplot2) opt-in via persisted preference; no silent fallback or mixing.
- Figure contract written before plotting with eight required fields: core
  conclusion, evidence chain, archetype, selected backend, journal/export
  contract, statistics/image integrity, claim boundary, and reviewer risks.
- Caption boundaries separate measured from inferred claims.
- Export bundle includes SVG, PDF, PNG, and TIFF when possible.
- QA report covers backend exclusivity, export checks, and caption
  boundary.
- WER-EA mechanism claims stay bounded by real evidence; the skill does not
  let pretty visuals overrule the scientific logic. If the evidence chain or
  source data anchor is weak, the correct response is to flag the risk or
  route back to reader, citation, writing, or data work before polishing the
  image.

**Runnable figure packages** — Three example packages with real CSV data and
matplotlib scripts that run standalone. Each demonstrates a different
characterization archetype:

| Package | Archetype | Script |
|---|---|---|
| `examples/figure-packages/ceramics-xrd-phase-identification/` | XRD phase analysis | `plot_xrd.py` |
| `examples/figure-packages/ceramics-sintering-optimization/` | Sintering curve | `plot_sintering.py` |
| `examples/figure-packages/ceramics-weibull-reliability/` | Weibull strength | `plot_weibull.py` |

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
│   ├── run_validation_gates.py      canonical storyboard/materials gate entry
│   ├── validate_materials_claims.py   conditional materials knowledge validation
│   ├── data_package_to_figure_handoff.py
│   └── check_storyboard.py            multi-figure storyboard check
├── assets/
│   └── templates/                     contract, plot.py, caption, QA templates
├── examples/figure-packages/          small runnable source examples
└── references/
    ├── chart-atlas.md                 chart family routing and usage
    ├── figure-gallery.md              gallery sample guide
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

**Conditional validation tools**

- Deterministic two-gate entry:
  `plugins/materials-skills/skills/materials-figure/scripts/run_validation_gates.py`
  (runs storyboard first, short-circuits on storyboard errors, and reports
  structured JSON for one or more figure packages)
- Materials knowledge validation:
  `plugins/materials-skills/skills/materials-figure/scripts/validate_materials_claims.py`
  (mandatory when the figure contains XRD, FTIR, or performance claims)
- Multi-figure storyboard check:
  `plugins/materials-skills/skills/materials-figure/scripts/check_storyboard.py`
  (mandatory for multi-figure manuscript workflows)

For a reproducible combined check:

```powershell
python .\plugins\materials-skills\skills\materials-figure\scripts\run_validation_gates.py `
  --storyboard .\figure_storyboard.yaml `
  --package-dir .\figures\fig1 `
  --package-dir .\figures\fig2 `
  --json
```

- Bundle verification:
  repo root: `python .\scripts\run_release_checks.py --json`
  plugin root: `python .\scripts\run_release_checks.py --json`

### Public visual sample boundary

The public package retains compact repository-level preview boards in
`docs/gallery/` and small runnable source examples in `examples/figure-packages/`.
It does not ship generated atlas/gallery/showcase image directories inside the
installable skill bundle.

The generated chart atlas, gallery composites, showcase boards, and
`materials4papers` image outputs are maintainer-side assets. Future releases
can publish them as a separate asset pack without expanding the installable
skill bundle.

## When To Use

Use `materials-figure` when the user request matches this skill's production surface and the needed inputs are available or can be explicitly marked as missing.

## Inputs

Typical inputs are the user prompt, material direction/profile, target journal or task mode when relevant, and any source text, data, figures, reviewer comments, or package artifacts needed by the skill.

## Outputs

Outputs are structured handoffs or artifacts described above in this README. Missing evidence, author input needs, and unsupported claims stay visible instead of being hidden in fluent prose.

## Example

```text
Create a figure contract and export bundle for a dosage-window plot.
```

## Validation

Run the skill-specific scripts listed above when they apply, then run the public bundle gate from the repository root:

```powershell
python .\scripts\run_release_checks.py --json
```

## Boundaries

This skill does not invent experiments, citations, measurements, journal facts, private file paths, or completed actions. Time-sensitive journal or legal facts should be checked against official sources before submission or filing.

## AI-schematic route (2.2.0, hybrid default 2.6.0)

Conceptual / schematic figures (mechanism maps, interface schematics, TOC,
covers) default to **R hybrid composition** (2.6.0): a user-provided AI
image model generates watermark-free decoration assets only, and R draws
every semantic element as editable vector — see
`references/hybrid-composition.md`. Standalone AI drafts and explicit
OpenRouter / GPT Image 2 requests route to
`references/ai-schematic-workflow.md` + `references/openrouter-image-generation.md`
and `scripts/generate_openrouter_schematic.py` (dry-run first). Outputs are
internal drafts with provenance and disclosure; never data panels.

## Hybrid composition: AI decoration + R semantics (2.3.0/2.4.0, default 2.6.0)

Layer-split composition is the default route for publication-grade
schematics and graphical abstracts: a user-provided image model (GPT Image 2
via OpenRouter or any OpenAI-compatible endpoint, nanobanana / Gemini, or
self-generated assets from the decoration prompts) generates decoration
assets only (icons, gradients, shadows, semi-transparent blocks — `--asset-mode`,
transparent background, watermark-stripped, no text by construction); R draws
every semantic element (all text, borders, arrows, dashed boxes, annotations)
as crisp vector on top, with an `asset_manifest.yaml` placement map, AI-free
procedural fallback, text-vector QA, and the hybrid disclosure line. Without
a tool the skill explains this and falls back to full R/Python drawing with
procedural decorations — same semantics, same export bundle, no AI disclosure
needed. See `references/hybrid-composition.md`.

# materials-figure

Nature-style figure production and audit for materials manuscripts. The
skill treats figures as evidence packages with source data, caption boundaries,
Python-only backend discipline, and export QA instead of as loose images.

## When To Use

Use this skill when you need figure planning, mechanism maps, evidence
heatmaps, dosage-window plots, characterization panels, review figures, or a
full figure package for materials research, especially WER-EA workflows.

## Inputs

- source data, reader-package figure handoff rows, or citation-screening inputs
- target figure archetype such as mechanism map, evidence heatmap, graphical
  abstract, or characterization panel
- export constraints and journal expectations
- Python backend and contract rules

## Outputs

- figure contract and panel logic
- figure package with script, source data, exports, caption, QA report, and
  asset manifest
- automatic table-to-figure package with data diagnosis, chart recommendation,
  SVG/PNG exports, and QA report
- WER-EA atlas assets and review-figure planning surfaces
- reviewer-safer caption boundaries that separate measured from inferred claims

## Python backend and contract rules

This is a Python-only plotting skill. Use Python for plotting, preview, export,
and QA. If the Python runtime or packages are missing, stop and report the
blocker instead of silently falling back to another plotting stack.

Before plotting, make the figure contract explicit:

- core conclusion
- evidence chain and source-data anchor
- panel map and figure archetype
- target journal or export bundle
- statistics, units, scale bars, or image provenance
- claim boundary and reviewer risk

## Figure package structure

Every serious output should be delivered as a figure package, not as a loose
image:

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

Audit the package with
`plugins/materials-skills/skills/materials-figure/scripts/audit_figure_package.py` before calling
it journal-ready.

## Automatic table-to-figure loop

When a CSV/TSV data table is available, use the automatic Python loop before
hand-writing a new plot:

```powershell
python plugins/materials-skills/skills/materials-figure/scripts/generate_figure_package.py `
  --data path/to/source_data.csv `
  --output-dir outputs/figure-packages/my-figure `
  --goal "Show the WER dosage trend for bonding strength." `
  --figure-name my_figure `
  --json
```

The loop performs:

```text
data diagnosis -> chart recommendation -> SVG/PNG export -> QA report
```

It writes `figure_intake.yaml`, `source_data.csv`, `plot.py`, `figure.svg`,
`figure.png`, `caption.md`, `qa_report.md`, `asset_manifest.md`, and
`figure_contract.md`. Use the QA report to decide whether the output is ready,
needs revision, or is blocked by missing evidence.

## Example

- Figure package example:
  `plugins/materials-skills/skills/materials-figure/examples/figure-packages/wer-ea-dosage-window/`
- Additional package:
  `plugins/materials-skills/skills/materials-figure/examples/figure-packages/wer-ea-evidence-heatmap/`
- Atlas gallery:
  `plugins/materials-skills/skills/materials-figure/assets/wer-ea-atlas/generated/`

## Validation

- Audit script:
  `plugins/materials-skills/skills/materials-figure/scripts/audit_figure_package.py`
- Core tests live under `plugins/materials-skills/skills/materials-figure/tests/`
- Bundle verification:
  `python .\scripts\run_release_checks.py --json`

## Reproduction checklist

- Python-only backend readiness checked
- no alternate plotting backend used
- figure contract written before plotting
- source data or source-map anchor present
- export bundle includes SVG, PDF, PNG, and TIFF when possible
- caption states what the figure supports and what it does not prove
- QA report covers Python backend exclusivity, export checks, and caption boundary
- automatic table plots include data diagnosis and chart choice rationale
- WER-EA mechanism claims stay bounded by real evidence

## Boundaries

This skill does not let pretty visuals overrule the scientific logic. If the
evidence chain or source data anchor is weak, the correct response is to flag
the risk or route back to reader, citation, writing, or data work before
polishing the image.

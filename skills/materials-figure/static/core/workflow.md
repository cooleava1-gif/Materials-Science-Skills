# Figure Hard Workflow

Run this workflow for any journal-ready figure, WER-EA review figure, plotted data figure, or figure audit.

## 1. Use the Python backend

Use the Python-only backend gate in `figure-contract.md`. Check Python and the required plotting packages before rendering. If a required package is unavailable, stop and report the blocker.

## 2. Build the figure contract

Before plotting, write or update `figure_contract.md` with:

- core conclusion,
- evidence chain,
- archetype,
- Python backend readiness,
- journal/export contract,
- statistics and image-integrity needs,
- WER-EA or materials claim boundary,
- reviewer risks.

## 3. Load The Python Backend Fragment

Load `static/fragments/backend/python.md` and follow its execution rules.

## 4. Check Source Data And Anchors

Use actual source data, a table-system row, a `source_map.json` anchor, or PDF visual asset metadata. If the user has no evidence yet, produce a plan or template only and label the package `template-only`.

## 5. Use the automatic table loop when possible

If the user provides a CSV/TSV table and asks for plotting, first try the
automatic Python package loop:

```text
data table -> data diagnosis -> chart recommendation -> SVG/PNG export -> QA report
```

Use `scripts/generate_figure_package.py` with `--data`, `--output-dir`,
`--goal`, and `--figure-name`. The loop writes `figure_intake.yaml`,
`source_data.csv`, `plot.py`, `figure.svg`, `figure.png`, `caption.md`,
`qa_report.md`, `asset_manifest.md`, and `figure_contract.md`.

Stop for human clarification only when the table lacks numeric response
columns, the scientific claim cannot be inferred safely, or the QA report has
critical issues.

## 6. Create the figure package

Use `references/figure-package-protocol.md` and `assets/templates/figure-package/`. A production package should contain the contract, source data, Python plotting script, SVG/PDF/PNG/TIFF exports, caption, QA report, and asset manifest.

## 7. Run visual QA

Apply `references/figure-qa-contract.md`. Check export formats, final size, text readability, color choices, units, n/error bars/statistics, image scale bars, image provenance, and caption boundary.

## 8. Return the package

Return the package path, a short claim-evidence summary, the caption boundary, any failed QA items, and the reviewer-risk notes. Do not call a package submission-ready if `scripts/audit_figure_package.py` reports `incomplete`.

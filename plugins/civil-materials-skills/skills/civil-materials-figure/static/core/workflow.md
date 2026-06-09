# Figure Hard Workflow

Run this workflow for any journal-ready figure, WER-EA review figure, plotted data figure, or figure audit.

## 1. Resolve the backend

Use the backend gate in `figure-contract.md`. If Python/R is unresolved, ask `Python or R?` and stop.

## 2. Build the figure contract

Before plotting, write or update `figure_contract.md` with:

- core conclusion,
- evidence chain,
- archetype,
- selected backend,
- journal/export contract,
- statistics and image-integrity needs,
- WER-EA or civil-materials claim boundary,
- reviewer risks.

## 3. Load The Matching Backend Fragment

Load only `static/fragments/backend/python.md` or `static/fragments/backend/r.md`. Do not load the other backend's execution rules.

## 4. Check Source Data And Anchors

Use actual source data, a table-system row, a `source_map.json` anchor, or PDF visual asset metadata. If the user has no evidence yet, produce a plan or template only and label the package `template-only`.

## 5. Create the figure package

Use `references/figure-package-protocol.md` and `assets/templates/figure-package/`. A production package should contain the contract, source data, selected-backend script, SVG/PDF/PNG/TIFF exports, caption, QA report, and asset manifest.

## 6. Run visual QA

Apply `references/figure-qa-contract.md`. Check export formats, final size, text readability, color choices, units, n/error bars/statistics, image scale bars, image provenance, and caption boundary.

## 7. Return the package

Return the package path, a short claim-evidence summary, the caption boundary, any failed QA items, and the reviewer-risk notes. Do not call a package submission-ready if `scripts/audit_figure_package.py` reports `incomplete`.

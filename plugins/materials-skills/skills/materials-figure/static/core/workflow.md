# Figure Hard Workflow

> **Figure contract is a blocking gate.** The contract is written and validated
> before any plotting code, data generation, preview, or rendered figure. This
> overrides general autonomy/default-execution behavior for figure tasks.

> **Domain context**: The `domain` axis has loaded domain-specific figure guidance. Before plotting, review the domain guide for recommended figure types, panel structures, and format conventions.

Run this workflow for any journal-ready figure, review figure, plotted data figure, or figure audit.

## 1. Use the Python backend

Use the Python-only backend gate in `figure-contract.md`. Check Python and the required plotting packages before rendering. If a required package is unavailable, stop and report the blocker.

## 2. Build and validate the figure contract

Before plotting, write or update `figure_contract.md` so that all seven points
hold substantive content — not template-only, placeholder, or empty fields:

- core conclusion,
- evidence chain,
- archetype,
- Python backend readiness,
- journal/export contract,
- statistics and image-integrity needs,
- WER-EA or materials claim boundary,
- reviewer risks.

Then validate `figure_contract.md` manually or with optional validation tools.

- Validation passes -> proceed to materials knowledge validation.
- Validation fails -> stop. Revise the contract so every point holds real
  content. Do not generate plotting scripts, mock data,
  previews, or rendered figures while the contract is invalid.

The contract always precedes plotting code. This is binding for both
interactive figure work and the automatic table-plotting loop.

## 2b. Validate materials-science claims

After the contract passes validation, optionally run
`validate_materials_claims.py` against `figure_contract.md`. The validator
extracts XRD peaks/phases, FTIR wavenumbers/functional groups, and performance
values from the evidence chain and checks them against
`static/core/materials_kb.yaml`.

- Claims that contradict known material relations (e.g. 915 cm⁻¹ assigned to
  C=O, or 30° 2θ assigned to Al2O3) are errors and block plotting.
- Values far outside typical ranges are warnings for review.
- Figures without materials-science entities (e.g. pure flowcharts) pass with
  no checks.

## 2c. Validate the multi-figure storyboard (multi-figure tasks only)

When the task spans more than one figure, write `figure_storyboard.yaml` (see
`assets/templates/figure-storyboard/`) and run `check_storyboard.py` before
individual figure contracts. The storyboard gate verifies:

- narrative arc completeness and role coverage,
- acyclic evidence dependencies (DAG),
- cross-figure non-redundancy (no two figures show the same data panel),
- style consistency declarations.

The storyboard must pass before individual figure contracts are written.

## 3. Load The Python Backend Fragment

Load `static/fragments/backend/python.md` and follow its execution rules.

## 4. Check Source Data And Anchors

Use actual source data, a table-system row, a `source_map.json` anchor, or PDF visual asset metadata. If the user has no evidence yet, produce a plan or template only and label the package `template-only`. If source anchors are missing, update the contract's evidence chain before proceeding; do not plot against an unanchored contract.

## 5. LLM-driven figure creation

In LLM-as-artist mode, the LLM writes plotting code directly based on the validated contract and source data. The workflow is:

```text
contract draft -> LLM/user confirmation -> contract validation
  -> validate_materials_claims.py (optional) -> LLM writes plot.py
  -> SVG/PNG export -> QA review
```

1. Draft `figure_contract.md` from the source table and the user's goal,
   filling all seven points with substantive content.
2. Confirm or revise the draft with the user/LLM until every point holds real
   content.
3. Validate the contract. If validation fails, stop; do not plot.
4. Optionally run `validate_materials_claims.py`. If it reports errors, stop and revise
   the contract.
5. The LLM writes `plot.py` directly using matplotlib or other Python plotting libraries, following the contract and source data.
6. The LLM generates exports (SVG, PNG, PDF, TIFF) and writes `caption.md`, `qa_report.md`, and `asset_manifest.md`.

Stop for human clarification only when the table lacks numeric response
columns, the scientific claim cannot be inferred safely, or the QA report has
critical issues. Contract validation failure is always a stop condition; it
never falls back to plotting.

## 6. Create the figure package

Use `references/figure-package-protocol.md` and `assets/templates/figure-package/`. A production package should contain the contract, source data, Python plotting script, SVG/PDF/PNG/TIFF exports, caption, QA report, and asset manifest.

## 7. Run visual QA

Apply `references/figure-qa-contract.md`. Check export formats, final size, text readability, color choices, units, n/error bars/statistics, image scale bars, image provenance, and caption boundary.

## 8. Return the package

Return the package path, a short claim-evidence summary, the caption boundary, any failed QA items, and the reviewer-risk notes.

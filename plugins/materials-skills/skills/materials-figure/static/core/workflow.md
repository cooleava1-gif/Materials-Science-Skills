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

Then run `check_figure_contract.py` against `figure_contract.md`.

- Validation passes -> proceed to materials knowledge validation.
- Validation fails -> stop. Revise the contract so every point holds real
  content and rerun validation. Do not generate plotting scripts, mock data,
  previews, or rendered figures while the contract is invalid.

The contract always precedes plotting code. This is binding for both
interactive figure work and the automatic table-plotting loop.

## 2b. Validate materials-science claims

After the contract passes `check_figure_contract.py`, run
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

## 5. Use the automatic table loop in contract-first order

If the user provides a CSV/TSV table and asks for plotting, run the automatic
Python package loop in **contract-first** order, not zero-interaction
auto-plotting:

```text
contract draft -> LLM/user confirmation -> check_figure_contract.py validation
  -> data diagnosis -> chart recommendation -> SVG/PNG export -> QA report
```

1. Draft `figure_contract.md` from the source table and the user's goal,
   filling all seven points with substantive content.
2. Confirm or revise the draft with the user/LLM until every point holds real
   content.
3. Run `check_figure_contract.py`. If validation fails, stop; do not plot.
4. Only after validation passes, run
   `scripts/generate_figure_package.py` with `--data`, `--output-dir`,
   `--goal`, and `--figure-name`. The loop writes `figure_intake.yaml`,
   `source_data.csv`, `plot.py`, `figure.svg`, `figure.png`, `caption.md`,
   `qa_report.md`, `asset_manifest.md`, and `figure_contract.md`.

Stop for human clarification only when the table lacks numeric response
columns, the scientific claim cannot be inferred safely, or the QA report has
critical issues. Contract validation failure is always a stop condition; it
never falls back to plotting.

## 6. Create the figure package

Use `references/figure-package-protocol.md` and `assets/templates/figure-package/`. A production package should contain the contract, source data, Python plotting script, SVG/PDF/PNG/TIFF exports, caption, QA report, and asset manifest.

## 7. Run visual QA

Apply `references/figure-qa-contract.md`. Check export formats, final size, text readability, color choices, units, n/error bars/statistics, image scale bars, image provenance, and caption boundary.

## 8. Return the package

Return the package path, a short claim-evidence summary, the caption boundary, any failed QA items, and the reviewer-risk notes. Do not call a package submission-ready if `scripts/audit_figure_package.py` reports `incomplete`.

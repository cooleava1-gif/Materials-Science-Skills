# Automatic Figure Package Loop

Use this reference when the user provides a CSV/TSV data table and asks for
plotting, visualization, paper figures, or one-click figure generation.

The loop is Python-only and contract-first:

```text
source table -> contract draft/review -> contract + materials validation -> chart recommendation -> SVG/PNG export -> QA report
```

## Interaction Modes

### Automatic Mode

Use when the user gives a table and a clear goal. Run the generator directly:

```powershell
python plugins/materials-skills/skills/materials-figure/scripts/generate_figure_package.py `
  --data path/to/source_data.csv `
  --output-dir outputs/figure-packages/my-figure `
  --goal "Show the WER dosage trend for bonding strength." `
  --figure-name my_figure `
  --json
```

On the first run, the generator may scaffold `figure_contract.md` and return a
blocked status until the contract is filled with substantive content. After the
contract is reviewed and passes both `check_figure_contract.py` and
`validate_materials_claims.py`, rerun the same command to render the figure
package.

Ask a follow-up only when the table has no numeric response column, the target
claim cannot be inferred safely, or the QA status is blocked for reasons the
draft contract cannot resolve.

### Guided Mode

Use when the source table is ambiguous. Ask only for the missing item:

- core conclusion,
- which column is the response,
- which column is the x-axis or grouping condition,
- whether error bars are SD, SE, CI, or range.

Then run the same generator, review the drafted contract if one is created, and
rerun after validation passes.

### Revision Mode

Use when the user gives an existing figure package or `plot.py`. Run QA first,
then patch the figure. Do not redraw from scratch unless the existing chart
choice is unsafe.

## Generated Package

The automatic generator writes:

```text
figure-package/
  figure_intake.yaml
  source_data.csv
  plot.py
  figure.svg
  figure.png
  caption.md
  qa_report.md
  asset_manifest.md
  figure_contract.md
```

`figure.svg` is the editable manuscript asset. `figure.png` is the quick
preview. `plot.py` is intentionally self-contained enough to rerun the package
from `source_data.csv`.

## Current Recommendation Rules

- Numeric x + numeric y + SD/SE/CI/error column -> `errorbar_trend`.
- Categorical group + numeric response -> `grouped_bar`.
- Repeated group keys -> `boxplot_points`.
- Four or more numeric property columns -> `correlation_heatmap`.
- Otherwise use `scatter_regression` only as an association plot.

These are conservative defaults. They protect the claim boundary more than they
optimize visual novelty.

## QA Report Contract

`qa_report.md` must include:

- `Status`
- `Figure Identity`
- `Data Check`
- `Chart Choice Check`
- `Scientific Claim Boundary`
- `Visual QA`
- `Reviewer Risk`
- `Final Recommendation`

The report must state whether replicate count, units, error bar definition,
missing values, and source-data anchors are present. Mechanism, field
durability, and statistical significance claims remain unsupported unless the
source data explicitly provide that evidence.

## Boundaries

The automatic loop is allowed to generate a figure from measured columns. It is
not allowed to invent missing replicate counts, statistical tests, mechanism
evidence, field durability, or image scale bars. When those are absent, the QA
report should mark them as reviewer risks instead of hiding the weakness.

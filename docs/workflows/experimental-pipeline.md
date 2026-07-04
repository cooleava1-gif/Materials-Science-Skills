# Experimental Pipeline: DOE -> Record -> Data -> Figure

This workflow wires together four existing skills into a single closed loop:

1. **materials-doe** designs the experiment and emits `experiment_plan.csv`.
2. **materials-doe** (or the user) converts the plan into `experiment-record.yaml`.
3. **materials-data** builds a FAIR dataset package from the record.
4. **materials-figure** generates a figure package skeleton from the FAIR package.

No new skills are required; the loop is implemented by three small conversion
scripts that live inside the existing skills.

## Pipeline diagram

```text
materials-doe
  |
  | experiment_plan.csv
  v
doe_plan_to_experiment_record.py
  |
  | experiment-record.yaml
  v
materials-data / build_fair_package.py
  |
  | dataset package
  v
data_package_to_figure_handoff.py
  |
  | figure package skeleton
  v
materials-figure
```

## Step 1: Design the experiment

Use `materials-doe` to produce an experiment plan. The standard output artifact
is `experiment_plan.csv` with columns such as:

```csv
exp_id,factor_A,factor_B,factor_C,factor_D,response_1,response_2,notes
1,1,1,1,1,,,
2,1,2,2,2,,,
...
```

## Step 2: Convert the plan to an experiment record

Run the new conversion script inside `materials-doe`:

```powershell
python plugins/materials-skills/skills/materials-doe/scripts/doe_plan_to_experiment_record.py `
    --plan-csv experiment_plan.csv `
    --output experiment-record.yaml `
    --study-id ceramics-sintering-001 `
    --title "Sintering temperature optimization" `
    --material-family ceramics `
    --domain ceramics `
    --design-type L9 `
    --factors '[
        {"name":"sintering_temperature","unit":"degC","type":"continuous","levels":[1400,1500,1600]},
        {"name":"additive_content","unit":"wt%","type":"continuous","levels":[0,1,2]}
    ]' `
    --responses '[
        {"name":"bulk_density","unit":"g/cm3","measurement_method":"Archimedes","replicate_count":3}
    ]'
```

The script:

- reads the factor-level matrix from the CSV,
- maps semantic factor/response names from `--factors` and `--responses`,
- validates the record against `_shared/core/experiment-record-schema.yaml` when
  `jsonschema` is installed,
- writes `experiment-record.yaml`.

## Step 3: Build a FAIR dataset package

Use the existing `materials-data` builder:

```powershell
python plugins/materials-skills/skills/materials-data/scripts/build_fair_package.py `
    --topic "ceramics sintering" `
    --domain ceramics `
    --journal generic `
    --output-dir ./datasets `
    --experiment-record ./experiment-record.yaml
```

Output structure:

```text
ceramics_sintering_generic_fair_package/
  raw_data/
    experiment_data_template.csv
  processed_data/
  figures/
  metadata.md
  README.md
  data_availability_statement.md
  fair_audit.md
  experiment_record_link.yaml
```

Fill measured response values into `raw_data/experiment_data_template.csv`.

## Step 4: Generate a figure package skeleton

Run the new conversion script inside `materials-figure`:

```powershell
python plugins/materials-skills/skills/materials-figure/scripts/data_package_to_figure_handoff.py `
    --dataset-dir ./datasets/ceramics_sintering_generic_fair_package `
    --output-dir ./figures `
    --claim "Sintering temperature and additive content jointly affect bulk density."
```

Output structure:

```text
ceramics_sintering_optimization_figure_package/
  figure_storyboard.yaml
  figure_contract.md
  caption_boundary.md
  figure_qa_report.md
  source_data.csv
  plot.py
  README.md
```

Next steps:

1. Fill measured values in `source_data.csv`.
2. Implement domain-specific plotting in `plot.py`.
3. Run `python plot.py` to produce `figure.pdf`, `figure.png`, etc.
4. Audit with `materials-figure/scripts/audit_figure_package.py`.

## Cross-skill handoff contracts

- `materials-doe` -> `materials-data`: `doe-handoff` (see
  `_shared/contracts/doe-handoff.yaml`). The contract now explicitly requires
  `experiment_record.yaml`.
- `materials-data` -> `materials-figure`: `data-package` (see
  `_shared/contracts/data-package.yaml`).

## Domain portability

The same four-step pipeline works for any material family. Only the
`--factors`, `--responses`, and `--claim` strings change:

- **Ceramics**: sintering temperature, additive content -> bulk density.
- **Polymers**: curing agent, filler loading -> tensile strength.
- **Metals**: heat treatment, alloy composition -> hardness.
- **Civil**: binder content, curing time -> compressive strength.

## Failure modes

- Missing `jsonschema`: schema validation is skipped with a warning; the record
  and package are still generated.
- Missing response values in the CSV: the scripts produce templates; plotting
  will fail until values are filled.
- Mismatched `--factors` / `--responses` length: the DOE script exits with an
  explicit error before writing an invalid record.

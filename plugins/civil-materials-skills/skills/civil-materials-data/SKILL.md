---
name: civil-materials-data
version: "1.1.0"
stability: stable
description: Use when organizing, auditing, packaging, or drafting data and FAIR materials for civil engineering and construction materials manuscripts, especially raw/processed datasets, metadata, data availability statements, asphalt pavement materials, waterborne epoxy modified emulsified asphalt, cement/concrete, durability, CBM, CCC, JBE, RMPD, IJPE, and JRE submissions.
---

# Civil Materials Data And FAIR

Prepare civil-materials datasets that a reviewer, co-author, or future you can reuse.

Use when the task involves FAIR data, raw/processed data organization, metadata, data availability statements, test matrices, supplementary datasets, or submission data packages.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect `task`, `domain`, and `journal`.
3. Load only the matching reference files.
4. Produce one of these outputs: experiment data template, FAIR audit, dataset package plan, data availability statement, or submission-ready dataset folder.
5. Never invent measurements, replicate counts, standards, or environmental conditions. Mark unknowns as `[needs confirmation]`.

## Default Output

For dataset packaging, use:

- `assets/templates/metadata-template.md`
- `assets/templates/dataset-readme-template.md`
- `assets/templates/data-availability-template.md`
- `assets/templates/experiment-data-template.csv`

For deterministic scaffolding, run:

```powershell
python scripts/build_fair_package.py --topic "<topic>" --domain asphalt --journal CBM --output-dir "<target>"
```

For an audit, run:

```powershell
python scripts/audit_fair_dataset.py --dataset-dir "<dataset-package>"
```

For review and manuscript tables, load `references/table-system.md` and use `assets/templates/table-system-template.md`. This covers literature-screening-table, mechanism-evidence-table, test-method-table, performance-comparison-table, durability-evidence-table, and journal-positioning-table.

## Civil Materials Data Rules

- Separate raw data, processed data, and figures.
- Keep units, test standards, sample IDs, mixture/formulation IDs, replicate counts, temperature, humidity, curing condition, and aging condition explicit.
- For asphalt and pavement materials, track asphalt type, emulsifier type, epoxy dosage, demulsification/curing condition, bonding test setup, viscosity, storage stability, and moisture/aging conditions.
- For cement/concrete, track binder composition, water-binder ratio, admixture dosage, curing regime, age, specimen geometry, test standard, strength, durability, and microstructure evidence.
- Data availability statements must not claim public availability unless the files are actually present or a repository link is supplied.

## Handoff

Use `civil-materials-figure` after data are organized enough for plotting. Use `civil-materials-citation` and `civil-materials-reader` when the dataset needs source-grounded claims or literature context.

# Dataset Package

Use this structure for civil-materials manuscript data packages:

```text
dataset-package/
  raw_data/
    experiment_data_template.csv
  processed_data/
  figures/
  metadata.md
  README.md
  data_availability_statement.md
  fair_audit.md
```

## Required Metadata

- topic
- material_domain
- target_journal
- sample_id logic
- formulation_id logic
- units
- test_standard
- replicate_count
- temperature
- humidity
- curing_condition
- aging_condition
- data_contact

## Raw Data Rules

- Keep instrument output or manually recorded raw values separate from processed data.
- Do not overwrite raw files after analysis.
- Use one row per replicate whenever possible.

## Processed Data Rules

- Processed tables should include formulas, aggregation logic, and uncertainty type.
- Figure-ready tables should keep links to raw sample IDs.

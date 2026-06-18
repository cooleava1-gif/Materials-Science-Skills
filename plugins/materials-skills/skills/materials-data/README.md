# materials-data

The data skill packages the material behind a manuscript into a cleaner,
FAIR-aware submission surface. It is where raw files, processed tables,
metadata, and availability statements stop being loose attachments.

## When To Use

Use this skill when you need a data or FAIR package for a materials paper,
especially for WER-EA, asphalt pavement materials, cement/concrete, durability,
or journal submission workflows that require clearer provenance and metadata.

## Inputs

- raw and processed data folders
- variable names, sample IDs, dosage labels, and test-condition metadata
- journal or repository expectations for data availability
- figure or manuscript claims that need traceable data backing

## Outputs

- FAIR-minded dataset package plan
- metadata and file-organization guidance
- data availability statement draft
- explicit missing-data or missing-metadata flags for later repair

## Example

- Example package:
  `plugins/materials-skills/skills/materials-data/examples/waterborne-epoxy-fair-package.md`
- Shared paper-production handoff context:
  `plugins/materials-skills/skills/_shared/paper-production/paper-gate-report-template.md`

## Validation

- Core regression test:
  `plugins/materials-skills/skills/materials-data/tests/test_data_fair_skill.py`
- Bundle verification:
  `python .\scripts\run_release_checks.py --json`

## Boundaries

This skill organizes and audits data packaging, but it does not invent missing
measurements, repair bad experiments, or certify that a dataset is complete
enough for publication without domain review.

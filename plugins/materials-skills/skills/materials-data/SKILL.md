---
name: materials-data
version: "1.2.0"
stability: stable
description: Use when organizing, auditing, packaging, or drafting data and FAIR materials for materials science and engineering manuscripts.
---

# Materials Science Data and FAIR Router

Read `manifest.yaml` and all declared `always_load` files. Apply profile-first routing, then detect `input_source`, `task`, `material_family`, `domain`, and `journal`; load only the mapped fragments and conditional stance/ethics guidance.

If the input is `experiment-record.yaml`, validate it against `_shared/core/experiment-record-schema.yaml` before scaffolding. Produce only the requested experiment data template, FAIR audit, dataset package, data availability statement, or submission-ready dataset folder.

Gates:

- Separate raw data, processed data, and figures. Keep units, test standards, sample IDs, mixture IDs, replicate counts, and environmental conditions explicit.
- Never invent measurements, replicate counts, standards, environmental conditions, or missing rows.
- A data availability statement must not claim public availability unless the files are present or a repository link is supplied.
- Preserve provenance from the experiment record through the dataset package and its handoff; mark unresolved metadata instead of guessing.

Use `scripts/build_fair_package.py` for deterministic scaffolding and `scripts/audit_fair_dataset.py` for FAIR audits. Return the schema result, provenance status, missing inputs, and package paths so a downstream figure, writing, or submission skill can consume a bounded artifact.

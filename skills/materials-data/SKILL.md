---
name: materials-data
version: "1.1.0"
stability: stable
description: Use when organizing, auditing, packaging, or drafting data and FAIR materials for civil engineering and construction materials manuscripts.
---

# Materials Science Data And FAIR

Prepare materials datasets that a reviewer, co-author, or future you can reuse.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Apply profile-first routing from `.materials/profile.yaml`; on first use, ask for direction once and save it locally.
3. Detect `task`, `domain`, and `journal`.
4. Load only the matching fragments.
5. Produce: experiment data template, FAIR audit, dataset package, data availability statement, or submission-ready dataset folder.
6. Never invent measurements, replicate counts, standards, or environmental conditions.

## Gates

- Separate raw data, processed data, and figures.
- Keep units, test standards, sample IDs, mixture IDs, replicate counts explicit.
- Data availability statements must not claim public availability unless files are present or a repository link is supplied.

## Tools

- `scripts/build_fair_package.py` for deterministic scaffolding.
- `scripts/audit_fair_dataset.py` for FAIR audits.

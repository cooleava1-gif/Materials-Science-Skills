# FAIR data package

## Outcome Snapshot

This showcase is the data-facing outcome surface for the bundle. The goal is a
submission-safe package with metadata, README structure, data availability
language, and explicit warnings when the evidence cannot support stronger
mechanism claims.

## Demo Prompt

```text
Package this WER-EA bonding dataset into a FAIR-ready submission bundle and flag anything missing before I write the data availability statement.
```

## Proof Assets

- Data showcase example:
  `plugins/materials-skills/skills/materials-data/examples/waterborne-epoxy-fair-package.md`
- Generated FAIR package sample:
  `plugins/materials-skills/skills/materials-data/examples/generated/waterborne_epoxy_modified_emulsified_asphalt_bonding_performance_cbm_fair_package/README.md`
- Data templates:
  `plugins/materials-skills/skills/materials-data/assets/templates/data-availability-template.md`
  and `plugins/materials-skills/skills/materials-data/assets/templates/metadata-template.md`
- Data skill contract:
  `plugins/materials-skills/skills/materials-data/README.md`

## Build Path

1. Start with `materials-data` when raw and processed files exist but the
   paper-facing package is still loose.
2. Build metadata, README, and data availability language from the templates.
3. Compare the output against the generated FAIR package sample and audit notes.
4. Route any missing mechanism-support metadata or figure-linkage gaps back into
   the paper workflow before overclaiming.

## When To Use This Route

Use this showcase when the paper needs a cleaner supplementary-data and
metadata story, especially for journals that expect clear availability
statements and traceable test conditions.

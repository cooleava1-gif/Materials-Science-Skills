---
name: materials-literature-pipeline
version: "1.1.0"
description: Use when setting up, running, or auditing a recurring materials literature discovery workflow with candidate scoring, evidence-layer labels, deduplication, digest notes, and next-reading actions.
---

# Materials Literature Pipeline Router

Read `manifest.yaml` and its `always_load` core. Apply profile-first routing, then detect `pipeline_mode`, `material_family`, and `output`; load selected axis paths and on-demand references only when the mode requires them.

In configure mode, define scope and operation without loading scoring unless the user asks to score, rank, calibrate, or audit. In run/audit mode, assign stable candidate IDs and deduplicate by DOI or normalized title plus year before scoring. Emit the candidate table, digest, and `literature-pipeline-handoff` requested by the route.

Evidence and scoring gates:

- Every row remains candidate evidence at every `source_depth` and score. Manuscript support requires a separate source-anchored reader or extraction artifact; never promote a candidate row to evidence.
- Keep one-shot citation retrieval separate from recurring pipeline configuration. Without a verified source, mark an unverified citation, do not invent DOI or metadata, and retain candidate evidence status.
- Recalculate totals from dimensions. A candidate with `topic_fit < 10` cannot rank top tier; every top-tier row requires `source_depth`, `evidence_boundary`, and `next_action`.
- `exclude` and `archive` rows require a documented reason. `next_action=read` routes to `materials-reader`; `next_action=cite-gap-audit` routes to `materials-citation`.
- Automated schedules remain local/profile-bound until listed and manually verified. Report degradation, partial coverage, and score uncertainty instead of hiding or inflating them.
- Persistent multi-skill candidates live only in `research-state.source_map.candidates`.

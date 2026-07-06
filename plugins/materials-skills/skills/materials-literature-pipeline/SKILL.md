---
name: materials-literature-pipeline
version: "1.1.0"
description: Use when setting up, running, or auditing a recurring materials literature discovery workflow with candidate scoring, evidence-layer labels, deduplication, digest notes, and next-reading actions.
---

# Materials Literature Pipeline

Run a structured materials literature discovery pipeline. This skill turns broad search results into an evidence-aware candidate table and digest, then routes deep reading and citation gaps to the existing materials skills. It can also define local cron-style recurring runs, push-message formats, source/delivery degradation, four-step gap analysis, and review-compilation handoffs.

## Layered architecture

This skill is split into two layers:

- A static layer under `static/` with the workflow, scoring rubric, and contract.
- A dynamic layer (this file plus `manifest.yaml`) that detects axes such as pipeline mode, material family, and output type.

## Protocol

1. Read `manifest.yaml`, then load every `always_load` file.
2. Apply profile-first routing from `.materials/profile.yaml` when available.
3. Detect `pipeline_mode`, `material_family`, and `output`.
4. Define the search scope: topic, material system, time window, source databases, inclusion/exclusion rules.
5. Build the candidate set: fetch or receive records, assign stable `candidate_id`, generate `dedup_key` from DOI/title+year, and deduplicate before scoring.
6. Score each candidate independently on the six dimensions (topic fit, evidence layer, method relevance, material-system proximity, source quality, actionability). Store them as six numeric table fields, recalculate totals, and do not trust inherited scores.
7. Label every candidate with `source_depth` (metadata-only, abstract-screened, full-text-read, or data-extracted), `next_action`, and `evidence_boundary`.
8. Emit `literature_candidate_table.csv` and `literature_digest.md` with ranked candidates, source-depth caveats, and next-action routing.
9. When the user asks for recurring operation, load `references/cron-operations.md` and verify the job is visible after creation; do not treat local cron as a cloud guarantee.
10. When delivery is requested, load `references/push-format.md` and preserve score, source-depth, evidence-boundary, and next-action fields in the message.
11. When a source, schedule, delivery, or archive step fails, load `references/degradation-strategy.md` and deliver a reduced but labeled result instead of silently dropping the run.
12. When the user asks whether a topic is unexplored, load `references/gap-analysis.md` and run the four-step gap method.
13. When pipeline outputs feed a review article, load `references/review-compilation-workflow.md` before routing to `materials-writing`.
14. Route full-text reading to `materials-reader`, citation-gap auditing to `materials-citation`, and cross-stage orchestration to `materials-research`.
15. Update or draft the shared research state `source_map` when the pipeline output feeds into a multi-skill workflow.

## Gates

- **BLOCKING**: Metadata-only candidates must not be treated as evidence for manuscript claims. They are candidate evidence only.
- **BLOCKING**: Scores must be recalculated from dimensions on every run; do not trust inherited or cached totals.
- **BLOCKING**: A candidate with `topic_fit < 10` cannot rank in the top tier, regardless of journal prestige or other scores.
- **BLOCKING**: Every top-tier candidate must have a `source_depth` label, `evidence_boundary`, and `next_action`.
- Candidates flagged as `exclude` or `archive` must have a documented reason.
- Any automated schedule is local/profile-bound until a list/manual-run verification proves it exists in the current environment.
- A failed source, delivery channel, or archive write must be reported as degradation; never hide partial coverage or compensate by inflating scores.
- When a multi-skill workflow is active, write candidates only to `research-state.source_map.candidates`; do not create a new database or downloader surface.

# Literature Pipeline Contract

`materials-literature-pipeline` produces a discovery-stage handoff. It is not a replacement for source reading or citation verification.

## Inputs

- Topic, material system, keywords, and time window.
- Optional `citation-handoff` from `materials-citation`.
- User-provided databases, journals, or inclusion/exclusion rules.

## Outputs

- `literature_candidate_table.csv`
- `literature_digest.md`
- Optional `search_strategy.md`
- Optional `gap_report.md`
- Optional `review_compilation_plan.md`

## Handoff Fields

The candidate table must include these public fields in this order:

- `candidate_id`
- `title`
- `year`
- `venue`
- `doi`
- `dedup_key`
- `material_system_match`
- `evidence_layer`
- `source_depth`
- `topic_fit`
- `evidence_layer_score`
- `method_relevance`
- `material_system_proximity`
- `source_quality`
- `actionability`
- `score_total`
- `next_action`
- `evidence_boundary`

`score_breakdown` means the six independent numeric fields above. Do not add a
separate JSON `score_breakdown` column to the CSV.

## Evidence Boundary

Metadata and abstracts can justify prioritization. They cannot justify manuscript claims until full source reading or source-anchored extraction is complete.

## Research-State Boundary

When the handoff is used by `materials-research`, candidate rows populate
`research-state.source_map.candidates`. The pipeline does not create a new
database, downloader, or external scheduling service.

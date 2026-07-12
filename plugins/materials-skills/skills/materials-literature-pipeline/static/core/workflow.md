# Literature Pipeline Workflow

## 1. Define Scope

Capture the discovery boundary before building the candidate set:

1. **Topic and research question**: What is the material system, phenomenon, or method under investigation?
2. **Material family**: Map to the manifest axis (`civil`, `polymers`, `metals`, `ceramics`, `functional`, `nano`).
3. **Date window**: Start year, end year, or "last N years".
4. **Source databases**: Web of Science, Scopus, Google Scholar, PubMed, or user-provided records.
5. **Inclusion rules**: Material system match, method relevance, language, document type.
6. **Exclusion rules**: Out-of-scope materials, wrong scale, non-peer-reviewed, duplicates.
7. **Target output**: digest, candidate table, or both.

## 2. Build Candidate Set

Use `materials-citation` or user-provided records to gather candidates:

1. Fetch or receive candidate records (title, authors, year, venue, DOI, abstract).
2. Assign a stable `candidate_id` (e.g. `CAND-{topic}-{seq}`).
3. Generate a `dedup_key` from DOI, external ID, or normalized title+year.
4. Deduplicate before scoring: remove candidates with identical `dedup_key`, keeping the most complete record.
5. Flag and group candidates with overlapping material systems (e.g. same asphalt/epoxy system) for cross-reference.

## 3. Score And Label

Apply the six-dimension scoring rubric from `scoring.md`:

### 3.1 Scoring dimensions

| # | Dimension | Weight | Key question |
|---|---|---|---|
| 1 | Topic fit | 30 | Does this paper directly address the research question? |
| 2 | Evidence layer | 20 | What level of evidence does it provide (data, mechanism, model, review)? |
| 3 | Method relevance | 15 | Are the experimental methods, characterization, or models applicable? |
| 4 | Material-system proximity | 15 | Same material family, binder/matrix, scale, or environment? |
| 5 | Source quality | 10 | Journal, peer review, DOI completeness, citation reliability? |
| 6 | Actionability | 10 | Clear next use in DOE, data, figure, writing, or review? |

### 3.2 Scoring procedure

1. Score each dimension independently on a 0-to-weight scale.
2. Store the six scores in the public table fields: `topic_fit`,
   `evidence_layer_score`, `method_relevance`,
   `material_system_proximity`, `source_quality`, and `actionability`.
3. Sum those six fields to get `score_total` (max 100). Do not trust inherited
   or imported totals; always recalculate.
4. If `topic_fit < 10`, the candidate cannot rank top tier regardless of other scores.
5. If a source or full-text path degrades, record the degradation and keep the
   weaker `source_depth`; do not compensate by increasing any score.

### 3.3 Source depth labels

Label every candidate with one of:

| Label | Meaning | Can be used as evidence? |
|---|---|---|
| `metadata-only` | Title, abstract, and bibliographic data only | No — candidate evidence only |
| `abstract-screened` | Abstract read and assessed for relevance | No — candidate evidence only |
| `full-text-read` | Full paper read, claims and data extracted | Yes — with source-anchored excerpts |
| `data-extracted` | Numerical data, figures, or tables extracted from the paper | Yes — strongest evidence tier |

### 3.4 Evidence boundary

For every candidate, write a one-sentence `evidence_boundary` that states what the paper can and cannot support. This is a hard requirement for candidates ranked in the top tier.

## 4. Write Digest

Report the top candidates with:

1. **Rank** by `score_total` (descending).
2. **Candidate ID** and **title**.
3. **Score** with a six-field breakdown when space permits.
4. **Source depth** label.
5. **Evidence boundary** — one sentence.
6. **Next action** — one of `read`, `cite-gap-audit`, `monitor`, `exclude`, or `archive`.

Also report low-tier, excluded, or deferred candidates with reasons. A digest is
not complete if it only lists winners.

## 5. Route Next Actions

| Next action | Route to | When |
|---|---|---|
| `read` | `materials-reader` | Candidate needs full-text reading and source excerpts |
| `cite-gap-audit` | `materials-citation` | Candidate may fill a citation gap in the claim-source matrix |
| `monitor` | `materials-literature-pipeline` | Topic is emerging, candidate is worth watching |
| `exclude` | (none) | Candidate is out of scope or irrelevant |
| `archive` | (none) | Candidate is read but not actionable for current claims |

### Citation gap routing

When a candidate fills a known citation gap:

1. Check the `source_map` in the research state for missing evidence types.
2. If the candidate provides evidence that no existing paper covers, flag it as `cite-gap-audit`.
3. Route to `materials-citation` with the gap description and candidate ID.

### Research-state update

When this pipeline feeds a multi-skill workflow, append candidate rows to
`research-state.source_map.candidates`. Keep the public table field names, and
do not create a separate database or service. `materials-research` remains the
orchestrator that validates cross-stage consistency.

## 6. Operational Modes

### Cron runs

When the user asks for a recurring push, load `references/cron-operations.md`.
Verify the local job is visible after creation and run one small manual dry run.
If the scheduled run is missed, manually backfill first and debug second.

### Push delivery

When the user asks for Feishu, Telegram, email, or Markdown delivery, load
`references/push-format.md`. The push must include score, source depth, evidence
boundary, and next action for each delivered candidate.

### Degradation

When a source, scheduler, delivery channel, or archive write fails, load
`references/degradation-strategy.md`. Continue with a partial but labeled result
instead of treating incomplete coverage as complete.

### Gap analysis

When the user asks whether a topic is unexplored, load `references/gap-analysis.md`
and run the four-step method: multi-source search, decompose/classify, extract
edge papers, and output a gap report.

### Review compilation

When the pipeline is feeding a review or mini-review, load
`references/review-compilation-workflow.md` before sending the synthesis package
to `materials-writing`.

## 7. Handoff Checklist

Before emitting the `literature-pipeline-handoff`, verify:

- [ ] All candidates have a `dedup_key` and deduplication is complete.
- [ ] `score_total` equals the sum of the six dimension scores.
- [ ] No candidate has `topic_fit < 10` and is ranked in the top tier.
- [ ] Every top-tier candidate has a `source_depth` label and `evidence_boundary`.
- [ ] `next_action` is set for every candidate.
- [ ] The digest includes both top candidates and excluded/deferred entries.
- [ ] Any cron, delivery, archive, or source degradation is explicitly reported.
- [ ] Any research-state update uses `source_map.candidates` and preserves
      source-depth caveats.

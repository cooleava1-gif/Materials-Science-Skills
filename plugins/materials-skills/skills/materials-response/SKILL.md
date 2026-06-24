---
name: materials-response
version: "1.2.0"
stability: stable
description: Use when drafting, auditing, or strengthening point-by-point reviewer response letters for civil engineering and construction materials manuscripts. Now includes reviewer strategy library, experiment remediation plans, and comment pattern recognition.
---

# Materials Science Response

Draft reviewer response letters that are complete, factual, and professional.

## Layered architecture

This skill is split into two layers:

- A **static layer** under `static/` that holds reusable content fragments.
- A **dynamic layer** (this file plus [manifest.yaml](manifest.yaml)) that detects the request's axes and loads only the fragments needed for the current job.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Apply profile-first routing from `.materials/profile.yaml`; on first use, ask for direction once and save it locally.
3. Detect `response_task`, `comment_type`, `journal_family`, and `experiment_type`.
4. Load only the matching fragments.
5. Assign stable IDs to each reviewer comment.
6. Classify each comment and draft a point-by-point response.
7. Map action: ACCEPT_TEXT, ACCEPT_ANALYSIS, SOFTEN_CLAIM, DISAGREE, or AUTHOR_INPUT_NEEDED.

## Enhanced Capabilities (v1.2.0)

### Reviewer Strategy Library

When reviewer comments require strategic responses beyond simple revision, use `references/reviewer-strategy-library.md`. This library provides:

- **Novelty challenges**: Strategies for "incremental contribution," "literature comparison insufficient," "research gap not clearly identified."
- **Method and evidence challenges**: Strategies for "method selection not justified," "sample size too small," "statistics insufficient," "mechanism not supported."
- **Writing and presentation challenges**: Strategies for "English needs revision," "figures need improvement," "structure unclear."
- **Scope and framing challenges**: Strategies for "beyond scope," "more suitable for another journal," "overclaiming."
- **Conflicting reviewer challenges**: Strategies for contradictory requests and different novelty assessments.
- **Data and reproducibility challenges**: Strategies for "provide raw data" and "reproducibility concerns."
- **Ethics and integrity challenges**: Strategies for "potential plagiarism" and "ethical concerns."

### Experiment Remediation Plans

When reviewers request additional experiments, use `references/experiment-remediation-plans.md`. This reference provides:

- **Mechanism evidence experiments**: FTIR, SEM, XRD, TG/DTG protocols.
- **Performance evidence experiments**: Mechanical testing, durability testing, bonding/adhesion testing, rheological testing.
- **Statistical evidence experiments**: Replicate testing, design of experiments (DOE).
- **Characterization evidence experiments**: Particle size distribution, BET surface area, spectroscopic characterization.
- **Comparison and benchmarking experiments**: Control/baseline experiments, literature benchmarking.
- **Decision framework**: Step-by-step guide for deciding whether to complete, plan, or defer experiments.
- **Response templates**: Templates for "experiment completed," "experiment planned," "experiment beyond scope," "experiment not feasible."

### Reviewer Comment Patterns

Use `references/reviewer-comment-patterns.md` to identify common reviewer comment patterns:

- **Novelty and contribution patterns**: "Incremental contribution," "literature comparison insufficient," "research gap not clearly identified."
- **Method and evidence patterns**: "Method selection not justified," "sample size too small," "statistics insufficient," "mechanism not supported."
- **Writing and presentation patterns**: "English needs revision," "figures need improvement," "structure unclear."
- **Scope and framing patterns**: "Beyond scope," "more suitable for another journal," "overclaiming."
- **Domain-specific patterns**: Civil/construction, polymers, metals, ceramics, nanomaterials.
- **Conflicting reviewer patterns**: Contradictory requests, different novelty assessments.

## Gates

- Never invent data, experiments, or citations.
- Do not fabricate added experiments or supplementary figures.
- Responses must stand alone without the reviewer needing to re-read the manuscript.
- Use experiment remediation plans to provide concrete, actionable experiment proposals.
- Use `AUTHOR_INPUT_NEEDED` when experiment status, line numbers, figure/table IDs, dates, citations, or data are not supplied.
- Do not say an experiment was completed, initiated, scheduled, or will be included unless the user/source explicitly confirms it.
- Apply reviewer strategy library for complex or challenging reviewer comments.
- Recognize common comment patterns to prepare appropriate responses.

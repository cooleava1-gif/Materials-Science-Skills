# Civil Materials Paper Production Design

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this design task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn `civil-materials-research` into a paper-production orchestrator that routes WER-EA mini-review work through standard artifacts, weakness routing, and paper-level gates.

**Architecture:** Keep `civil-materials-research` as the front door, but move the production logic into one reference document plus shared routing artifacts. Companion skills remain responsible for deep work; the orchestrator only decides the next route, enforces stage-aware gates, and returns the exact artifact needed for the next step.

**Tech Stack:** Markdown references, YAML manifests, CSV/MD gate templates, Python release checks, existing civil-materials skill pack

---

## Problem

`civil-materials-research` already routes topic and journal intent, but it still behaves more like a smart router than a true production orchestrator. The PRD calls for a system that can move a civil-materials project from idea to review-ready package with explicit handoffs, stage-aware gates, and weakness routing.

## Scope

This design covers the first production slice only:

- WER-EA mini-review orchestration
- paper-stage aware routing in `civil-materials-research`
- standard intermediate artifacts
- weakness routing and gate reporting
- release-check coverage for the new contract

Experimental manuscript routing and submission-package polishing remain part of the broader PRD, but they are not the first implementation slice.

## Target Architecture

### 1. `civil-materials-research` as the orchestrator

`SKILL.md` stays short and declarative. It should:

- detect `task`, `paper_stage`, `workflow_mode`, `output_package`, `domain`, and `journal`
- name the active route in one line
- load only the reference and fragment files needed for the next step
- hand off to companion skills whenever the request requires deeper work

The router must never duplicate the full logic of reading, writing, citation, figures, response, or data work.

### 2. Paper-production reference layer

Add `skills/civil-materials-research/references/paper-production-orchestrator.md` as the canonical route map for:

- WER-EA mini-review
- experimental manuscript
- submission package
- quality gates
- weakness routing
- standard artifacts

This file is the human-readable contract for how the orchestrator should behave.

### 3. Shared weakness routing

Use a single weakness-routing table format so gates, reviewer comments, and self-review findings can be mapped to a responsible skill and a concrete fix artifact.

The route table should always include:

- weakness description
- `route_to`
- expected artifact
- status
- regression-check status

### 4. Paper-level gates

Paper-level gates should be explicit and machine-readable enough to consume in later automation:

- literature coverage
- source anchoring
- mechanism boundary
- figure/table integrity
- manuscript logic
- reviewer simulation
- submission fit

### 5. Standard artifacts

The orchestrator should prefer these artifacts when they exist:

- `reader-package/package_manifest.json`
- `reader-package/source_map.json`
- `reader-package/citation_handoff.csv`
- `reader-package/figure_handoff.csv`
- `reader-package/review_handoff.md`
- claim-evidence-boundary table
- mechanism-evidence table
- weakness-routing report
- `figure_contract.md`
- `data/FAIR package manifest`
- `submission checklist`

## Behavioral Rules

1. If the user asks for a full WER-EA review workflow, `civil-materials-research` should route through citation, reader, writing, figure, reviewer, and response modules in that order when needed.
2. If a gate fails, the orchestrator should return the blocked gate, the missing input, and the next skill instead of trying to solve everything itself.
3. If a companion skill is the right tool, the orchestrator should hand off and stop.
4. If journal facts are needed, mark them for live verification instead of guessing.
5. If evidence is missing, preserve the gap explicitly rather than fabricating a complete package.

## First Implementation Slice

The first slice should implement only the WER-EA mini-review route with these phases:

- scope and angle
- literature coverage
- source anchoring
- review architecture
- figure planning
- reviewer simulation
- revision loop
- submission fit

This is the smallest route that still proves the orchestrator concept end to end.

## File Map

### Modify

- `skills/civil-materials-research/SKILL.md`
- `skills/civil-materials-research/manifest.yaml`
- `skills/civil-materials-research/references/paper-production-orchestrator.md`
- `tests/test_product_docs_contract.py`
- `scripts/run_release_checks.py`
- plugin mirror copies of the same files

### Likely Additions

- weakness-routing templates under `skills/civil-materials-research/assets/templates/`
- gate report template under `skills/civil-materials-research/assets/templates/`
- route smoke-test fixtures under `skills/civil-materials-research/tests/`

## Verification Strategy

- unit tests should confirm the router advertises the new paper-production route
- contract tests should confirm the reference file exists and is linked from the skill
- release checks should confirm root and plugin mirrors stay aligned
- smoke tests should cover the WER-EA mini-review route and its required artifacts

## Risks

- If the orchestrator becomes too large, it will duplicate companion skills.
- If gates are too vague, they become decorative checklists.
- If weakness routing is not standardized, reviewer feedback will keep fragmenting across modules.

## Decision

Implement the WER-EA mini-review orchestrator slice first, then expand to experimental manuscript and submission-package routes only after the route contract is stable.

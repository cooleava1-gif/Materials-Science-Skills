---
name: civil-materials-response
description: Use when drafting, structuring, auditing, or polishing reviewer responses, rebuttal letters, revision summaries, point-by-point replies, response tables, or resubmission packages for civil engineering and construction materials manuscripts, especially CBM, CCC, JBE, RMPD, IJPE, asphalt pavement, emulsified asphalt, cement/concrete, durability, and mechanism-related reviewer comments.
---

# Civil Materials Response

Build reviewer response packages that are respectful, evidence-first, and revision-verifiable.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect `response_task`, `comment_type`, and `journal_family`.
3. Load only the matching reference files.
4. Produce a point-by-point response, revision action table, rebuttal strategy, or risk audit.
5. Do not promise experiments, analyses, or manuscript changes unless the user has provided evidence or explicitly chooses that revision path.

## Default Output

Use `assets/templates/response-package-template.md`.

Each reviewer comment should become:

- comment ID,
- reviewer concern,
- concern type,
- response strategy,
- manuscript action,
- evidence or data needed,
- polite response draft,
- risk note.

## Civil Materials Response Rules

- Start with agreement or clarification when possible; avoid defensive language.
- Keep "response to reviewer" and "change made in manuscript" separate.
- For mechanism comments, tie the answer to FTIR, SEM, fluorescence, rheology, hydration, or other actual evidence.
- For performance comments, cite test conditions, standards, repeatability, statistics, or limitations.
- For journal fit comments, avoid arguing prestige; argue scope, evidence, and contribution.
- If a reviewer is correct, fix the manuscript and say exactly where.
- If a reviewer is partially mistaken, acknowledge the valid part, explain the boundary, and revise text to prevent misunderstanding.

Use `scripts/build_response_package.py` to scaffold a point-by-point response package.

Use `examples/cbm-major-revision-response-example.md` as a concrete model. Use `tests/pressure-tests/aggressive-reviewer-mechanism-request.md` to check that responses stay respectful, evidence-bound, and honest about missing data.

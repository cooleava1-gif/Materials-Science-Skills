---
name: civil-materials-writing
version: "1.1.0"
stability: stable
description: Use when drafting, restructuring, or planning civil engineering and construction-materials manuscripts from claims, results, figures, notes, outlines, or Chinese drafts, especially abstracts, introductions, methods, results/discussion, conclusions, review papers, experimental papers, waterborne epoxy modified emulsified asphalt, cement/concrete, durability, mechanisms, CBM, CCC, RMPD, JBE, CSCM, and JRE.
---

# Civil Materials Writing

Draft civil-materials manuscripts like a professional researcher: claim first, evidence second, boundary always visible.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect `paper_type`, `section`, `language`, and `journal_family`.
3. Load only the matching fragments and references.
4. Before drafting, write the one-sentence argument and a claim-evidence-boundary map.
5. Draft the requested section using supplied evidence only.
6. Mark missing evidence explicitly instead of inventing data, citations, standards, mechanisms, or novelty.

## Output Contract

Every substantial writing output should include:

- route and section target,
- one-sentence argument,
- claim-evidence-boundary table,
- draft text,
- missing evidence to confirm,
- reviewer-risk notes.

Use `assets/templates/manuscript-argument-template.md` for planning and `assets/templates/section-draft-template.md` for section drafting. Use `scripts/build_manuscript_outline.py` to scaffold an argument chain and manuscript outline.

## WER-EA mini-review writing pipeline

Use this pipeline for WER-EA, waterborne epoxy resin modified emulsified asphalt, waterborne epoxy modified emulsified asphalt, or a small review on modified emulsified asphalt bonding performance.

Load `references/wer-ea-mini-review-pipeline.md` and use `assets/templates/wer-ea-mini-review-template.md` before drafting a WER-EA mini-review. For literature-screening-table, mechanism-evidence-table, test-method-table, performance-comparison-table, durability-evidence-table, or journal-positioning-table outputs, load `references/table-system.md` and use `assets/templates/table-system-template.md`.

1. Literature screening: require a screened source list or make a visible placeholder for search strings, inclusion/exclusion criteria, and study categories.
2. Mechanism evidence chain: convert reader or citation outputs into a table covering bonding performance, emulsion stability, rheology, curing/demulsification, microstructure/chemistry, durability, and engineering boundary.
3. Review outline: build sections from evidence roles, not from paper titles. A default structure is background -> WER-EA modification strategies -> bonding and interface performance -> mechanism evidence -> durability/service gaps -> application and future work.
4. Figure planning: specify figures before drafting claims, including a study-selection flow, mechanism-evidence map, test-method matrix, and claim-strength heatmap.
5. Submission route: write the manuscript angle differently for pavement journals, construction-materials journals, and case-study outlets; mark current journal facts for live verification.

Default WER-EA output: research question, screening criteria, evidence matrix, review outline, paragraph skeleton, gap wording, reviewer risk, figure planning list, submission route, and reviewer-risk notes.

## Boundaries

This skill writes from provided data and explicitly stated assumptions. It does not replace experiments, deep reading, citation verification, supervisor judgment, or current journal instructions.

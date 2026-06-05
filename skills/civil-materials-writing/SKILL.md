---
name: civil-materials-writing
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

## Boundaries

This skill writes from provided data and explicitly stated assumptions. It does not replace experiments, deep reading, citation verification, supervisor judgment, or current journal instructions.

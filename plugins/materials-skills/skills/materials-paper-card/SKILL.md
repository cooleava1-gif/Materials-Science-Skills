---
name: materials-paper-card
version: 1.0.0
stability: beta
description: >-
  Build a source-grounded deep-reading Paper Card for one materials-science
  paper, preprint, PDF, DOI page, or pasted text: fixed Sections 01-16
  covering bibliographic position, research question, background route, pain
  point, core insight, material system and processing route, method and
  module logic, essential formulas, experiment-to-claim evidence chain,
  characterization-chain reading, conclusion boundaries, author-stated
  limitations, critical analysis, learned knowledge, knowledge connections,
  and testable research ideas. Also trigger for 深读卡、论文精读卡片、单篇
  深度解析、证据链、批判性分析、研究想法. Do not use for full-paper
  translation, formal peer-review reports, batch literature monitoring, or
  public-article writing.
---

# Materials Paper Card Router

Read `manifest.yaml` and its `always_load` files, then resolve the source
and paper-type axes before loading any reference.

## Blocking gates

- **source-gate** — no card without an identified source; partial material
  produces a visibly partial card with `Not assessable` sections.
- **invention-gate** — every analytical statement ties to supplied text or
  a reader-package evidence tuple; never invent evidence, data, or
  mechanisms to fill a section.
- **boundary-gate** — the card is a reading artifact, not a peer-review
  report (that is `materials-reviewer`) or a translation.

## Routing protocol

1. Establish the source boundary: full paper / text-only / abstract or
   metadata / an existing `materials-reader` package (preferred — reuse its
   evidence IDs; do not re-extract). Record the locator mode:
   `page-grounded`, `structure-grounded`, or `source-limited`.
2. Classify the paper type (research / review / methods-short / datasets)
   and load its fragment.
3. Build the evidence inventory (claims, figures, tables, equations,
   characterization results, stated limitations) before drafting.
4. Draft the fixed Sections 01-16 per `static/core/output-format.md` and
   `references/card-schema.md`.
5. Read `references/evidence-and-provenance.md` before any analytical or
   externally verified claim; `references/research-idea-gates.md` before
   Section 16.
6. Run the delivery QA: all 16 sections present in order, every
   `Not assessable` justified, evidence IDs resolve, language matches the
   user's.

Hand off re-reading to `materials-reader`, citation checks for Section 01/15
to `materials-citation`, idea routing to `materials-research`, and re-plot
proposals to `materials-figure`.

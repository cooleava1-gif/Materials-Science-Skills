---
name: civil-materials-reader
version: "1.1.0"
stability: stable
description: Use when reading, translating, extracting, auditing, or structuring civil engineering and construction materials papers, especially for source-grounded notes, evidence-chain reading, claim-evidence-mechanism matrices, Chinese-English paper notes, figure/table-aware reading, literature matrices, journal-club preparation, asphalt pavement materials, cement/concrete, durability, sustainability, and waterborne epoxy modified emulsified asphalt.
---

# Civil Materials Reader

Build source-grounded civil materials reading artifacts, not shallow summaries.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect the `source_type` and `output_type`.
3. Load only the matching fragments and references.
4. Produce a Markdown reader, matrix, or evidence-chain audit that preserves the paper's evidence chain.
5. Keep all numbers, figures, tables, mechanisms, and limitations tied to the source.

## Default Output

Use `assets/templates/literature-reading-template.md` as the base structure unless the user requests another format.

For full-text intensive reading, PDF/text-to-`paper.md`, figure/table anchoring, source mapping, or WER-EA mini-review extraction, load `references/fulltext-figure-anchored-reading.md` and use:

- `assets/templates/paper-md-template.md`,
- `assets/templates/source-map-template.json`,
- `assets/templates/translation-notes-template.md`,
- `assets/templates/figure-table-card-template.md`,
- `assets/templates/mechanism-evidence-table-template.md`,
- `assets/templates/dosage-window-table-template.md`,
- `assets/templates/review-handoff-template.md`,
- `assets/templates/obsidian-note-template.md`.

For WER-EA 30-paper intensive-reading packages, also load `references/wer-ea-intensive-reading-package.md`. Produce a linked package with:

- `paper.md`,
- `source_map.json`,
- `translation_notes.md`,
- `figure_table_cards.md`,
- `mechanism_evidence_table.md`,
- `dosage_window_table.md`,
- `review_handoff.md`,
- `obsidian_note.md`,
- `visual_asset_spec.json`,
- `assets/`.

When a source PDF is available and figure/table visual verification is requested, also load `references/pdf-visual-asset-extraction.md` and use `scripts/extract_pdf_visual_assets.py` to create rendered pages, cropped assets, `asset_manifest.md`, `visual_asset_report.json`, and `contact_sheet.png`.

The output should include:

- paper identity,
- research question,
- material system,
- experiment matrix,
- figure/table evidence map,
- mechanism chain,
- limitations,
- what the user can borrow for their own topic.
- claim-evidence-mechanism-boundary audit when the paper will inform a manuscript or review.
- paper.md, source_map.json, translation_notes.md, assets/, visual_asset_spec.json, asset_manifest.md, contact_sheet.png, original excerpt, Chinese understanding, figure card, table card, mechanism_evidence_table.md, dosage_window_table.md, review_handoff.md, obsidian_note.md, and borrowable writing when full-text anchoring is requested.

## Civil Materials Reading Rules

- Extract test conditions and standards when present.
- Do not convert figure captions into unsupported conclusions.
- Separate measured results from inferred mechanisms.
- For asphalt/pavement papers, always capture binder/emulsion, interface, mixture, and service-condition evidence separately.
- For cement/concrete papers, always capture fresh properties, strength, durability, hydration/microstructure, and sustainability boundary separately.
- For review writing, convert each borrowable idea into: claim -> evidence -> mechanism -> boundary -> citation role.
- Flag reviewer risks when a conclusion is stronger than the measurements.
- Use `references/microstructure-interpretation.md` when interpreting SEM, fluorescence microscopy, AFM, DSC/TG, or morphology figures.

If the user asks for a PPT after reading, hand off to `civil-materials-paper2ppt`. If the user asks for polished English after reading, hand off to `civil-materials-polishing`.

For literature tables, mechanism tables, method comparison tables, performance tables, durability tables, or journal positioning tables, load `references/table-system.md` and use `assets/templates/table-system-template.md`.

Use `examples/waterborne-epoxy-evidence-chain-example.md` as a concrete model for evidence-chain reading. Use `tests/pressure-tests/overclaim-from-figure-caption.md` to check that figure captions are not converted into unsupported conclusions.

## WER-EA mini-review reading protocol

Use this protocol for WER-EA, waterborne epoxy resin modified emulsified asphalt, or small-review preparation tasks.

- Literature screening: tag each source by material system, WER dosage, curing agent, emulsifier, asphalt/emulsion type, substrate/interface, and whether it is experimental, review, field, or method evidence.
- Mechanism evidence chain: extract claim -> evidence -> mechanism -> boundary rows for bonding strength, rheology, storage stability, demulsification/curing behavior, FTIR, fluorescence microscopy, SEM/AFM, thermal analysis, moisture/aging durability, and service-condition evidence.
- Review outline handoff: summarize each paper's borrowable role as background, mechanism support, performance comparison, method reference, durability gap, or reviewer-risk caution.
- Figure planning handoff: mark which rows can support a mechanism map, evidence heatmap, study-selection flow, test-method comparison, or performance-mechanism boundary figure.
- PDF visual asset handoff: when the PDF is available, render source pages, crop key figures/tables, record `visual_checked`, `asset_file`, `crop_status`, `defects`, and `qa_status`, and keep local PDF paths out of release artifacts.
- Submission route handoff: flag whether the paper supports pavement/asphalt journals, construction-materials journals, or only background context.
- Obsidian handoff: produce a three-layer `obsidian_note.md` with `1 快读判断`, `2 实验证据层`, `3 写作转化层`, and concept links centered on WER-EA knowledge nodes rather than paper-title chains.

Never treat performance improvement alone as proof of WER-EA mechanism. Keep direct evidence, inferred mechanism, and missing tests visibly separate.

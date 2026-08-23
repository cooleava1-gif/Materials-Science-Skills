---
name: materials-reader
version: "1.4.0"
description: >-
  Use when reading, translating, extracting, or organizing full papers for
  materials science and engineering research. Trigger for figure-aware
  Chinese-English paper readers, deep-reading notes, method and data
  extraction, paper cards, and reader-package handoffs from PDFs. Also produces
  a Chinese-first interactive bilingual HTML reading page (sentence-level
  hover/focus to reveal the English source) for full-paper translation requests.
  Chinese triggers 中文触发：论文精读、文献阅读、读文献、论文笔记、证据链整理、
  生成中文版、全文翻译、可交互双语网页、悬停看原文.

---

# Materials Science Reader Router

Read `manifest.yaml` and its `always_load` files. Apply profile-first routing, detect `source_format`, `output_type`, `material_family`, and `domain`, then load the selected source, output, terminology, and ethics fragments.

For each paper, return bilingual Markdown notes when requested, `source_map.json`, a terminology ledger, and figure grounding. Keep every claim anchored to a page, paragraph, table, figure, or other supplied source location; metadata-only records must remain metadata-only.

When the user asks for a full-paper Chinese reading page ("生成中文版", "全文翻译", "可交互双语网页"), produce a Chinese-first interactive HTML page from `assets/templates/bilingual-reader-template.html` following `references/bilingual-html-reader.md`: sentence-level English-Chinese alignment, hover/focus to reveal the English source, figure/table/caption/hierarchy preserved. This reuses the same source grounding and terminology ledger as the Markdown package — it is an output format, not a separate skill.

Evidence boundary:

- Distinguish what the paper says from what you infer. Separate abstract/metadata leads from full-text evidence.
- Never interpret microstructure or mechanism claims without explicit evidence; flag overclaim risks in a confidence note.
- If full text, caption, source page, or supplementary file is unavailable, mark the gap and request it instead of reconstructing content.

When the package feeds another skill, emit a bounded `reader-package` with stable IDs, source anchors, evidence status, and terminology decisions. Route claim-citation mapping to `materials-citation` and recurring discovery to `materials-literature-pipeline` rather than silently expanding the reader scope.

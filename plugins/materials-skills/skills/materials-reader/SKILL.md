---
name: materials-reader
version: "1.3.0"
description: Use when reading, translating, extracting, or organizing full papers for materials science and engineering research.
---

# Materials Science Reader Router

Read `manifest.yaml` and its `always_load` files. Apply profile-first routing, detect `source_format`, `output_type`, `material_family`, and `domain`, then load the selected source, output, terminology, and ethics fragments.

For each paper, return bilingual Markdown notes when requested, `source_map.json`, a terminology ledger, and figure grounding. Keep every claim anchored to a page, paragraph, table, figure, or other supplied source location; metadata-only records must remain metadata-only.

Evidence boundary:

- Distinguish what the paper says from what you infer. Separate abstract/metadata leads from full-text evidence.
- Never interpret microstructure or mechanism claims without explicit evidence; flag overclaim risks in a confidence note.
- If full text, caption, source page, or supplementary file is unavailable, mark the gap and request it instead of reconstructing content.

When the package feeds another skill, emit a bounded `reader-package` with stable IDs, source anchors, evidence status, and terminology decisions. Route claim-citation mapping to `materials-citation` and recurring discovery to `materials-literature-pipeline` rather than silently expanding the reader scope.

---
name: materials-reader
version: "1.2.0"
description: Use when reading, translating, extracting, or organizing full papers for civil engineering and construction materials research.
---

# Materials Science Reader

Read and organize materials papers into structured bilingual notes with source anchors.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Apply profile-first routing from `.materials/profile.yaml`; on first use, ask for direction once and save it locally.
3. Detect `source_format` and `output_type` from the user input.
4. Load only the matching source and output fragments.
5. For each paper, produce: bilingual Markdown notes, source_map.json, terminology ledger, figure grounding.
6. Never interpret microstructure or mechanism claims without explicit evidence.

## Gates

- Source anchor every claim to page, paragraph, or figure.
- Distinguish what the paper says from what you infer.
- Flag overclaim risks in the confidence note.

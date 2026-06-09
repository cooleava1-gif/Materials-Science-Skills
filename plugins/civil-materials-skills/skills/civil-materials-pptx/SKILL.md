---
name: civil-materials-pptx
version: "1.0.0"
stability: stable
description: Use when generating, converting, or polishing real PowerPoint .pptx slide decks for civil engineering and construction materials research, including image embedding, figure cropping, speaker notes, paper-to-PPTX, group meeting slides, journal club decks, thesis reports, asphalt pavement materials, emulsified asphalt, waterborne epoxy, cement/concrete, durability, mechanisms, CBM, CCC, JBE, RMPD, and IJPE presentations.
---

# Civil Materials PPTX

Generate real `.pptx` decks for civil materials research, not only slide outlines.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect `deck_type`, `material_domain`, and `source_type`.
3. Load only the matching references.
4. Build a slide plan first unless the user already provided one.
5. Use `scripts/build_civil_materials_pptx.py` for one-click `.pptx` generation from a scaffold, Markdown outline, or JSON outline with optional images, crop settings, and speaker notes.
6. Return the `.pptx` path, deck logic, and any missing evidence placeholders.

## Default Deck Logic

Engineering problem -> material design -> experiment chain -> key results -> mechanism -> durability/service relevance -> limitations -> next work.

Use Chinese slide titles by default for group meeting, thesis, and journal-club decks. Use English titles only when the user asks for an English presentation.

## PPTX Rules

- Keep claims tied to figures, tests, or source papers.
- Do not overload slides with manuscript paragraphs.
- Use one main message per slide.
- When embedding images, keep text on the left and figures on the right unless the user requests another layout.
- Use crop only to remove margins or irrelevant borders; do not crop away data labels, axes, legends, or scale bars.
- Speaker notes should explain the evidence chain, not repeat slide bullets.
- Separate measured results from inferred mechanisms.
- For asphalt/emulsified asphalt decks, separate binder/emulsion, interface bonding, mixture, and service-condition evidence.
- For cement/concrete decks, separate fresh properties, strength, durability, hydration/microstructure, and sustainability boundary.

If the user provides a Markdown outline from `civil-materials-paper2ppt`, pass it to `scripts/build_civil_materials_pptx.py --input outline.md`. Use JSON input when images, crop settings, or speaker notes must be controlled per slide.

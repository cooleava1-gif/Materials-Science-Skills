---
name: civil-materials-paper2ppt
version: "1.0.0"
stability: stable
description: Use when turning civil engineering and construction materials papers, projects, review notes, manuscripts, or evidence-chain matrices into Chinese PPT outlines, PPTX-ready Markdown, or one-click PPTX handoff for journal club, group meetings, thesis reports, literature presentations, asphalt pavement materials, cement/concrete, durability, sustainability, CBM, CCC, JBE, RMPD, IJPE, and JRE.
---

# Civil Materials Paper2PPT

Create civil materials presentations around the evidence chain, not manuscript section order.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect the `deck_type` and `paper_type`.
3. Use the matching reference and `assets/templates/civil-materials-ppt-template.md`.
4. Build a slide outline or PPTX-ready structure with Chinese titles by default.
5. Keep every figure, claim, and takeaway tied to evidence.
6. If the user requests a file, use `scripts/build_ppt_markdown.py --pptx-output` or hand off to `civil-materials-pptx`.

## Default Slide Logic

Engineering problem -> material design -> experiment chain -> key results -> mechanism -> limitations -> what to borrow or do next.

If a real `.pptx` is requested, use `scripts/build_ppt_markdown.py --pptx-output deck.pptx` when a scaffold is enough. Use `civil-materials-pptx` directly when the user already has a Markdown/JSON outline.

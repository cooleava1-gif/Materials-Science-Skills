---
name: materials-paper2ppt
version: "1.0.0"
stability: stable
description: Use when turning civil engineering and construction materials papers into Chinese PPT outlines or PPTX-ready decks.
---

# Materials Science Paper2PPT

Create materials presentations around the evidence chain, not manuscript section order.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Apply profile-first routing from `.materials/profile.yaml`; on first use, ask for direction once and save it locally.
3. Detect `deck_type`, `paper_type`, and `task`.
4. Load only the matching fragments.
5. Build a slide outline or PPTX-ready structure with Chinese titles by default.
6. Keep every figure, claim, and takeaway tied to evidence.

## Gates

- If a real `.pptx` is requested, use `scripts/build_ppt_markdown.py --pptx-output` or hand off to `materials-pptx`.

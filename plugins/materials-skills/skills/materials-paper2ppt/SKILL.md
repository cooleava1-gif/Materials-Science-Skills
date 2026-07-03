---
name: materials-paper2ppt
version: "1.0.0"
stability: stable
description: Use when turning materials science and engineering papers into Chinese PPT outlines or PPTX-ready decks.
---

# Materials Science Paper2PPT

Create materials presentations around the evidence chain, not manuscript section order.

## Layered architecture

This skill is split into two layers:

- A **static layer** under `static/` that holds reusable content fragments.
- A **dynamic layer** (this file plus [manifest.yaml](manifest.yaml)) that detects the request's axes and loads only the fragments needed for the current job.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Apply profile-first routing from `.materials/profile.yaml`; on first use, ask for direction once and save it locally.
3. Detect `deck_type`, `paper_type`, and `task`.
4. Load only the matching fragments.
5. Build a slide outline or PPTX-ready structure with Chinese titles by default.
6. Keep every figure, claim, and takeaway tied to evidence.

## Gates

- If a real `.pptx` is requested, use `scripts/build_ppt_markdown.py --pptx-output` or hand off to `materials-pptx`.

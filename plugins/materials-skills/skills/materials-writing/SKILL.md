---
name: materials-writing
version: "1.1.0"
description: Use when drafting, restructuring, or auditing manuscripts for civil engineering and construction materials research.
---

# Materials Science Writing

Draft materials manuscripts with evidence-grounded claims and journal-aware structure.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Apply profile-first routing from `.materials/profile.yaml`; on first use, ask for direction once and save it locally.
3. Detect `paper_type`, `section`, `language`, and `journal_family`.
4. Load only the matching fragments.
5. Follow the argument chain for the detected paper type.
6. Draft section by section, keeping each claim anchored to evidence.

## Gates

- Claims must match the evidence contract: no overclaim, no speculation presented as fact.
- Use the claim-strength ladder to calibrate causal vs. associative language.
- For WER-EA manuscripts: follow the mini-review pipeline if this is a review-style paper.

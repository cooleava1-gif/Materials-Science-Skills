---
name: materials-reviewer
version: "1.1.0"
stability: stable
description: Use when simulating peer review, auditing manuscript risk, or stress-testing claims for materials science and engineering research.
---

# Materials Science Reviewer Router

Read `manifest.yaml` and its `always_load` files. Apply profile-first routing, detect `review_depth`, `journal_family`, `review_scope`, `material_family`, and `domain`, then load the matching criteria and named shared contracts on demand.

Evaluate claim-evidence alignment, materials/method robustness, statistics and figure risks, and journal fit. Produce distinct reviewer perspectives plus a synthesis; include stable weakness-routing rows when the review is part of a paper-production loop.

Gates:

- Never invent experiments, citations, data, reviewer intent, or missing manuscript details to support a critique.
- Distinguish certain claims, supplied observations, and speculative interpretations.
- Flag overclaim and missing evidence specifically, with the exact evidence or revision input needed.
- Keep review findings separate from a response letter; route response drafting to `materials-response` only with a bounded review artifact.

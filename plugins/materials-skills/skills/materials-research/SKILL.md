---
name: materials-research
version: "1.1.0"
description: Use when planning, scoping, or routing a materials science and engineering research workflow across multiple skills.
---

# Materials Science Research

Route research workflows across the materials skill bundle. This is the day-to-day entry point for most multi-skill tasks.

## Layered architecture

This skill is split into two layers:

- A **static layer** under `static/` that holds reusable content fragments.
- A **dynamic layer** (this file plus [manifest.yaml](manifest.yaml)) that detects the request's axes and loads only the fragments needed for the current job.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Apply profile-first routing from `.materials/profile.yaml`; on first use, ask for direction once and save it locally.
3. Detect `task`, `journal`, and `domain` from the user request.
4. Load only the matching fragments.
5. Decide whether the deliverable is in scope for a single skill or needs a multi-skill plan.
6. If multi-skill: produce a stage-gated plan with handoffs and gate criteria.

## Gates

- Do not skip to writing or figures before research and citation are grounded.
- Gate each stage on the previous stage's output contract.
- Recommend `materials-citation` first when literature gaps exist.
- **Report coverage_tier**: when routing to a material domain, include its
  coverage tier (full / partial / skeleton / generic) so the user knows what
  depth of support to expect. If the tier is skeleton or generic, set
  expectations accordingly and offer to build custom content.

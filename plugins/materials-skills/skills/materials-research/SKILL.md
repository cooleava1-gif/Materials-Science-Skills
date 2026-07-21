---
name: materials-research
version: "1.2.0"
description: Use when planning, scoping, or routing a materials science and engineering research workflow across multiple skills.
---

# Materials Science Research Router

Read `manifest.yaml` and its `always_load` files. Apply profile-first routing from `.materials/profile.yaml` (explicit direction > saved profile > neutral fallback), then detect the request's task, journal, domain, paper stage, and workflow mode. Read the mapped fragment for each selected axis; do not infer its contents from trigger words.

If the deliverable spans multiple skills, produce a stage-gated plan with inputs, handoffs, gate criteria, and the output contract for each stage. Load `_shared/core/research-state-contract.md` when state must persist across literature, DOE, data, figures, writing, reviewer, or submission work. Load `_shared/core/evidence-contract.md` for a claim-evidence ladder and `_shared/paper-production/weakness-routing.md` for reviewer or paper-gate weaknesses.

Gates:

- Never invent citations, data, mechanisms, reviewer intent, journal facts, experimental results, or completed actions. Mark missing evidence and route the gap.
- Do not start writing or figures before research and citation are grounded; each stage is gated by its previous output contract.
- Recommend `materials-citation` first for literature gaps and `materials-literature-pipeline` for recurring discovery, candidate scoring, or digest triage.
- When routing to a material domain, report `coverage_tier` as full, partial, skeleton, or generic; set expectations for skeleton/generic coverage and offer a bounded custom-content route.

Return a bounded plan or gate report with route, coverage tier, stage status, missing inputs, and handoffs. Do not silently continue through a failed gate.

---
name: materials-research
version: "1.3.0"
description: >-
  Use when planning, scoping, or routing a materials research workflow across
  skills. Trigger for research positioning,
  novelty and gap analysis, mini-reviews, evidence audits, topic selection,
  and multi-skill pipeline orchestration across civil, polymers, metals,
  ceramics, functional, and nano families.
  Chinese triggers 中文触发：材料科研、科研选题、文献综述规划、实验方案规划、投稿策略.

---

# Materials Science Research Router

Read `manifest.yaml` and its `always_load` files. Apply profile-first routing from `.materials/profile.yaml` (explicit direction > saved profile > neutral fallback), then detect the request's task, journal, domain, paper stage, and workflow mode. Read the mapped fragment for each selected axis; do not infer its contents from trigger words.

For multi-skill deliverables, produce a stage-gated plan with inputs, handoffs, gates, and an output contract. Load `_shared/core/research-state-contract.md` when state must persist across literature, DOE, data, figures, writing, reviewer, or submission work. Load `_shared/core/evidence-contract.md` for a claim-evidence ladder and `_shared/paper-production/weakness-routing.md` for reviewer or paper-gate weaknesses.

Gates:

- Never invent citations, data, mechanisms, reviewer intent, journal facts, experimental results, or completed actions. Mark missing evidence and route the gap.
- Do not start writing or figures before research and citation are grounded; each stage is gated by its previous output contract.
- Recommend `materials-citation` first for literature gaps and `materials-literature-pipeline` for recurring discovery, candidate scoring, or digest triage.
- When routing to a material domain, report `coverage_tier` as full, partial, skeleton, or generic; set expectations for skeleton/generic coverage and offer a bounded custom-content route.

Return a plan or gate report with route, coverage tier, stage status, missing inputs, and handoffs. Do not continue through a failed gate.

session_guard:
  scope: materials-skills/materials-research
  state_file: .materials/session-context.yaml
  warm_fragment:
    key_format: "<scope>::<fragment path>"
    if: qualified key in warm_fragments and loaded_turn ≤ current turn
    then: acknowledge "[context: <label> — turn <N>]"; apply routing silently without re-stating
    else: load fully; append {key, scope, path, label, loaded_turn} to warm_fragments
    legacy: entries missing key or scope are cold; never match by path alone
  routing_change:
    if: detected domain, material_family, or task differs from active_routing
    then: clear warm entries for changed axis owned by this scope; reload; update active_routing; emit routing change
  contract: ../_shared/core/session-context-contract.md

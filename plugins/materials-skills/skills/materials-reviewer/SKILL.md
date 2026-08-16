---
name: materials-reviewer
version: "1.1.0"
stability: stable
description: Use when simulating peer review, auditing manuscript risk, or stress-testing claims for materials research. Trigger for referee reports, desk-reject prechecks, methodology/statistics audits, claim-evidence checks, and journal-tier calibration from domain journals to flagship titles. Chinese triggers 中文触发：模拟审稿、审稿意见模拟、拒稿风险、投稿前审查.
---
route:
  detect: [review_depth, journal_family, review_scope, material_family, domain, journal_tier]
  priority: explicit_request > .materials/profile.yaml > neutral_fallback
  load: manifest.yaml axes only
gates:  # check in order; first matching gate triggers
  - id: fabrication-gate
    if: reviewer intent invented or manuscript detail fabricated to support a critique
    then: flag the gap as [evidence needed]; never invent content to fill it

  - id: claim-status-gate
    if: claim status is ambiguous (certain vs observed vs speculative)
    then: distinguish explicitly before evaluating; never collapse into a single verdict

  - id: separation-gate
    if: response letter drafting requested in the same output as the review
    then: decline; route to materials-response with the bounded review artifact as input

output:
  required:
    perspectives: "≥2 distinct reviewer angles: originality, evidence sufficiency, method robustness, stats/figures, journal fit"
    synthesis: consolidated risk assessment and priority matrix
  per_finding:
    type: overclaim | missing_evidence | figure_risk | stats_gap | novelty_concern
    specifics: exact missing evidence or revision input needed — not generic advice
    severity: desk_reject | major | minor | optional
  tier_addendum:
    instruction: apply loaded journal_tier fragment as an additional pass on all findings
    tier1: flag domain-specific fatal flaws; incremental novelty is acceptable
    tier2: flag missing quantitative mechanism and state-of-the-art comparison
    tier3: flag absence of scientific significance, generalizability, or unexpected finding
  paper_production_loop:
    weakness_routing_rows: required when review is part of a paper-production gate (weakness-routing contract)

handoffs:
  response_drafting: → materials-response (requires bounded review artifact as input)

session_guard:
  scope: materials-skills/materials-reviewer
  state_file: .materials/session-context.yaml
  warm_fragment:
    key_format: "<scope>::<fragment path>"
    if: matching key in warm_fragments and loaded_turn ≤ current turn
    then: acknowledge "[context: <label> — turn <N>]"; apply criteria silently
    else: load; append {key, scope, path, label, loaded_turn}
    legacy: missing key/scope entries are cold; never match by path
  routing_change:
    if: domain, material_family, or journal_tier differs from active_routing
    then: clear changed-axis entries in this scope; reload; update; emit "[routing: <old> → <new>]"
  contract: ../_shared/core/session-context-contract.md

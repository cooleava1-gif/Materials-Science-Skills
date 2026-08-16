---
name: materials-figure
description: >-
  Use when creating, revising, auditing, polishing submission-grade materials-science figures, multi-panel plots, mechanism schematics, evidence maps, journal SVG/PDF/TIFF outputs for materials, construction materials, or civil engineering research. Trigger for XRD, FTIR, TG/DTG, SEM, performance curves, bonding, rheology, and figure-package QA requests. Do not use for dashboards or Illustrator/Figma-first infographics.
  Chinese triggers 中文触发：论文配图、科研绘图、出版级图表、多面板图、机制示意图.
version: "2.3.0"
stability: stable
---

route:
  priority: explicit_request > .materials/profile.yaml > neutral_fallback
  load: manifest axes only
  ai_schematic: AI-image request (OpenRouter/GPT Image 2) → ai-schematic-workflow.md + openrouter-image-generation.md + generate_openrouter_schematic.py; skips backend gate; hybrid → hybrid-composition.md

gates:  # ordered
  - id: backend-gate
    if: backend runtime or required plotting packages are absent
    then: report the exact missing dependency; halt before rendering
    backend_rule: python default; r opt-in via scripts/figure_backend.py (explicit or saved choice); selected backend exclusive

  - id: contract-gate
    if: the figure contract or source-data anchor is missing
    then: request it; do not guess, fabricate, or use placeholder data

  - id: materials-kb-gate  # the materials gate
    if: materials-science entities appear — XRD phases, FTIR wavenumbers, performance values
    then: load static/core/materials_kb.yaml; wrong assignment blocks plotting; warnings visible

  - id: storyboard-gate
    if: request covers multiple figures
    then: validate storyboard as DAG before individual contracts

  - id: ai-asset-gate
    if: AI imagery requested (standalone or hybrid)
    then: standalone → internal draft; hybrid → AI decorates, backend draws semantics; policy gate + disclosure + no data panels

  - id: mock-data-gate
    if: data is mock data, template-only, or illustrative
    then: label as template; never present as experimental result

output:
  required: [plot.py or plot.R, figure.svg, caption.md, qa_report.md]
  caption_rule: "measured claims | inferred claims — boundary explicit in every caption"
  qa_rule: "exclusive backend (python default, r opt-in); export bundle = SVG + PDF + PNG + TIFF; visual QA status reported"

handoffs:
  html_decks: → materials-html-deck

session_guard:
  scope: materials-skills/materials-figure
  state_file: .materials/session-context.yaml
  warm_fragment:
    key_format: "<scope>::<fragment path>"
    if: matching key in warm_fragments and loaded_turn ≤ current turn
    then: acknowledge "[context: <label>]"
    else: load fully; append {key, scope, path, label, loaded_turn} to warm_fragments
    legacy: entries missing key or scope are cold; never match by path alone
  routing_change:
    if: material_family or domain differs from active_routing
    then: clear domain entries in this scope; reload; update active_routing; emit routing change
  contract: ../_shared/core/session-context-contract.md

# Changelog

All notable changes to **Materials Science Skills** are documented in this
file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/) loosely:
- `feat` commits raise the minor version
- `fix` commits raise the patch version
- breaking schema or manifest changes raise the major version

## [Unreleased]

### Added — hybrid mode tool gate and fallback (2026-08-16, third session)
- `materials-figure` 2.4.0: hybrid composition now requires a
  **user-provided AI image model** (GPT Image 2 via OpenRouter or any
  OpenAI-compatible endpoint, nanobanana / Gemini, or user-self-generated
  assets from the decoration prompts). When no tool is available the
  skill explains the requirement and falls back to full R/Python drawing
  with procedural decoration approximations — first-class path, same
  export bundle, no AI disclosure needed; it never fabricates
  AI-generated provenance. Gate reworked (`ai-asset-gate`), workflow and
  references updated, fallback eval added (25 total).

### Added — GPT Image 2 + R hybrid composition (2026-08-16, second session)
- `materials-figure` 2.3.0: hybrid composition mode for publication-grade
  schematics and graphical abstracts — GPT Image 2 generates decoration
  assets only (icons, gradients, shadows, semi-transparent blocks;
  `--asset-mode` with transparent background and no-text constraints by
  construction), R draws every semantic element (all text, borders,
  arrows, dashed boxes, scientific annotations) as vector on top.
  Ships `references/hybrid-composition.md` (layer contract, R compositing
  patterns, `asset_manifest.yaml` placement map, text-vector/z-order/
  alignment/palette QA additions, AI-free fallback, hybrid disclosure),
  an asset-mode variant of `generate_openrouter_schematic.py` (dry-run
  verified), and a layer-split enforcement eval.

### Added — nature-skills benchmark upgrade (2026-08-16)
- Add `materials-statistics` as the 15th skill: statistical-reporting
  audit/revision/drafting for materials manuscripts — replicate and `n`
  definitions (specimens vs repeated readings, pseudoreplication),
  design-matched tests (factorial ANOVA, Taguchi S/N with stated error
  term, RSM with lack-of-fit, Scheffé mixture), multiple-comparison
  corrections, effect sizes with uncertainty, figure-statistics alignment,
  and reviewer-facing risk; wired into the research router
  (`statistics-audit` task fragment, companion map) with its own evals.
- Add `materials-paper-card` as the 16th skill: source-grounded
  16-section deep-reading cards (bibliographic position → material system
  and processing route → characterization-chain reading → conclusion
  boundaries → gated testable research ideas), three locator modes, and
  reader-package evidence reuse; wired into the router
  (`deep-reading-card` task fragment) with its own evals.
- Add reference verification to `materials-citation` (1.2.0):
  field-by-field multi-source cross-check via the academic-search MCP —
  volume-year vs DOI-year conflicts, hallucinated first authors, author
  order anomalies, page drift, journal renames — structured OK/WARN/ERROR
  report with Zotero-style fix suggestions (adapted from nature-skills'
  ref-verifier patterns).
- Add an AI-schematic route to `materials-figure` (2.2.0): explicit
  OpenRouter / GPT Image 2 requests route through a policy-gated workflow
  (`references/ai-schematic-workflow.md`,
  `references/openrouter-image-generation.md`,
  `scripts/generate_openrouter_schematic.py` with dry-run-first mode);
  outputs are provenance-tracked internal drafts, never data panels.
- Add an opt-in R backend to `materials-figure` (2.2.0):
  ggplot2/patchwork/ComplexHeatmap with persisted preference
  (`scripts/figure_backend.py`, `MATERIALS_FIGURE_BACKEND` override),
  exclusive-per-package rule, and `references/r-backend.md`; Python stays
  the default.
- Add bilingual (EN+中文) trigger keywords to all skill descriptions for
  reliable Chinese-language invocation.
- Add `scripts/autoupdate_skills.py` + `docs/autoupdate.md`: throttled,
  offline-safe, fast-forward-only session-start auto-update for claude /
  opencode / antigravity / zcode / codex / dsh destinations, with drift
  repair, per-destination state/locks, and hook snippets for Claude Code
  and Codex (8 pytest cases).
- Verify and document `npx skills` compatibility: discovery and install
  work out of the box (`npx skills add <repo> --list/--copy`); the flat
  copy does not resolve the two `_shared` trees — boundary documented in
  install.md with the single-shared-tree restructure on the roadmap.

### Changed
- `materials-research` 1.3.0: two new task fragments
  (`statistics-audit`, `deep-reading-card`), companion-skill and
  companion-module entries for the two new skills; task axis now 17
  values.
- Skill-count invariants across README, skills-index, host-packaging
  validation (MIN_BUNDLE_SKILLS 16), and submission docs tests updated
  14 → 16.

### Added
- Add cross-platform adapters and installer (`scripts/install_skills.py`):
  install the bundle on Claude Code (`--target claude`), OpenCode
  (`--target opencode`), Antigravity (`--target antigravity`), Codex
  (`--target codex`), or any SKILL.md-aware agent
  (`--target generic --dest <dir>`). Non-codex targets *materialize* each
  skill: both `_shared` trees are merged into `<skill>/_shared/`, all
  relative references are rewritten to the merged tree, Codex-only
  `agents/` is dropped, and every reference is re-verified after install.
- Add a Claude Code plugin marketplace manifest
  (`.claude-plugin/marketplace.json`) and plugin manifest
  (`plugins/materials-skills/.claude-plugin/plugin.json`) for plugin-based
  distribution without materialization.
- Add `adapters/` per-platform READMEs (Claude Code, OpenCode, Antigravity)
  covering install commands, skills locations, MCP registration, and
  compatibility notes.
- Add `scripts/test_install_skills.py` (12 pytest cases) covering
  materialization, reference rewriting, MCP merging, dry-run purity, and
  codex-layout preservation.
- Add beta `materials-literature-pipeline` as the 14th skill for recurring
  materials literature discovery, candidate scoring, source-depth triage,
  digest delivery, degradation handling, gap analysis, and review-compilation
  handoffs.
- Add a shared research-state contract and template linking literature
  candidates, reader packages, citation handoffs, DOE, data, figures, claims,
  and reviewer risks through `source_map`, `doe_map`, `data_map`,
  `figure_map`, `claim_map`, and `risk_map`.
- Add `literature-pipeline-handoff.yaml` with an explicit candidate-table
  interface and six-field score breakdown.
- Add `materials-writing` foundation templates, project `state.json` template,
  writing-mode fragments, and a lightweight initializer for compose/revise/
  hybrid/QA writing loops.
- Add anchored `materials-writing` evaluation rubric, stopping rules, and
  validation checklist for content-first QA decisions.
- Add ZCode support: a `--target zcode` install path in the cross-platform
  installer (`~/.zcode/skills/`) and a `.zcode-plugin/plugin.json` manifest
  (skills bundle plus inline `materials-academic-search` MCP server resolved
  through `${ZCODE_PLUGIN_ROOT}`) for plugin-marketplace installation.
- Add deepseek-harness (dsh) support: `scripts/sync_dsh_skills.py` for
  layout-preserving sync into project/user skill roots, a zero-copy
  `dsh/cordis.patch.yml` overlay (customSkillDirs plus an inserted
  `@deepseek-ai/dsh-mcp-client` row), and dsh invocation-policy keys on
  `_shared/SKILL.md` (`disable-model-invocation`, `user-invocable`) so the
  shared support skill stays out of dsh catalogs. Verified end-to-end on dsh
  0.1.0-rc.6: 14 skills discovered, MCP tools registered.
- Add cross-host packaging validation (`validate_host_packaging.py`) to the
  release gate: Claude and ZCode manifests, the marketplace pair (root and
  `.claude-plugin/` copies must stay identical), SKILL.md frontmatter
  compatibility (name pattern, 1024-char description cap), and dsh-specific
  checks (kebab-case names, `_shared` invocation policy, sync script and
  overlay presence).
- Add `adapters/zcode/` and `adapters/dsh/` per-platform READMEs.

### Changed
- Neutralize platform coupling in the skill corpus: replace `$CODEX_HOME`
  hard-coded paths in `materials-citation` and `materials-research`
  references with platform-neutral `<skills-dir>` placeholders.
- Update `README.md` and `install.md` with a multi-platform support matrix;
  the Codex plugin/manual install paths remain unchanged.
- Declare the Claude plugin's MCP server inline in
  `plugins/materials-skills/.claude-plugin/plugin.json` (`$CLAUDE_PLUGIN_ROOT`
  args) instead of relying on the plugin-root `.mcp.json`.
- Route `materials-research` to `materials-literature-pipeline` only for
  recurring discovery, candidate scoring, and literature-digest triage before
  deep reading.
- Refactor the 14 local Skill entry points toward constraint-dense routers:
  generic workflow prose is reduced while evidence boundaries, material gates,
  DOE constraints, source anchors, handoff schemas, and missing-input blockers
  remain explicit. Authenticated A/B/C behavior evidence is now complete for
  the local candidate, with the full campaign and targeted high-risk
  regressions recorded under `reports/skill-simplification/`.
- Converge the duplicate citation contract to
  `materials-citation/static/core/contract.md`; keep the former path only as a
  compatibility pointer and remove it from default loading.
- Update release checks to require the literature-pipeline, research-state, and
  content-first QA assets added by this upgrade.
- Clarify that literature-pipeline scores are discovery priorities only:
  metadata-only and abstract-screened records cannot support manuscript claims
  until full-source reading or data extraction verifies them.
- Extend `materials-writing` routing with a visible `writing_mode` axis and
  require state-machine outputs to report artifact, score/status, remaining
  risks, stop-or-continue reason, and one next action.
- Slim the public GitHub delivery boundary: generated figure atlas/gallery/
  showcase images and Python regression tests are maintainer-side assets, while
  the public release gate checks installable skill contracts, templates,
  references, and lightweight preview documentation.

### Documentation
- Add the constraint-density candidate architecture, current inventory,
  shared-layer decision record, authenticated behavior evidence summary, and
  explicit unreleased-local status to the README and
  `reports/skill-simplification/`.
- Sync root `README.md` and 6 key skill READMEs (`materials-research`,
  `materials-figure`, `materials-writing`, `materials-data`,
  `materials-reviewer`, `materials-paper-to-patent`) to actual code: 14
  skills listed, 21/12/20 figure-asset counts corrected, profile-first
  routing described, 6-axis manuscript writing explained, 22 domain
  reviewer-criteria enumerated.
- Refresh `docs/gallery/README.md` with full atlas / gallery /
  `materials4papers` inventories and a quantitative asset summary.
- Add `install.md` Path D "Paper to Chinese Invention Patent" plus a
  patent-pointer in the recommended-reading order.

## v1.1.0 — 2026-06-20 — 13 skills + figure upgrade

### Added
- 13th skill: `materials-paper-to-patent` (Chinese invention patent
  conversion, evidence-grounded).
- 3-axis routing in `materials-paper-to-patent`:
  `source_format` × `task_mode` × `invention_type` (default
  `process-material`).
- Civil patent knowledge base
  `static/core/patent_kb.yaml` covering 5 patent-law articles (22 / 26.3
  / 26.4 / 31.1 / 33 + Implementing Regulations article 20), CNIPA
  examination guidelines (2023 edition, second-part substantive
  examination), 4 invention-type verb patterns, 9 claim anti-patterns,
  7 unit-alias groups, and 6 material-domain links
  (`civil_cement_concrete`, `civil_asphalt`, `civil_insulation`,
  `ceramics_structural`, `polymer_composite`, `metal_alloy`).
- Claim-content validation engine
  `scripts/validate_patent_claims.py` with 7 rule functions (independent
  technical features, dependent-claim references, specification support,
  anti-patterns, unit consistency, invention-type alignment, claim-count
  limits) — 36 unit tests.
- 9 patent scripts: PDF text extraction, project init, claim audit,
  structural validation, claim-content validation, package builder,
  DOCX renderer, SVG flowchart renderer, LaTeX→OMML math conversion.
- Patent worked example
  `examples/civil-concrete-strengthening/` (concrete-strengthening
  patent package with `draft.json`, `flow-steps.json`, `README.md`).
- `materials-figure` upgraded:
  - 21 chart-atlas boards (XRD, mechanical, thermal, spectroscopy,
    microscopy, performance, durability, electrochemistry, comparison,
    composite layout, phase diagram, kinetics, adsorption, rheology,
    degradation, pore size, EIS, MIP, multiscale architecture,
    mechanism flowchart, graphical abstract).
  - 12 gallery composites (cement hydration, steel microstructure,
    polymer composite, ceramics reliability, asphalt modification,
    concrete durability, functional coating, multipanel FTIR/TG/morph,
    graphical abstract, evidence chain, etc.).
  - 20 `materials4papers` worked figure packages (cement hydration XRD,
    steel EBSD, polymer thermal degradation, ceramics Weibull, 2D Raman
    mapping, nanoparticle size distribution, asphalt bonding, concrete
    durability retention, multifunctional radar, S-N fatigue, alloy
    stress-strain, tack-coat schematic, multiscale graphical abstract,
    hierarchical mechanism, ceramic Nyquist, polymer GPC, GISAXS 2D,
    in-situ XRD, multifield temperature/strain, asphalt fracture CT).
  - 53 production-grade figure assets total.
- Materials knowledge validation engine
  `scripts/validate_materials_claims.py` with 210-entry `materials_kb`
  across 7 families.
- 12-case `evals/evals.json` for `materials-figure`.
- Profile-first routing protocol in `_shared/core/direction-profile.md`
  (first-use question, `.materials/profile.yaml` local storage, 3-layer
  routing fallback).
- 7 `_shared/core/` protocols: `direction-profile`,
  `claim-strength-ladder`, `evidence-contract`, `source-basis`,
  `stance`, `terminology-ledger`, `ethics`.
- 17 journal-format guides in `_shared/journal-formats/`
  (CBM, CCC, RMPD, JBE, IJPE, WER-EA, nature-materials, acs-nano,
  acta-materialia, advanced-materials, advanced-functional-materials,
  ceramics-international, energy-buildings, jacers, jmca, nano-letters,
  progress-polymer-science, thermal-sciences, …).

### Changed
- 22 reviewer-criteria documents in `materials-reviewer` (one per
  material sub-direction: asphalt, cement, ceramics,
  construction-materials, civil-generic, waterproofing-sealants,
  timber-masonry, steel, geotechnical, nano, nano-thin-films,
  2d-materials, nanocomposites, nanoparticles, photonic-optoelectronic,
  dielectrics-piezoelectrics, semiconductors, polymers, metals,
  insulation, functional, sustainability-durability).
- `materials-writing` upgraded to 6-axis routing (added `material_family`
  and `domain` to existing `paper_type` / `section` / `language` /
  `journal_family`).
- `materials-data` 9 domain data schemas (asphalt, cement-concrete,
  ceramics, civil, functional, metals, nano, polymers, thermal-insulation).

## v2026.06.05-review-first — 2026-06-05 — Initial public release

### Added
- Initial tagged release of the civil-materials-skills Codex plugin bundle.
- 12 starter skills covering the full research pipeline: router,
  reader, citation, writing, polishing, figure, data, doe, reviewer,
  response, paper2ppt, pptx.
- Codex plugin packaging at `plugins/materials-skills/`.
- Manual install script `scripts/install.ps1`.
- Academic-search MCP server under
  `plugins/materials-skills/skills/materials-citation/mcp/`.
- Shared support directory `_shared/` and the 4 earliest core protocols
  (`terminology-ledger`, `stance`, `source-basis`, `ethics`).
- First journal-format guide set under `_shared/journal-formats/`.

[Unreleased]: https://github.com/cooleava1-gif/Materials-Science-Skills/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/cooleava1-gif/Materials-Science-Skills/compare/v2026.06.05-review-first...v1.1.0
[v2026.06.05-review-first]: https://github.com/cooleava1-gif/Materials-Science-Skills/releases/tag/v2026.06.05-review-first

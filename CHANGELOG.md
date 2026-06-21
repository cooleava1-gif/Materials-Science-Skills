# Changelog

All notable changes to **Materials Science Skills** are documented in this
file. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project follows [Semantic Versioning](https://semver.org/) loosely:
- `feat` commits raise the minor version
- `fix` commits raise the patch version
- breaking schema or manifest changes raise the major version

## [Unreleased]

### Documentation
- Sync root `README.md` and 6 key skill READMEs (`materials-research`,
  `materials-figure`, `materials-writing`, `materials-data`,
  `materials-reviewer`, `materials-paper-to-patent`) to actual code: 13
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

# materials-reader

**What it does** — The source-grounded reading engine for the bundle. Use it
when the raw material is a paper, PDF, abstract, figure caption, or pasted
source text and you need structured notes you can trust downstream. It
produces standard reader packages with bilingual notes, source anchors,
figure/table evidence maps, and claim-evidence-mechanism-boundary matrices,
plus handoff rows for the citation and figure skills. It detects the source
format (pdf-text, scanned-pdf, doi-arxiv, html, pasted-text) and the output
type (full notes, literature matrix, evidence-chain audit, figure-anchored
reading, journal-club reading, microstructure interpretation) and loads only
the matching fragments.

**Built from** — A source-grounded reading engine with 14 reference
protocols, schema-validated output packages, and reusable templates:

- `references/wer-ea-intensive-reading-package.md` — WER-EA intensive reading
  protocol (30-paper package, translation notes, mechanism-evidence table,
  dosage window, review handoff)
- `references/ceramics-intensive-reading-package.md` — ceramics intensive
  reading protocol
- `references/full-reader.md` — full bilingual notes protocol
- `references/fulltext-figure-anchored-reading.md` — figure/table-anchored
  full-text reading
- `references/evidence-chain-audit.md` — claim-evidence audit protocol
- `references/evidence-to-review-handoff.md` — citation/figure handoff
- `references/source-grounding.md` — source-anchor rules
- `references/standard-output-package.md` — package manifest and source map
- `references/pdf-reading.md`, `pdf-visual-asset-extraction.md`,
  `microstructure-interpretation.md`, `literature-matrix.md`,
  `journal-club-reading.md`, `table-system.md` — supporting protocols
- `assets/schemas/` — 4 JSON schemas (package manifest, source map, visual
  asset spec, visual asset report)
- `assets/templates/` — 15 templates (notes, handoffs, tables, QA)
- `scripts/` — build / audit / validate reader package, evidence-chain audit,
  PDF visual asset extraction, new-note scaffolding
- `tests/pressure-tests/overclaim-from-figure-caption.md` — overclaim
  regression

**Key rules enforced**

- Source-anchor every claim to page, paragraph, or figure; no floating
  assertions.
- Build claim-evidence-mechanism-boundary rows: what the paper claims, what
  evidence supports it, the proposed mechanism, and the claim boundary.
- Distinguish what the paper says from what you infer; flag overclaim in the
  confidence note.
- Never interpret microstructure or mechanism without explicit evidence.
- Keep source anchors stable so citation and figure handoffs stay traceable.

**Reference files**

```text
skills/materials-reader/
├── README.md
├── SKILL.md
├── manifest.yaml
├── scripts/
│   ├── build_reader_package.py          assembles reader package
│   ├── validate_reader_package.py       package contract validator
│   ├── audit_reader_package.py          package QA auditor
│   ├── build_evidence_chain_audit.py    evidence-chain audit builder
│   ├── extract_pdf_visual_assets.py     PDF visual asset extractor
│   └── new_reader_note.py               new-note scaffolding
├── assets/
│   ├── schemas/                         4 JSON schemas (manifest, source-map, visual-asset)
│   └── templates/                       15 templates (notes, handoffs, tables, QA)
├── static/
│   ├── core/                            contract, reader-contract, workflow
│   └── fragments/
│       ├── domain/                      6 material-domain routing fragments
│       └── source/                      5 source-format fragments
└── references/
    ├── wer-ea-intensive-reading-package.md    WER-EA intensive reading protocol
    ├── ceramics-intensive-reading-package.md  ceramics intensive reading protocol
    ├── full-reader.md                         full bilingual notes protocol
    ├── fulltext-figure-anchored-reading.md    figure/table-anchored reading
    ├── evidence-chain-audit.md                claim-evidence audit protocol
    ├── evidence-to-review-handoff.md          citation/figure handoff
    ├── source-grounding.md                    source-anchor rules
    ├── standard-output-package.md             package manifest and source map
    ├── pdf-reading.md                         PDF reading guidance
    ├── pdf-visual-asset-extraction.md         PDF visual asset extraction
    ├── microstructure-interpretation.md       SEM/AFM/TG microstructure reading
    ├── literature-matrix.md                   literature matrix protocol
    ├── journal-club-reading.md                journal-club reading protocol
    └── table-system.md                        table-system templates
```

**Validation**

- Contract tests live under
  `plugins/materials-skills/skills/materials-reader/tests/`
- Key checks: `test_reader_package_contract.py`,
  `test_reader_handoff.py`, `test_validate_reader_package.py`,
  `test_reader_package_scripts.py`, `test_reader_references.py`,
  `test_pdf_visual_assets.py`
- Pressure test:
  `plugins/materials-skills/skills/materials-reader/tests/pressure-tests/overclaim-from-figure-caption.md`
- Bundle verification:
  `python .\scripts\run_release_checks.py --json`

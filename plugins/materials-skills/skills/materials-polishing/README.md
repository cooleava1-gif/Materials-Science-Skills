# materials-polishing

**What it does** — The language and claim-strength control layer for materials
prose. It polishes rough English, rewrites Chinese source into academic
English, tightens journal tone, and audits overclaim risk for abstracts,
introductions, discussions, conclusions, highlights, and cover letters. Output
preserves facts, units, citations, and evidence strength, keeps
missing-evidence markers visible, and returns revision-safe wording that can
hand back to writing or response workflows.

**Built from** — A reference rulebook plus section, journal-family, language,
and domain fragments routed by the manifest axes:

- `references/claim-strength-ladder.md` — calibrates causal vs. associative
  wording and downgrade paths
- `references/hourglass-structure.md` — verifies section flow and paragraph
  order
- `references/language-rulebook.md` — SCI style and academic style rules
- `references/chinese-to-english-patterns.md` — zh-to-en rewriting patterns
- `references/` — 22 files total: section guides (abstract, introduction,
  results-discussion, conclusions, cover-letter), domain language guides
  (pavement, cement-concrete, polymers, ceramics, metals, insulation, nano,
  functional), plus style-guardrails, vocabulary-upgrade, citation-integrity,
  british-english, and proofreading
- `assets/templates/polishing-request-template.md` — request scaffolding
- `scripts/audit_sentences.py` — sentence-length and style auditing
- `static/fragments/` — language (en, zh-to-en), paper_type (research, review),
  and domain fragments

**Key rules enforced**

| Domain | Core rule |
|---|---|
| Sentence length | Keep sentences <=35 words; split long compound claims. |
| Hedging | Calibrate causal vs. associative language via the claim-strength ladder. |
| Section tense | Match tense to section (methods past, results past, discussion mixed). |
| Citation integrity | Preserve attribution and density; no silent citation drops. |
| Overclaim | Downgrade mechanism/performance claims to evidence level; flag risk. |
| British English | Apply journal-specific spelling and consistency checks. |

**Reference files**

```text
skills/materials-polishing/
├── README.md
├── SKILL.md
├── manifest.yaml
├── scripts/
│   └── audit_sentences.py              sentence-length and style audit
├── assets/templates/
│   └── polishing-request-template.md
├── references/
│   ├── claim-strength-ladder.md        causal vs. associative calibration
│   ├── hourglass-structure.md          section flow and paragraph order
│   ├── language-rulebook.md            SCI / academic style rules
│   ├── chinese-to-english-patterns.md  zh-to-en rewriting patterns
│   ├── style-guardrails.md             generic polishing guardrails
│   ├── vocabulary-upgrade.md           weak-word and verb calibration
│   ├── citation-integrity.md           attribution and density audit
│   ├── british-english.md              spelling and consistency
│   ├── proofreading.md                 final mechanical checks
│   ├── abstract.md                     section polishing guides
│   ├── introduction.md
│   ├── results-discussion.md
│   ├── conclusions.md
│   ├── cover-letter.md
│   ├── pavement-language.md            domain language guides
│   ├── cement-concrete-language.md
│   ├── ceramics-language.md
│   ├── polymers-language.md
│   ├── metals-language.md
│   ├── insulation-language.md
│   ├── nano-language.md
│   └── functional-language.md
└── static/fragments/
    ├── language/        en, zh-to-en
    ├── paper_type/      research, review
    └── domain/          civil, polymers, metals, ceramics, functional, nano
```

**Validation**

- Audit script:
  `plugins/materials-skills/skills/materials-polishing/scripts/audit_sentences.py`
- Bundle verification:
  `python .\scripts\run_release_checks.py --json`

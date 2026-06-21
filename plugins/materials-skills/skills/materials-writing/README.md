# materials-writing

**What it does** — Turns evidence and structure into manuscript prose for
materials science. It drafts review outlines, argument chains, and bounded
section text (abstracts, introductions, methods, results/discussion,
conclusions) from claims, results, reader-package artifacts, or Chinese source
drafts. Every claim stays anchored to evidence through a
claim-evidence-mechanism-boundary matrix, and missing evidence is kept explicit
so the output hands off cleanly to polishing, reviewer, or response loops
instead of hiding gaps.

**Built from** — A large narrative and section-pattern library plus phrase
banks routed by 6 axes simultaneously (paper type, section, language,
journal family, material family, domain):

**Six routing axes** — Drives the section template, phrase bank, and domain
narrative simultaneously:

| Axis | Examples |
|---|---|
| `paper_type` | experimental-manuscript / review-paper / methods-paper |
| `section` | abstract / introduction / methods / results-discussion / conclusion / full-argument |
| `language` | zh / en |
| `journal_family` | CBM / CCC / RMPD / JBE / nature-materials / acs-nano / … |
| `material_family` | civil / polymers / metals / ceramics / functional / nano |
| `domain` | WER-EA / asphalt / cement-concrete / refractories / bioceramics / … |

The two material axes (`material_family` and `domain`) are what make the
writing skill vertical for materials science: they route into the matching
domain narrative, the matching phrase bank, and the matching section-pattern
arc in a single pass.

- `references/` — 42 narrative and strategy references: 34 domain narrative
  guides (asphalt, cement/concrete, ceramics, polymers, metals, functional,
  nano, insulation, timber/masonry, WER-EA, refractories, bioceramics, etc.)
  plus argument-chain, review-paper-strategy, wer-ea-mini-review-pipeline,
  reviewer-risk-writing, published-article-patterns, and table-system
- `references/section-patterns/` — 5 section arcs: abstract claim arc,
  introduction gap ladder, results-discussion evidence chain, conclusion
  boundary, review synthesis patterns
- `references/phrase-banks/` — 10 domain phrase banks (WER-EA, thermal
  insulation, polymer composites, cement/concrete, ceramics, metals/alloys,
  durability/sustainability, civil-general, nano, functional)
- `assets/templates/` — manuscript-argument, section-draft, table-system, and
  WER-EA mini-review templates
- `scripts/` — `build_manuscript_outline.py` for outline scaffolding and
  `audit_materials_manuscript.py` for draft auditing
- `static/fragments/` — section, paper_type, journal_family, language,
  material_family, and domain fragments loaded by the manifest axes

**Key rules enforced**

| Domain | Core rule |
|---|---|
| Evidence first | Every claim maps to evidence; no overclaim, no speculation as fact. |
| Abstract | Background pain -> contribution -> result -> application boundary. |
| Introduction | Gap ladder from field progress to explicit evidence gap and novelty. |
| Method | Replicates, standards, units, and conditions stay explicit. |
| Results/Discussion | Observation -> mechanism evidence -> alternative-explanation exclusion. |
| Conclusion | State contribution, limitations, next steps, and overclaim boundary. |
| Chinese notes | zh-to-en drafting preserves facts and evidence strength, not literal wording. |

**Reference files**

```text
skills/materials-writing/
├── README.md
├── SKILL.md
├── manifest.yaml
├── scripts/
│   ├── build_manuscript_outline.py    outline scaffolding
│   └── audit_materials_manuscript.py  draft auditing
├── assets/templates/
│   ├── manuscript-argument-template.md
│   ├── section-draft-template.md
│   ├── table-system-template.md
│   └── wer-ea-mini-review-template.md
├── references/
│   ├── argument-chain.md              paper logic and contribution chain
│   ├── review-paper-strategy.md       mini-review / review strategy
│   ├── wer-ea-mini-review-pipeline.md WER-EA review pipeline
│   ├── reviewer-risk-writing.md       overclaim and missing-evidence risk
│   ├── published-article-patterns.md  sentence templates from real papers
│   ├── table-system.md                table system templates
│   ├── *-narrative.md                 34 domain narrative guides (asphalt,
│   │                                   cement, ceramics, polymers, metals,
│   │                                   functional, nano, insulation, WER-EA,
│   │                                   timber/masonry, refractories, ...)
│   ├── section-patterns/              5 section arcs (abstract, intro, R&D, conclusion, review)
│   └── phrase-banks/                  10 domain phrase banks
└── static/fragments/
    ├── section/        abstract, introduction, methods, results-discussion, conclusion
    ├── paper_type/     experimental-manuscript, review-paper, methods-paper
    └── domain/         civil, polymers, metals, ceramics, functional, nano
```

**Validation**

- Audit script:
  `plugins/materials-skills/skills/materials-writing/scripts/audit_materials_manuscript.py`
- Outline scaffolding:
  `plugins/materials-skills/skills/materials-writing/scripts/build_manuscript_outline.py`
- Unit test:
  `plugins/materials-skills/skills/materials-writing/tests/test_writing_skill.py`
- Bundle verification:
  `python .\scripts\run_release_checks.py --json`

## When To Use

Use `materials-writing` when the user request matches this skill's production surface and the needed inputs are available or can be explicitly marked as missing.

## Inputs

Typical inputs are the user prompt, material direction/profile, target journal or task mode when relevant, and any source text, data, figures, reviewer comments, or package artifacts needed by the skill.

## Outputs

Outputs are structured handoffs or artifacts described above in this README. Missing evidence, author input needs, and unsupported claims stay visible instead of being hidden in fluent prose.

## Example

```text
Draft a bounded results/discussion argument chain from evidence rows.
```

## Validation

Run the skill-specific scripts or tests listed above when they apply, then run the bundle gate from the repository root:

```powershell
python .\scripts\run_release_checks.py --json
```

## Boundaries

This skill does not invent experiments, citations, measurements, journal facts, private file paths, or completed actions. Time-sensitive journal or legal facts should be checked against official sources before submission or filing.

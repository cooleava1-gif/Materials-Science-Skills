# materials-reviewer

**What it does** — Simulates 2-3 independent peer reviewers plus a
cross-review synthesis before you submit or resubmit. It pressure-tests
novelty and evidence sufficiency, flags figure and statistics gaps, audits
journal fit, and produces reviewer-style reports with a desk-reject risk
reading. Feed it an abstract, a section draft, a full manuscript, or a figure
package; name a target journal when fit matters; and call out weak spots you
want prioritized. It is the bundle's main pre-submission and
pre-resubmission risk screen.

**Built from** — A review-criteria system organized along five axes
(originality, importance, interdisciplinary scope, technical validity,
readability), plus scope and domain routing:

- `references/review-axes.md` — standard-depth review axes and scoring
- `references/report-structure.md` — detailed referee report skeleton
- `references/qa-checklist.md` — quick-scan / desk-reject precheck
- `references/editorial-criteria.md` — CBM / CCC / RMPD / JBE editorial fit
- `references/mechanism-evidence-checklist.md` — FTIR / SEM / XRD / TG evidence
- 22 domain-specific `*-reviewer-criteria.md` files — asphalt, cement,
  ceramics, metals, polymers, functional, nano, insulation, steel,
  civil-generic, construction-materials, geotechnical, timber-masonry,
  waterproofing-sealants, sustainability-durability, semiconductors,
  dielectrics-piezoelectrics, photonic-optoelectronic, nanoparticles,
  nano-thin-films, nanocomposites, 2d-materials
- `static/fragments/review_scope/` — full-manuscript, figures-tables,
  methodology scope fragments
- `static/fragments/domain/` — 6 material-domain routing fragments
- `assets/templates/review-report-template.md` — report scaffold
- `scripts/build_review_report.py` — assembles the reviewer-style report
- `tests/pressure-tests/weak-manuscript-review.md` — weak-manuscript regression

**Key rules enforced**

- Never invent reviewer identities, experiments, citations, or data to
  support a critique.
- Mark unresolved items `AUTHOR_INPUT_NEEDED` instead of papering over them.
- Separate technical validity from broad-interest judgment; a method can be
  sound yet still out of scope.
- Distinguish certain claims from speculative ones and flag overclaim
  specifically.
- Simulated review is not a real editor or journal; time-sensitive journal
  facts still need a live check on official pages.

**What it returns** — A reviewer-style report with major and minor concerns,
a risk prioritization that can be routed into fixes, weakness-routing
guidance for companion skills (reader, citation, writing, figure, data), and
a desk-reject risk reading for revision planning or final gating.

**Reference files**

```text
skills/materials-reviewer/
├── README.md
├── SKILL.md
├── manifest.yaml
├── scripts/
│   └── build_review_report.py          assembles reviewer-style report
├── assets/
│   └── templates/
│       └── review-report-template.md   report scaffold
├── static/
│   ├── core/                           contract, reviewer-stance, workflow
│   └── fragments/
│       ├── domain/                     6 material-domain routing fragments
│       └── review_scope/               full-manuscript, figures-tables, methodology
└── references/
    ├── review-axes.md                  standard review axes and scoring
    ├── report-structure.md             detailed referee report skeleton
    ├── qa-checklist.md                 quick-scan / desk-reject precheck
    ├── editorial-criteria.md           CBM/CCC/RMPD/JBE editorial fit
    ├── mechanism-evidence-checklist.md FTIR/SEM/XRD/TG mechanism evidence
    ├── asphalt-reviewer-criteria.md    asphalt emulsion domain criteria
    ├── cement-reviewer-criteria.md     cement/concrete domain criteria
    ├── ceramics-reviewer-criteria.md   ceramics domain criteria
    ├── metals-reviewer-criteria.md     metals domain criteria
    ├── polymers-reviewer-criteria.md   polymers domain criteria
    ├── functional-reviewer-criteria.md functional materials criteria
    ├── nano-reviewer-criteria.md       nanomaterials domain criteria
    ├── insulation-reviewer-criteria.md thermal insulation criteria
    ├── steel-reviewer-criteria.md      steel domain criteria
    ├── civil-generic-reviewer-criteria.md          civil generic criteria
    ├── construction-materials-reviewer-criteria.md construction materials criteria
    ├── geotechnical-reviewer-criteria.md           geotechnical criteria
    ├── timber-masonry-reviewer-criteria.md         timber/masonry criteria
    ├── waterproofing-sealants-reviewer-criteria.md waterproofing criteria
    ├── sustainability-durability-reviewer-criteria.md sustainability criteria
    ├── semiconductors-reviewer-criteria.md         semiconductor criteria
    ├── dielectrics-piezoelectrics-reviewer-criteria.md dielectric/piezoelectric criteria
    ├── photonic-optoelectronic-reviewer-criteria.md    photonic/optoelectronic criteria
    ├── nanoparticles-reviewer-criteria.md          nanoparticle criteria
    ├── nano-thin-films-reviewer-criteria.md        nano thin-film criteria
    ├── nanocomposites-reviewer-criteria.md         nanocomposite criteria
    └── 2d-materials-reviewer-criteria.md           2D material criteria
```

**Validation**

- Core regression test:
  `plugins/materials-skills/skills/materials-reviewer/tests/test_reviewer_skill.py`
- Pressure test:
  `plugins/materials-skills/skills/materials-reviewer/tests/pressure-tests/weak-manuscript-review.md`
- Bundle verification:
  `python .\scripts\run_release_checks.py --json`

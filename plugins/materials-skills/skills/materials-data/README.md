# materials-data

**What it does** — Packages the material behind a manuscript into a cleaner,
FAIR-aware submission surface. It organizes raw and processed datasets, writes
metadata and file-organization plans, drafts data availability statements,
runs FAIR audits, and scaffolds supplementary data packages for WER-EA,
asphalt, cement/concrete, durability, and journal submission workflows.
Missing measurements and missing metadata are flagged explicitly rather than
papered over.

**Built from** — FAIR and dataset-package references, domain data schemas, and
templates routed by task, domain, and journal:

**Nine domain data schemas** — One per material sub-direction, covering the
canonical CSV column order, FAIR metadata fields, and journal-adapted
data-availability statement template:

- `asphalt` — mix design, modifier dosage, performance window
- `cement-concrete` — mix proportions, hydration, durability
- `ceramics` — sintering, mechanical, Weibull reliability
- `civil` — generic civil-engineering measurement
- `functional` — sensors, energy storage, smart materials
- `metals` — composition, heat-treatment, mechanical response
- `nano` — nanoparticle size, surface area, dispersion
- `polymers` — formulation, processing, mechanical/thermal
- `thermal-insulation` — thermal conductivity, density, fire resistance

- `references/fair-checklist.md` — lightweight FAIR audit checklist
- `references/dataset-package.md` — dataset package and experiment template
  rules
- `references/data-availability-statements.md` — journal-specific availability
  statements
- `references/` — 13 files total: 9 domain data schemas (asphalt,
  cement-concrete, ceramics, civil, functional, metals, nano, polymers,
  thermal-insulation) plus fair-checklist, dataset-package,
  data-availability-statements, and table-system
- `assets/templates/` — 8 templates: experiment-data-template (generic,
  ceramics, insulation), metadata, dataset-readme, data-availability,
  fair-audit, and table-system
- `scripts/` — `build_fair_package.py` for scaffolding and
  `audit_fair_dataset.py` for FAIR audits
- `static/fragments/` — data_task (availability-statement, fair-check,
  repository-plan) and domain fragments

**Key rules enforced**

- Separate raw data, processed data, and figures.
- Keep units, test standards, sample IDs, mixture IDs, and replicate counts
  explicit in metadata and CSV headers.
- Never invent measurements, replicate counts, standards, accession numbers,
  licences, or access restrictions.
- Missing data or missing metadata must be flagged explicitly for later repair.
- Data availability statements must not claim public availability unless files
  are present or a repository link is supplied.

**Useful CLI options**

Scaffold a FAIR dataset package:

```powershell
python plugins/materials-skills/skills/materials-data/scripts/build_fair_package.py `
  --topic "waterborne epoxy modified emulsified asphalt" `
  --domain asphalt `
  --journal CBM `
  --output-dir outputs/data-packages
```

Audit an existing dataset against the FAIR checklist:

```powershell
python plugins/materials-skills/skills/materials-data/scripts/audit_fair_dataset.py `
  --dataset-dir outputs/data-packages/my_dataset `
  --json
```

**Reference files**

```text
skills/materials-data/
├── README.md
├── SKILL.md
├── manifest.yaml
├── scripts/
│   ├── build_fair_package.py    scaffold a FAIR dataset package
│   └── audit_fair_dataset.py    FAIR audit (Markdown or JSON)
├── assets/templates/
│   ├── experiment-data-template.csv             generic experiment CSV
│   ├── experiment-data-template-ceramics.csv    ceramics experiment CSV
│   ├── experiment-data-template-insulation.csv  insulation experiment CSV
│   ├── metadata-template.md
│   ├── dataset-readme-template.md
│   ├── data-availability-template.md
│   ├── fair-audit-template.md
│   └── table-system-template.md
├── references/
│   ├── fair-checklist.md                FAIR audit checklist
│   ├── dataset-package.md               package and experiment template rules
│   ├── data-availability-statements.md  journal-specific statements
│   ├── table-system.md                  table system templates
│   ├── asphalt-data-schema.md           domain data schemas
│   ├── cement-concrete-data-schema.md
│   ├── ceramics-data-schema.md
│   ├── civil-data-schema.md
│   ├── functional-data-schema.md
│   ├── metals-data-schema.md
│   ├── nano-data-schema.md
│   ├── polymers-data-schema.md
│   └── thermal-insulation-data-schema.md
└── static/fragments/
    ├── data_task/   availability-statement, fair-check, repository-plan
    └── domain/      asphalt, cement-concrete, materials, ceramics,
                      thermal-insulation, polymers, metals, nano, functional
```

**Validation**

- Audit script:
  `plugins/materials-skills/skills/materials-data/scripts/audit_fair_dataset.py`
- Bundle verification:
  `python .\scripts\run_release_checks.py --json`

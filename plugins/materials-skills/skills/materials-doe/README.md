# materials-doe

**What it does** — Design-of-experiments planning and matrix generation for
civil engineering and construction materials research. Supports classical
factorial, Taguchi orthogonal array, and mixture/simplex designs with factor
screening and response surface extensions. Use it when the user needs an
experimental matrix, factor screening plan, orthogonal array, mixture design,
response surface plan, or guidance on sample size and replication for materials
testing. The skill plans experiments and emits structured matrices; it does not
execute tests, analyze collected data, or produce manuscript text.

**Built from** — Three design-mode cores plus a domain experiment library:

- `static/core/classical-doe.md` — full/fractional factorial, OFAT, sample size,
  replication, randomization, RSM and central composite design
- `static/core/orthogonal-tables.md` — Taguchi L9/L16/L25 arrays, S/N ratio,
  range and ANOVA analysis guidance
- `static/core/mix-design-guide.md` — mixture/simplex, D-optimal, component
  bounds and constraints for multi-component systems
- `static/reference/` — 8 domain experiment references (asphalt,
  cement-concrete, polymers, metals, ceramics, functional, nano, insulation)
  plus a factor-level template and DOE figure-package routing
- `scripts/` — 3 helpers: `orthogonal_analysis.py`, `mix_design_calc.py`,
  `experiment_plot.py`
- `assets/templates/` — analysis script, experiment plan CSV, and methods
  paragraph templates

**Supported design types** — Full factorial, fractional factorial, OFAT,
Taguchi orthogonal array (L9/L16/L25), signal-to-noise ratio analysis,
mixture/simplex design, D-optimal mixture, response surface methodology (RSM),
central composite design (CCD), factor screening (Plackett-Burman).

**Outputs** — Factor-level matrices, analysis strategy notes, and a structured
handoff for downstream skills:

| Output | Description |
|---|---|
| Test matrix | Factor-level table in CSV or markdown |
| Analysis strategy | Notes on ANOVA, S/N ratio, or RSM approach |
| DOE handoff | Structured handoff for downstream skills |

**Usage examples** — Typical requests the skill handles:

- "Design an L9 orthogonal array for asphalt modifier dosage, curing time, and temperature"
- "Generate a mix design matrix for three-component mortar system"
- "Plan a factorial experiment for concrete durability factors"

**Key rules enforced**

- Plans experiments and generates matrices only; never executes tests or
  analyzes collected data.
- Factor list and level count must be confirmed before generating any matrix
  (blocking gate).
- Design mode (classical, orthogonal, mix-design) must be resolved before
  loading mode-specific references.
- Claims about optimality or statistical power must be backed by the chosen
  design's properties.
- For data analysis or figure production, hand off to `materials-data` or
  `materials-figure` instead of doing it here.

**Reference files**

```text
skills/materials-doe/
├── README.md
├── SKILL.md
├── manifest.yaml
├── scripts/
│   ├── orthogonal_analysis.py    Taguchi S/N ratio and range analysis
│   ├── mix_design_calc.py        mixture/simplex matrix calculator
│   └── experiment_plot.py        DOE matrix and response plotting
├── assets/
│   └── templates/
│       ├── analysis-script-template.py   ANOVA/regression analysis scaffold
│       ├── experiment-plan-template.csv  factor-level matrix template
│       └── methods-paragraph-template.md methods section paragraph template
└── static/
    ├── core/
    │   ├── classical-doe.md       factorial, OFAT, sample size, RSM/CCD
    │   ├── orthogonal-tables.md   Taguchi arrays and S/N analysis
    │   ├── mix-design-guide.md    mixture/simplex/D-optimal guidance
    │   ├── contract.md            evidence contract
    │   ├── stance.md              skill stance
    │   └── workflow.md            planning workflow
    └── reference/
        ├── asphalt-experiments.md       asphalt/binder experiment factors
        ├── cement-experiments.md         cement/concrete/mortar factors
        ├── polymers-experiments.md       polymer/composite factors
        ├── metals-experiments.md         metal/alloy factors
        ├── ceramics-experiments.md       ceramic sintering factors
        ├── functional-experiments.md     functional/dielectric factors
        ├── nano-experiments.md           nanoparticle/2D material factors
        ├── insulation-experiments.md     insulation material factors
        ├── factor-level-template.md      factor-level matrix template
        └── doe-figure-package.md         DOE figure-package routing
```

**Validation**

- Bundle verification: `python .\scripts\run_release_checks.py --json`
- Architecture check: `python .\scripts\check_skill_architecture.py --json`

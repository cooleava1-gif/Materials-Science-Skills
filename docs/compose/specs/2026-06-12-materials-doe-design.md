# materials-doe Skill Design Spec

## [S1] Problem

The materials-skills bundle covers the full paper lifecycle but lacks a dedicated experiment design skill. Researchers must manually construct orthogonal arrays, calculate mix proportions, and write experiment plans outside the skill system. This creates gaps in the pipeline between research planning and manuscript drafting.

## [S2] Solution Overview

Add a `materials-doe` skill that handles three experiment design modes: Classical (single/multi-factor), Orthogonal (L9/L16/L25 arrays with range/ANOVA analysis), and Mix Design (proportion optimization). The skill produces five output types that hand off to existing skills.

## [S3] Design Modes

| Mode | Use Case | Methods |
|------|----------|---------|
| Classical | Initial exploration, single-factor | Control variable, one-factor-at-a-time |
| Orthogonal | Multi-factor screening | L9/L16/L25 arrays, range analysis, ANOVA |
| Mix Design | Material proportion optimization | Dense packing, volume method, empirical formulas |

## [S4] Output Products

| Product | Format | Receiving Skill |
|---------|--------|-----------------|
| Experiment plan | CSV + Markdown | Direct use |
| Analysis scripts | Python (pandas + scipy + matplotlib) | Direct execution |
| Methods paragraph | Markdown | → materials-writing |
| Experiment figures | Python scripts | → materials-figure |
| Data templates | CSV (pre-filled with IDs and factor combos) | → materials-data |

## [S5] Skill Structure

```
skills/materials-doe/
├── SKILL.md
├── manifest.yaml
├── README.md
├── static/
│   ├── core/
│   │   ├── orthogonal-tables.md
│   │   ├── mix-design-guide.md
│   │   └── classical-doe.md
│   └── reference/
│       ├── factor-level-template.md
│       └── anova-template.md
├── scripts/
│   ├── orthogonal_analysis.py
│   ├── mix_design_calc.py
│   └── experiment_plot.py
├── templates/
│   ├── experiment-plan.csv
│   ├── data-template.csv
│   └── methods-paragraph.md
└── tests/
    ├── test_doe_skill.py
    ├── test_orthogonal.py
    └── test_mix_design.py
```

## [S6] Integration Points

- **materials-research**: Add `experiment-design` task type to routing table
- **materials-writing**: Receive methods paragraph handoff
- **materials-figure**: Receive experiment figure handoff
- **materials-data**: Receive data template handoff
- **_shared/contracts/**: New `doe-handoff.yaml` defining output fields

## [S7] Core Functionality

### Orthogonal Design
- Input: number of factors, levels, optimization goal (larger-is-better/smaller-is-better/target)
- Output: orthogonal array arrangement, experiment IDs, blank column assignment
- Analysis: range analysis, ANOVA, optimal combination prediction

### Mix Design
- Input: material type, performance targets, constraints
- Output: proportion plan, dosage range, recommended content
- Methods: dense packing, volume method, empirical formulas

### Classical Design
- Input: factor list, response variables
- Output: experiment matrix, control variable description
- Use: initial exploration, one-factor-at-a-time

## [S8] Handoff Contract Fields

```yaml
doe-handoff:
  experiment_plan: string  # path to experiment plan CSV
  design_mode: string      # classical | orthogonal | mix_design
  factors: array           # list of factors with levels
  analysis_script: string  # path to analysis Python script
  methods_paragraph: string # ready-to-paste methods text
  figure_script: string    # path to figure generation script
  data_template: string    # path to data recording template
  optimal_combination: object # predicted optimal factor levels
```

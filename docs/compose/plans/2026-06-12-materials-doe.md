# materials-doe Skill Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use compose:subagent (recommended) or compose:execute to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a `materials-doe` skill that handles experiment design (Classical, Orthogonal, Mix Design) with full pipeline integration.

**Architecture:** New skill module under `skills/materials-doe/` following existing patterns: manifest.yaml for routing, SKILL.md for protocol, static/ for reference docs, scripts/ for analysis tools, templates/ for output formats, tests/ for validation. Integrates via handoff contracts to writing/figure/data skills.

**Tech Stack:** Python 3.11+, pandas, scipy, matplotlib, numpy, unittest

---

### Task 1: Create skill directory structure and manifest.yaml

**Covers:** S3, S5

**Files:**
- Create: `skills/materials-doe/manifest.yaml`
- Create: `skills/materials-doe/SKILL.md`
- Create: `skills/materials-doe/README.md`
- Create: `skills/materials-doe/static/core/`
- Create: `skills/materials-doe/static/reference/`
- Create: `skills/materials-doe/scripts/`
- Create: `skills/materials-doe/templates/`
- Create: `skills/materials-doe/tests/`

- [ ] **Step 1: Create directory structure**

```powershell
New-Item -ItemType Directory -Force -Path @(
    "skills/materials-doe/static/core",
    "skills/materials-doe/static/reference",
    "skills/materials-doe/scripts",
    "skills/materials-doe/templates",
    "skills/materials-doe/tests"
)
```

- [ ] **Step 2: Write manifest.yaml**

```yaml
version: "1.0.0"

always_load:
  - static/core/contract.md
  - static/core/stance.md
  - ../_shared/core/stance.md

axes:
  design_mode:
    default: classical
    detect: "What experiment design method does the user need?"
    values:
      classical:
        path: static/core/classical-doe.md
        triggers: ["single factor", "one factor", "control variable", "单因素", "控制变量", "经典实验"]
      orthogonal:
        path: static/core/orthogonal-tables.md
        triggers: ["orthogonal", "L9", "L16", "L25", "正交", "正交表", "正交实验", "极差分析"]
      mix-design:
        path: static/core/mix-design-guide.md
        triggers: ["mix design", "proportion", "dosage", "配比", "掺量", "配合比", "最密堆积"]

  domain:
    default: materials
    detect: "Which materials field is the experiment for?"
    values:
      asphalt:
        path: static/reference/asphalt-experiments.md
        triggers: ["asphalt", "emulsified asphalt", "waterborne epoxy", "沥青", "乳化沥青"]
      cement-concrete:
        path: static/reference/cement-experiments.md
        triggers: ["cement", "concrete", "mortar", "水泥", "混凝土", "砂浆"]
      materials:
        path: static/reference/general-experiments.md
        triggers: ["materials", "construction materials", "建筑材料", "土木材料"]
      ceramics:
        path: static/reference/ceramics-experiments.md
        triggers: ["ceramic", "sintering", "陶瓷", "烧结"]
      thermal-insulation:
        path: static/reference/insulation-experiments.md
        triggers: ["insulation", "thermal conductivity", "隔热", "保温"]

  output:
    default: plan
    detect: "What experiment design output does the user need?"
    values:
      plan:
        path: templates/experiment-plan.csv
        triggers: ["plan", "matrix", "experiment table", "方案", "实验表", "实验方案"]
      analysis:
        path: scripts/orthogonal_analysis.py
        triggers: ["analysis", "ANOVA", "range analysis", "分析", "方差分析", "极差分析"]
      methods:
        path: templates/methods-paragraph.md
        triggers: ["methods", "paragraph", "方法", "方法段落"]
      figures:
        path: scripts/experiment_plot.py
        triggers: ["figure", "plot", "chart", "图", "图表"]
      data-template:
        path: templates/data-template.csv
        triggers: ["data template", "CSV", "数据模板", "记录表"]

references:
  on_demand:
    orthogonal-guide:
      path: static/core/orthogonal-tables.md
      when: "The task involves orthogonal arrays, L9/L16/L25, range analysis, or ANOVA."
    mix-design-guide:
      path: static/core/mix-design-guide.md
      when: "The task involves material proportions, dosage optimization, or mix design."
    classical-guide:
      path: static/core/classical-doe.md
      when: "The task involves single-factor, multi-factor, or control-variable experiments."
    statistical-methods:
      path: ../materials-research/references/statistical-methods.md
      when: "The task involves significance testing, ANOVA details, or sample size decisions."
    factor-level-template:
      path: static/reference/factor-level-template.md
      when: "The user needs to define factors and levels for an experiment."

assets: []
scripts:
  - scripts
tests:
  - tests
quality_gates:
  - release gate must report no issues for this skill
  - claims must stay inside the skill evidence contract
handoffs:
  provides:
    doe-handoff:
      description: "Experiment design plan with analysis scripts and templates"
      contract: ../../_shared/contracts/doe-handoff.yaml
      version: "1.0"
  consumes: []
release_checks:
  - scripts/run_release_checks.py --json
  - scripts/check_skill_architecture.py --json
```

- [ ] **Step 3: Write SKILL.md**

```markdown
---
name: materials-doe
version: "1.0.0"
description: Use when designing experiments, planning test matrices, optimizing material proportions, or setting up orthogonal/Classical/mix-design experiments for civil engineering and construction materials research.
---

# Materials Experiment Design

Design defensible experiment matrices for civil materials research.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect `design_mode`, `domain`, and `output` from the user request.
3. Load only the matching fragments.
4. Produce the requested output: experiment plan, analysis script, methods paragraph, figure script, or data template.
5. Hand off to companion skills when requested.

## Design Modes

- **Classical**: Single-factor or multi-factor with control variables. Best for initial exploration.
- **Orthogonal**: L9/L16/L25 arrays with range analysis and ANOVA. Best for multi-factor screening.
- **Mix Design**: Material proportion optimization via dense packing, volume method, or empirical formulas.

## Gates

- Every experiment plan must include a blank/control group.
- Orthogonal designs must specify the blank column assignment for error estimation.
- Mix designs must state the constraint (volume, strength, workability) and the optimization target.
- Do not claim optimal results before running the experiment.
```

- [ ] **Step 4: Write README.md**

```markdown
# materials-doe

Experiment design skill for civil engineering and construction materials research.

## What It Does

- **Classical Design**: Single-factor and multi-factor experiments with control variables
- **Orthogonal Design**: L9/L16/L25 arrays with range analysis and ANOVA
- **Mix Design**: Material proportion optimization (dense packing, volume method, empirical formulas)

## Outputs

| Output | Format | Description |
|--------|--------|-------------|
| Experiment plan | CSV + Markdown | Factor-level table and experiment matrix |
| Analysis script | Python | Range analysis, ANOVA, optimal combination prediction |
| Methods paragraph | Markdown | Ready-to-paste Methods section text |
| Experiment figures | Python | Factor-response plots, dosage-performance curves |
| Data template | CSV | Pre-filled with experiment IDs and factor combinations |

## Usage

Start with `materials-research` for routing, or invoke directly:

- `Design an L16 orthogonal experiment for 4 factors at 4 levels`
- `Optimize the mix proportion for waterborne epoxy modified emulsified asphalt`
- `Plan a single-factor experiment for curing temperature`
```

- [ ] **Step 5: Verify directories exist**

```powershell
ls skills/materials-doe/
```

Expected: `manifest.yaml`, `SKILL.md`, `README.md`, `static/`, `scripts/`, `templates/`, `tests/`

- [ ] **Step 6: Commit**

```powershell
git add skills/materials-doe/manifest.yaml skills/materials-doe/SKILL.md skills/materials-doe/README.md
git commit -m "feat(doe): scaffold materials-doe skill with manifest, SKILL.md, README"
```

---

### Task 2: Create core reference files

**Covers:** S3, S7

**Files:**
- Create: `skills/materials-doe/static/core/contract.md`
- Create: `skills/materials-doe/static/core/stance.md`
- Create: `skills/materials-doe/static/core/orthogonal-tables.md`
- Create: `skills/materials-doe/static/core/classical-doe.md`
- Create: `skills/materials-doe/static/core/mix-design-guide.md`

- [ ] **Step 1: Write contract.md**

```markdown
# materials-doe Contract

## Output Handoff

The skill produces a `doe-handoff` with these fields:

| Field | Type | Description |
|-------|------|-------------|
| experiment_plan | string | Path to experiment plan CSV |
| design_mode | string | classical / orthogonal / mix_design |
| factors | array | List of factors with levels |
| analysis_script | string | Path to analysis Python script |
| methods_paragraph | string | Ready-to-paste Methods text |
| figure_script | string | Path to figure generation script |
| data_template | string | Path to data recording template |
| optimal_combination | object | Predicted optimal factor levels |

## Quality Gates

- Every plan includes a control/blank group.
- Orthogonal designs specify blank column assignment.
- Mix designs state constraints and optimization targets.
- No claims about optimal results before experiments run.
```

- [ ] **Step 2: Write stance.md**

```markdown
# materials-doe Stance

- Experiment design is planning, not execution. Do not claim results.
- Every experiment needs a control group or blank.
- Orthogonal arrays are efficient but assume no interaction effects; flag this limitation.
- Mix design methods are domain-specific; do not generalize across material types.
- Statistical power matters: recommend replicates based on expected variability.
```

- [ ] **Step 3: Write orthogonal-tables.md**

```markdown
# Orthogonal Experiment Design

## Standard Orthogonal Arrays

### L9 (3^4) — 4 factors, 3 levels each, 9 experiments

| Exp | A | B | C | D |
|-----|---|---|---|---|
| 1   | 1 | 1 | 1 | 1 |
| 2   | 1 | 2 | 2 | 2 |
| 3   | 1 | 3 | 3 | 3 |
| 4   | 2 | 1 | 2 | 3 |
| 5   | 2 | 2 | 3 | 1 |
| 6   | 2 | 3 | 1 | 2 |
| 7   | 3 | 1 | 3 | 2 |
| 8   | 3 | 2 | 1 | 3 |
| 9   | 3 | 3 | 2 | 1 |

### L16 (4^5) — 5 factors, 4 levels each, 16 experiments

| Exp | A | B | C | D | E |
|-----|---|---|---|---|---|
| 1   | 1 | 1 | 1 | 1 | 1 |
| 2   | 1 | 2 | 2 | 2 | 2 |
| 3   | 1 | 3 | 3 | 3 | 3 |
| 4   | 1 | 4 | 4 | 4 | 4 |
| 5   | 2 | 1 | 2 | 3 | 4 |
| 6   | 2 | 2 | 1 | 4 | 3 |
| 7   | 2 | 3 | 4 | 1 | 2 |
| 8   | 2 | 4 | 3 | 2 | 1 |
| 9   | 3 | 1 | 3 | 4 | 2 |
| 10  | 3 | 2 | 4 | 3 | 1 |
| 11  | 3 | 3 | 1 | 2 | 4 |
| 12  | 3 | 4 | 2 | 1 | 3 |
| 13  | 4 | 1 | 4 | 2 | 3 |
| 14  | 4 | 2 | 3 | 1 | 4 |
| 15  | 4 | 3 | 2 | 4 | 1 |
| 16  | 4 | 4 | 1 | 3 | 2 |

### L25 (5^6) — 6 factors, 5 levels each, 25 experiments

| Exp | A | B | C | D | E | F |
|-----|---|---|---|---|---|---|
| 1   | 1 | 1 | 1 | 1 | 1 | 1 |
| 2   | 1 | 2 | 2 | 2 | 2 | 2 |
| 3   | 1 | 3 | 3 | 3 | 3 | 3 |
| 4   | 1 | 4 | 4 | 4 | 4 | 4 |
| 5   | 1 | 5 | 5 | 5 | 5 | 5 |
| 6   | 2 | 1 | 2 | 3 | 4 | 5 |
| 7   | 2 | 2 | 3 | 4 | 5 | 1 |
| 8   | 2 | 3 | 4 | 5 | 1 | 2 |
| 9   | 2 | 4 | 5 | 1 | 2 | 3 |
| 10  | 2 | 5 | 1 | 2 | 3 | 4 |
| 11  | 3 | 1 | 3 | 5 | 2 | 4 |
| 12  | 3 | 2 | 4 | 1 | 3 | 5 |
| 13  | 3 | 3 | 5 | 2 | 4 | 1 |
| 14  | 3 | 4 | 1 | 3 | 5 | 2 |
| 15  | 3 | 5 | 2 | 4 | 1 | 3 |
| 16  | 4 | 1 | 4 | 2 | 5 | 3 |
| 17  | 4 | 2 | 5 | 3 | 1 | 4 |
| 18  | 4 | 3 | 1 | 4 | 2 | 5 |
| 19  | 4 | 4 | 2 | 5 | 3 | 1 |
| 20  | 4 | 5 | 3 | 1 | 4 | 2 |
| 21  | 5 | 1 | 5 | 4 | 3 | 2 |
| 22  | 5 | 2 | 1 | 5 | 4 | 3 |
| 23  | 5 | 3 | 2 | 1 | 5 | 4 |
| 24  | 5 | 4 | 3 | 2 | 1 | 5 |
| 25  | 5 | 5 | 4 | 3 | 2 | 1 |

## Range Analysis (极差分析)

For each factor, compute the average response at each level:

```
K_i = sum of responses where factor = level i
k_i = K_i / (number of experiments at level i)
R = max(k_i) - min(k_i)
```

The factor with the largest R is the most influential.

## ANOVA (方差 Analysis)

| Source | SS | df | MS | F |
|--------|----|----|----|---|
| Factor A | SS_A | a-1 | MS_A = SS_A/(a-1) | MS_A/MS_e |
| Factor B | SS_B | b-1 | MS_B = SS_B/(b-1) | MS_B/MS_e |
| Error | SS_e | df_e | MS_e = SS_e/df_e | — |
| Total | SS_T | N-1 | — | — |

Where:
- SS_A = sum of (k_i - grand_mean)^2 * n_i
- SS_T = sum of (y_i - grand_mean)^2
- SS_e = SS_T - sum of all factor SS
- F_critical from F-distribution table at alpha = 0.05

## Optimal Combination Prediction

```
y_opt = grand_mean + sum of (best_level_mean_i - grand_mean) for each factor
```

Flag: this is a prediction, not a measured result. Verify with confirmation experiments.
```

- [ ] **Step 4: Write classical-doe.md**

```markdown
# Classical Experiment Design

## Single-Factor Design

Vary one factor while holding all others constant.

### Procedure
1. Identify the factor to study (e.g., curing temperature).
2. Choose levels that span the practical range (e.g., 20, 40, 60, 80 °C).
3. Hold all other factors constant (curing time, humidity, specimen size).
4. Prepare replicate specimens at each level (minimum n=3).
5. Measure the response variable(s).
6. Analyze: plot response vs. factor level, identify trends.

### Output
- Factor-level table with constants specified.
- Replicate plan (n per level).
- Response variables and measurement methods.

## Multi-Factor Design (One-Factor-at-a-Time)

### Procedure
1. Start with a baseline condition (all factors at center or reference level).
2. Vary Factor A through its levels, hold others constant.
3. Select the best level of Factor A.
4. Vary Factor B, hold A at its best and others constant.
5. Repeat for all factors.

### Limitation
- Cannot detect interaction effects.
- May miss the true optimum if factors interact.
- Use orthogonal design when interactions are suspected.

## When to Use Classical vs. Orthogonal

| Scenario | Classical | Orthogonal |
|----------|-----------|------------|
| Initial exploration (1-2 factors) | Yes | No |
| 3+ factors, screening | No | Yes |
| Interaction effects suspected | No | Yes (with interaction columns) |
| Limited resources | Yes | Yes (fewer experiments) |
| Regulatory/compliance testing | Yes | Sometimes |
```

- [ ] **Step 5: Write mix-design-guide.md**

```markdown
# Mix Design Guide

## Dense Packing Method (最密堆积法)

Used for: concrete, mortar, asphalt mixtures.

### Procedure
1. Determine the packing density of each component (cement, aggregate, filler).
2. Use the Furnas or Aim-Goff model to calculate optimal proportions.
3. Adjust for workability (add water, superplasticizer, or emulsifier).
4. Verify with trial batches.

### Key Formula
```
phi_total = 1 - (1 - phi_1)(1 - phi_2)...(1 - phi_n)
```

Where phi_i is the packing density of component i.

## Volume Method (体积法)

Used for: concrete mix design (ACI 211.1, JGJ 55).

### Procedure
1. Determine required strength and workability.
2. Calculate water content from workability requirements.
3. Calculate cement content from water-cement ratio.
4. Calculate aggregate volumes to fill the remaining volume.
5. Adjust for air content.

## Empirical Formula Method (经验公式法)

Used for: asphalt emulsion mixes, polymer-modified systems.

### Procedure
1. Start from a known reference mix.
2. Apply empirical corrections for:
   - Material source differences
   - Environmental conditions
   - Performance requirements
3. Validate with bench-scale tests.

## Mix Design Output Template

| Component | Proportion (wt%) | Proportion (vol%) | Role |
|-----------|------------------|-------------------|------|
| Binder | — | — | Binding matrix |
| Filler | — | — | Void filling |
| Aggregate | — | — | Skeleton |
| Additive | — | — | Performance modifier |
| Water/Medium | — | — | Workability |

## Constraints to Specify

- Minimum strength requirement
- Maximum water/binder ratio
- Workability range (slump, flow, viscosity)
- Durability requirements (freeze-thaw, sulfate resistance)
- Cost budget (if applicable)
```

- [ ] **Step 6: Commit**

```powershell
git add skills/materials-doe/static/
git commit -m "feat(doe): add core reference files for orthogonal, classical, and mix design"
```

---

### Task 3: Create domain-specific reference files

**Covers:** S3, S5

**Files:**
- Create: `skills/materials-doe/static/reference/factor-level-template.md`
- Create: `skills/materials-doe/static/reference/asphalt-experiments.md`
- Create: `skills/materials-doe/static/reference/cement-experiments.md`
- Create: `skills/materials-doe/static/reference/general-experiments.md`
- Create: `skills/materials-doe/static/reference/ceramics-experiments.md`
- Create: `skills/materials-doe/static/reference/insulation-experiments.md`

- [ ] **Step 1: Write factor-level-template.md**

```markdown
# Factor-Level Table Template

## Example: Waterborne Epoxy Modified Emulsified Asphalt

| Factor | Name | Level 1 | Level 2 | Level 3 | Level 4 | Unit |
|--------|------|---------|---------|---------|---------|------|
| A | Epoxy content | 0 | 5 | 10 | 15 | wt% of asphalt |
| B | Curing temperature | 25 | 40 | 60 | — | °C |
| C | Curing time | 24 | 48 | 72 | — | h |
| D | Filler content | 0 | 3 | 6 | 9 | wt% of aggregate |

## How to Define Factors

1. **Identify controllable variables** that may affect the response.
2. **Choose levels** that span the practical range and can reveal trends.
3. **Include a zero/baseline level** for comparison.
4. **Avoid levels too close together** — they won't reveal differences.
5. **Avoid levels too far apart** — they may miss the optimum.

## Common Factor Ranges by Domain

### Asphalt
- Modifier content: 0–20 wt%
- Curing temperature: 25–80 °C
- Mixing speed: 500–3000 rpm
- Asphalt content: 4–7 wt%

### Cement/Concrete
- Water-binder ratio: 0.30–0.60
- Superplasticizer: 0–2 wt%
- Silica fume: 0–15 wt%
- Curing temperature: 20–80 °C

### Ceramics
- Sintering temperature: 1000–1600 °C
- Holding time: 1–8 h
- Additive content: 0–10 wt%
- Pressing pressure: 10–100 MPa
```

- [ ] **Step 2: Write asphalt-experiments.md**

```markdown
# Asphalt Experiment Design Guide

## Common Experiment Types

### Tack Coat Bond Strength
- Factors: emulsion type, application rate, curing time, surface condition
- Response: shear strength, pull-off strength
- Standard: ASTM D7313, AASHTO T 380

### Modified Emulsified Asphalt
- Factors: modifier type, modifier content, emulsifier content, curing condition
- Response: penetration, softening point, ductility, storage stability
- Standard: GB/T 4509, ASTM D5, GB/T 4508

### Moisture Damage Resistance
- Factors: anti-stripping agent type, dosage, conditioning method
- Response: tensile strength ratio (TSR), retained strength
- Standard: AASHTO T 283, ASTM D4867

## Typical Orthogonal Setup

For modified emulsified asphalt optimization:
- Factor A: Modifier content (3, 5, 7, 9 wt%)
- Factor B: Emulsifier content (0.3, 0.5, 0.7, 0.9 wt%)
- Factor C: Curing temperature (25, 40, 55, 70 °C)
- Factor D: Curing time (12, 24, 48, 72 h)
- L16 orthogonal array
- Responses: penetration, softening point, storage stability
```

- [ ] **Step 3: Write cement-experiments.md**

```markdown
# Cement/Concrete Experiment Design Guide

## Common Experiment Types

### Mix Proportion Design
- Factors: water-binder ratio, sand ratio, superplasticizer dosage, mineral admixture
- Response: compressive strength, workability (slump), cost
- Standard: JGJ 55, ACI 211.1, EN 206

### Durability Testing
- Factors: exposure condition, curing age, mix design
- Response: chloride penetration, carbonation depth, freeze-thaw resistance
- Standard: GB/T 50082, ASTM C1202, ASTM C666

### Supplementary Cementitious Materials
- Factors: SCM type, replacement level, curing condition
- Response: strength, hydration heat, microstructure
- Standard: ASTM C618, ASTM C989

## Typical Orthogonal Setup

For concrete mix optimization:
- Factor A: Water-binder ratio (0.35, 0.40, 0.45, 0.50)
- Factor B: Sand ratio (0.35, 0.38, 0.41, 0.44)
- Factor C: Superplasticizer (0.8, 1.0, 1.2, 1.4 wt%)
- Factor D: Silica fume (0, 5, 10, 15 wt%)
- L16 orthogonal array
- Responses: 7d/28d compressive strength, slump
```

- [ ] **Step 4: Write general-experiments.md**

```markdown
# General Construction Materials Experiment Design

## Applicable Materials
- Repair materials (patching mortar, bonding agent)
- Waterproofing materials (membrane, coating, sealant)
- Thermal insulation materials (aerogel, foam, EPS)
- Geotechnical materials (soil stabilizer, grout)

## Common Factor Types
- Material composition (binder type, additive content)
- Processing parameters (mixing time, temperature, pressure)
- Curing conditions (temperature, humidity, duration)
- Testing conditions (loading rate, specimen size, age)

## Standard Experiment Flow
1. Literature review → identify key factors and ranges
2. Screening experiment (Plackett-Burman or fractional factorial) → reduce factors
3. Optimization experiment (orthogonal or RSM) → find optimal conditions
4. Confirmation experiments → verify predicted optimum
5. Sensitivity analysis → assess robustness
```

- [ ] **Step 5: Write ceramics-experiments.md**

```markdown
# Ceramics Experiment Design Guide

## Common Experiment Types

### Sintering Optimization
- Factors: sintering temperature, holding time, heating rate, atmosphere
- Response: density, porosity, flexural strength, hardness
- Standard: ASTM C373, ASTM C1161, ISO 17565

### Additive Effects
- Factors: additive type, additive content, mixing method
- Response: phase composition, microstructure, mechanical properties

### Grain Growth Control
- Factors: sintering temperature, holding time, additive content
- Response: grain size distribution, fracture toughness

## Typical Orthogonal Setup

For alumina ceramic optimization:
- Factor A: Sintering temperature (1400, 1500, 1600 °C)
- Factor B: Holding time (1, 2, 4 h)
- Factor C: MgO additive (0, 0.5, 1.0 wt%)
- Factor D: Pressing pressure (50, 100, 150 MPa)
- L9 orthogonal array
- Responses: relative density, flexural strength, grain size
```

- [ ] **Step 6: Write insulation-experiments.md**

```markdown
# Thermal Insulation Experiment Design Guide

## Common Experiment Types

### Thermal Conductivity Optimization
- Factors: density, porosity, fiber content, binder content
- Response: thermal conductivity, compressive strength
- Standard: ASTM C518, ISO 8301, GB/T 10294

### Aerogel Composite Design
- Factors: aerogel content, fiber type, binder ratio, drying method
- Response: thermal conductivity, hydrophobicity, mechanical strength

### Foam Material Design
- Factors: foaming agent content, curing temperature, density target
- Response: cell structure, thermal conductivity, compressive strength

## Typical Orthogonal Setup

For aerogel insulation composite:
- Factor A: Aerogel content (20, 30, 40, 50 vol%)
- Factor B: Fiber content (0, 2, 4, 6 wt%)
- Factor C: Binder ratio (0.3, 0.4, 0.5, 0.6)
- Factor D: Drying temperature (60, 80, 100, 120 °C)
- L16 orthogonal array
- Responses: thermal conductivity, density, compressive strength
```

- [ ] **Step 7: Commit**

```powershell
git add skills/materials-doe/static/reference/
git commit -m "feat(doe): add domain-specific experiment reference files"
```

---

### Task 4: Create analysis scripts

**Covers:** S4, S7

**Files:**
- Create: `skills/materials-doe/scripts/orthogonal_analysis.py`
- Create: `skills/materials-doe/scripts/mix_design_calc.py`
- Create: `skills/materials-doe/scripts/experiment_plot.py`

- [ ] **Step 1: Write orthogonal_analysis.py**

```python
"""Orthogonal experiment analysis: range analysis and ANOVA."""

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats


def range_analysis(df, factors, response):
    """Compute range analysis (极差分析) for orthogonal experiment."""
    grand_mean = df[response].mean()
    results = []

    for factor in factors:
        level_means = df.groupby(factor)[response].mean()
        R = level_means.max() - level_means.min()
        best_level = level_means.idxmax()
        results.append({
            "factor": factor,
            "level_means": level_means.to_dict(),
            "range_R": R,
            "best_level": best_level,
        })

    results.sort(key=lambda x: x["range_R"], reverse=True)
    return {"grand_mean": grand_mean, "factors": results}


def anova_analysis(df, factors, response):
    """Compute one-way ANOVA for each factor."""
    grand_mean = df[response].mean()
    n = len(df)
    ss_total = ((df[response] - grand_mean) ** 2).sum()

    factor_results = []
    ss_explained = 0

    for factor in factors:
        groups = [group[response].values for _, group in df.groupby(factor)]
        k = len(groups)
        n_i = len(groups[0])

        ss_factor = sum(n_i * (g.mean() - grand_mean) ** 2 for g in groups)
        df_factor = k - 1
        ms_factor = ss_factor / df_factor if df_factor > 0 else 0

        ss_explained += ss_factor
        factor_results.append({
            "factor": factor,
            "SS": ss_factor,
            "df": df_factor,
            "MS": ms_factor,
        })

    ss_error = ss_total - ss_explained
    df_error = n - 1 - sum(r["df"] for r in factor_results)
    ms_error = ss_error / df_error if df_error > 0 else 0

    for r in factor_results:
        r["F"] = r["MS"] / ms_error if ms_error > 0 else float("inf")
        r["F_critical_005"] = float(stats.f.ppf(0.95, r["df"], df_error)) if df_error > 0 else float("inf")
        r["significant"] = r["F"] > r["F_critical_005"]

    return {
        "ss_total": ss_total,
        "ss_error": ss_error,
        "df_error": df_error,
        "ms_error": ms_error,
        "factors": factor_results,
    }


def predict_optimal(df, factors, response, goal="maximize"):
    """Predict optimal combination from level means."""
    grand_mean = df[response].mean()
    optimal = {}
    contribution = 0

    for factor in factors:
        level_means = df.groupby(factor)[response].mean()
        if goal == "maximize":
            best_level = level_means.idxmax()
        else:
            best_level = level_means.idxmin()
        optimal[factor] = best_level
        contribution += level_means[best_level] - grand_mean

    predicted = grand_mean + contribution
    return {"optimal_levels": optimal, "predicted_response": predicted, "grand_mean": grand_mean}


def main():
    parser = argparse.ArgumentParser(description="Orthogonal experiment analysis")
    parser.add_argument("input_csv", help="Path to experiment data CSV")
    parser.add_argument("--factors", nargs="+", required=True, help="Factor column names")
    parser.add_argument("--response", required=True, help="Response column name")
    parser.add_argument("--goal", default="maximize", choices=["maximize", "minimize", "target"])
    parser.add_argument("--output", help="Output JSON path")
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)
    range_result = range_analysis(df, args.factors, args.response)
    anova_result = anova_analysis(df, args.factors, args.response)
    optimal_result = predict_optimal(df, args.factors, args.response, args.goal)

    output = {
        "range_analysis": range_result,
        "anova": anova_result,
        "optimal_prediction": optimal_result,
    }

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False, default=str)
        print(f"Analysis saved to {args.output}")
    else:
        print(json.dumps(output, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Write mix_design_calc.py**

```python
"""Mix design calculation tools for civil materials."""

import argparse
import json
import sys
from pathlib import Path


def dense_packing(components):
    """Calculate dense packing proportions using Furnas model.

    Args:
        components: list of dicts with keys: name, packing_density, max_fraction
    Returns:
        dict with optimal_volume_fractions and total_packing_density
    """
    sorted_comp = sorted(components, key=lambda c: c["packing_density"], reverse=True)
    remaining = 1.0
    result = []

    for comp in sorted_comp:
        fraction = remaining * comp["packing_density"]
        fraction = min(fraction, comp.get("max_fraction", 1.0))
        result.append({"name": comp["name"], "volume_fraction": fraction})
        remaining -= fraction

    total_density = sum(r["volume_fraction"] for r in result)
    return {"components": result, "total_packing_density": total_density}


def volume_method(target_strength, water_cement_ratio, cement_density=3.15,
                  water_density=1.0, air_content=0.02):
    """Calculate concrete mix proportions using volume method.

    Args:
        target_strength: target compressive strength (MPa)
        water_cement_ratio: W/C ratio
        cement_density: specific gravity of cement
        water_density: specific gravity of water (1.0)
        air_content: air content fraction
    Returns:
        dict with mix proportions per cubic meter
    """
    cement_content = 400 * (target_strength / 40) / water_cement_ratio
    water_content = cement_content * water_cement_ratio
    cement_volume = cement_content / (cement_density * 1000)
    water_volume = water_content / 1000
    aggregate_volume = 1 - cement_volume - water_volume - air_content

    return {
        "cement_content_kg": round(cement_content, 1),
        "water_content_kg": round(water_content, 1),
        "water_cement_ratio": water_cement_ratio,
        "aggregate_volume_m3": round(aggregate_volume, 4),
        "air_content": air_content,
    }


def empirical_correction(base_mix, corrections):
    """Apply empirical corrections to a base mix.

    Args:
        base_mix: dict of component -> base_proportion
        corrections: list of dicts with keys: component, factor, reason
    Returns:
        dict with corrected proportions
    """
    result = dict(base_mix)
    for corr in corrections:
        comp = corr["component"]
        if comp in result:
            result[comp] *= corr["factor"]
            result[f"{comp}_correction_reason"] = corr["reason"]
    return result


def main():
    parser = argparse.ArgumentParser(description="Mix design calculator")
    subparsers = parser.add_subparsers(dest="command")

    packing_parser = subparsers.add_parser("dense-packing")
    packing_parser.add_argument("--input", required=True, help="JSON file with components")

    volume_parser = subparsers.add_parser("volume-method")
    volume_parser.add_argument("--strength", type=float, required=True)
    volume_parser.add_argument("--wc-ratio", type=float, required=True)

    args = parser.parse_args()

    if args.command == "dense-packing":
        with open(args.input, "r", encoding="utf-8") as f:
            components = json.load(f)
        result = dense_packing(components)
    elif args.command == "volume-method":
        result = volume_method(args.strength, args.wc_ratio)
    else:
        parser.print_help()
        return

    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
```

- [ ] **Step 3: Write experiment_plot.py**

```python
"""Experiment visualization scripts for materials research."""

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_factor_response(df, factors, response, output_path, goal="maximize"):
    """Plot factor-response relationship (main effects plot)."""
    n_factors = len(factors)
    fig, axes = plt.subplots(1, n_factors, figsize=(4 * n_factors, 4))
    if n_factors == 1:
        axes = [axes]

    for ax, factor in zip(axes, factors):
        means = df.groupby(factor)[response].mean()
        ax.plot(means.index, means.values, "o-", linewidth=2, markersize=8)
        ax.set_xlabel(factor, fontsize=11)
        ax.set_ylabel(response, fontsize=11)
        ax.set_title(f"Effect of {factor}", fontsize=12)
        ax.grid(True, alpha=0.3)

        if goal == "maximize":
            best = means.idxmax()
        else:
            best = means.idxmin()
        ax.axvline(x=best, color="red", linestyle="--", alpha=0.5, label=f"Best: {best}")
        ax.legend()

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Factor-response plot saved to {output_path}")


def plot_range_bar(ranges, output_path):
    """Plot range analysis bar chart."""
    factors = [r["factor"] for r in ranges]
    R_values = [r["range_R"] for r in ranges]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(factors, R_values, color=["#2196F3", "#4CAF50", "#FF9800", "#F44336"][:len(factors)])
    ax.set_xlabel("Factor", fontsize=12)
    ax.set_ylabel("Range R", fontsize=12)
    ax.set_title("Range Analysis (极差分析)", fontsize=13)
    ax.grid(axis="y", alpha=0.3)

    for bar, val in zip(bars, R_values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01,
                f"{val:.3f}", ha="center", fontsize=10)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Range bar chart saved to {output_path}")


def plot_dosage_performance(df, dosage_col, response_col, output_path):
    """Plot dosage-performance curve with optimum identification."""
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df[dosage_col], df[response_col], "o-", linewidth=2, markersize=8, color="#2196F3")
    ax.set_xlabel(dosage_col, fontsize=12)
    ax.set_ylabel(response_col, fontsize=12)
    ax.set_title("Dosage-Performance Curve", fontsize=13)
    ax.grid(True, alpha=0.3)

    best_idx = df[response_col].idxmax()
    best_x = df.loc[best_idx, dosage_col]
    best_y = df.loc[best_idx, response_col]
    ax.plot(best_x, best_y, "r*", markersize=15, label=f"Optimum: {best_x}")
    ax.legend(fontsize=11)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Dosage-performance plot saved to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Experiment plotting")
    subparsers = parser.add_subparsers(dest="command")

    fr_parser = subparsers.add_parser("factor-response")
    fr_parser.add_argument("--input", required=True)
    fr_parser.add_argument("--factors", nargs="+", required=True)
    fr_parser.add_argument("--response", required=True)
    fr_parser.add_argument("--output", required=True)
    fr_parser.add_argument("--goal", default="maximize")

    range_parser = subparsers.add_parser("range-bar")
    range_parser.add_argument("--input", required=True, help="JSON with range analysis results")
    range_parser.add_argument("--output", required=True)

    dosage_parser = subparsers.add_parser("dosage-performance")
    dosage_parser.add_argument("--input", required=True)
    dosage_parser.add_argument("--dosage-col", required=True)
    dosage_parser.add_argument("--response-col", required=True)
    dosage_parser.add_argument("--output", required=True)

    args = parser.parse_args()

    if args.command == "factor-response":
        df = pd.read_csv(args.input)
        plot_factor_response(df, args.factors, args.response, args.output, args.goal)
    elif args.command == "range-bar":
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
        plot_range_bar(data["range_analysis"]["factors"], args.output)
    elif args.command == "dosage-performance":
        df = pd.read_csv(args.input)
        plot_dosage_performance(df, args.dosage_col, args.response_col, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Commit**

```powershell
git add skills/materials-doe/scripts/
git commit -m "feat(doe): add analysis and plotting scripts"
```

---

### Task 5: Create output templates

**Covers:** S4

**Files:**
- Create: `skills/materials-doe/templates/experiment-plan.csv`
- Create: `skills/materials-doe/templates/data-template.csv`
- Create: `skills/materials-doe/templates/methods-paragraph.md`

- [ ] **Step 1: Write experiment-plan.csv**

```csv
exp_id,factor_A,factor_B,factor_C,factor_D,response_1,response_2,notes
1,level_1,level_1,level_1,level_1,,,
2,level_1,level_2,level_2,level_2,,,
3,level_1,level_3,level_3,level_3,,,
4,level_2,level_1,level_2,level_3,,,
5,level_2,level_2,level_3,level_1,,,
6,level_2,level_3,level_1,level_2,,,
7,level_3,level_1,level_3,level_2,,,
8,level_3,level_2,level_1,level_3,,,
9,level_3,level_3,level_2,level_1,,,
```

- [ ] **Step 2: Write data-template.csv**

```csv
exp_id,factor_A,factor_B,factor_C,factor_D,replicate,response_1,response_2,response_3,mean,std,cv,notes
1,,,,,,,,,,,,,
2,,,,,,,,,,,,,
3,,,,,,,,,,,,,
4,,,,,,,,,,,,,
5,,,,,,,,,,,,,
6,,,,,,,,,,,,,
7,,,,,,,,,,,,,
8,,,,,,,,,,,,,
9,,,,,,,,,,,,,
```

- [ ] **Step 3: Write methods-paragraph.md**

```markdown
# Methods Paragraph Template

## Orthogonal Experiment Design

To optimize [material/system], an L[N] ([factors]^([levels])) orthogonal experimental design was employed. [Number] factors were investigated: [Factor A] ([list levels]), [Factor B] ([list levels]), [Factor C] ([list levels]), and [Factor D] ([list levels]). The experimental matrix is shown in Table [X]. Each experiment was replicated [n] times to assess reproducibility. The response variable(s) included [response 1] and [response 2], measured according to [standard/method]. Range analysis (极差分析) was conducted to determine the influence ranking of each factor, and analysis of variance (ANOVA) was performed at a significance level of α = 0.05 using [software].

## Single-Factor Experiment

To investigate the effect of [factor] on [response], a single-factor experiment was conducted. [Factor] was varied at [number] levels: [list levels with units]. All other parameters were held constant: [list constants with values]. [Number] replicate specimens were prepared at each level. [Response] was measured at [age/condition] according to [standard]. Results are presented as mean ± standard deviation.

## Mix Design

The mix design for [material] was performed using the [method name] method. The target [strength/workability/performance] was [value]. [Component 1] content was calculated based on [formula/criterion]. [Component 2] was adjusted to achieve [target]. The final mix proportions are summarized in Table [X]. Trial batches were prepared and tested according to [standard] to verify the design.
```

- [ ] **Step 4: Commit**

```powershell
git add skills/materials-doe/templates/
git commit -m "feat(doe): add experiment plan, data template, and methods paragraph templates"
```

---

### Task 6: Create handoff contract

**Covers:** S6

**Files:**
- Create: `_shared/contracts/doe-handoff.yaml`

- [ ] **Step 1: Write doe-handoff.yaml**

```yaml
name: doe-handoff
version: "1.0"
description: "Experiment design plan with analysis scripts, methods text, and data templates"
produced_by: materials-doe
consumed_by:
  - materials-writing
  - materials-figure
  - materials-data
  - materials-research

artifacts:
  experiment_plan.csv:
    description: "CSV with experiment IDs and factor-level assignments"
    required: true
    columns:
      exp_id: { type: string, required: true }
      factor_columns: { type: string, required: true }
  analysis_script.py:
    description: "Python script for range analysis and ANOVA"
    required: true
  methods_paragraph.md:
    description: "Ready-to-paste Methods section text"
    required: true
  figure_script.py:
    description: "Python script for factor-response and dosage-performance plots"
    required: false
  data_template.csv:
    description: "Pre-filled data recording template"
    required: true
  analysis_results.json:
    description: "JSON with range analysis, ANOVA, and optimal prediction"
    required: false

templates:
  - ../../skills/materials-doe/templates/experiment-plan.csv
  - ../../skills/materials-doe/templates/data-template.csv
  - ../../skills/materials-doe/templates/methods-paragraph.md
```

- [ ] **Step 2: Commit**

```powershell
git add _shared/contracts/doe-handoff.yaml
git commit -m "feat(doe): add doe-handoff contract to shared contracts"
```

---

### Task 7: Update materials-research routing

**Covers:** S6

**Files:**
- Modify: `skills/materials-research/manifest.yaml`
- Modify: `skills/materials-research/SKILL.md`
- Modify: `skills/materials-research/references/companion-modules.md`

- [ ] **Step 1: Update manifest.yaml — add doe to companion_skills**

In `skills/materials-research/manifest.yaml`, add to the `companion_skills` section:

```yaml
  doe: materials-doe
```

- [ ] **Step 2: Update manifest.yaml — update experiment-design task fragment path**

The `experiment-design` task in `axes.task.values` already points to `static/fragments/task/experiment-design.md`. Update this fragment to reference the new skill.

- [ ] **Step 3: Update experiment-design.md fragment**

Replace the content of `skills/materials-research/static/fragments/task/experiment-design.md`:

```markdown
# Task: Experiment Design

Goal: produce a defensible materials experiment matrix.

Route to **materials-doe** for structured experiment design:

- **Classical**: single-factor, multi-factor, control-variable experiments
- **Orthogonal**: L9/L16/L25 arrays with range analysis and ANOVA
- **Mix Design**: proportion optimization via dense packing, volume method, or empirical formulas

Minimum experiment-design output:

- Research question.
- Independent variables and levels.
- Control groups.
- Measured properties.
- Mechanism tests.
- Durability or service-condition tests.
- Statistical/replication plan.
- Expected figure/table outputs.
- Risks and fallback plan.

Civil materials matrix rules:

- Include a blank/control material.
- Include at least one practical benchmark when possible.
- Use dosage levels that can reveal an optimum, not only monotonic improvement.
- Separate fresh/workability/stability properties from hardened/service properties.
- Do not add expensive characterization unless it answers a mechanism question.

For a master's project, prefer a compact matrix that can be finished and defended over an impressive but unfinishable matrix.
```

- [ ] **Step 4: Update companion-modules.md**

Add to `skills/materials-research/references/companion-modules.md`:

```markdown
## materials-doe

Experiment design skill for classical, orthogonal, and mix-design experiments.

**When to route:**
- User asks for experiment design, test matrix, or experimental plan
- User needs orthogonal array setup (L9/L16/L25)
- User needs mix proportion optimization
- User asks for factor-level table or experiment scheduling

**Handoff:** `doe-handoff` contract with experiment plan, analysis scripts, methods paragraph, and data templates.
```

- [ ] **Step 5: Commit**

```powershell
git add skills/materials-research/manifest.yaml skills/materials-research/SKILL.md skills/materials-research/static/fragments/task/experiment-design.md skills/materials-research/references/companion-modules.md
git commit -m "feat(doe): integrate materials-doe into research routing"
```

---

### Task 8: Create tests

**Covers:** S7

**Files:**
- Create: `skills/materials-doe/tests/__init__.py`
- Create: `skills/materials-doe/tests/test_doe_skill.py`
- Create: `skills/materials-doe/tests/test_orthogonal.py`
- Create: `skills/materials-doe/tests/test_mix_design.py`

- [ ] **Step 1: Write test_doe_skill.py**

```python
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS_ROOT = REPO_ROOT / "skills"
DOE_ROOT = SKILLS_ROOT / "materials-doe"
SHARED_CONTRACTS = SKILLS_ROOT / "_shared" / "contracts"


class DoeSkillStructureTest(unittest.TestCase):
    def test_manifest_exists_and_has_required_keys(self):
        manifest_path = DOE_ROOT / "manifest.yaml"
        self.assertTrue(manifest_path.exists())
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))

        self.assertIn("version", manifest)
        self.assertIn("always_load", manifest)
        self.assertIn("axes", manifest)
        self.assertIn("references", manifest)
        self.assertIn("handoffs", manifest)

    def test_manifest_axes_have_detect_and_values(self):
        manifest = yaml.safe_load((DOE_ROOT / "manifest.yaml").read_text(encoding="utf-8"))
        for axis_name, axis in manifest["axes"].items():
            self.assertIn("detect", axis, f"Axis {axis_name} missing detect")
            self.assertIn("default", axis, f"Axis {axis_name} missing default")
            self.assertIn("values", axis, f"Axis {axis_name} missing values")
            for val_name, val in axis["values"].items():
                self.assertIn("path", val, f"Value {val_name} in {axis_name} missing path")
                self.assertIn("triggers", val, f"Value {val_name} in {axis_name} missing triggers")

    def test_skill_md_exists_with_frontmatter(self):
        skill_path = DOE_ROOT / "SKILL.md"
        self.assertTrue(skill_path.exists())
        content = skill_path.read_text(encoding="utf-8")
        self.assertIn("name: materials-doe", content)
        self.assertIn("version:", content)
        self.assertIn("## Protocol", content)
        self.assertIn("## Gates", content)

    def test_readme_exists(self):
        readme_path = DOE_ROOT / "README.md"
        self.assertTrue(readme_path.exists())
        content = readme_path.read_text(encoding="utf-8")
        self.assertIn("materials-doe", content)

    def test_always_load_files_exist(self):
        manifest = yaml.safe_load((DOE_ROOT / "manifest.yaml").read_text(encoding="utf-8"))
        for rel_path in manifest["always_load"]:
            full_path = DOE_ROOT / rel_path
            self.assertTrue(full_path.exists(), f"Missing always_load file: {rel_path}")

    def test_doe_handoff_contract_exists(self):
        contract_path = SHARED_CONTRACTS / "doe-handoff.yaml"
        self.assertTrue(contract_path.exists())
        contract = yaml.safe_load(contract_path.read_text(encoding="utf-8"))
        self.assertEqual(contract["name"], "doe-handoff")
        self.assertIn("materials-doe", contract["produced_by"])
        self.assertIn("materials-writing", contract["consumed_by"])
        self.assertIn("materials-figure", contract["consumed_by"])

    def test_companion_skill_registered_in_research(self):
        research_manifest = yaml.safe_load(
            (SKILLS_ROOT / "materials-research" / "manifest.yaml").read_text(encoding="utf-8")
        )
        self.assertIn("doe", research_manifest.get("companion_skills", {}))
        self.assertEqual(research_manifest["companion_skills"]["doe"], "materials-doe")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Write test_orthogonal.py**

```python
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = REPO_ROOT / "skills" / "materials-doe" / "scripts"


class OrthogonalAnalysisTest(unittest.TestCase):
    def _make_l9_data(self):
        """Create synthetic L9 orthogonal experiment data."""
        np.random.seed(42)
        data = {
            "exp_id": list(range(1, 10)),
            "A": [1, 1, 1, 2, 2, 2, 3, 3, 3],
            "B": [1, 2, 3, 1, 2, 3, 1, 2, 3],
            "C": [1, 2, 3, 2, 3, 1, 3, 1, 2],
            "D": [1, 2, 3, 3, 1, 2, 2, 3, 1],
            "response": [10 + i * 2 + np.random.normal(0, 0.5) for i in range(9)],
        }
        return pd.DataFrame(data)

    def test_range_analysis_identifies_most_influential_factor(self):
        sys_path = str(SCRIPTS_DIR)
        import sys
        if sys_path not in sys.path:
            sys.path.insert(0, sys_path)

        from orthogonal_analysis import range_analysis

        df = self._make_l9_data()
        result = range_analysis(df, ["A", "B", "C", "D"], "response")

        self.assertIn("grand_mean", result)
        self.assertIn("factors", result)
        self.assertEqual(len(result["factors"]), 4)

        ranges = [f["range_R"] for f in result["factors"]]
        self.assertEqual(ranges, sorted(ranges, reverse=True))

    def test_anova_produces_f_values(self):
        sys_path = str(SCRIPTS_DIR)
        import sys
        if sys_path not in sys.path:
            sys.path.insert(0, sys_path)

        from orthogonal_analysis import anova_analysis

        df = self._make_l9_data()
        result = anova_analysis(df, ["A", "B", "C", "D"], "response")

        self.assertIn("factors", result)
        self.assertEqual(len(result["factors"]), 4)
        for factor in result["factors"]:
            self.assertIn("F", factor)
            self.assertIn("significant", factor)

    def test_predict_optimal_returns_valid_combination(self):
        sys_path = str(SCRIPTS_DIR)
        import sys
        if sys_path not in sys.path:
            sys.path.insert(0, sys_path)

        from orthogonal_analysis import predict_optimal

        df = self._make_l9_data()
        result = predict_optimal(df, ["A", "B", "C", "D"], "response", "maximize")

        self.assertIn("optimal_levels", result)
        self.assertIn("predicted_response", result)
        self.assertEqual(len(result["optimal_levels"]), 4)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Write test_mix_design.py**

```python
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPTS_DIR = REPO_ROOT / "skills" / "materials-doe" / "scripts"


class MixDesignCalcTest(unittest.TestCase):
    def test_dense_packing_returns_valid_fractions(self):
        import sys
        sys.path.insert(0, str(SCRIPTS_DIR))
        from mix_design_calc import dense_packing

        components = [
            {"name": "cement", "packing_density": 0.5, "max_fraction": 0.3},
            {"name": "sand", "packing_density": 0.6, "max_fraction": 0.4},
            {"name": "gravel", "packing_density": 0.55, "max_fraction": 0.5},
        ]
        result = dense_packing(components)

        self.assertIn("components", result)
        self.assertIn("total_packing_density", result)
        self.assertGreater(result["total_packing_density"], 0)
        self.assertLessEqual(result["total_packing_density"], 1.0)

    def test_volume_method_returns_proportions(self):
        import sys
        sys.path.insert(0, str(SCRIPTS_DIR))
        from mix_design_calc import volume_method

        result = volume_method(40.0, 0.45)

        self.assertIn("cement_content_kg", result)
        self.assertIn("water_content_kg", result)
        self.assertGreater(result["cement_content_kg"], 0)
        self.assertGreater(result["water_content_kg"], 0)

    def test_empirical_correction_applies_factors(self):
        import sys
        sys.path.insert(0, str(SCRIPTS_DIR))
        from mix_design_calc import empirical_correction

        base = {"cement": 400, "water": 180}
        corrections = [
            {"component": "cement", "factor": 1.1, "reason": "source adjustment"},
        ]
        result = empirical_correction(base, corrections)

        self.assertAlmostEqual(result["cement"], 440.0)
        self.assertAlmostEqual(result["water"], 180.0)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 4: Run tests**

```powershell
python -m unittest discover -s skills/materials-doe/tests -p "test_*.py" -v
```

Expected: All tests pass.

- [ ] **Step 5: Commit**

```powershell
git add skills/materials-doe/tests/
git commit -m "feat(doe): add unit tests for skill structure, orthogonal analysis, and mix design"
```

---

### Task 9: Update release checks and root tests

**Covers:** S6

**Files:**
- Modify: `scripts/run_release_checks.py`
- Modify: `tests/test_manifest_validation.py` (if needed)

- [ ] **Step 1: Check if release checks auto-discover the new skill**

```powershell
python scripts/run_release_checks.py --json
```

If the output shows `"status": "pass"`, no changes needed. If it reports issues for `materials-doe`, fix them.

- [ ] **Step 2: Run all root tests**

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: All tests pass, including manifest validation for the new skill.

- [ ] **Step 3: Run full test suite**

```powershell
$skills = @("materials-citation", "materials-data", "materials-doe", "materials-figure", "materials-paper2ppt", "materials-polishing", "materials-pptx", "materials-reader", "materials-research", "materials-response", "materials-reviewer", "materials-writing")
foreach ($s in $skills) {
    Write-Host "=== $s ==="
    python -m unittest discover -s "skills/$s/tests" -p "test_*.py" 2>&1 | Select-Object -Last 3
}
```

Expected: All skills pass.

- [ ] **Step 4: Commit if changes were needed**

```powershell
git add -A
git commit -m "fix(doe): resolve release check issues for materials-doe skill"
```

---

### Task 10: Final verification and documentation update

**Covers:** S1, S5

**Files:**
- Modify: `README.md`
- Modify: `RELEASE_NOTES.md` (optional)
- Modify: `docs/skills-index.md` (if exists)

- [ ] **Step 1: Update README.md skill status table**

Add to the skill status table in `README.md`:

```markdown
| `materials-doe` | Stable design skill | Yes | Yes | Factors, levels, design mode, optimization goal | Experiment plan, analysis script, methods paragraph, data template |
```

- [ ] **Step 2: Run final release check**

```powershell
python scripts/run_release_checks.py --json
```

Expected: `{"status": "pass", "issues": {}}`

- [ ] **Step 3: Run full test count**

```powershell
$skills = @("materials-citation", "materials-data", "materials-doe", "materials-figure", "materials-paper2ppt", "materials-polishing", "materials-pptx", "materials-reader", "materials-research", "materials-response", "materials-reviewer", "materials-writing")
$total = 0
foreach ($s in $skills) {
    $result = python -m unittest discover -s "skills/$s/tests" -p "test_*.py" 2>&1 | Select-String "Ran (\d+) tests"
    if ($result -match "Ran (\d+) tests") {
        $total += [int]$Matches[1]
    }
}
Write-Host "Total skill tests: $total"
```

Expected: ~210+ tests (original 199 + new materials-doe tests).

- [ ] **Step 4: Commit**

```powershell
git add README.md
git commit -m "docs: add materials-doe to skill status index"
```

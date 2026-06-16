# Ceramics Experiment Design Reference

## Typical factors and levels

| Factor | Low | Medium | High | Notes |
|---|---|---|---|---|
| Sintering temperature (°C) | 1400 | 1500 | 1600 | Dependent on ceramic system |
| Heating rate (°C/min) | 2 | 5 | 10 | Affects grain growth |
| Dwell time (h) | 1 | 2 | 4 | Longer → denser but coarser |
| Dopant content (wt%) | 0 | 0.5 | 2 | System-dependent optimum |
| Forming pressure (MPa) | 50 | 150 | 250 | Green density affects sintered density |

## Typical responses and measurement methods

| Response | Method | Standard | Units |
|---|---|---|---|
| Relative density | Archimedes | ASTM C373 / ISO 18754 | % of theoretical |
| Open/closed porosity | Archimedes | ASTM C373 | % |
| Linear shrinkage | Caliper (before/after) | — | % |
| Flexural strength | 3-point or 4-point bending | ASTM C1161 / ISO 14704 | MPa |
| Fracture toughness | SENB, SEPB, IF, CNB | ASTM C1421 | MPa·m^(1/2) |
| Vickers hardness | Indentation | ASTM C1327 / ISO 14705 | GPa |
| Weibull modulus | Maximum likelihood | ASTM C1239 | — |
| Thermal conductivity | Laser flash, guarded hot plate | ASTM E1461 | W m⁻¹ K⁻¹ |
| Thermal expansion | Dilatometry | ASTM E228 | 10⁻⁶ K⁻¹ |
| Grain size | Linear intercept | ASTM E112 | µm |

## Recommended experimental designs

### 1. Composition screening: Full factorial

**Purpose**: Identify which component significantly affects density/strength.
**Design**: 2^k factorial, where k = number of composition variables.
**Example**: 3 dopants × 2 levels = 8 runs + 2 center points.
**Analysis**: ANOVA, Pareto chart of standardized effects.

### 2. Sintering optimization: Central Composite Design (CCD)

**Purpose**: Find the optimal sintering T, ramp, and dwell for maximum density.
**Design**: CCD with 3 factors (T, ramp, dwell), 2^3 = 8 factorial + 6 axial + 2 center = 16 runs.
**Response surface**: Fit quadratic model; contour plot of density vs T and dwell.
**Verification**: Run 3 confirmation trials at predicted optimum.

### 3. Robust sintering: Taguchi L9

**Purpose**: Minimize sensitivity to uncontrollable factors (furnace variation, powder batch).
**Design**: L9 orthogonal array with 4 factors at 3 levels.
**Signal-to-noise**: Larger-the-better for density and strength.
**Confirmation**: Run at optimal levels; compare with initial condition.

### 4. Multi-component formulation: Mixture design

**Purpose**: Optimize ternary/ quaternary ceramic composition.
**Design**: Simplex centroid or D-optimal mixture design.
**Constraints**: Component fractions sum to 1; lower/upper bounds on each.
**Analysis**: Ternary contour plot of the target property.

## Replication and statistics

| Response | Minimum replicates | Notes |
|---|---|---|
| Density | 3 specimens | Per condition |
| Flexural strength | 10 specimens (30 recommended) | For Weibull analysis |
| Hardness | 5 indentations | Per specimen |
| Fracture toughness | 5 specimens | Valid KIC requires precrack verification |
| Thermal conductivity | 3 measurements | At each temperature |
| Grain size | ≥200 grains | From ≥3 SEM images |

## Standard reporting checklist

- [ ] Sintering profile: ramp rate, target T, dwell time, cooling rate, atmosphere
- [ ] Theoretical density and calculation basis
- [ ] Density measurement method (Archimedes, geometric, He pycnometry)
- [ ] XRD: 2θ range, step size, reference pattern source (ICDD/JCPDS numbers)
- [ ] SEM: accelerating voltage, working distance, magnification, scale bar
- [ ] Mechanical test: standard number, specimen geometry, span, crosshead speed
- [ ] Weibull: number of specimens, estimator method, confidence bounds

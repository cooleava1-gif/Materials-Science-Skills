# Thermal Insulation Experiment Reference

Common experiment types, typical factor-response pairs, and standard references for thermal insulation materials research.

## Experiment Type 1: Thermal Conductivity Optimization

Minimize thermal conductivity while maintaining mechanical integrity and meeting fire-resistance requirements.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Density (kg/m³) | kg/m³ | 20–200 |
| Porosity | % | 50–95 |
| Pore size | μm | 10–500 |
| Binder content (%) | % | 5–30 |
| Additive type | — | aerogel, hollow microspheres, vermiculite |
| Additive content (%) | % | 5–40 |
| Sample thickness (mm) | mm | 10–50 |

| Response | Unit | Standard |
|----------|------|----------|
| Thermal conductivity | W/(m·K) | ASTM C518 (heat flow meter) |
| Compressive strength | kPa | ASTM C165 |
| Flexural strength | kPa | ASTM C203 |
| Water absorption | kg/m² | ASTM C1104 |
| Fire rating | class | ASTM E119 / GB 8624 |
| Linear shrinkage | % | ASTM C356 |

### Standards

- ASTM C518 — Steady-state thermal transmission properties by heat flow meter
- ASTM C165 — Measuring compressive properties of thermal insulations
- ASTM C203 — Flexural properties of block-type thermal insulation
- ASTM C533 — Calcium silicate block and pipe thermal insulation
- GB/T 10295 — Determination of steady-state thermal resistance (Chinese, equivalent to ISO 8301)
- GB 8624 — Classification for burning behavior of building materials

## Experiment Type 2: Aerogel Composite Insulation

Optimize the formulation of aerogel-enhanced insulation materials (blanket, board, or coating).

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Aerogel content (%) | % | 10–60 |
| Aerogel particle size (mm) | mm | 0.1–5 |
| Binder type | — | cement, gypsum, polymer, fiber |
| Binder content (%) | % | 10–40 |
| Fiber reinforcement (%) | % | 0–5 |
| Pressing density (kg/m³) | kg/m³ | 80–200 |
| Curing temperature (°C) | °C | 20–80 |

| Response | Unit | Standard |
|----------|------|----------|
| Thermal conductivity | W/(m·K) | ASTM C518 |
| Compressive strength | kPa | ASTM C165 |
| Tensile strength | kPa | ASTM C686 |
| Hydrophobicity | contact angle | — |
| Density | kg/m³ | ASTM C303 |
| Service temperature | °C | — |

### Standards

- ASTM C1728 — Flexible aerogel insulation
- ASTM C518 — Thermal conductivity measurement
- ISO 9229 — Thermal insulation vocabulary
- GB/T 34336 — Aerogel composite insulation blanket (Chinese)

## Experiment Type 3: Foam Material Insulation

Optimize foaming parameters and formulation for polyurethane, phenolic, or cement-based foam insulation.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Foaming agent type | — | pentane, HFC-245fa, water, CO₂ |
| Foaming agent content (%) | % | 2–15 |
| Surfactant content (%) | % | 0.5–3 |
| Catalyst content (%) | % | 0.1–2 |
| Isocyanate index | — | 80–120 (for PU) |
| Mixing ratio (A:B) | — | 1:1 to 1:2 |
| Mold temperature (°C) | °C | 20–60 |
| Free rise density (kg/m³) | kg/m³ | 25–60 |

| Response | Unit | Standard |
|----------|------|----------|
| Thermal conductivity | W/(m·K) | ASTM C518 |
| Closed-cell content | % | ASTM D6226 |
| Density | kg/m³ | ASTM D1622 |
| Compressive strength | kPa | ASTM D1621 |
| Dimensional stability | % | ASTM D2126 |
| Water vapor permeability | perm | ASTM E96 |
| Oxygen index | % | ASTM D2863 |
| Flame spread index | — | ASTM E84 |

### Standards

- ASTM D1621 — Compressive properties of rigid cellular plastics
- ASTM D1622 — Apparent density of rigid cellular plastics
- ASTM D2126 — Dimensional stability of rigid cellular plastics
- ASTM D6226 — Open-cell content of rigid cellular plastics
- ASTM D2863 — Minimum oxygen concentration to sustain candle-like combustion
- GB/T 8813 — Rigid cellular plastics compression test method (Chinese)
- GB/T 10801.1 — Rigid polyurethane foam for thermal insulation (Chinese)

## Typical Orthogonal Setup: Foam Insulation (L9)

4 factors, 3 levels each, 9 runs.

| Factor | Level 1 | Level 2 | Level 3 |
|--------|---------|---------|---------|
| Foaming agent content (%) | 4 | 7 | 10 |
| Surfactant content (%) | 0.8 | 1.2 | 1.6 |
| Catalyst content (%) | 0.3 | 0.6 | 1.0 |
| Mold temperature (°C) | 25 | 35 | 45 |

| Run | Foaming (%) | Surfactant (%) | Catalyst (%) | Temp (°C) |
|-----|-------------|---------------|--------------|-----------|
| 1 | 4 | 0.8 | 0.3 | 25 |
| 2 | 4 | 1.2 | 0.6 | 35 |
| 3 | 4 | 1.6 | 1.0 | 45 |
| 4 | 7 | 0.8 | 0.6 | 45 |
| 5 | 7 | 1.2 | 1.0 | 25 |
| 6 | 7 | 1.6 | 0.3 | 35 |
| 7 | 10 | 0.8 | 1.0 | 35 |
| 8 | 10 | 1.2 | 0.3 | 45 |
| 9 | 10 | 1.6 | 0.6 | 25 |

Responses: thermal conductivity, density, compressive strength, closed-cell content.

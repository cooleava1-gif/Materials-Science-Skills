# Ceramics Experiment Reference

Common experiment types, typical factor-response pairs, and standard references for structural and functional ceramics research.

## Experiment Type 1: Sintering Optimization

Optimize sintering temperature, time, and atmosphere to achieve target density, strength, and microstructure.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Sintering temperature (°C) | °C | 1000–1400 (oxide); 1600–2000 (non-oxide) |
| Sintering time (h) | h | 1–8 |
| Heating rate (°C/min) | °C/min | 2–10 |
| Cooling rate (°C/min) | °C/min | 2–10 |
| Atmosphere | — | air, N₂, Ar, vacuum, H₂ |
| Compaction pressure (MPa) | MPa | 50–300 |

| Response | Unit | Standard |
|----------|------|----------|
| Bulk density | g/cm³ | ASTM C373 |
| Relative density | % | ASTM C373 |
| Open porosity | % | ASTM C373 |
| Linear shrinkage | % | ASTM C326 |
| Flexural strength | MPa | ASTM C1161 |
| Hardness | GPa | ASTM C1327 (Vickers) |
| Grain size | μm | ASTM E112 (intercept method) |

### Standards

- ASTM C373 — Water absorption, bulk density, apparent porosity
- ASTM C1161 — Flexural strength of advanced ceramics at ambient temperature
- ASTM C1327 — Vickers indentation hardness
- ASTM C326 — Drying and firing shrinkage of ceramic whiteware clays
- ISO 17561 — Flexural strength of monolithic ceramics at room temperature

## Experiment Type 2: Additive Effects

Evaluate the influence of sintering aids, grain growth inhibitors, and property enhancers on ceramic performance.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Additive type | — | MgO, Y₂O₃, Al₂O₃, CeO₂, SiO₂, TiO₂ |
| Additive content (%) | % | 0.1–10 |
| Additive particle size | μm | 0.01–5 |
| Sintering temperature (°C) | °C | 1200–1600 |
| Sintering time (h) | h | 2–6 |

| Response | Unit | Standard |
|----------|------|----------|
| Relative density | % | ASTM C373 |
| Grain size | μm | ASTM E112 |
| Flexural strength | MPa | ASTM C1161 |
| Fracture toughness | MPa·m^½ | ASTM C1421 |
| Thermal conductivity | W/(m·K) | ASTM E1461 (laser flash) |
| Dielectric constant | — | ASTM D150 |
| Transmittance (%) | % | UV-Vis spectrophotometry |

### Standards

- ASTM C1421 — Fracture toughness of advanced ceramics
- ASTM E1461 — Thermal diffusivity by laser flash
- ASTM E112 — Determining average grain size
- ISO 18754 — Density and porosity of fine ceramics

## Experiment Type 3: Grain Growth Control

Study the kinetics of grain growth and the effectiveness of inhibitors during sintering.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Sintering temperature (°C) | °C | 1300–1600 |
| Isothermal hold time (h) | h | 0.5, 1, 2, 4, 8, 16 |
| Grain growth inhibitor | — | MgO, Y₂O₃, Nb₂O₅ |
| Inhibitor content (%) | % | 0.1–5 |
| Initial grain size | μm | 0.1–2 |
| Atmosphere | — | air, vacuum, N₂ |

| Response | Unit | Standard |
|----------|------|----------|
| Average grain size | μm | ASTM E112 |
| Grain size distribution | — | SEM + image analysis |
| Grain growth exponent (n) | — | Burke-Turnbull fit |
| Activation energy | kJ/mol | Arrhenius analysis |
| Density | g/cm³ | ASTM C373 |
| Strength | MPa | ASTM C1161 |

### Grain Growth Kinetics

The Burke-Turnbull equation:

$$G^n - G_0^n = K_0 \cdot t \cdot \exp\left(-\frac{Q}{RT}\right)$$

where $G$ is grain size at time $t$, $G_0$ is initial grain size, $n$ is the grain growth exponent (typically 2–4), $Q$ is activation energy, $R$ is gas constant, and $T$ is absolute temperature.

### Standards

- ASTM E112 — Standard test methods for determining average grain size
- ASTM C1322 — Fractography of advanced ceramics

## Typical Orthogonal Setup: Sintering Optimization (L9)

4 factors, 3 levels each, 9 runs.

| Factor | Level 1 | Level 2 | Level 3 |
|--------|---------|---------|---------|
| Sintering temperature (°C) | 1200 | 1300 | 1400 |
| Sintering time (h) | 2 | 4 | 6 |
| MgO additive (%) | 0.5 | 1.0 | 2.0 |
| Heating rate (°C/min) | 3 | 5 | 8 |

| Run | Temp (°C) | Time (h) | MgO (%) | Rate (°C/min) |
|-----|-----------|----------|---------|---------------|
| 1 | 1200 | 2 | 0.5 | 3 |
| 2 | 1200 | 4 | 1.0 | 5 |
| 3 | 1200 | 6 | 2.0 | 8 |
| 4 | 1300 | 2 | 1.0 | 8 |
| 5 | 1300 | 4 | 2.0 | 3 |
| 6 | 1300 | 6 | 0.5 | 5 |
| 7 | 1400 | 2 | 2.0 | 5 |
| 8 | 1400 | 4 | 0.5 | 8 |
| 9 | 1400 | 6 | 1.0 | 3 |

Responses: relative density, flexural strength, average grain size.

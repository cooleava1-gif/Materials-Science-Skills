# Functional Materials Experiment Reference

Common experiment types, typical factor-response pairs, and standard references for semiconductor, dielectric, piezoelectric, and photonic material research.

## Experiment Type 1: Dielectric Ceramic Sintering Optimization

Optimize sintering conditions for maximum density and dielectric performance.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Sintering temperature (°C) | °C | 1100–1400 |
| Sintering time (h) | h | 2–12 |
| Heating rate (°C/min) | °C/min | 2–10 |
| Atmosphere | — | air, O₂, N₂ |
| Dopant concentration (mol%) | mol% | 0–5 |

| Response | Unit | Standard |
|----------|------|----------|
| Relative density | % | Archimedes |
| Grain size | µm | SEM intercept (ASTM E112) |
| Dielectric constant (εr) | — | IEC 60250 |
| Loss tangent (tan δ) | — | IEC 60250 |
| Curie temperature (Tc) | °C | DSC or εr vs T |

### Standards

- IEC 60250 — Dielectric constant and loss measurement
- IEEE 176 — Piezoelectric crystals
- ASTM E112 — Grain size determination

## Experiment Type 2: Thin Film Deposition for Optoelectronics

Optimize deposition and annealing parameters for optical and electrical performance.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Deposition method | — | PLD, sputtering, spin coating, MBE, CVD |
| Substrate temperature (°C) | °C | 25–800 |
| Annealing temperature (°C) | °C | 200–600 |
| Annealing atmosphere | — | air, N₂, O₂, vacuum |
| Film thickness (nm) | nm | 50–2000 |
| Doping level (mol%) | mol% | 0–10 |

| Response | Unit | Standard |
|----------|------|----------|
| Optical band gap | eV | UV-Vis (Tauc plot) |
| Transmittance (550 nm) | % | UV-Vis |
| Sheet resistance | Ω/sq | four-point probe (ASTM F390) |
| Carrier concentration | cm⁻³ | Hall effect |
| Mobility | cm²/V·s | Hall effect |
| Surface roughness (Ra) | nm | AFM |

### Standards

- ASTM F390 — Sheet resistance by four-point probe
- ASTM E308 — CIE color computation
- IEC 62805 — Measurement of PV module transmittance

## Experiment Type 3: Piezoelectric Performance Optimization

Optimize composition, poling, and processing for maximum piezoelectric response.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Composition (dopant x) | mol% | 0–10 |
| Sintering temperature (°C) | °C | 1100–1350 |
| Poling field (kV/cm) | kV/cm | 10–60 |
| Poling temperature (°C) | °C | 25–150 |
| Poling time (min) | min | 5–30 |

| Response | Unit | Standard |
|----------|------|----------|
| d₃₃ | pC/N | Berlincourt meter (IEEE 176) |
| d₃₁ | pC/N | impedance method |
| Coupling factor (k₃₃, kₚ) | — | IEEE 176 |
| Dielectric constant (εr) | — | IEC 60250 |
| Coercive field (Ec) | kV/cm | P-E loop |
| Remanent polarization (Pr) | µC/cm² | P-E loop |

### Standards

- IEEE 176 — Piezoelectric crystals
- IEC 61094 — Measurement microphones
- IEC 60250 — Dielectric measurements

## Typical Orthogonal Setup: BaTiO₃ Doping (L9)

4 factors, 3 levels each, 9 runs.

| Factor | Level 1 | Level 2 | Level 3 |
|--------|---------|---------|---------|
| Nb doping (mol%) | 0.5 | 1.0 | 2.0 |
| Sintering temp (°C) | 1250 | 1300 | 1350 |
| Sintering time (h) | 2 | 4 | 6 |
| Atmosphere | air | O₂ | N₂ |

| Run | Nb (mol%) | Temp (°C) | Time (h) | Atm |
|-----|-----------|-----------|----------|-----|
| 1 | 0.5 | 1250 | 2 | air |
| 2 | 0.5 | 1300 | 4 | O₂ |
| 3 | 0.5 | 1350 | 6 | N₂ |
| 4 | 1.0 | 1250 | 4 | N₂ |
| 5 | 1.0 | 1300 | 6 | air |
| 6 | 1.0 | 1350 | 2 | O₂ |
| 7 | 2.0 | 1250 | 6 | O₂ |
| 8 | 2.0 | 1300 | 2 | N₂ |
| 9 | 2.0 | 1350 | 4 | air |

Responses: relative density, grain size, dielectric constant, loss tangent, d₃₃.

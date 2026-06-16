# Metals Experiment Reference

Common experiment types, typical factor-response pairs, and standard references for metals and alloys research.

## Experiment Type 1: Heat Treatment Optimization

Optimize quenching and tempering parameters to achieve target strength-toughness balance in structural steels.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Austenitizing temperature (°C) | °C | 820–950 (low-alloy), 1000–1200 (stainless/tool) |
| Austenitizing time (min) | min | 15–120 |
| Quench medium | — | water, oil, air, polymer, brine |
| Tempering temperature (°C) | °C | 150–650 |
| Tempering time (min) | min | 30–360 |

| Response | Unit | Standard |
|----------|------|----------|
| Yield strength (Rp0.2) | MPa | ASTM E8 / ISO 6892 |
| UTS | MPa | ASTM E8 / ISO 6892 |
| Elongation | % | ASTM E8 / ISO 6892 |
| Hardness | HRC / HV | ASTM E18 / ASTM E92 |
| Impact energy (Charpy V) | J | ASTM E23 / ISO 148 |

### Standards

- ASTM E8 — Tension testing of metallic materials
- ISO 6892 — Metallic materials — Tensile testing
- ASTM E23 — Notched bar impact testing
- ASTM E18 — Rockwell hardness
- ASTM E92 — Vickers hardness

## Experiment Type 2: Additive Manufacturing Process Optimization

Optimize laser powder bed fusion (LPBF/SLM) parameters for density, microstructure, and mechanical properties.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Laser power (W) | W | 100–400 |
| Scan speed (mm/s) | mm/s | 400–1600 |
| Layer thickness (µm) | µm | 20–60 |
| Hatch spacing (µm) | µm | 80–200 |
| Scan strategy | — | stripe, chessboard, 67° rotation |
| Energy density (J/mm³) | J/mm³ | 30–150 (calculated from above) |

| Response | Unit | Standard |
|----------|------|----------|
| Relative density | % | Archimedes (ASTM B311) |
| Surface roughness (Ra) | µm | profilometer |
| Yield strength | MPa | ASTM E8 |
| Elongation | % | ASTM E8 |
| Residual porosity | % | metallographic cross-section |
| Microhardness | HV | ASTM E92 |

### Standards

- ASTM B311 — Density of powder metallurgy materials
- ASTM E8 — Tensile testing
- ISO/ASTM 52900 — Additive manufacturing — General principles
- ISO/ASTM 52901 — Requirements for purchased AM parts

## Experiment Type 3: Corrosion Resistance

Evaluate the pitting and general corrosion resistance of stainless steels or coated alloys in chloride environments.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Alloy type | — | 304, 316, 316L, 2205 duplex, 2507 super duplex |
| Cl⁻ concentration (mol/L) | mol/L | 0.01–6.0 (NaCl solution) |
| Temperature (°C) | °C | 20, 40, 60, 80 |
| pH | — | 1–10 |
| Surface finish | — | ground, polished, pickled, passivated |
| Exposure time (h) | h | 24, 168, 720, 3000 |

| Response | Unit | Standard |
|----------|------|----------|
| Corrosion rate | mm/year | ASTM G102 (from polarization) |
| Pitting potential (E_pit) | mV vs SCE | ASTM G61 |
| Repassivation potential (E_rp) | mV vs SCE | ASTM G61 |
| Critical pitting temperature (CPT) | °C | ASTM G48 |
| Mass loss | mg/cm² | ASTM G31 |

### Standards

- ASTM G5 — Potentiodynamic anodic polarization
- ASTM G61 — Cyclic potentiodynamic polarization
- ASTM G48 — Pitting and crevice corrosion (FeCl₃)
- ASTM B117 — Salt spray (fog) testing
- ASTM A262 — Intergranular corrosion testing

## Experiment Type 4: Welding Parameter Optimization

Optimize welding parameters for defect-free joints with balanced strength and toughness.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Welding method | — | GTAW, GMAW, SMAW, SAW, laser, EBW |
| Current (A) | A | 80–300 (GTAW), 150–400 (GMAW) |
| Voltage (V) | V | 10–30 |
| Travel speed (mm/s) | mm/s | 2–15 |
| Preheat temperature (°C) | °C | 25–300 |
| Interpass temperature (°C) | °C | 150–250 |
| Post-weld heat treatment | — | none, stress relief, PWHT |

| Response | Unit | Standard |
|----------|------|----------|
| Weld metal tensile strength | MPa | AWS D1.1 / ISO 4136 |
| HAZ hardness | HV | ASTM E92 |
| Charpy impact (weld metal) | J | ASTM E23 |
| Charpy impact (HAZ) | J | ASTM E23 |
| Defect rate (porosity, crack) | — | radiography (ASTM E94) |
| Dilution ratio | % | metallographic cross-section |

### Standards

- AWS D1.1 — Structural welding code — Steel
- ISO 4136 — Destructive tests on welds — Transverse tensile test
- ASTM E94 — Radiographic examination
- ISO 17637 — Visual testing of welds

## Typical Orthogonal Setup: 4340 Steel Q&T (L9)

4 factors, 3 levels each, 9 runs.

| Factor | Level 1 | Level 2 | Level 3 |
|--------|---------|---------|---------|
| Austenitizing temp (°C) | 830 | 860 | 890 |
| Quench medium | oil | water | polymer |
| Tempering temp (°C) | 200 | 400 | 600 |
| Tempering time (min) | 60 | 120 | 180 |

| Run | Aus. (°C) | Quench | Temp. (°C) | Time (min) |
|-----|-----------|--------|------------|------------|
| 1 | 830 | oil | 200 | 60 |
| 2 | 830 | water | 400 | 120 |
| 3 | 830 | polymer | 600 | 180 |
| 4 | 860 | oil | 400 | 180 |
| 5 | 860 | water | 600 | 60 |
| 6 | 860 | polymer | 200 | 120 |
| 7 | 890 | oil | 600 | 120 |
| 8 | 890 | water | 200 | 180 |
| 9 | 890 | polymer | 400 | 60 |

Responses: yield strength, UTS, elongation, hardness, Charpy impact energy.

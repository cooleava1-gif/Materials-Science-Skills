# Polymers Experiment Reference

Common experiment types, typical factor-response pairs, and standard references for polymer, rubber, and polymer composite research.

## Experiment Type 1: Injection Molding Process Optimization

Optimize processing parameters to maximize mechanical performance of injection-molded thermoplastic parts.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Melt temperature (°C) | °C | 200–300 (PP), 260–320 (PA6), 300–380 (PEEK) |
| Mold temperature (°C) | °C | 20–120 |
| Injection speed (mm/s) | mm/s | 20–150 |
| Holding pressure (MPa) | MPa | 30–100 |
| Cooling time (s) | s | 10–60 |

| Response | Unit | Standard |
|----------|------|----------|
| Tensile strength | MPa | ASTM D638 / ISO 527 |
| Elongation at break | % | ASTM D638 / ISO 527 |
| Impact strength (Izod) | J/m | ASTM D256 |
| Warpage | mm | visual / CMM |
| Surface roughness | µm | profilometer |

### Standards

- ASTM D638 — Tensile properties of plastics
- ISO 527 — Tensile test for plastics
- ASTM D256 — Izod impact resistance
- ISO 294 — Injection molding test specimens

## Experiment Type 2: Filler Reinforcement and Interface Design

Evaluate the effect of filler type, content, and surface treatment on mechanical and thermal properties of polymer composites.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Filler type | — | glass fiber, carbon fiber, nano-SiO2, CNT, clay, CaCO3, graphene |
| Filler content (wt%) | wt% | 5–50 (micro), 0.1–5 (nano) |
| Surface treatment | — | untreated, silane KH-550, MAH-g-PP, acid-treated |
| Mixing method | — | melt compounding, solution blending, in-situ polymerization |
| Mixing time (min) | min | 5–30 |
| Screw speed (rpm) | rpm | 50–200 (twin-screw extruder) |

| Response | Unit | Standard |
|----------|------|----------|
| Tensile strength | MPa | ASTM D638 |
| Tensile modulus | GPa | ASTM D638 |
| Flexural strength | MPa | ASTM D790 |
| Impact strength | J/m | ASTM D256 |
| HDT at 0.45 MPa | °C | ASTM D648 |
| Filler dispersion quality | — | SEM image rating (1–5) |

### Standards

- ASTM D638 — Tensile properties
- ASTM D790 — Flexural properties
- ASTM D256 — Impact resistance
- ASTM D648 — Heat deflection temperature
- ISO 178 — Flexural test for plastics

## Experiment Type 3: Thermo-Oxidative and UV Aging

Evaluate long-term thermal stability and UV resistance of polymers under accelerated aging conditions.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Stabilizer type | — | hindered amine (HALS), hindered phenol, phosphite, benzotriazole UV absorber |
| Stabilizer content (wt%) | wt% | 0.1–2.0 |
| Exposure type | — | thermal oven, UV chamber (ASTM G154), xenon arc (ASTM G155) |
| Exposure temperature (°C) | °C | 70–150 (thermal), 50–70 (UV panel) |
| Exposure duration (h) | h | 500, 1000, 2000, 3000 |
| Atmosphere | — | air, nitrogen |

| Response | Unit | Standard |
|----------|------|----------|
| Retained tensile strength | % | ASTM D638 (before/after) |
| Retained elongation at break | % | ASTM D638 |
| Carbonyl index (FTIR) | — | absorbance ratio 1715 cm⁻¹ / reference peak |
| Color change (ΔE) | — | ASTM D2244 |
| Weight loss | % | gravimetric |
| Tg shift | °C | DSC (ASTM D3418) |

### Standards

- ASTM G154 — Fluorescent UV lamp exposure
- ASTM G155 — Xenon arc exposure
- ASTM D3045 — Heat aging of plastics (no load)
- ASTM D2244 — Color difference calculation
- ISO 4892 — Plastics — Methods of exposure to laboratory light sources

## Experiment Type 4: Thermoset Cure Kinetics and Gel Point

Optimize the curing schedule of thermoset systems (epoxy, unsaturated polyester, phenolic) by mapping cure kinetics.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Hardener type | — | amine (DDS, DDM), anhydride (MNA), peroxide (BPO) |
| Hardener stoichiometric ratio | — | 0.7–1.2 (amine/epoxy equivalents) |
| Cure temperature (°C) | °C | 80–200 |
| Cure time (min) | min | 30–480 |
| Post-cure temperature (°C) | °C | 120–220 |
| Post-cure time (h) | h | 1–8 |

| Response | Unit | Standard |
|----------|------|----------|
| Gel time | min | ASTM D2471 (gel timer) |
| Degree of cure (DSC) | % | DSC residual enthalpy |
| Tg (onset) | °C | DSC (ASTM D3418) |
| Storage modulus (25°C) | MPa | DMA (ASTM D4065) |
| Gel content | % | solvent extraction (ASTM D2765) |
| Crosslink density | mol/m³ | swelling equilibrium (Flory–Rehner) |

### Standards

- ASTM D2471 — Gel time and peak exotherm of thermosetting resins
- ASTM D3418 — Tg and Tm by DSC
- ASTM D4065 — DMA measurement
- ASTM D2765 — Gel content of crosslinked plastics

## Typical Orthogonal Setup: PA6/GF Composite (L9)

4 factors, 3 levels each, 9 runs.

| Factor | Level 1 | Level 2 | Level 3 |
|--------|---------|---------|---------|
| Glass fiber content (wt%) | 10 | 20 | 30 |
| Melt temperature (°C) | 240 | 260 | 280 |
| Injection speed (mm/s) | 40 | 80 | 120 |
| Mold temperature (°C) | 40 | 80 | 120 |

| Run | GF (wt%) | Temp (°C) | Speed (mm/s) | Mold (°C) |
|-----|----------|-----------|--------------|-----------|
| 1 | 10 | 240 | 40 | 40 |
| 2 | 10 | 260 | 80 | 80 |
| 3 | 10 | 280 | 120 | 120 |
| 4 | 20 | 240 | 80 | 120 |
| 5 | 20 | 260 | 120 | 40 |
| 6 | 20 | 280 | 40 | 80 |
| 7 | 30 | 240 | 120 | 80 |
| 8 | 30 | 260 | 40 | 120 |
| 9 | 30 | 280 | 80 | 40 |

Responses: tensile strength, impact strength, warpage, surface roughness.

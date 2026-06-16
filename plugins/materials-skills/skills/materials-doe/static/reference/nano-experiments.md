# Nano Experiment Reference

Common experiment types, typical factor-response pairs, and standard references for nanomaterial research.

## Experiment Type 1: Nanoparticle Synthesis Optimization

Control size, morphology, and monodispersity of nanoparticles via wet-chemical synthesis.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Precursor concentration (mol/L) | mol/L | 0.001–0.5 |
| Reducing/capping agent ratio | — | 0.5–10 (agent:precursor) |
| Reaction temperature (°C) | °C | 25–300 |
| Reaction time (min) | min | 5–720 |
| pH | — | 2–12 |
| Stirring rate (rpm) | rpm | 200–1500 |

| Response | Unit | Standard |
|----------|------|----------|
| Mean particle size | nm | TEM / DLS (ISO 13321) |
| Polydispersity index (PDI) | — | DLS |
| Surface area (BET) | m²/g | ISO 9277 |
| Zeta potential | mV | electrophoretic light scattering |
| Yield | % | gravimetric |

### Standards

- ISO 13321 — Particle size analysis by DLS
- ISO 9277 — BET specific surface area
- ISO 22412 — Particle size analysis by DLS (updated)
- ASTM B822 — Particle size by light scattering

## Experiment Type 2: Nanocomposite Preparation and Property Enhancement

Evaluate the effect of nanofiller loading, dispersion method, and surface treatment on polymer or ceramic matrix composites.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Filler type | — | MMT clay, nano-SiO₂, CNT, graphene, nano-Al₂O₃, nano-TiO₂ |
| Filler loading (wt%) | wt% | 0.1–10 (nano), 5–50 (micro) |
| Surface treatment | — | silane, surfactant, polymer grafting, acid treatment |
| Dispersion method | — | ultrasonication, high-shear mixing, three-roll mill, in-situ polymerization |
| Dispersion time (min) | min | 5–120 |
| Matrix type | — | epoxy, PP, PA6, HDPE, PVA, alumina |

| Response | Unit | Standard |
|----------|------|----------|
| Tensile strength | MPa | ASTM D638 |
| Tensile modulus | GPa | ASTM D638 |
| Thermal conductivity | W/m·K | ASTM D5930 / laser flash |
| Tg (DSC) | °C | ASTM D3418 |
| Barrier permeability | cm³·mm/m²·d·atm | ASTM D1434 |
| Filler dispersion quality | — | TEM image rating |

### Standards

- ASTM D638 — Tensile properties
- ASTM D3418 — Tg by DSC
- ASTM D5930 — Thermal conductivity of plastics
- ASTM D1434 — Gas transmission rate

## Experiment Type 3: Thin Film Deposition and Characterization

Optimize thin film deposition parameters for optical, electrical, or functional coatings.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Deposition method | — | spin coating, dip coating, sputtering, CVD, ALD, PLD |
| Substrate type | — | Si wafer, glass, ITO, FTO, PET, sapphire |
| Deposition temperature (°C) | °C | 25–800 |
| Deposition time (min) | min | 1–120 |
| Precursor/Target | — | solution, solid target, gas precursor |
| Annealing condition | — | none, 300°C/1h in air, 500°C/2h in N₂ |

| Response | Unit | Standard |
|----------|------|----------|
| Film thickness | nm | profilometer / ellipsometry |
| Surface roughness (Ra) | nm | AFM |
| Optical band gap | eV | UV-Vis (Tauc plot) |
| Sheet resistance | Ω/sq | four-point probe |
| Transmittance (550 nm) | % | UV-Vis spectrophotometry |
| Crystallinity | — | XRD |

### Standards

- ISO 4524 — Electrodeposited metallic coatings
- ASTM E284 — Terminology of appearance
- ASTM F390 — Sheet resistance by four-point probe

## Typical Orthogonal Setup: AgNP Synthesis (L9)

4 factors, 3 levels each, 9 runs.

| Factor | Level 1 | Level 2 | Level 3 |
|--------|---------|---------|---------|
| AgNO₃ concentration (mmol/L) | 5 | 10 | 20 |
| Citrate:Ag molar ratio | 1.5 | 3.0 | 5.0 |
| Reaction temperature (°C) | 60 | 80 | 100 |
| Reaction time (min) | 15 | 30 | 60 |

| Run | AgNO₃ (mmol/L) | Citrate:Ag | Temp (°C) | Time (min) |
|-----|----------------|------------|-----------|------------|
| 1 | 5 | 1.5 | 60 | 15 |
| 2 | 5 | 3.0 | 80 | 30 |
| 3 | 5 | 5.0 | 100 | 60 |
| 4 | 10 | 1.5 | 80 | 60 |
| 5 | 10 | 3.0 | 100 | 15 |
| 6 | 10 | 5.0 | 60 | 30 |
| 7 | 20 | 1.5 | 100 | 30 |
| 8 | 20 | 3.0 | 60 | 60 |
| 9 | 20 | 5.0 | 80 | 15 |

Responses: mean particle size, PDI, zeta potential, UV-Vis peak wavelength.

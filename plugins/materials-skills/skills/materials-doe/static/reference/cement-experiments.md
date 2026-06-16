# Cement and Concrete Experiment Reference

Common experiment types, typical factor-response pairs, and standard references for cement, concrete, and supplementary cementitious materials (SCMs).

## Experiment Type 1: Mix Proportion Design

Optimize concrete mix proportions to achieve target strength, workability, and durability.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| Water-cement ratio | — | 0.30–0.60 |
| Cement content (kg/m³) | kg/m³ | 300–500 |
| Sand ratio (%) | % | 30–45 |
| Superplasticizer (%) | % | 0–2.0 |
| Coarse aggregate type | — | crushed stone, gravel, recycled |
| Maximum aggregate size (mm) | mm | 10, 16, 20, 25 |
| SCM type | — | fly ash, slag, silica fume |
| SCM replacement (%) | % | 0–40 |

| Response | Unit | Standard |
|----------|------|----------|
| 28-day compressive strength | MPa | ASTM C39 / GB/T 50081 |
| Slump | mm | ASTM C143 / GB/T 50080 |
| Air content (%) | % | ASTM C231 |
| Setting time | min | ASTM C191 / GB/T 1346 |
| Unit weight | kg/m³ | ASTM C138 |

### Standards

- ACI 211.1 — Standard practice for selecting proportions for normal concrete
- EN 206 — Concrete specification, performance, production and conformity
- GB/T 50080 — Standard for test method of performance on ordinary fresh concrete
- JGJ 55 — Specification for mix proportion design of ordinary concrete (Chinese)

## Experiment Type 2: Durability Testing

Evaluate concrete resistance to aggressive environments.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| w/c ratio | — | 0.35–0.55 |
| SCM type | — | fly ash, slag, silica fume, metakaolin |
| SCM replacement (%) | % | 0–40 |
| Curing condition | — | water, sealed, air, accelerated |
| Exposure type | — | chloride, sulfate, freeze-thaw, carbonation |
| Exposure duration | days | 28, 56, 90, 180, 365 |

| Response | Unit | Standard |
|----------|------|----------|
| Chloride migration coefficient | ×10⁻¹² m²/s | NT Build 492 / GB/T 50082 |
| Depth of carbonation | mm | GB/T 50082 |
| Mass loss after freeze-thaw | % | ASTM C666 / GB/T 50082 |
| Expansion after sulfate attack | % | ASTM C1012 |
| Compressive strength after exposure | MPa | ASTM C39 |
| Rapid chloride permeability | Coulombs | ASTM C1202 |

### Standards

- ASTM C666 — Resistance of concrete to rapid freezing and thawing
- ASTM C1012 — Length change of hydraulic-cement mortars exposed to sulfate solution
- ASTM C1202 — Electrical indication of concrete's ability to resist chloride penetration
- NT Build 492 — Chloride migration coefficient from non-steady-state migration
- GB/T 50082 — Standard for test methods of long-term performance and durability of ordinary concrete

## Experiment Type 3: Supplementary Cementitious Materials (SCMs)

Evaluate the effect of SCMs on fresh and hardened properties of concrete or mortar.

### Factors and Responses

| Factor | Unit | Typical Range |
|--------|------|---------------|
| SCM type | — | fly ash (Class F/C), slag, silica fume, metakaolin |
| Replacement level (%) | % | 5, 10, 15, 20, 30, 40 |
| Fineness (m²/kg) | m²/kg | 300–600 |
| w/b ratio | — | 0.35–0.50 |
| Curing temperature (°C) | °C | 20, 40, 60 |
| Curing age (days) | days | 3, 7, 28, 56, 90 |

| Response | Unit | Standard |
|----------|------|----------|
| Compressive strength | MPa | ASTM C39 |
| Activity index | % | ASTM C311 / GB/T 1596 |
| Water demand ratio | % | GB/T 1596 |
| Setting time | min | ASTM C191 |
| Heat of hydration | J/g | ASTM C1702 |
| Pozzolanic activity | — | EN 196-5 |

### Standards

- ASTM C618 — Fly ash and raw calcined natural pozzolan
- ASTM C989 — Ground granulated blast-furnace slag
- ASTM C1240 — Silica fume
- GB/T 1596 — Fly ash for cement and concrete (Chinese)
- GB/T 18046 — Ground granulated blast furnace slag used in cement and concrete (Chinese)

## Typical Orthogonal Setup: Concrete Durability (L9)

4 factors, 3 levels each, 9 runs.

| Factor | Level 1 | Level 2 | Level 3 |
|--------|---------|---------|---------|
| w/c ratio | 0.38 | 0.43 | 0.48 |
| Fly ash replacement (%) | 10 | 20 | 30 |
| Silica fume replacement (%) | 0 | 3 | 6 |
| Curing temperature (°C) | 20 | 35 | 50 |

| Run | w/c | Fly ash (%) | Silica fume (%) | Temp (°C) |
|-----|-----|------------|----------------|-----------|
| 1 | 0.38 | 10 | 0 | 20 |
| 2 | 0.38 | 20 | 3 | 35 |
| 3 | 0.38 | 30 | 6 | 50 |
| 4 | 0.43 | 10 | 3 | 50 |
| 5 | 0.43 | 20 | 6 | 20 |
| 6 | 0.43 | 30 | 0 | 35 |
| 7 | 0.48 | 10 | 6 | 35 |
| 8 | 0.48 | 20 | 0 | 50 |
| 9 | 0.48 | 30 | 3 | 20 |

Responses: 28-day compressive strength, chloride migration coefficient, water absorption.

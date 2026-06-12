# General Materials Experiment Reference

Applicable materials, common factor types, and standard experiment flow for materials not covered by domain-specific references.

## Applicable Materials

This reference covers materials that do not fall into the specific domains of asphalt, cement/concrete, ceramics, or thermal insulation:

- Polymers and polymer composites (FRP, epoxy systems, adhesives)
- Geopolymer and alkali-activated materials
- Fiber-reinforced cementitious composites (UHPC, SHCC, ECC)
- Grouting materials and sealants
- Surface coatings and protective treatments
- Corrosion inhibitors and waterproofing agents
- Recycled aggregate and reclaimed materials
- Soil stabilization additives (lime, cement, polymers)
- 3D-printed construction materials
- Self-healing materials and microcapsule systems

## Common Factor Types

### Material composition factors

| Factor | Unit | Examples |
|--------|------|----------|
| Binder content | kg/m³ or % | cement, resin, asphalt |
| Additive dosage | % by mass | superplasticizer, accelerator, retarder |
| Filler content | % | silica fume, fly ash, nanomaterials |
| Fiber volume fraction | % | steel, glass, PVA, basalt |
| Water-binder ratio | — | 0.25–0.55 |
| Solids content | % | for emulsions, dispersions |

### Process factors

| Factor | Unit | Examples |
|--------|------|----------|
| Mixing time | min | 2–30 |
| Mixing speed | rpm | 100–3000 |
| Mixing method | — | hand, mechanical, high-shear |
| Casting method | — | poured, sprayed, extruded, printed |

### Curing and conditioning factors

| Factor | Unit | Examples |
|--------|------|----------|
| Curing temperature | °C | 20–80 (standard: 23 ± 2) |
| Curing humidity | % | 50–100 (standard: ≥95 for moist cure) |
| Curing duration | days | 1, 3, 7, 28, 56, 90 |
| Curing regime | — | water, sealed, air, steam, autoclave |
| Pre-conditioning | — | oven-dry, saturated, freeze-thaw cycled |

### Environmental exposure factors

| Factor | Unit | Examples |
|--------|------|----------|
| Exposure temperature | °C | -20 to 60 |
| Exposure duration | days | 28–365 |
| Chemical environment | — | chloride, sulfate, acid, alkaline |
| Mechanical loading | — | static, cyclic, sustained |

## Common Response Variables

### Mechanical properties

| Response | Unit | Typical Standard |
|----------|------|-----------------|
| Compressive strength | MPa | ASTM C39, ISO 679 |
| Tensile strength | MPa | ASTM C496, ISO 527 |
| Flexural strength | MPa | ASTM C78, ISO 178 |
| Elastic modulus | GPa | ASTM C469, ISO 527 |
| Bond strength | MPa | ASTM C1583 |
| Fracture toughness | MPa·m^½ | ASTM E399 |

### Durability properties

| Response | Unit | Typical Standard |
|----------|------|-----------------|
| Water absorption | % | ASTM C642 |
| Porosity | % | ASTM C642 |
| Chloride permeability | Coulombs | ASTM C1202 |
| Carbonation depth | mm | GB/T 50082 |
| Freeze-thaw resistance | % mass/strength loss | ASTM C666 |

### Fresh-state / workability

| Response | Unit | Typical Standard |
|----------|------|-----------------|
| Slump | mm | ASTM C143 |
| Flow | % | ASTM C230 |
| Setting time | min | ASTM C191 |
| Viscosity | mPa·s | ASTM D2196 |
| Pot life | min | — |

## Standard Experiment Flow

### Phase 1: Literature Review

1. Search for prior studies on the material system.
2. Identify commonly used factors, ranges, and levels.
3. Note which factors are reported as most influential.
4. Collect standard test methods and acceptance criteria.

### Phase 2: Screening Experiment

5. Select 3–6 candidate factors from literature.
6. Use a small orthogonal array (L9 for ≤4 factors) or fractional factorial to screen.
7. Identify the 2–3 most influential factors (largest range R or significant F in ANOVA).
8. Eliminate factors with negligible effect.

### Phase 3: Optimization Experiment

9. Refine the range of the 2–3 significant factors.
10. Use a denser orthogonal array (L16, L25) or response surface methodology (RSM).
11. Fit a regression model (linear, quadratic, or interaction terms).
12. Predict the optimal factor combination.

### Phase 4: Confirmation Experiment

13. Conduct 3–5 replications at the predicted optimal combination.
14. Compare the mean response to the predicted value.
15. If the confirmation result falls within the prediction interval, accept the optimum.
16. If not, investigate possible interactions or expand the factor range.

### Phase 5: Sensitivity Analysis

17. Vary each optimal factor by ±1 level while holding others at optimum.
18. Quantify the sensitivity of the response to each factor.
19. Report the robustness of the optimum — small sensitivity indicates a robust design.

## Decision Table: Which Design to Use

| Scenario | Recommended Design | Runs |
|----------|--------------------|------|
| 3–4 factors, screening only | L9 orthogonal | 9 |
| 4 factors, interaction suspected | Full factorial (3^4 = 81 or 2^4 = 16) | 16–81 |
| 5–6 factors, screening only | L16 or L25 orthogonal | 16–25 |
| 2–3 factors, optimization | Central composite (RSM) | 9–15 |
| 1 factor, detailed characterization | Single-factor with 4–5 levels | 12–20 (with replications) |
| Proportions that sum to 100% | Simplex mixture design | 7–15 |

# Golden Sample: Thermal Insulation Materials

> **Coverage Tier**: 🟡 partial  
> **Registry entry**: `_shared/material-registry/entries/thermal-insulation.yaml`  
> **Domain fragment**: `skills/materials-research/static/fragments/domain/thermal-insulation.md`  
> **Narrative guide**: `skills/materials-writing/references/thermal-insulation-narrative.md`  
> **Reviewer criteria**: `skills/materials-reviewer/references/insulation-reviewer-criteria.md`

Covers aerogels, foams, fibrous insulation, vacuum insulation panels (VIPs),
phase-change materials (PCMs), and related thermal management materials.

**Status**: partial → the narrative guide, reviewer criteria, and 4 figure
scripts exist. To reach 🟢 full, add an example data package and one
end-to-end showcase workflow.

---

## 🔍 1. Search Strategy

| Layer | Boolean query | Target databases |
|---|---|---|
| Performance | `(aerogel OR "silica aerogel") AND "thermal conductivity" AND lambda` | Scopus, Web of Science |
| Mechanical | `(aerogel OR foam) AND (compressive OR mechanical) AND insulation` | Scopus, ScienceDirect |
| Moisture | `(aerogel OR "mineral wool") AND (hygrothermal OR moisture uptake) AND insulation` | Scopus, Taylor & Francis |
| Sustainability | `("vacuum insulation" OR VIP) AND LCA AND building` | Scopus, Building and Environment |

## 📖 2. Reader Package

After search, `materials-reader` produces a standard reader package with:

| Claim type | Evidence needed | Common reviewer risk |
|---|---|---|
| Low thermal conductivity | Lambda value with mean temperature | Reporting conductivity without temperature |
| Mechanical integrity | Compressive strength at 10% strain | No stress-strain curve, only max stress |
| Moisture resistance | Conductivity after humidity exposure | Claiming hydrophobicity without contact angle data |
| Building applicability | Fire rating, aging data | "Suitable for building" without fire or aging test |

## 📊 3. Evidence Matrix

| Claim | Evidence required | Typical values | Figure archetype |
|---|---|---|---|
| Low λ | Heat flow meter (ASTM C518) | 0.015–0.030 W/(m·K) | `conductivity_vs_density` |
| Mechanical support | Compressive test (ASTM C165) | 10–500 kPa | `insulation_stress_strain` |
| Thermal stability | TGA up to 800 °C | 5% mass loss temp | `tga_curve` |
| Moisture effect | λ at 50% / 90% RH | +0–30% increase | `conductivity_vs_temperature` |

## 🧪 4. Experiment Design

| Factor | Levels | Response |
|---|---|---|
| Density (kg/m³) | 50, 100, 150, 200 | λ, compressive strength |
| Temperature (°C) | 10, 25, 40, 60 | λ, thermal diffusivity |
| RH (%) | 0, 50, 90 | λ increase, moisture uptake |

## 📈 5. Typical Figures

Available scripts:

| Script | Output |
|---|---|
| `plot_insulation_conductivity_vs_density.py` | λ vs. density scatter |
| `plot_insulation_conductivity_vs_temp.py` | λ vs. temperature at multiple RH levels |
| `plot_insulation_stress_strain.py` | Compressive stress-strain curve |
| `plot_insulation_multipanel.py` | 3-panel: density + humidity + stress-strain |

## ⚠️ 6. Reviewer Risks

| Risk | How to avoid |
|---|---|
| Reporting λ without mean temperature | Always state: "λ = 0.028 W/(m·K) at T_mean = 25 °C" |
| Claiming "superinsulating" | Only if λ < 0.020 W/(m·K) at stated conditions |
| No moisture data for building claim | Measure λ at ≥2 RH levels |
| Bench marking against wrong material | Compare with same-class commercial products |

## 📝 7. Submission Advice

| Journal | Fit | Notes |
|---|---|---|
| Energy and Buildings | 🟢 Strong | Building insulation + energy |
| Building and Environment | 🟢 Strong | Hygrothermal + indoor environment |
| Cement and Concrete Composites | 🟡 If cement-based foam | Cementitious matrix |
| ACS Applied Materials & Interfaces | 🟡 Novel aerogel | Advanced materials focus |

---

## Next Steps to Reach 🟢 Full

1. Create an example data package in `skills/materials-figure/examples/figure-packages/`
2. Add a worked workflow output in `outputs/`
3. Create a ceramic-composites variant of the figure scripts

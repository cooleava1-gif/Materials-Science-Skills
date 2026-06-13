# Golden Sample: Polymer Composites (FRP/CFRP/GFRP)

> **Coverage Tier**: 🟡 partial
> **Registry entry**: `_shared/material-registry/entries/polymer-composites.yaml`
> **Domain fragment**: `skills/materials-research/static/fragments/domain/polymer-composites.md`
> **Narrative guide**: `skills/materials-writing/references/polymer-composites-narrative.md`
> **Reviewer criteria**: `skills/materials-reviewer/references/polymers-reviewer-criteria.md`

Covers carbon-, glass-, and aramid-fiber reinforced polymer composites for
aerospace, automotive, wind energy, and civil infrastructure applications.

**Status**: partial → narrative guide + reviewer criteria + generic figure
scripts exist. To reach 🟢 full, add dedicated composite figure scripts
(laminate orientation bars, delamination resistance, fatigue S-N curves)
and an example data package.

---

## 🔍 1. Search Strategy

| Layer | Boolean query | Target databases |
|---|---|---|
| Performance | `(CFRP OR GFRP) AND (tensile OR flexural) AND (laminate OR composite)` | Scopus, Web of Science, Compendex |
| Interface | `(fiber-matrix OR interface OR ILSS) AND (CFRP OR GFRP) AND (silane OR sizing)` | Scopus, ScienceDirect |
| Fatigue | `(CFRP OR GFRP) AND fatigue AND (S-N OR delamination)` | Scopus, Taylor & Francis |
| Durability | `(CFRP OR GFRP) AND (moisture OR hygrothermal OR UV) AND (aging OR durability)` | Scopus, ASTM journals |

## 📖 2. Reader Package

| Claim type | Evidence needed | Common reviewer risk |
|---|---|---|
| High specific strength | Tensile test (ASTM D3039), 0° and 90° | Only testing in fiber direction |
| Interface quality | ILSS (ASTM D2344) + SEM fracture surface | Claiming interface improvement without SEM |
| Fatigue resistance | S-N curve with R-ratio, frequency | Only run-out data, no stiffness degradation |
| Environmental durability | Conditioned testing (moisture, temp) | "Durability" from un-conditioned coupons only |

## 📊 3. Evidence Matrix

| Claim | Evidence required | Typical values | Figure archetype |
|---|---|---|---|
| Tensile strength 0° | ASTM D3039, 5+ replicates | 500–3500 MPa | `stress_strain` |
| Flexural modulus | ASTM D7264, span-to-thickness 32:1 | 50–200 GPa | `stress_strain` |
| ILSS | ASTM D2344, short-beam shear | 30–100 MPa | grouped bar |
| Fiber volume fraction | ASTM D3171 (digestion) | 40–70% | stacked bar |
| DMA Tg | ASTM D4065, tan δ peak | 100–250 °C | `dsc_curve` |

## 🧪 4. Experiment Design

| Factor | Levels | Response |
|---|---|---|
| Fiber orientation | 0°, ±45°, 90°, [0/90]s, quasi-isotropic | Tensile, flexural, ILSS |
| Fiber volume (%) | 40, 50, 60, 70 | Stiffness, strength, cost |
| Environmental conditioning | Dry, 85% RH @70°C, freeze-thaw | Retention ratio |
| Impact energy (J) | 10, 25, 50, 100 | CAI (compression after impact) |

## 📈 5. Typical Figures

Available generic scripts (adaptable with COLUMN_MAP):

| Script | Output | Data needed |
|---|---|---|
| `plot_stress_strain.py` | Stress-strain curves with yield/UTS annotation | strain, multiple sample columns |
| `plot_mechanical_property_radar.py` | Multi-property radar for formulation comparison | normalized property scores |
| `plot_dsc_curve.py` | DSC thermal transitions (Tg, Tm, Tc) | temperature, heat flow |

Recommended additions to reach 🟢 full:
- `plot_laminate_strength.py`: grouped bar for [0], [90], [±45], [0/90]s layups
- `plot_sn_curve.py`: fatigue S-N curve with run-out markers
- `plot_cai_comparison.py`: compression-after-impact bar chart

## ⚠️ 6. Reviewer Risks

| Risk | How to avoid |
|---|---|
| "0° tensile strength reported as material strength" | Always report 0°, 90°, and shear properties |
| "Interface improved" without SEM or ILSS | Show both ILSS data + SEM fracture surface |
| "Fatigue resistant" from static-only data | Need S-N curve with ≥3 stress levels |
| "No delamination" under flexure | Report acoustic emission or C-scan if available |
| Moisture absorption % without mechanical retention | Always pair weight gain with mechanical retention |

## 📝 7. Submission Advice

| Journal | Fit | Notes |
|---|---|---|
| Composites Part A: Applied Science | 🟢 Strong | Processing + properties |
| Composites Part B: Engineering | 🟢 Strong | Structural applications |
| Composite Structures | 🟢 Strong | Mechanics + design |
| Journal of Composite Materials | 🟢 Strong | Broad scope |
| ACS Applied Materials & Interfaces | 🟡 If novel interface | Chemistry-heavy |

---

## Next Steps to Reach 🟢 Full

1. Create `plot_laminate_strength.py` with COLUMN_MAP support
2. Create `plot_sn_curve.py` for fatigue data
3. Create a sample figure package in `skills/materials-figure/examples/figure-packages/`
4. Add composite-specific data CSVs in `figures4materials/data/`

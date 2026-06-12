# Materials Expansion Design: Civil → General Materials Science

**Date**: 2026-06-12
**Status**: Draft
**Scope**: Expand from civil-engineering-only to general materials science, keeping civil as a subdomain.

## 1. Goal

Expand the Materials Science Skills bundle from civil-engineering materials (asphalt, cement, ceramics, insulation) to a general materials science platform covering:

- **Civil/construction** (existing, kept as subdomain)
- **Polymers** (thermoplastics, thermosets, rubber, polymer composites)
- **Metals** (ferrous, nonferrous, high-temperature alloys, additive manufacturing)
- **Ceramics** (structural, functional, refractories, bioceramics)
- **Functional/electronic** (semiconductors, dielectrics, piezoelectrics, photonics)
- **Nanomaterials** (nanoparticles, thin films, 2D materials, nanocomposites)

## 2. Architecture Change: Two-Layer Domain Routing

### 2.1 Current State

Single `domain` axis with 9 values, all civil-oriented:

```
domain:
  asphalt-pavement | cement-concrete | construction-materials | steel-metal |
  geotechnical-materials | timber-masonry | waterproofing-sealants |
  sustainability-durability | civil-generic
```

### 2.2 New State: Two Independent Axes

**Axis 1: `material_family`** (new, coarse-grained)

| Value | Description | Triggers |
|---|---|---|
| `civil` | Civil/construction materials | civil, construction, building, 土木, 建筑 |
| `polymers` | Polymers and polymer-based | polymer, resin, rubber, epoxy, 高分子, 聚合物, 树脂 |
| `metals` | Metallic materials | metal, alloy, steel, aluminum, 金属, 合金, 钢 |
| `ceramics` | Ceramic materials | ceramic, porcelain, refractory, 陶瓷, 耐火 |
| `functional` | Functional/electronic materials | semiconductor, dielectric, piezoelectric, 半导体, 介电, 压电 |
| `nano` | Nanomaterials | nano, nanoparticle, 2D material, 纳米, 纳米材料 |
| `general` | Fallback | general, materials, 通用 |

**Axis 2: `domain`** (existing, now fine-grained, grouped by family)

Civil family (existing 9 values):
- `asphalt-pavement`, `cement-concrete`, `construction-materials`, `steel-metal`, `geotechnical-materials`, `timber-masonry`, `waterproofing-sealants`, `sustainability-durability`, `civil-generic` (kept as civil family fallback)

Polymers family (new 4 values):
- `thermoplastics` — PE, PP, PET, nylon, PEEK
- `thermosets` — epoxy, phenolic, polyimide
- `rubber-elastomers` — natural rubber, SBR, silicone
- `polymer-composites` — fiber-reinforced, particle-filled

Metals family (new 4 values):
- `ferrous-alloys` — carbon steel, stainless, tool steel
- `nonferrous-alloys` — aluminum, copper, magnesium
- `high-temperature-alloys` — superalloys, Ni-based, Ti alloys
- `additive-metals` — AM process-microstructure-properties

Ceramics family (new 4 values):
- `structural-ceramics` — alumina, zirconia, SiC
- `functional-ceramics` — piezo, ferroelectric, LTCC
- `refractories` — high-temperature linings
- `bioceramics` — hydroxyapatite, bioactive glass

Functional family (new 3 values):
- `semiconductors` — Si, GaAs, perovskites
- `dielectrics-piezoelectrics` — capacitors, actuators
- `photonic-optoelectronic` — LEDs, solar cells, photodetectors

Nano family (new 4 values):
- `nanoparticles` — synthesis, characterization, applications
- `nano-thin-films` — deposition, epitaxy, multilayers
- `2d-materials` — graphene, MoS2, MXenes
- `nanocomposites` — polymer-matrix, ceramic-matrix

General (new 1 value):
- `general-materials` — universal fallback, not family-specific

**Total**: 7 families, 29 specific domains (9 existing civil + 20 new).

### 2.3 Routing Logic

1. `material_family` is detected first from user input keywords
2. `domain` is detected within the family context
3. If no family matches, fall back to `general`
4. If family is detected but no specific domain, use the family-level fragment

## 3. Journal Expansion

### 3.1 Civil Journals (trimmed to 5)

| Keep | Remove | Move to ceramics |
|---|---|---|
| CBM, CCC, CSCM, JBE, RMPD/IJPE | JRE, CBM-transportation | JACerS, Ceramics International |

### 3.2 New Top-Tier Journals (~8)

| Journal | Family | Fragment file |
|---|---|---|
| Nature Materials | all | `nature-materials.md` |
| Advanced Materials | all | `advanced-materials.md` |
| ACS Nano | nano | `acs-nano.md` |
| Nano Letters | nano | `nano-letters.md` |
| Advanced Functional Materials | functional | `advanced-functional-materials.md` |
| J. Mater. Chem. A | functional/energy | `jmca.md` |
| Progress in Polymer Science | polymers | `progress-polymer-science.md` |
| Acta Materialia | metals | `acta-materialia.md` |

### 3.3 Total: ~15 journal formats

5 (civil) + 2 (ceramics, existing) + 8 (new) = 15

## 4. Reviewer Criteria Files

### 4.1 Existing (5 files, keep)
- `asphalt-reviewer-criteria.md`
- `cement-reviewer-criteria.md`
- `ceramics-reviewer-criteria.md`
- `insulation-reviewer-criteria.md`
- `editorial-criteria.md`

### 4.2 New (5 files)
- `polymers-reviewer-criteria.md`
- `metals-reviewer-criteria.md`
- `functional-reviewer-criteria.md`
- `nano-reviewer-criteria.md`
- `materials-general-reviewer-criteria.md` (universal cross-domain)

Total: 10 reviewer criteria files.

## 5. Generic Figure Scripts

Keep existing 4 domain-specific scripts. Add generic materials science plots:

| Script | Purpose | Applicable families |
|---|---|---|
| `plot_stress_strain.py` | Tensile/compressive curves | metals, polymers, ceramics, composites |
| `plot_xrd_pattern.py` | X-ray diffraction patterns | all crystalline materials |
| `plot_dsc_tga.py` | Thermal analysis (DSC/TGA) | polymers, ceramics, general |
| `plot_particle_size.py` | Particle size distribution | nano, ceramics, general |
| `plot_eis.py` | Electrochemical impedance spectroscopy | functional, energy |
| `plot_cv.py` | Cyclic voltammetry | functional, energy |

Total: 32 existing + 6 new = 38 figure scripts.

## 6. Manifest Changes

Every skill's `manifest.yaml` gets a new `material_family` axis:

```yaml
material_family:
  detect: "Which materials family is central?"
  default: general
  values:
    civil:
      path: static/fragments/domain/civil-family.md
      triggers: ["civil", "construction", "building", "pavement", "土木", "建筑"]
    polymers:
      path: static/fragments/domain/polymers-family.md
      triggers: ["polymer", "resin", "rubber", "epoxy", "高分子", "聚合物"]
    metals:
      path: static/fragments/domain/metals-family.md
      triggers: ["metal", "alloy", "steel", "金属", "合金"]
    ceramics:
      path: static/fragments/domain/ceramics-family.md
      triggers: ["ceramic", "porcelain", "陶瓷", "耐火"]
    functional:
      path: static/fragments/domain/functional-family.md
      triggers: ["semiconductor", "dielectric", "半导体", "介电"]
    nano:
      path: static/fragments/domain/nano-family.md
      triggers: ["nano", "nanoparticle", "纳米"]
    general:
      path: static/fragments/domain/general-materials.md
      triggers: ["materials", "通用"]
```

## 7. Brand and Documentation Updates

- **README.md**: "civil engineering and construction-materials research" → "materials science research"
- **_shared/core/stance.md**: "civil materials" → "materials science"
- **_shared/core/source-basis.md**: expand source types beyond civil journals
- **docs/skills-index.md**: update domain descriptions

## 8. Implementation Order

1. Create `material_family` axis fragment files (7 files)
2. Create new `domain` fragment files (20 files)
3. Update all 11 skill manifests with `material_family` axis
4. Add new journal format files (8 files)
5. Add new reviewer criteria files (5 files)
6. Add generic figure scripts (6 files)
7. Update shared core files (stance, source-basis)
8. Update README and docs
9. Update tests
10. Run release checks

## 9. Risk and Mitigation

| Risk | Mitigation |
|---|---|
| Manifest axis count grows, routing becomes slower | `material_family` has `default: general`, only 7 values |
| New domains lack real examples | Use synthetic data only (existing rule) |
| Figure scripts for unfamiliar domains | Keep scripts generic, not domain-specific |
| Test count explosion | Reuse test patterns from existing domains |

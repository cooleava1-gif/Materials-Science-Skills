# Materials Coverage Dashboard

> **Honest coverage**: this bundle is strongest where the author has direct
> research experience (asphalt emulsions, WER-EA, pavement materials). Other
> domains have structural support (trigger routing, registry, templates) but
> less material-specific depth. The tier tells you what to expect.

## Coverage by Material System

| Material System | Family | Tier | Narrative Guide | Reviewer Criteria | Figure Scripts | Example Package |
|---|---|---|---|---|---|---|
| **asphalt-pavement** | civil | 🟢 **full** | ✅ asphalt-pavement-narrative | ✅ asphalt-reviewer-criteria | ✅ 21 scripts | ✅ 3 packages |
| **cement-concrete** | civil | 🟡 **partial** | ✅ cement-concrete-narrative | ✅ cement-reviewer-criteria | — | — |
| **construction-materials** | civil | ⚪ **generic** | — | — | — | — |
| **steel-metal** | civil | 🔵 **skeleton** | ✅ steel-metal-narrative | — | ✅ 2 generic | — |
| **geotechnical-materials** | civil | 🔵 **skeleton** | ✅ geotechnical-materials-narrative | — | — | — |
| **timber-masonry** | civil | 🔵 **skeleton** | ✅ timber-masonry-narrative | — | — | — |
| **waterproofing-sealants** | civil | 🔵 **skeleton** | ✅ waterproofing-sealants-narrative | — | — | — |
| **sustainability-durability** | civil | 🔵 **skeleton** | ✅ sustainability-durability-narrative | — | ✅ 2 generic | — |
| **thermal-insulation** | civil | 🟡 **partial** | ✅ thermal-insulation-narrative | ✅ insulation-reviewer-criteria | ✅ 4 scripts | — |
| **civil-generic** | civil | ⚪ **generic** | — | — | — | — |
| **thermoplastics** | polymers | 🟡 **partial** | ✅ thermoplastics-narrative | ✅ polymers-reviewer-criteria | ✅ 3 generic | — |
| **thermosets** | polymers | 🟡 **partial** | ✅ thermosets-narrative | ✅ polymers-reviewer-criteria | ✅ 2 generic | — |
| **rubber-elastomers** | polymers | 🟡 **partial** | ✅ rubber-elastomers-narrative | ✅ polymers-reviewer-criteria | ✅ 1 generic | — |
| **polymer-composites** | polymers | 🟡 **partial** | ✅ polymer-composites-narrative | ✅ polymers-reviewer-criteria | ✅ 2 generic | — |
| **ferrous-alloys** | metals | 🔵 **skeleton** | ✅ ferrous-alloys-narrative | ✅ metals-reviewer-criteria | ✅ 2 generic | — |
| **nonferrous-alloys** | metals | 🔵 **skeleton** | ✅ nonferrous-alloys-narrative | ✅ metals-reviewer-criteria | ✅ 1 generic | — |
| **high-temperature-alloys** | metals | 🔵 **skeleton** | ✅ high-temperature-alloys-narrative | ✅ metals-reviewer-criteria | ✅ 1 generic | — |
| **additive-metals** | metals | 🔵 **skeleton** | ✅ additive-metals-narrative | ✅ metals-reviewer-criteria | ✅ 1 generic | — |
| **structural-ceramics** | ceramics | 🟡 **partial** | ✅ structural-ceramics-narrative | ✅ ceramics-reviewer-criteria | ✅ 5 scripts | ✅ 2 packages |
| **functional-ceramics** | ceramics | 🔵 **skeleton** | ✅ functional-ceramics-narrative | ✅ ceramics-reviewer-criteria | ✅ 2 generic | — |
| **refractories** | ceramics | 🔵 **skeleton** | ✅ refractories-narrative | ✅ ceramics-reviewer-criteria | ✅ 1 generic | — |
| **bioceramics** | ceramics | 🔵 **skeleton** | ✅ bioceramics-narrative | ✅ ceramics-reviewer-criteria | ✅ 2 generic | — |
| **semiconductors** | functional | 🔵 **skeleton** | ✅ semiconductors-narrative | ✅ functional-reviewer-criteria | — | — |
| **dielectrics-piezoelectrics** | functional | 🔵 **skeleton** | ✅ dielectrics-piezoelectrics-narrative | ✅ functional-reviewer-criteria | ✅ 1 generic | — |
| **photonic-optoelectronic** | functional | 🔵 **skeleton** | ✅ photonic-optoelectronic-narrative | ✅ functional-reviewer-criteria | — | — |
| **nanoparticles** | nano | 🔵 **skeleton** | ✅ nanoparticles-narrative | ✅ nano-reviewer-criteria | — | — |
| **nano-thin-films** | nano | 🔵 **skeleton** | ✅ nano-thin-films-narrative | ✅ nano-reviewer-criteria | ✅ 1 generic | — |
| **2d-materials** | nano | 🔵 **skeleton** | ✅ 2d-materials-narrative | ✅ nano-reviewer-criteria | — | — |
| **nanocomposites** | nano | 🔵 **skeleton** | ✅ nanocomposites-narrative | ✅ nano-reviewer-criteria | ✅ 2 generic | — |

## Tier Definitions

| Tier | Emoji | Meaning | What you get |
|---|---|---|---|
| **full** | 🟢 | Battle-tested | Narrative guide + figure scripts + reviewer criteria + example packages + hand-crafted content |
| **partial** | 🟡 | Structured support | Narrative guide + at least one of (figure scripts, reviewer criteria) |
| **skeleton** | 🔵 | Routable | Domain fragment + auto-generated narrative guide (may need human editing) |
| **generic** | ⚪ | Scoped fallback | Family-level guidance, no material-specific content |

## How to Read This

- **Full** materials: route to them confidently. Everything has been tested end-to-end.
- **Partial** materials: the structure is there but you may need to fill in domain-specific details.
- **Skeleton** materials: routing works and a template narrative exists, but depth comes from family-level infrastructure.
- **Generic**: family-scoped fallback for civil/construction topics that do not match a deeper domain.

## How Tiers Evolve

A material moves up tiers when a researcher contributes:
1. **skeleton → partial**: a reviewed narrative guide + one figure script or data schema
2. **partial → full**: end-to-end example package + reviewer criteria + figure script suite

See `_shared/material-registry/` for the current registry entries and
`_shared/triggers/` for the routing keyword files.

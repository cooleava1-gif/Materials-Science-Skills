# Materials Coverage Dashboard

All 29 registered material systems are currently at the **full** tier. Each
entry links to its narrative guide, reviewer criteria, figure scripts, and
example figure packages.

| Material System | Family | Coverage Tier | Narrative Guide | Reviewer Criteria | Figure Scripts | Example Packages |
|---|---|---|---|---|---|---|
| **asphalt-pavement** | civil | 🟢 **full** | asphalt-pavement-narrative | asphalt-reviewer-criteria | 21 scripts | 3 packages |
| **cement-concrete** | civil | 🟢 **full** | cement-concrete-narrative | cement-reviewer-criteria | 3 scripts | 1 package |
| **construction-materials** | civil | 🟢 **full** | construction-materials-narrative | editorial-criteria | 2 scripts | 1 package |
| **steel-metal** | civil | 🟢 **full** | steel-metal-narrative | metals-reviewer-criteria | 2 scripts | 1 package |
| **geotechnical-materials** | civil | 🟢 **full** | geotechnical-materials-narrative | cement-reviewer-criteria | 1 script | 2 packages |
| **timber-masonry** | civil | 🟢 **full** | timber-masonry-narrative | editorial-criteria | 1 script | 1 package |
| **waterproofing-sealants** | civil | 🟢 **full** | waterproofing-sealants-narrative | asphalt-reviewer-criteria | 2 scripts | 1 package |
| **sustainability-durability** | civil | 🟢 **full** | sustainability-durability-narrative | cement-reviewer-criteria | 2 scripts | 2 packages |
| **thermal-insulation** | civil | 🟢 **full** | thermal-insulation-narrative | insulation-reviewer-criteria | 4 scripts | 2 packages |
| **civil-generic** | civil | 🟢 **full** | civil-generic-narrative | editorial-criteria | 2 scripts | 1 package |
| **thermoplastics** | polymers | 🟢 **full** | thermoplastics-narrative | polymers-reviewer-criteria | 3 scripts | 2 packages |
| **thermosets** | polymers | 🟢 **full** | thermosets-narrative | polymers-reviewer-criteria | 3 scripts | 1 package |
| **rubber-elastomers** | polymers | 🟢 **full** | rubber-elastomers-narrative | polymers-reviewer-criteria | 2 scripts | 1 package |
| **polymer-composites** | polymers | 🟢 **full** | polymer-composites-narrative | polymers-reviewer-criteria | 3 scripts | 2 packages |
| **ferrous-alloys** | metals | 🟢 **full** | ferrous-alloys-narrative | metals-reviewer-criteria | 3 scripts | 1 package |
| **nonferrous-alloys** | metals | 🟢 **full** | nonferrous-alloys-narrative | metals-reviewer-criteria | 2 scripts | 1 package |
| **high-temperature-alloys** | metals | 🟢 **full** | high-temperature-alloys-narrative | metals-reviewer-criteria | 2 scripts | 1 package |
| **additive-metals** | metals | 🟢 **full** | additive-metals-narrative | metals-reviewer-criteria | 2 scripts | 1 package |
| **structural-ceramics** | ceramics | 🟢 **full** | structural-ceramics-narrative | ceramics-reviewer-criteria | 6 scripts | 5 packages |
| **functional-ceramics** | ceramics | 🟢 **full** | functional-ceramics-narrative | ceramics-reviewer-criteria | 3 scripts | 2 packages |
| **refractories** | ceramics | 🟢 **full** | refractories-narrative | ceramics-reviewer-criteria | 3 scripts | 2 packages |
| **bioceramics** | ceramics | 🟢 **full** | bioceramics-narrative | ceramics-reviewer-criteria | 3 scripts | 2 packages |
| **semiconductors** | functional | 🟢 **full** | semiconductors-narrative | semiconductors-reviewer-criteria | 2 scripts | 1 package |
| **dielectrics-piezoelectrics** | functional | 🟢 **full** | dielectrics-piezoelectrics-narrative | dielectrics-piezoelectrics-reviewer-criteria | 2 scripts | 1 package |
| **photonic-optoelectronic** | functional | 🟢 **full** | photonic-optoelectronic-narrative | photonic-optoelectronic-reviewer-criteria | 2 scripts | 1 package |
| **nanoparticles** | nano | 🟢 **full** | nanoparticles-narrative | nanoparticles-reviewer-criteria | 2 scripts | 1 package |
| **nano-thin-films** | nano | 🟢 **full** | nano-thin-films-narrative | nano-thin-films-reviewer-criteria | 2 scripts | 1 package |
| **2d-materials** | nano | 🟢 **full** | 2d-materials-narrative | 2d-materials-reviewer-criteria | 2 scripts | 1 package |
| **nanocomposites** | nano | 🟢 **full** | nanocomposites-narrative | nanocomposites-reviewer-criteria | 2 scripts | 1 package |

## Domain routing

`materials-research` resolves user input against 52 domains. The registry above
tracks the 29 systems with `full` coverage. The remaining domains are family or
sub-family fallbacks that route to the nearest registered system.

## Tier Definitions

| Tier | Meaning |
|---|---|
| **full** | Narrative guide + figure scripts + reviewer criteria + example packages |
| **partial** | Narrative guide + at least one support resource |
| **skeleton** | Domain fragment + auto-generated narrative |
| **generic** | Family-level guidance only |

## Honest Scope

The bundle is deepest where the authors have direct research experience:
asphalt emulsions, WER-EA, pavement materials, cement-based materials, and
thermal insulation. Other domains have structural support through the registry
and routing system, and their depth is growing through the same narrative +
figure script + reviewer criteria pattern.

## Files to inspect

- Registry entries: `plugins/materials-skills/_shared/material-registry/entries/`
- Registry index: `plugins/materials-skills/_shared/material-registry/registry-index.yaml`
- Routing keywords: `plugins/materials-skills/_shared/triggers/`

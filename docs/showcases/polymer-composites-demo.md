# Polymer Matrix Composites (FRP / CFRP / GFRP)

Covers carbon-, glass-, and aramid-fiber reinforced polymer composites for
aerospace, automotive, wind energy, sporting goods, and civil infrastructure
applications.

This domain is at **full** tier: narrative guide, reviewer criteria,
3 dedicated figure scripts, and 2 end-to-end example packages are all in place.

---

## What the bundle gives you for this domain

| Asset | Location |
|---|---|
| Domain fragment | `plugins/materials-skills/skills/materials-research/static/fragments/domain/polymer-composites.md` |
| Narrative guide | `plugins/materials-skills/skills/materials-writing/references/polymer-composites-narrative.md` |
| Reviewer criteria | `plugins/materials-skills/skills/materials-reviewer/references/polymers-reviewer-criteria.md` |
| Figure scripts | `plot_stress_strain.py`, `plot_mechanical_property_radar.py`, `plot_polymers_multipanel.py` |
| Example packages | `plugins/materials-skills/skills/materials-figure/examples/figure-packages/polymer-composites-partial-to-full/` |
| Registry entry | `plugins/materials-skills/_shared/material-registry/entries/polymer-composites.yaml` |

## Narrative arc

Fiber + Matrix → Processing → Interface → Laminate Properties → Structural Performance

## Key evidence categories

- Fiber architecture: orientation, volume fraction, weave/stacking sequence
- Matrix properties: modulus, Tg, cure degree
- Interface: ILSS, SEM fracture surface, fiber-matrix debonding
- Mechanical: tensile, flexural, compression, ILSS, CAI, fatigue S-N
- Environmental: moisture uptake, hygrothermal aging, UV exposure, freeze-thaw
- Manufacturing: void content, cure cycle, processing defects

## Available figures

| Archetype | Script | What it shows |
|---|---|---|
| `stress_strain` | `plot_stress_strain.py` | Tensile/compressive stress-strain curves |
| `mechanical_radar` | `plot_mechanical_property_radar.py` | Multi-property radar for formulation comparison |
| `composite_multipanel` | `plot_polymers_multipanel.py` | Stress-strain + interface properties combined |

## Example package

`polymer-composites-partial-to-full` demonstrates how to move from basic
mechanical curves to a full characterization figure:

- Panel A: stress-strain response
- Panel B: fiber orientation and interface mechanism evidence
- Panel C: fatigue retention
- Panel D: interlaminar shear and fracture-mechanism boundary

## Common reviewer risks

| Risk | How to avoid |
|---|---|
| "0° tensile strength reported as material strength" | Report 0°, 90°, and shear properties separately |
| "Interface improved" without evidence | Show both ILSS data and SEM fracture surface |
| "Fatigue resistant" from static-only data | Provide S-N curve with ≥3 stress levels |
| Moisture absorption without mechanical retention | Pair weight gain with retention ratio |
| CAI without damage characterization | Report impact energy and C-scan / acoustic emission |

## Suggested journals

| Journal | Fit |
|---|---|
| Composites Part A: Applied Science and Manufacturing | Processing + properties |
| Composites Part B: Engineering | Structural applications |
| Composite Structures | Mechanics + design |
| Journal of Composite Materials | Broad scope |
| ACS Applied Materials & Interfaces | If novel interface chemistry |

## Try it

```text
I have tensile, flexural, and ILSS data for CFRP laminates. Build a
polymer-composites figure package, flag reviewer risks, and draft a results
paragraph for Composites Part A.
```

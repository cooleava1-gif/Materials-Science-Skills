# Thermal Insulation Materials

Covers aerogels, foams, fibrous insulation, vacuum insulation panels (VIPs),
phase-change materials (PCMs), and related thermal-management materials.

This domain is at **full** tier: narrative guide, reviewer criteria,
4 dedicated figure scripts, and 2 end-to-end example packages are all in place.

---

## What the bundle gives you for this domain

| Asset | Location |
|---|---|
| Domain fragment | `plugins/materials-skills/skills/materials-research/static/fragments/domain/thermal-insulation.md` |
| Narrative guide | `plugins/materials-skills/skills/materials-writing/references/thermal-insulation-narrative.md` |
| Reviewer criteria | `plugins/materials-skills/skills/materials-reviewer/references/insulation-reviewer-criteria.md` |
| Figure scripts | `plugins/materials-skills/skills/materials-figure/scripts/figures4materials/plot_insulation_*.py` |
| Example packages | `plugins/materials-skills/skills/materials-figure/examples/figure-packages/thermal-insulation-partial-to-full/` |
| Registry entry | `plugins/materials-skills/_shared/material-registry/entries/thermal-insulation.yaml` |

## Narrative arc

Material Design → Pore Structure → Thermal Performance → Mechanical Integrity → Service Durability

## Key evidence categories

- Physical: density, porosity, pore size distribution, specific surface area
- Thermal: thermal conductivity (λ), thermal diffusivity, specific heat, R-value, U-value
- Measurement: ASTM C518 / ISO 8301, mean temperature, specimen size, heat-flow direction
- Mechanical: compressive strength at 10% deformation, flexural strength, handling fragility
- Durability: hygrothermal aging, freeze-thaw, moisture effect on conductivity
- Fire: reaction to fire, limiting oxygen index, cone calorimeter

## Available figures

| Archetype | Script | What it shows |
|---|---|---|
| `conductivity_vs_density` | `plot_insulation_conductivity_vs_density.py` | λ vs. density scatter |
| `conductivity_vs_temperature` | `plot_insulation_conductivity_vs_temp.py` | λ vs. temperature across humidity levels |
| `insulation_stress_strain` | `plot_insulation_stress_strain.py` | Compressive stress-strain curve |
| `insulation_multipanel` | `plot_insulation_multipanel.py` | Density + humidity + stress-strain combined |

## Example package

`thermal-insulation-partial-to-full` demonstrates how to move from a single
conductivity-density result to a full application-window figure:

- Panel A: conductivity-density relationship
- Panel B: pore structure evidence
- Panel C: hygrothermal aging retention
- Panel D: application window combining λ, density, moisture, and fire performance

## Common reviewer risks

| Risk | How to avoid |
|---|---|
| Thermal conductivity without mean temperature | Always state: "λ = 0.028 W/(m·K) at T_mean = 25 °C" |
| "Superinsulating" claim without benchmark | Only use if λ < 0.020 W/(m·K) and compare to air / commercial products |
| Building applicability without fire/aging data | Report fire rating and conditioned performance |
| Hydrophobic claim without contact angle | Measure water contact angle or moisture uptake |

## Suggested journals

| Journal | Fit |
|---|---|
| Energy and Buildings | Strong for building insulation + energy |
| Building and Environment | Strong for hygrothermal + indoor environment |
| Cement and Concrete Composites | If cementitious foam |
| ACS Applied Materials & Interfaces | If novel aerogel chemistry |

## Try it

```text
Run a thermal-insulation mini-review on aerogel-polymer composite insulation.
I have a CSV with density and thermal conductivity; build a figure package and
flag reviewer risks before drafting the discussion.
```

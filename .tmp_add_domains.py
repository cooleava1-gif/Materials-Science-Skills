#!/usr/bin/env python3
"""Add ceramics and thermal-insulation domain support."""
import os

BASE = r"C:\Users\97218\Desktop\civil-materials-skills-release"

def write(rel_path, content):
    full = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content.lstrip("\n"))
    print(f"  OK {rel_path}")

# ============================================================
# 1. SHARED JOURNAL FORMATS
# ============================================================
write("skills/_shared/journal-formats/jacers.md", """\
# Journal of the American Ceramic Society (JACerS) — Formatting Facts

> Always verify against the journal's current Guide for Authors before final submission.
> Official page: https://ceramics.onlinelibrary.wiley.com/journal/15512916

## Article types and limits

| Article type | Word limit | Abstract | References | Figures/Tables |
|---|---|---|---|---|
| Research article | ~8,000 | Unstructured (~200 words) | No hard cap | No hard cap |
| Review article | ~10,000 | Unstructured (~250 words) | Comprehensive | Flexible |
| Rapid communication | ~4,000 | ~100 words | ~20 | ~5 |

## Formatting

- Double-spaced, numbered lines.
- Figures: TIFF/EPS at 300 dpi minimum.
- References: numbered Vancouver style.
""")

write("skills/_shared/journal-formats/ceramics-international.md", """\
# Ceramics International — Formatting Facts

> Always verify against the journal's current Guide for Authors before final submission.
> Official page: https://www.sciencedirect.com/journal/ceramics-international

## Article types and limits

| Article type | Word limit | Abstract | References |
|---|---|---|---|
| Research article | No strict limit (~6,000 typical) | Structured (~200 words) | No hard cap |
| Review article | ~12,000 | Unstructured (~300 words) | Comprehensive |

## Formatting

- Single column, double-spaced.
- Figures: 300 dpi TIFF/PDF/EPS.
- References: numbered IEEE style.
""")

write("skills/_shared/journal-formats/energy-buildings.md", """\
# Energy and Buildings — Formatting Facts

> Always verify against the journal's current Guide for Authors before final submission.
> Official page: https://www.sciencedirect.com/journal/energy-and-buildings

## Article types and limits

| Article type | Word limit | Abstract | References |
|---|---|---|---|
| Research article | ~9,000 | Structured (~300 words) | No hard cap |
| Review article | ~12,000 | Unstructured (~300 words) | Comprehensive |

## Formatting

- Double-spaced, numbered lines.
- Figures: 300 dpi TIFF/EPS.
- References: numbered Vancouver style.
- SI units required.
""")

write("skills/_shared/journal-formats/building-environment.md", """\
# Building and Environment — Formatting Facts

> Always verify against the journal's current Guide for Authors before final submission.
> Official page: https://www.sciencedirect.com/journal/building-and-environment

## Article types and limits

| Article type | Word limit | Abstract | References |
|---|---|---|---|
| Research article | ~9,000 | Structured (~300 words) | No hard cap |
| Review article | ~12,000 | Unstructured (~300 words) | Comprehensive |
| Short communication | ~4,000 | ~150 words | ~20 |

## Formatting

- Double-spaced, numbered lines.
- Figures: 300 dpi TIFF/PDF/EPS.
- References: numbered Harvard style optional.
""")

write("skills/_shared/journal-formats/thermal-sciences.md", """\
# International Journal of Thermal Sciences — Formatting Facts

> Always verify against the journal's current Guide for Authors before final submission.
> Official page: https://www.sciencedirect.com/journal/international-journal-of-thermal-sciences

## Article types and limits

| Article type | Word limit | Abstract | References |
|---|---|---|---|
| Research article | ~8,000 | Structured (~200 words) | No hard cap |
| Review article | ~10,000 | Unstructured (~250 words) | Comprehensive |

## Formatting

- Double-spaced.
- Figures: 300 dpi TIFF/EPS.
- References: numbered Vancouver style.
""")

# ============================================================
# 2. RESEARCH SKILL — DOMAIN FRAGMENTS + JOURNAL FRAGMENTS
# ============================================================
write("skills/materials-research/static/fragments/domain/ceramics.md", """\
# Domain: Ceramics

Use for advanced ceramics, structural ceramics, functional ceramics, ceramic matrix composites, electroceramics, bioceramics, refractory materials, and ceramic processing.

## Core logic

Ceramics papers need to connect:

1. Powder processing/pyrolysis/sintering route.
2. Phase composition and densification.
3. Microstructure and grain boundary engineering.
4. Mechanical/thermal/electrical/optical properties.
5. Processing-structure-property relationship.

## Key evidence categories

- Processing: powder synthesis, green forming, sintering (temperature, atmosphere, heating rate, dwell time), HIP, SPS, flash sintering.
- Phase analysis: XRD, Rietveld refinement, phase fraction.
- Microstructure: SEM, TEM, EDS, EBSD, grain size distribution.
- Mechanical: flexural strength (MOR), fracture toughness (SENB, SEVNB, indentation), hardness, Weibull modulus, creep.
- Thermal: thermal conductivity, thermal expansion, thermal shock resistance, specific heat.
- Functional: dielectric, piezoelectric, ferroelectric, ionic conductivity, optical transmittance.

## Reviewer risks

- Strength reported without Weibull statistics.
- Sintering conditions insufficiently reported (atmosphere, ramp rate, dwell).
- Porosity/density not reported alongside mechanical properties.
- Grain size reported without distribution or imaging.
- Thermal/functional claims without error bars or temperature dependence.
""")

write("skills/materials-research/static/fragments/domain/thermal-insulation.md", """\
# Domain: Thermal Insulation

Use for thermal insulation materials, aerogels, foams, fibrous insulation, vacuum insulation panels, phase change materials for thermal management, and building envelope materials.

## Core logic

Thermal insulation papers need to connect:

1. Material formulation and pore/void structure design.
2. Thermal conductivity measurement and heat transfer mechanisms.
3. Mechanical integrity and handling strength.
4. Durability under humidity/temperature/aging.
5. Application-specific performance (building, industrial, cryogenic).

## Key evidence categories

- Physical properties: density, porosity, pore size distribution, specific surface area.
- Thermal properties: thermal conductivity (lambda), thermal diffusivity, specific heat capacity, R-value, U-value.
- Measurement details: testing standard (ASTM C518, ISO 8301, ASTM E1530), mean temperature, specimen size, heat flow direction.
- Mechanical: compressive strength (at 10% deformation), flexural strength, handling fragility.
- Durability: hygrothermal aging, freeze-thaw, moisture absorption effect on conductivity.
- Fire performance: reaction to fire, limiting oxygen index, cone calorimeter.

## Reviewer risks

- Thermal conductivity reported without mean temperature or standard.
- Density changes after aging not reported.
- Mechanical strength measured without reporting strain/deflection at failure.
- Moisture effect on thermal performance ignored.
- Aerogel/foam claimed as "super-insulating" without comparison to air conductivity or existing benchmarks.
""")

write("skills/materials-research/static/fragments/journal/jacers.md", """\
# Journal: Journal of the American Ceramic Society (JACerS)

Official page: https://ceramics.onlinelibrary.wiley.com/journal/15512916

## Best fit

Ceramics processing, phase equilibria, microstructure, mechanical/thermal/electrical/optical properties, and ceramic matrix composites.

## Strong manuscript profile

- Clear processing-structure-property linkage.
- Quantitative phase analysis and microstructure characterization.
- Mechanical or functional properties with statistical treatment.
- Comparison with existing literature and processing alternatives.
""")

write("skills/materials-research/static/fragments/journal/ceramics-international.md", """\
# Journal: Ceramics International

Official page: https://www.sciencedirect.com/journal/ceramics-international

## Best fit

Applied ceramics research covering processing, characterization, and properties of ceramic materials from lab to application.

## Strong manuscript profile

- Well-characterized processing-microstructure relationships.
- Mechanical, thermal, or functional property data with error analysis.
- Novel processing routes or composition design.
- Application-oriented discussion.
""")

write("skills/materials-research/static/fragments/journal/energy-buildings.md", """\
# Journal: Energy and Buildings

Official page: https://www.sciencedirect.com/journal/energy-and-buildings

## Best fit

Building energy performance, thermal insulation, building envelope materials, HVAC systems, energy-efficient building design.

## Strong manuscript profile

- Thermal insulation performance with standard-compliant measurement.
- Building-scale energy simulation validated by material properties.
- Hygrothermal durability assessment.
- Life-cycle energy or cost analysis.
""")

write("skills/materials-research/static/fragments/journal/building-environment.md", """\
# Journal: Building and Environment

Official page: https://www.sciencedirect.com/journal/building-and-environment

## Best fit

Indoor environmental quality, building physics, building materials performance in service, thermal comfort, moisture control.

## Strong manuscript profile

- Material performance under realistic service conditions.
- Coupled heat-air-moisture transfer analysis.
- Experimental validation of building envelope assemblies.
- Occupant comfort and health considerations.
""")

# ============================================================
# 3. CITATION DOMAIN FRAGMENTS
# ============================================================
write("skills/materials-citation/static/fragments/domain/ceramics.md", """\
# Ceramics Domain Citation Rules

For ceramics manuscripts, keep evidence separated by:

- **Processing**: powder synthesis, green forming, sintering (temperature, atmosphere, ramp rate, dwell).
- **Phase composition**: XRD phase identification, Rietveld quantification, amorphous content.
- **Microstructure**: grain size, grain boundary phase, porosity, SEM/TEM evidence.
- **Mechanical properties**: flexural strength, fracture toughness, hardness, Weibull modulus.
- **Functional properties**: dielectric, piezoelectric, thermal conductivity, optical, ionic conductivity.

Separate processing-property citations from mechanism citations. Report sintering conditions precisely.
""")

write("skills/materials-citation/static/fragments/domain/thermal-insulation.md", """\
# Thermal Insulation Domain Citation Rules

For thermal insulation manuscripts, keep evidence separated by:

- **Material design**: formulation, density, porosity, pore structure.
- **Thermal performance**: thermal conductivity (lambda), R-value, testing standard, mean temperature.
- **Mechanical integrity**: compressive strength, handling fragility, dimensional stability.
- **Durability**: moisture absorption, freeze-thaw, hygrothermal aging effect on conductivity.
- **Application context**: building code compliance, fire performance, cost.

Report thermal conductivity with testing standard and mean temperature. Always cite measurement conditions.
""")

# ============================================================
# 4. DATA DOMAIN FRAGMENTS
# ============================================================
write("skills/materials-data/static/fragments/domain/ceramics.md", """\
# Ceramics Domain Data Rules

For ceramics data, track:

- Powder source, purity, particle size distribution, specific surface area.
- Green forming method, pressure, binder content.
- Sintering: furnace type, atmosphere, heating rate, target temperature, dwell time, cooling rate.
- Density measurement method (Archimedes, geometric), theoretical density, relative density.
- Phase composition from XRD/Rietveld.
- Mechanical test standard, specimen geometry, loading rate, span (for bending).
- Number of specimens for Weibull statistics.
""")

write("skills/materials-data/static/fragments/domain/thermal-insulation.md", """\
# Thermal Insulation Domain Data Rules

For thermal insulation data, track:

- Density (bulk, skeletal), porosity (open/closed/total), pore size distribution.
- Thermal conductivity measurement: standard (ASTM C518, ISO 8301, ASTM E1530), mean temperature, temperature gradient, specimen dimensions, heat flow direction.
- Mechanical: compressive stress at 10% or 25% deformation, elastic modulus, flexural strength where applicable.
- Moisture: equilibrium moisture content at specified RH, effect on conductivity.
- Aging: test conditions, duration, property retention.
""")

# ============================================================
# 5. FIGURE DOMAIN FRAGMENTS
# ============================================================
write("skills/materials-figure/static/fragments/domain/ceramics.md", """\
# Ceramics Figure Rules

Common figure types for ceramics manuscripts:

- XRD patterns with phase labels and reference patterns overlay.
- SEM/TEM micrographs with grain size distribution inset.
- Sintering curve (density vs temperature) or shrinkage curve.
- Mechanical property bar charts (strength, toughness, hardness) grouped by composition.
- Weibull probability plot for strength distribution.
- Thermal conductivity vs temperature or porosity.
- Impedance spectroscopy (Nyquist plot) for electroceramics.

Use SEM image panels with consistent magnification and scale bars. For Weibull plots, show confidence bounds.
""")

write("skills/materials-figure/static/fragments/domain/thermal-insulation.md", """\
# Thermal Insulation Figure Rules

Common figure types for thermal insulation manuscripts:

- Thermal conductivity vs density or porosity scatter plot.
- Thermal conductivity vs temperature at different humidity levels.
- Compressive stress-strain curves at various densities.
- Pore size distribution from mercury intrusion or micro-CT.
- Hygrothermal aging: conductivity or strength retention over time.
- Heat flux or temperature profile across insulation thickness.

Always label testing standard and mean temperature on thermal conductivity figures. Use dual y-axis when combining thermal and mechanical properties.
""")

# ============================================================
# 6. CIVIL-MATERIALS → MATERIALS rename for domain fragments
# write() handles paths with the old name in fragments
# ============================================================

# Update research manifest.yaml — domain and journal axes
print("\nDone creating fragments. Now updating manifests...")

# I'll handle the manifest updates separately
print("Fragment files created. Proceeding to manifest updates.")
PYEOF
# Methods

> **Domain context**: The `domain` axis has loaded domain-specific writing guidance for [detected domain]. The reporting requirements below vary by material family — the domain guide contains characterization-specific details.

Methods must make the experiment reproducible.

## General requirements (all domains)

- Material source, purity/specification, and pretreatment.
- Composition/formulation in precise units (wt%, phr, mol%, ratio).
- Processing parameters: temperature, time, pressure, atmosphere, cooling rate.
- Test standards (ASTM, EN, ISO, GB/T, JIS) or detailed protocol if adapted.
- Specimen geometry, dimensions, and number of replicates.
- Statistical methods and software used.

## Domain-specific reporting

Refer to the domain writing guide for the full list. Key items per domain:

- **Civil**: binder source, emulsifier type, additive dosage, curing condition, substrate preparation, moisture conditioning.
- **Ceramics**: powder purity and particle size, forming method, sintering profile (ramp rate, T, dwell, atmosphere), density method, theoretical density.
- **Metals**: composition (wt%), processing history (casting/rolling/heat treatment), cooling rate, specimen orientation, test standards.
- **Polymers**: molecular weight or grade, processing (temperature profile, pressure, cooling), post-curing, conditioning.
- **Functional**: synthesis method, substrate, electrode preparation, measurement setup (frequency, voltage, temperature, atmosphere).
- **Nanomaterials**: precursor concentration, synthesis T/t, capping agent, purification, TEM sample preparation, DLS measurement conditions.

If a method detail is unknown, keep a placeholder instead of smoothing over it.

## Domain checklist

- [ ] Are all standard numbers (ASTM, EN, ISO, GB/T) correctly cited?
- [ ] Would a researcher in the same field reproduce your experiment from the description?
- [ ] Are all processing variables that affect the result reported?
- [ ] Is the number of replicates and statistical treatment reported?

## Record-driven Methods drafting

If the user provides `experiment-record.yaml`, follow `methods-from-record.md` to generate the first draft, then apply the domain-specific reporting checklist above.

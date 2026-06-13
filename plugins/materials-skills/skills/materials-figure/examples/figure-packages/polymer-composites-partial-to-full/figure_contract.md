# Figure Contract

## Core Conclusion

Polymer-composite mechanical claims should connect stress-strain behavior to
fiber orientation, interfacial bonding, fatigue retention, interlaminar shear,
and fracture mechanism evidence.

## Evidence Chain

| Panel | Evidence source | Source anchor | What it supports | Boundary |
|---|---|---|---|---|
| A | source_data.csv | row:stress_strain | stress-strain | Static loading only |
| B | source_data.csv | row:fiber_interface | fiber orientation and interface mechanism | Placeholder orientation evidence |
| C | source_data.csv | row:fatigue | fatigue retention | Synthetic cycle count |
| D | source_data.csv | row:ilss_fracture | interlaminar shear and fracture mechanism | Fractography placeholder |

## Archetype

property-performance + process-structure-property + durability-aging + mechanism-evidence

## Backend

- Selected backend: Python
- Runtime/package status: generated as synthetic golden package
- Backend exclusivity note: all plotting, previews, exports, and QA renders use Python.

## Journal/Export Contract

- Target journal family: materials/composites-ready package
- Width: double-column
- Font size: readable at final size
- Vector formats: SVG, PDF
- Raster formats: PNG, TIFF
- DPI: 300+

## Statistics And Image Integrity

- n definition: synthetic package; replace before manuscript use
- replicate definition: synthetic package
- center/spread: not used in template panels
- test/correction: not applicable until real data are inserted
- image provenance: no raw microscopy image in this package
- scale bars: not applicable
- crop/contrast notes: not applicable

## WER-EA Boundary

- Not a WER-EA package; this section is retained for the shared audit contract.
- Performance evidence: stress-strain and ILSS placeholders.
- Direct mechanism evidence: interface and fracture placeholders.
- Durability/service evidence: fatigue retention placeholder.
- Unsupported or missing evidence: real fiber orientation distribution, void content, and fatigue spectrum.

## Reviewer Risk

- Do not claim stronger interface from static strength alone.
- Do not claim fatigue performance from stress-strain behavior without cyclic data.

# Materials Science Figure Gallery

Use this gallery when the user asks for a journal-ready figure plan, a PPT figure, a manuscript figure package, or a visual style example for civil engineering and construction-materials research.

The gallery is not a decoration library. Each figure card links visual form to a reviewer-safe claim, the required data structure, a caption pattern, and common overclaim risks.

## Gallery Index

| Gallery card | Best use | Evidence role |
|---|---|---|
| bonding strength bar | Compare control and modified asphalt/concrete groups | Direct performance evidence |
| dosage-performance curve | Show dosage-response or optimum modifier content | Material-design rationale |
| FTIR peak annotation | Mark chemical groups, curing, or interaction evidence | Mechanism evidence |
| SEM/fluorescence plate | Compare morphology, phase distribution, interface quality | Microstructure evidence |
| durability radar | Summarize retained performance under aging/moisture/freeze-thaw | Durability trade-off evidence |
| mechanism schematic | Explain material design and claim boundaries | Interpretive summary, not direct data |
| characterization templates | Plan XRD, TG/DTG, FTIR overlay, SEM/TEM, and uncertainty figures | Mechanism or method evidence when measurements support it |

## Gallery Composite Figures (PNG Previews)

The `assets/gallery/` directory contains 5 submission-grade composite
figures demonstrating complete materials science visual narratives. Each
figure uses asymmetric GridSpec layouts with labeled panels (a)-(i).

| Gallery file | Theme | Panels | Journal style |
|---|---|---|---|
| `fig1-cement-hydration-mechanism.png` | Cement hydration mechanism | 6 (a-f) | Cement and Concrete Research |
| `fig2-steel-microstructure-property.png` | Steel microstructure-property | 7 (a-g) | Acta Materialia |
| `fig3-polymer-composite-multifunctional.png` | Polymer composite multifunctional | 8 (a-h) | Advanced Functional Materials |
| `fig4-ceramics-reliability-assessment.png` | Ceramics reliability assessment | 8 (a-h) | J. Am. Ceram. Soc. |
| `fig5-asphalt-modification-review.png` | Asphalt modification review | 9 (a-i) | Construction and Building Materials |

Use these as visual reference for:
- Asymmetric multi-panel layout patterns
- Information flow: Overview → Characterization → Performance → Summary
- Panel labeling conventions (a), (b), (c)...
- Journal-specific style matching

## Style Presets

Use `assets/templates/figure-style-presets.yaml` before plotting.

- `cbm`: applied performance, restrained earth tones, clear controls.
- `ccc`: mechanism-forward, cooler palette, stronger subfigure discipline.
- `rmpd_ijpe`: pavement-service framing, traffic/environment colors.
- `jbe`: building-engineering clarity, accessible palette.

## Figure Card Requirements

Every gallery-derived figure should include:

- `Figure Intent`: what claim the visual supports.
- `Data Structure`: exact rows/columns or image inputs needed.
- `Caption Pattern`: what can be safely claimed.
- `Reviewer Risk`: what the figure cannot prove.
- `Borrowing Note`: what the user can reuse in a paper, PPT, or review.

## Materials Science Rules

- Keep performance figures separate from mechanism figures unless both measurements exist.
- Do not use a mechanism schematic as proof of chemical reaction.
- Do not infer durability from short-term bonding strength.
- For waterborne epoxy modified emulsified asphalt, separate emulsion stability, epoxy curing, interface bonding, viscosity, storage stability, and moisture/aging evidence.
- Put control, dosage, temperature, curing condition, and test standard in the figure plan or caption when available.
- For XRD, TG/DTG, FTIR, SEM/TEM, and error-bar choices, load `references/characterization-figures.md`.

## Recommended Workflow

1. Pick the closest gallery card.
2. Copy its data structure into `figure-plan-template.md`.
3. Select a journal preset from `figure-style-presets.yaml`.
4. The LLM generates the figure using matplotlib or other Python plotting libraries.
5. Write the caption as claim -> evidence -> boundary.
6. Run reviewer-risk audit before using the figure in a manuscript.

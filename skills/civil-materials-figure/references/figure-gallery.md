# Civil Materials Figure Gallery

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

## Civil Materials Rules

- Keep performance figures separate from mechanism figures unless both measurements exist.
- Do not use a mechanism schematic as proof of chemical reaction.
- Do not infer durability from short-term bonding strength.
- For waterborne epoxy modified emulsified asphalt, separate emulsion stability, epoxy curing, interface bonding, viscosity, storage stability, and moisture/aging evidence.
- Put control, dosage, temperature, curing condition, and test standard in the figure plan or caption when available.

## Recommended Workflow

1. Pick the closest gallery card.
2. Copy its data structure into `figure-plan-template.md`.
3. Select a journal preset from `figure-style-presets.yaml`.
4. Generate a draft with `scripts/gallery_demo.py` or `scripts/civil_materials_plot_svg.py`.
5. Write the caption as claim -> evidence -> boundary.
6. Run reviewer-risk audit before using the figure in a manuscript.

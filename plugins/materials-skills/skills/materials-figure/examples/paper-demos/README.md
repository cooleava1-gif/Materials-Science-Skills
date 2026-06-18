# Paper Demos: Real CBM Figure Reproductions

This directory contains runnable figure scripts based on published
CBM (Construction and Building Materials) papers on waterborne epoxy
modified emulsified asphalt (WER-EA).

Each demo reproduces a key figure from the paper using the
`materials_plot_lib.py` helper library.

## Demos

| Paper | Directory | Figures | Chart Types |
|---|---|---|---|
| Kong et al. (2024) CBM 419 | `kong-2024-cbm-bonding/` | Bonding strength, Shear vs temperature | Grouped bar, Line trend |
| Zhang et al. (2017) CBM 155 | `zhang-2017-cbm-tack-coat/` | Viscosity curing, Shear strength | Line trend, Grouped bar |
| Yao et al. (2022) CBM 318 | `yao-2022-cbm-wer-sbr/` | DSR rheology, FTIR spectra | Line trend, FTIR overlay |

## Usage

```powershell
# Run a single demo
python plugins/materials-skills/skills/materials-figure/examples/paper-demos/kong-2024-cbm-bonding/plot_bonding_strength.py --output-dir ./my-figures

# Run all demos in a paper
python plugins/materials-skills/skills/materials-figure/examples/paper-demos/kong-2024-cbm-bonding/plot_bonding_strength.py --output-dir ./figures
python plugins/materials-skills/skills/materials-figure/examples/paper-demos/kong-2024-cbm-bonding/plot_shear_vs_temperature.py --output-dir ./figures
```

## Data Sources

The data in these scripts is extracted from the published figures and tables.
For research use, always refer to the original paper for the authoritative data.

## Claim Boundary Discipline

Each demo includes a `Claim boundary` note in its caption output, reminding
the writer what evidence is needed before making mechanism or durability claims.

## Adding New Demos

1. Create a directory: `paper-demos/<firstauthor-year-journal-topic>/`
2. Add a `plot_*.py` script using `materials_plot_lib.py`
3. Include the full paper citation in the docstring
4. Add a claim boundary note in the caption output
5. Update this README with the new demo entry

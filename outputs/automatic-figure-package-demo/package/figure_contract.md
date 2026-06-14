# Figure Contract

## Core Conclusion
Show the optimum WER dosage window for bonding strength.

## Evidence Chain
- Source table: `wer_bond_strength.csv`
- Recognized numeric columns: WER content (%), Bond strength (MPa), SD
- Recognized error columns: SD
- Selected chart: `errorbar_trend`

## Archetype
Automatic Python materials figure package using `errorbar_trend`.

## Backend
Python backend only.

## Journal/Export Contract
SVG and PNG are generated. SVG is the editable primary manuscript asset.

## Statistics And Image Integrity
Error bars are mapped from `SD`. Replicate count must be confirmed in the methods or caption before production-ready use.

## WER-EA Boundary
The figure can support measured WER-EA performance trends only when the source table describes that system. It does not prove field durability or interface mechanism by itself.

## Reviewer Risk
State replicate count (n) in caption or methods before using the figure as manuscript evidence.; Define error bars as SD, SE, CI, or range.; Do not call a dosage optimum unless the caption names the tested range and supporting durability evidence.

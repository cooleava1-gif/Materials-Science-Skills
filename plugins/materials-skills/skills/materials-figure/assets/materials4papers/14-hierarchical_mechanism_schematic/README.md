# 14 — Hierarchical mechanism schematic

Step-by-step mechanism tree (bitumen → epoxy → IPN → performance) for a
WER-EA review figure.

## Run

```powershell
python plot.py
```

## Files

- `data/synthetic.csv` — 4 rows with `step,label,parent`.
- `plot.py` — reads CSV, draws a left-to-right arrow chain of steps.
- `figures/hierarchical_mechanism_schematic.png` + `.svg` — generated output.

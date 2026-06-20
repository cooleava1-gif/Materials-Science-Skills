# 15 — Ceramic Nyquist plot

Electrochemical impedance spectroscopy (EIS) for a solid-electrolyte
ceramic sample, showing the classic Z' vs -Z'' semicircle.

## Run

```powershell
python plot.py
```

## Files

- `data/synthetic.csv` — 7 rows with `freq_Hz,Z_real_ohm,Z_imag_ohm`.
- `plot.py` — reads CSV, plots Nyquist curve with equal aspect.
- `figures/ceramic_nyquist_plot.png` + `.svg` — generated output.

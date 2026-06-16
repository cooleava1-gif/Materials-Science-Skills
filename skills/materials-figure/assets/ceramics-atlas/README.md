# Ceramics Figure Atlas

Generated figures for common ceramics manuscript types.

## Contents

| Figure | Data source | Script function |
|---|---|---|
| `ceramics_sintering_curve.png` | `data/sintering_curve.csv` | `plot_sintering_curve()` |
| `ceramics_xrd_pattern.png` | `data/xrd_pattern.csv` | `plot_xrd_pattern()` |
| `ceramics_weibull_plot.png` | `data/weibull_data.csv` | `plot_weibull()` |
| `ceramics_thermal_conductivity.png` | `data/thermal_conductivity.csv` | `plot_thermal_conductivity()` |
| `ceramics_grain_size_dist.png` | `data/grain_size_distribution.csv` | `plot_grain_size_distribution()` |
| `ceramics_eis_nyquist.png` | (simulated) | `plot_eis_nyquist()` |

## Generation

```bash
python ../../scripts/ceramics_atlas/plot_ceramics_atlas.py
```

Requires: Python 3.10+, matplotlib, numpy, pillow.

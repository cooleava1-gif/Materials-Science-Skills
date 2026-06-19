# Materials for Papers

Real-world example figures for materials science manuscripts, following Nature-style plotting conventions.

## Purpose

This directory contains complete, reproducible figure examples for common materials science manuscript types. Each example includes:

- **plot.py**: Complete plotting script with Nature-style formatting
- **data/**: CSV source data files
- **figures/**: Generated PNG preview images

These examples demonstrate how to create publication-ready figures using matplotlib with proper rcParams, font handling, and output settings.

## Examples

### 1. figure_ceramics_xrd

XRD phase identification for Al₂O₃-ZrO₂ composite ceramics.

- **Chart type**: Line plot with peak annotations
- **Data**: `data/xrd_data.csv` (2θ vs intensity for Al₂O₃, t-ZrO₂, m-ZrO₂)
- **Output**: `figures/xrd_pattern.png`
- **Script**: `plot_xrd.py`

### 2. figure_ceramics_sintering

Sintering optimization: density and grain size vs temperature.

- **Chart type**: Dual-panel line plot
- **Data**: `data/sintering_data.csv` (temperature vs density and grain size)
- **Output**: `figures/sintering_curve.png`
- **Script**: `plot_sintering.py`

### 3. figure_ceramics_weibull

Weibull reliability analysis: 3Y-TZP vs Al₂O₃-doped strength distribution.

- **Chart type**: Weibull probability plot
- **Data**: `data/weibull_data.csv` (fracture strength measurements)
- **Output**: `figures/weibull_plot.png`
- **Script**: `plot_weibull.py`

### 4. figure_cement_durability

Cement durability: retention percentage under different aging conditions.

- **Chart type**: Bar chart with error bars
- **Data**: `data/durability_data.csv` (property retention for control vs modified cement)
- **Output**: `figures/durability_retention.png`
- **Script**: `plot.py`

### 5. figure_steel_corrosion

Steel corrosion trend: corrosion rate over exposure time.

- **Chart type**: Errorbar plot
- **Data**: `data/corrosion_data.csv` (corrosion rate vs time for different groups)
- **Output**: `figures/corrosion_trend.png`
- **Script**: `plot.py`

## Running Examples

Each example is self-contained. To regenerate a figure:

```powershell
cd figure_ceramics_xrd
python plot_xrd.py
```

The script will read data from `data/` and save the figure to `figures/`.

## Requirements

- Python 3.10+
- matplotlib
- numpy
- csv (standard library)

All scripts use `matplotlib.use("Agg")` for headless rendering.

## Nature-Style Conventions

All scripts follow these publication defaults:

- **SVG text**: `matplotlib.rcParams["svg.fonttype"] = "none"` (editable text)
- **PDF fonts**: `matplotlib.rcParams["pdf.fonttype"] = 42` (TrueType)
- **Font family**: sans-serif (Helvetica/Arial compatible)
- **Spines**: Top and right spines removed
- **Line width**: 1.5 pt for axes, 2 pt for data lines
- **DPI**: 300+ for PNG previews
- **bbox_inches**: "tight" to prevent label clipping

## Relationship to Other Assets

This directory complements:

- **chart-atlas/**: Generic chart type examples
- **ceramics-atlas/**: Ceramics-specific figure templates
- **rich-gallery/**: Complex multi-panel figures
- **review-first/**: Review article figure templates
- **wer-ea-atlas/**: WER-EA specific figures

The `materials4papers/` examples are **reference implementations**, not automated tools. They demonstrate best practices for creating publication-ready figures from real experimental data.

## License

These examples are provided as reference material for materials science figure generation. Use them as templates for your own manuscript figures.

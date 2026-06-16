#!/usr/bin/env python3
"""Generate showcase figures for the Visual Gallery."""

import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from materials_plot_lib import (
    apply_pub_style,
    finalize_figure,
    make_grouped_bar,
    make_line_trend,
    make_scatter_regression,
    make_radar,
    make_correlation_heatmap,
    make_ftir_overlay,
    make_errorbar_trend,
    add_panel_label,
    PALETTE_CBM,
    PALETTE_ASPHALT,
    PALETTE_POLYMER,
    PALETTE_CERAMIC,
    PALETTE_CCC,
)

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "assets" / "showcase-proof"


def generate_multi_panel_overview():
    """2×2 multi-panel: grouped bar + line trend + scatter + radar."""
    apply_pub_style()
    fig = plt.figure(figsize=(10, 8))
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.3)
    ax_bar = fig.add_subplot(gs[0, 0])
    ax_line = fig.add_subplot(gs[0, 1])
    ax_scatter = fig.add_subplot(gs[1, 0])
    ax_radar = fig.add_subplot(gs[1, 1], projection="polar")

    pal = PALETTE_CBM

    # Panel a — grouped bar: bonding strength
    make_grouped_bar(
        ax_bar,
        labels=["0%", "1%", "3%", "5%", "7%"],
        groups=["Dry", "Wet"],
        values=[[0.42, 0.58, 0.73, 0.69, 0.61],
                [0.31, 0.44, 0.56, 0.52, 0.45]],
        palette=pal,
    )
    ax_bar.set_ylabel("Bond strength (MPa)")
    ax_bar.set_xlabel("W-EA dosage")
    add_panel_label(ax_bar, "a")

    # Panel b — line trend: thermal conductivity vs temperature
    temps = np.array([10, 20, 30, 40, 50, 60, 70, 80])
    make_line_trend(
        ax_line,
        x=temps,
        y_series=[
            [0.042, 0.044, 0.047, 0.051, 0.056, 0.062, 0.069, 0.078],
            [0.038, 0.040, 0.042, 0.045, 0.049, 0.054, 0.060, 0.067],
            [0.035, 0.036, 0.038, 0.041, 0.044, 0.048, 0.053, 0.059],
        ],
        labels=["Control", "3% W-EA", "5% W-EA"],
        palette=pal,
    )
    ax_line.set_ylabel("Thermal conductivity (W/mK)")
    ax_line.set_xlabel("Temperature (°C)")
    add_panel_label(ax_line, "b")

    # Panel c — scatter regression: dosage vs strength
    x = np.array([0, 1, 2, 3, 4, 5, 6, 7])
    y = np.array([0.42, 0.51, 0.62, 0.73, 0.78, 0.73, 0.66, 0.61])
    make_scatter_regression(
        ax_scatter,
        x=x,
        y=y,
        palette=pal,
        label="WER-EA",
    )
    ax_scatter.set_ylabel("Peak bond strength (MPa)")
    ax_scatter.set_xlabel("Dosage (%)")
    add_panel_label(ax_scatter, "c")

    # Panel d — radar: multi-criteria comparison
    make_radar(
        ax_radar,
        categories=["Adhesion", "Durability", "Thermal\nstability", "Rheology", "Cost\nindex"],
        series_dict={
            "Control": [0.42, 0.55, 0.60, 0.50, 0.85],
            "Optimized": [0.73, 0.78, 0.82, 0.71, 0.65],
        },
        palette=pal,
    )
    add_panel_label(ax_radar, "d")

    fig.subplots_adjust(left=0.08, right=0.95, top=0.95, bottom=0.08, hspace=0.35, wspace=0.3)
    finalize_figure(fig, "showcase_multi_panel_overview", OUTPUT_DIR, formats=("png", "svg"), dpi=300)
    plt.close(fig)
    print("  [OK] showcase_multi_panel_overview")


def generate_ftir_comparison():
    """FTIR spectral overlay — polymer/composite domain."""
    apply_pub_style()
    fig, ax = plt.subplots(figsize=(8, 4))

    wavenumber = np.linspace(400, 4000, 361)
    np.random.seed(42)

    def ftir_peak(wavenumber, center, height, width):
        return height * np.exp(-0.5 * ((wavenumber - center) / width) ** 2)

    baseline_control = 0.05 - 0.000008 * wavenumber
    baseline_sbr = 0.06 - 0.000008 * wavenumber

    ctrl = baseline_control
    ctrl += ftir_peak(wavenumber, 2920, 0.35, 80)
    ctrl += ftir_peak(wavenumber, 2850, 0.28, 70)
    ctrl += ftir_peak(wavenumber, 1735, 0.15, 40)
    ctrl += ftir_peak(wavenumber, 1460, 0.12, 30)
    ctrl += ftir_peak(wavenumber, 1375, 0.08, 25)
    ctrl += ftir_peak(wavenumber, 1160, 0.10, 50)
    ctrl += ftir_peak(wavenumber, 1030, 0.18, 45)
    ctrl += ftir_peak(wavenumber, 870, 0.06, 20)
    ctrl += np.random.normal(0, 0.008, len(wavenumber))

    sbr = baseline_sbr
    sbr += ftir_peak(wavenumber, 2920, 0.38, 80)
    sbr += ftir_peak(wavenumber, 2850, 0.30, 70)
    sbr += ftir_peak(wavenumber, 1735, 0.22, 40)
    sbr += ftir_peak(wavenumber, 1600, 0.08, 25)
    sbr += ftir_peak(wavenumber, 1460, 0.14, 30)
    sbr += ftir_peak(wavenumber, 1030, 0.24, 45)
    sbr += ftir_peak(wavenumber, 698, 0.05, 15)
    sbr += np.random.normal(0, 0.008, len(wavenumber))

    modified = baseline_sbr * 1.02
    modified += ftir_peak(wavenumber, 2920, 0.40, 80)
    modified += ftir_peak(wavenumber, 2850, 0.32, 70)
    modified += ftir_peak(wavenumber, 1735, 0.26, 40)
    modified += ftir_peak(wavenumber, 1600, 0.10, 25)
    modified += ftir_peak(wavenumber, 1460, 0.15, 30)
    modified += ftir_peak(wavenumber, 1030, 0.28, 45)
    modified += ftir_peak(wavenumber, 698, 0.06, 15)
    modified += np.random.normal(0, 0.008, len(wavenumber))

    ax.plot(wavenumber, ctrl, color=PALETTE_CBM["control"], linewidth=1.2, label="Base binder")
    ax.plot(wavenumber, sbr, color=PALETTE_CBM["modified"], linewidth=1.2, label="SBR-WER")
    ax.plot(wavenumber, modified, color=PALETTE_CBM["optimal"], linewidth=1.2, label="SBR-WER + 5% W-EA")

    ax.set_xlabel("Wavenumber (cm$^{-1}$)")
    ax.set_ylabel("Absorbance (a.u.)")
    ax.invert_xaxis()
    ax.legend(frameon=False, loc="upper left", fontsize=9)

    annotations = [
        (2920, 0.45, "CH stretching"),
        (1735, 0.32, "C=O stretch"),
        (1030, 0.38, "C-O / Si-O"),
    ]
    for x_a, y_a, txt in annotations:
        ax.annotate(txt, xy=(x_a, y_a), fontsize=7.5, ha="center",
                    color=PALETTE_CBM["mechanism"])

    finalize_figure(fig, "showcase_ftir_overlay", OUTPUT_DIR, formats=("png", "svg"), dpi=300)
    plt.close(fig)
    print("  [OK] showcase_ftir_overlay")


def generate_thermal_performance():
    """Line chart with error bars — thermal performance across temperatures."""
    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))

    temps = np.array([25, 50, 75, 100, 125, 150, 175, 200])

    data = {
        "Neat epoxy":       ([0.22, 0.25, 0.30, 0.38, 0.49, 0.63, 0.81, 1.05], [0.02, 0.02, 0.03, 0.03, 0.04, 0.05, 0.06, 0.08]),
        "10 phr CNT":       ([0.18, 0.20, 0.24, 0.30, 0.38, 0.49, 0.63, 0.82], [0.01, 0.02, 0.02, 0.03, 0.03, 0.04, 0.05, 0.06]),
        "20 phr CNT":       ([0.15, 0.17, 0.20, 0.25, 0.31, 0.40, 0.51, 0.66], [0.01, 0.01, 0.02, 0.02, 0.03, 0.03, 0.04, 0.05]),
        "20 phr CNT + BN":  ([0.12, 0.14, 0.16, 0.20, 0.25, 0.32, 0.41, 0.53], [0.01, 0.01, 0.01, 0.02, 0.02, 0.03, 0.03, 0.04]),
    }

    palette = {
        "Neat epoxy": PALETTE_POLYMER["control"],
        "10 phr CNT": PALETTE_POLYMER["modified"],
        "20 phr CNT": PALETTE_POLYMER["optimal"],
        "20 phr CNT + BN": PALETTE_POLYMER["mechanism"],
    }

    for name, (means, errs) in data.items():
        ax.errorbar(
            temps, means, yerr=errs,
            marker="o", markersize=5, linewidth=1.8, capsize=3,
            color=palette[name], label=name,
        )

    ax.set_xlabel("Temperature (°C)")
    ax.set_ylabel("Thermal conductivity (W/mK)")
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    ax.set_xlim(20, 205)

    finalize_figure(fig, "showcase_thermal_performance", OUTPUT_DIR, formats=("png", "svg"), dpi=300)
    plt.close(fig)
    print("  [OK] showcase_thermal_performance")


def generate_property_heatmap():
    """Correlation heatmap — materials property relationships."""
    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 6))

    props = ["Bond\nstrength", "Tensile\nstrength", "Elongation", "Hardness",
             "Thermal\ncond.", "Density", "Water\nabsorption"]
    n = len(props)
    np.random.seed(7)
    raw = np.random.randn(n, n)
    corr = (raw + raw.T) / 2
    np.fill_diagonal(corr, 1.0)
    corr = np.clip(corr, -1, 1)

    make_correlation_heatmap(ax, corr, props)

    finalize_figure(fig, "showcase_property_heatmap", OUTPUT_DIR, formats=("png", "svg"), dpi=300)
    plt.close(fig)
    print("  [OK] showcase_property_heatmap")


if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating showcase figures...")
    generate_multi_panel_overview()
    generate_ftir_comparison()
    generate_thermal_performance()
    generate_property_heatmap()
    print("Done. Output:", OUTPUT_DIR)

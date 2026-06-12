#!/usr/bin/env python3
"""Generate chart-type atlas: one dense multi-panel preview per chart family.

Outputs SVG + PNG for each chart family, similar to nature-skills' chart atlas.
"""

from __future__ import annotations

import argparse
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Ensure we can import the project's plot lib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from materials_plot_lib import (
    PALETTE_CBM,
    PALETTE_SEMANTIC,
    apply_pub_style,
    finalize_figure,
    add_panel_label,
    make_grouped_bar,
)


def atlas_bar_charts(output_dir: str) -> str:
    """Grouped bars, stacked bars, horizontal bars."""
    apply_pub_style()
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    fig.suptitle("Bar Charts", fontsize=14, fontweight="bold")

    # Panel a: Grouped bar
    materials = ["Al2O3", "ZrO2", "SiC", "Si3N4"]
    groups = ["Control", "Modified"]
    values = [[320, 380, 410, 450], [420, 520, 460, 530]]
    errors = [[15, 20, 25, 30], [25, 35, 30, 28]]
    make_grouped_bar(axes[0, 0], materials, groups, values, PALETTE_CBM, error_bars=errors, ylabel="Strength (MPa)")
    add_panel_label(axes[0, 0], "a")

    # Panel b: Simple bar
    x = np.arange(len(materials))
    axes[0, 1].bar(x, [92, 96, 88, 94], color=[PALETTE_CBM["control"], PALETTE_CBM["optimal"], PALETTE_CBM["modified"], PALETTE_CBM["mechanism"]])
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(materials, fontsize=8)
    axes[0, 1].set_ylabel("Relative density (%)")
    axes[0, 1].set_ylim(80, 100)
    add_panel_label(axes[0, 1], "b")

    # Panel c: Horizontal bar
    axes[1, 0].barh(np.arange(len(materials)), [450, 520, 410, 380], color=PALETTE_CBM["optimal"])
    axes[1, 0].set_yticks(np.arange(len(materials)))
    axes[1, 0].set_yticklabels(materials, fontsize=8)
    axes[1, 0].set_xlabel("Flexural strength (MPa)")
    add_panel_label(axes[1, 0], "c")

    # Panel d: Stacked bar proxy
    categories = ["A", "B", "C", "D"]
    bottom = np.zeros(4)
    for name, color in [("Control", PALETTE_CBM["control"]), ("Modified", PALETTE_CBM["modified"])]:
        vals = np.random.randint(10, 40, 4)
        axes[1, 1].bar(categories, vals, bottom=bottom, label=name, color=color)
        bottom += vals
    axes[1, 1].set_ylabel("Composition (%)")
    axes[1, 1].legend(fontsize=7)
    add_panel_label(axes[1, 1], "d")

    fig.tight_layout()
    name = "atlas-bar-charts"
    finalize_figure(fig, name, output_dir=output_dir)
    plt.close(fig)
    return name


def atlas_line_trends(output_dir: str) -> str:
    """Line charts, trends, fill_between."""
    apply_pub_style()
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    fig.suptitle("Line and Trend Charts", fontsize=14, fontweight="bold")

    x = np.linspace(0, 10, 20)

    # Panel a: Single line
    axes[0, 0].plot(x, np.sin(x) * 10 + 30, "o-", color=PALETTE_CBM["control"], markersize=3)
    axes[0, 0].fill_between(x, np.sin(x) * 10 + 28, np.sin(x) * 10 + 32, alpha=0.15, color=PALETTE_CBM["control"])
    axes[0, 0].set_xlabel("Temperature (C)")
    axes[0, 0].set_ylabel("Strength (MPa)")
    add_panel_label(axes[0, 0], "a")

    # Panel b: Multiple lines
    for i, (name, color) in enumerate([("Control", PALETTE_CBM["control"]), ("Modified", PALETTE_CBM["modified"]), ("Optimal", PALETTE_CBM["optimal"])]):
        axes[0, 1].plot(x, np.sin(x + i) * 8 + 30 - i * 2, "o-", color=color, markersize=3, label=name)
    axes[0, 1].set_xlabel("Time (h)")
    axes[0, 1].set_ylabel("Property")
    axes[0, 1].legend(fontsize=7)
    add_panel_label(axes[0, 1], "b")

    # Panel c: Dual y-axis
    ax1 = axes[1, 0]
    ax2 = ax1.twinx()
    ax1.plot(x, np.sin(x) * 5 + 50, "o-", color=PALETTE_CBM["control"], markersize=3, label="Density")
    ax2.plot(x, np.cos(x) * 3 + 10, "s--", color=PALETTE_CBM["modified"], markersize=3, label="Porosity")
    ax1.set_xlabel("Temperature (C)")
    ax1.set_ylabel("Density (%)", color=PALETTE_CBM["control"])
    ax2.set_ylabel("Porosity (%)", color=PALETTE_CBM["modified"])
    add_panel_label(axes[1, 0], "c")

    # Panel d: Step change
    axes[1, 1].step(x, np.heaviside(x - 3, 0) * 30 + 50, where="mid", color=PALETTE_CBM["danger"])
    axes[1, 1].set_xlabel("Cycle")
    axes[1, 1].set_ylabel("Retention (%)")
    axes[1, 1].set_ylim(0, 100)
    add_panel_label(axes[1, 1], "d")

    fig.tight_layout()
    name = "atlas-line-trends"
    finalize_figure(fig, name, output_dir=output_dir)
    plt.close(fig)
    return name


def atlas_heatmaps(output_dir: str) -> str:
    """Heatmaps, z-score matrices, annotated tables."""
    apply_pub_style()
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    fig.suptitle("Heatmaps", fontsize=14, fontweight="bold")

    data = np.random.randn(6, 8)

    # Panel a: Sequential
    im = axes[0, 0].imshow(np.abs(data), cmap="YlOrRd", aspect="auto")
    axes[0, 0].set_xlabel("Property")
    axes[0, 0].set_ylabel("Formulation")
    plt.colorbar(im, ax=axes[0, 0], shrink=0.6)
    add_panel_label(axes[0, 0], "a")

    # Panel b: Diverging
    im = axes[0, 1].imshow(data, cmap="RdBu_r", aspect="auto", vmin=-2.5, vmax=2.5)
    axes[0, 1].set_xlabel("Property")
    axes[0, 1].set_ylabel("Formulation")
    plt.colorbar(im, ax=axes[0, 1], shrink=0.6, label="Z-score")
    add_panel_label(axes[0, 1], "b")

    # Panel c: Annotated
    small = np.random.randint(0, 100, (4, 5))
    im = axes[1, 0].imshow(small, cmap="Blues", aspect="auto")
    for i in range(4):
        for j in range(5):
            axes[1, 0].text(j, i, str(small[i, j]), ha="center", va="center", fontsize=7)
    add_panel_label(axes[1, 0], "c")

    # Panel d: Clustered blocks
    blocks = np.random.randn(8, 8)
    im = axes[1, 1].imshow(blocks, cmap="viridis", aspect="auto")
    plt.colorbar(im, ax=axes[1, 1], shrink=0.6)
    add_panel_label(axes[1, 1], "d")

    fig.tight_layout()
    name = "atlas-heatmaps"
    finalize_figure(fig, name, output_dir=output_dir)
    plt.close(fig)
    return name


def atlas_scatter_bubble(output_dir: str) -> str:
    """Scatter, bubble, volcano-style plots."""
    apply_pub_style()
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    fig.suptitle("Scatter and Bubble Plots", fontsize=14, fontweight="bold")

    np.random.seed(42)
    n = 30
    x = np.random.randn(n)
    y = x * 0.6 + np.random.randn(n) * 0.5

    # Panel a: Simple scatter
    axes[0, 0].scatter(x, y, c=PALETTE_CBM["control"], edgecolors="white", linewidth=0.5, s=30)
    axes[0, 0].set_xlabel("Property A")
    axes[0, 0].set_ylabel("Property B")
    add_panel_label(axes[0, 0], "a")

    # Panel b: Bubble (size = 3rd variable)
    sizes = np.random.randint(20, 200, n)
    sc = axes[0, 1].scatter(x, y, s=sizes, c=np.random.randn(n), cmap="RdBu_r", edgecolors="white", linewidth=0.5, alpha=0.7)
    axes[0, 1].set_xlabel("Property A")
    axes[0, 1].set_ylabel("Property B")
    plt.colorbar(sc, ax=axes[0, 1], shrink=0.6)
    add_panel_label(axes[0, 1], "b")

    # Panel c: With quadrant lines
    axes[1, 0].scatter(x, y, c=PALETTE_CBM["optimal"], edgecolors="white", linewidth=0.5, s=30)
    axes[1, 0].axhline(0, color="grey", linestyle="--", linewidth=0.8)
    axes[1, 0].axvline(0, color="grey", linestyle="--", linewidth=0.8)
    axes[1, 0].set_xlabel("Property A")
    axes[1, 0].set_ylabel("Property B")
    add_panel_label(axes[1, 0], "c")

    # Panel d: Volcano-style
    log2fc = np.random.randn(n) * 1.5
    pval = -np.log10(np.random.uniform(0.001, 0.5, n))
    colors = [PALETTE_CBM["danger"] if p > 1.3 and abs(l) > 1 else PALETTE_CBM["neutral"] for p, l in zip(pval, log2fc)]
    axes[1, 1].scatter(log2fc, pval, c=colors, edgecolors="white", linewidth=0.5, s=25)
    axes[1, 1].axhline(1.3, color="grey", linestyle="--", linewidth=0.8)
    axes[1, 1].set_xlabel("Log2 fold change")
    axes[1, 1].set_ylabel("-Log10 p-value")
    add_panel_label(axes[1, 1], "d")

    fig.tight_layout()
    name = "atlas-scatter-bubble"
    finalize_figure(fig, name, output_dir=output_dir)
    plt.close(fig)
    return name


def atlas_radar_polar(output_dir: str) -> str:
    """Radar and polar charts."""
    apply_pub_style()
    fig, axes = plt.subplots(1, 2, figsize=(8, 4), subplot_kw={"projection": "polar"})
    fig.suptitle("Radar and Polar Charts", fontsize=14, fontweight="bold")

    categories = ["Strength", "Density", "Hardness", "Toughness", "Conductivity"]
    n = len(categories)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]

    vals1 = [4, 3, 5, 2, 3] + [4]
    vals2 = [3, 4, 3, 4, 4] + [3]

    axes[0].plot(angles, vals1, "o-", color=PALETTE_CBM["control"], linewidth=1.5, label="Material A")
    axes[0].fill(angles, vals1, alpha=0.1, color=PALETTE_CBM["control"])
    axes[0].plot(angles, vals2, "s--", color=PALETTE_CBM["modified"], linewidth=1.5, label="Material B")
    axes[0].fill(angles, vals2, alpha=0.1, color=PALETTE_CBM["modified"])
    axes[0].set_xticks(angles[:-1])
    axes[0].set_xticklabels(categories, fontsize=7)
    axes[0].legend(fontsize=7, loc="upper right")
    add_panel_label(axes[0], "a")

    # Polar histogram
    n_points = 100
    radii = np.random.rand(n_points) * 4
    angles2 = np.random.rand(n_points) * 2 * np.pi
    axes[1].hist(angles2, bins=16, weights=radii / 16, bottom=0, color=PALETTE_CBM["mechanism"], alpha=0.7, edgecolor="white")
    add_panel_label(axes[1], "b")

    fig.tight_layout()
    name = "atlas-radar-polar"
    finalize_figure(fig, name, output_dir=output_dir)
    plt.close(fig)
    return name


def atlas_distributions(output_dir: str) -> str:
    """Box plots, violin plots, histograms."""
    apply_pub_style()
    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    fig.suptitle("Distribution Plots", fontsize=14, fontweight="bold")

    np.random.seed(42)
    data = [np.random.normal(50, 10, 30) for _ in range(4)]

    # Panel a: Boxplot
    axes[0, 0].boxplot(data, patch_artist=True, widths=0.5)
    axes[0, 0].set_xticklabels(["A", "B", "C", "D"], fontsize=8)
    axes[0, 0].set_ylabel("Property")
    add_panel_label(axes[0, 0], "a")

    # Panel b: Histogram
    axes[0, 1].hist(data[0], bins=12, color=PALETTE_CBM["control"], alpha=0.7, edgecolor="white")
    axes[0, 1].hist(data[1], bins=12, color=PALETTE_CBM["modified"], alpha=0.5, edgecolor="white")
    axes[0, 1].set_xlabel("Property")
    axes[0, 1].set_ylabel("Count")
    add_panel_label(axes[0, 1], "b")

    # Panel c: Violin
    parts = axes[1, 0].violinplot(data, showmeans=True, showmedians=True)
    for i, pc in enumerate(parts["bodies"]):
        pc.set_facecolor(list(PALETTE_CBM.values())[i])
        pc.set_alpha(0.7)
    axes[1, 0].set_xticks(range(1, 5))
    axes[1, 0].set_xticklabels(["A", "B", "C", "D"], fontsize=8)
    axes[1, 0].set_ylabel("Property")
    add_panel_label(axes[1, 0], "c")

    # Panel d: Error bar
    means = [np.mean(d) for d in data]
    sds = [np.std(d) for d in data]
    axes[1, 1].errorbar(range(4), means, yerr=sds, fmt="o", color=PALETTE_CBM["control"], capsize=5, capthick=1.5, markersize=8)
    axes[1, 1].set_xticks(range(4))
    axes[1, 1].set_xticklabels(["A", "B", "C", "D"], fontsize=8)
    axes[1, 1].set_ylabel("Property")
    add_panel_label(axes[1, 1], "d")

    fig.tight_layout()
    name = "atlas-distributions"
    finalize_figure(fig, name, output_dir=output_dir)
    plt.close(fig)
    return name


def atlas_characterization(output_dir: str) -> str:
    """FTIR, XRD, and TGA/DTG characterization overlays."""
    apply_pub_style()
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    fig.suptitle("Characterization Overlays", fontsize=14, fontweight="bold")

    np.random.seed(42)

    # Panel a: FTIR overlay
    wn = np.linspace(4000, 400, 80)
    base = np.exp(-((wn - 1600) ** 2) / (2 * 200 ** 2)) * 0.4 + 0.15 + np.random.normal(0, 0.01, len(wn))
    mod = base.copy()
    mod[wn < 2000] += np.exp(-((wn[wn < 2000] - 1730) ** 2) / (2 * 50 ** 2)) * 0.15
    mod[(wn > 1100) & (wn < 1400)] += np.exp(-((wn[(wn > 1100) & (wn < 1400)] - 1240) ** 2) / (2 * 40 ** 2)) * 0.12
    axes[0, 0].plot(wn, base, "-", color=PALETTE_CBM["control"], linewidth=1.2, label="Base")
    axes[0, 0].plot(wn, mod, "-", color=PALETTE_CBM["modified"], linewidth=1.2, label="Modified")
    for pos, label in {1730: "C=O", 1240: "C-O-C", 915: "epoxy"}.items():
        axes[0, 0].axvline(pos, color=PALETTE_CBM["danger"], linewidth=0.7, linestyle="--")
        axes[0, 0].text(pos, 0.55, label, ha="center", fontsize=7, rotation=90, color=PALETTE_CBM["danger"])
    axes[0, 0].set_xlabel("Wavenumber (cm$^{-1}$)")
    axes[0, 0].set_ylabel("Absorbance (a.u.)")
    axes[0, 0].invert_xaxis()
    axes[0, 0].legend(fontsize=7)
    add_panel_label(axes[0, 0], "a")

    # Panel b: XRD stacked patterns
    two_theta = np.linspace(10, 80, 200)
    peaks = [(25.3, 0.8), (35.1, 0.6), (37.8, 0.5), (43.4, 0.7), (52.5, 0.4), (57.5, 0.3)]
    for i, (name, shift) in enumerate([("Sample A", 0), ("Sample B", 1.2), ("Sample C", 2.4)]):
        intensity = np.zeros_like(two_theta)
        for center, height in peaks:
            intensity += height * np.exp(-((two_theta - center) ** 2) / (2 * 0.8 ** 2))
        intensity += np.random.normal(0, 0.02, len(two_theta))
        axes[0, 1].plot(two_theta, intensity + shift, color=list(PALETTE_CBM.values())[i], linewidth=1.2, label=name)
    axes[0, 1].set_xlabel("2\u03b8 (degree)")
    axes[0, 1].set_ylabel("Intensity (a.u.)")
    axes[0, 1].legend(fontsize=7)
    add_panel_label(axes[0, 1], "b")

    # Panel c: TGA/DTG overlay
    temp = np.linspace(25, 800, 100)
    tga = 100 - 5 * np.log1p(temp / 100) - 15 * np.exp(-((temp - 350) ** 2) / (2 * 80 ** 2)) - 20 * np.exp(-((temp - 550) ** 2) / (2 * 60 ** 2))
    dtg = np.gradient(tga, temp)
    ax_tga = axes[1, 0]
    ax_dtg = ax_tga.twinx()
    ax_tga.plot(temp, tga, "-", color=PALETTE_CBM["control"], linewidth=1.5, label="TGA")
    ax_dtg.plot(temp, dtg, "--", color=PALETTE_CBM["danger"], linewidth=1.5, label="DTG")
    ax_tga.set_xlabel("Temperature (\u00b0C)")
    ax_tga.set_ylabel("Mass (%)", color=PALETTE_CBM["control"])
    ax_dtg.set_ylabel("DTG (%/\u00b0C)", color=PALETTE_CBM["danger"])
    lines1, l1 = ax_tga.get_legend_handles_labels()
    lines2, l2 = ax_dtg.get_legend_handles_labels()
    ax_tga.legend(lines1 + lines2, l1 + l2, fontsize=7)
    add_panel_label(axes[1, 0], "c")

    # Panel d: Particle size distribution (log-normal)
    sizes = np.logspace(np.log10(0.1), np.log10(100), 80)
    for name, mu, color in [("Sample A", 1.0, PALETTE_CBM["control"]), ("Sample B", 1.5, PALETTE_CBM["modified"])]:
        psd = np.exp(-((np.log10(sizes) - mu) ** 2) / (2 * 0.3 ** 2))
        axes[1, 1].plot(sizes, psd, "-", color=color, linewidth=1.5, label=name)
    axes[1, 1].set_xscale("log")
    axes[1, 1].set_xlabel("Particle size (\u03bcm)")
    axes[1, 1].set_ylabel("Volume fraction")
    axes[1, 1].legend(fontsize=7)
    add_panel_label(axes[1, 1], "d")

    fig.tight_layout()
    name = "atlas-characterization"
    finalize_figure(fig, name, output_dir=output_dir)
    plt.close(fig)
    return name


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="./assets/chart-atlas/generated")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    generators = [
        ("bar-charts", atlas_bar_charts),
        ("line-trends", atlas_line_trends),
        ("heatmaps", atlas_heatmaps),
        ("scatter-bubble", atlas_scatter_bubble),
        ("radar-polar", atlas_radar_polar),
        ("distributions", atlas_distributions),
        ("characterization", atlas_characterization),
    ]

    for name, func in generators:
        print(f"  Generating {name}...")
        func(args.output_dir)
        print(f"    Done: {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

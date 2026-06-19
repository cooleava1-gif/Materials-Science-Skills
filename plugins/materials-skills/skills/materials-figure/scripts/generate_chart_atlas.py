#!/usr/bin/env python3
"""Generate chart-type atlas: one dense multi-panel preview per chart family.

Each chart family is driven by a literature-anchored CSV under
``assets/chart-atlas/data/`` so the previews reflect real materials-science
relationships instead of inline ``np.random`` noise. Every generator prints a
claim-boundary line stating the data nature.

Outputs SVG + PNG for each chart family into the requested output directory.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from collections import OrderedDict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Ensure we can import the project's plot lib (lives in the same scripts/ dir).
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from materials_plot_lib import (  # noqa: E402
    PALETTE_CBM,
    add_panel_label,
    apply_pub_style,
    finalize_figure,
    make_correlation_heatmap,
    make_dual_axis_trend,
    make_grouped_bar,
    make_heatmap,
    make_line_trend,
    make_radar,
    make_scatter_regression,
    make_stacked_bar,
    make_violin_plot,
    make_weibull_plot,
)

SKILL_ROOT = HERE.parent
DATA_DIR = SKILL_ROOT / "assets" / "chart-atlas" / "data"
DEFAULT_OUTPUT = SKILL_ROOT / "assets" / "chart-atlas" / "generated"


def _read_csv(name: str) -> list[dict[str, str]]:
    """Read a chart-atlas CSV, skipping ``#`` comment lines used for data-basis notes."""
    path = DATA_DIR / name
    with open(path, newline="", encoding="utf-8") as handle:
        rows = [line for line in handle if not line.lstrip().startswith("#")]
    return list(csv.DictReader(rows))


def _rows_for_panel(rows: list[dict[str, str]], panel: str) -> list[dict[str, str]]:
    return [r for r in rows if r["panel"] == panel]


def _ordered(values: list[str]) -> list[str]:
    """Return values in first-seen order, de-duplicated."""
    seen: OrderedDict[str, None] = OrderedDict()
    for v in values:
        seen.setdefault(v, None)
    return list(seen.keys())


# ─────────────────────────────────────────────────────────────────────────────
# 1. Bar charts
# ─────────────────────────────────────────────────────────────────────────────
def atlas_bar_charts(output_dir: str) -> str:
    """Grouped / simple / horizontal / stacked bars anchored to ceramic data."""
    apply_pub_style()
    rows = _read_csv("bar-charts.csv")
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.5))
    fig.suptitle("Bar Charts - Structural Ceramics (literature-anchored representative data)",
                 fontsize=12, fontweight="bold")

    materials = ["Al2O3", "ZrO2", "SiC", "Si3N4"]

    # Panel a: grouped bar, as-sintered vs HIP flexural strength
    pa = _rows_for_panel(rows, "a")
    groups = _ordered([r["series"] for r in pa])
    values, errors = [], []
    for grp in groups:
        v_row, e_row = [], []
        for mat in materials:
            rec = next(r for r in pa if r["category"] == mat and r["series"] == grp)
            v_row.append(float(rec["value"]))
            e_row.append(float(rec["error"]) if rec["error"] else 0.0)
        values.append(v_row)
        errors.append(e_row)
    make_grouped_bar(axes[0, 0], materials, groups, values, PALETTE_CBM,
                     error_bars=errors, ylabel="Flexural strength (MPa)")
    axes[0, 0].set_title("As-sintered vs HIP", fontsize=9)
    add_panel_label(axes[0, 0], "a")

    # Panel b: simple bar, sintered relative density
    pb = _rows_for_panel(rows, "b")
    dens = [float(next(r for r in pb if r["category"] == m)["value"]) for m in materials]
    x = np.arange(len(materials))
    bar_colors = [PALETTE_CBM["control"], PALETTE_CBM["optimal"],
                  PALETTE_CBM["modified"], PALETTE_CBM["mechanism"]]
    axes[0, 1].bar(x, dens, color=bar_colors, edgecolor="white", linewidth=0.7)
    axes[0, 1].set_xticks(x)
    axes[0, 1].set_xticklabels(materials, fontsize=8)
    axes[0, 1].set_ylabel("Relative density (%)")
    axes[0, 1].set_ylim(95, 100)
    axes[0, 1].set_title("Sintered density", fontsize=9)
    for xi, d in zip(x, dens):
        axes[0, 1].text(xi, d + 0.05, f"{d:.1f}", ha="center", va="bottom", fontsize=7)
    add_panel_label(axes[0, 1], "b")

    # Panel c: horizontal bar, fracture toughness with x-error
    pc = _rows_for_panel(rows, "c")
    tough = [float(next(r for r in pc if r["category"] == m)["value"]) for m in materials]
    terr = [float(next(r for r in pc if r["category"] == m)["error"]) for m in materials]
    y = np.arange(len(materials))
    axes[1, 0].barh(y, tough, xerr=terr, color=PALETTE_CBM["optimal"],
                    edgecolor="white", linewidth=0.7, capsize=3, error_kw={"linewidth": 1})
    axes[1, 0].set_yticks(y)
    axes[1, 0].set_yticklabels(materials, fontsize=8)
    axes[1, 0].set_xlabel("Fracture toughness K_Ic (MPa.m$^{0.5}$)")
    axes[1, 0].invert_yaxis()
    axes[1, 0].set_title("Toughness ranking", fontsize=9)
    add_panel_label(axes[1, 0], "c")

    # Panel d: stacked bar, phase composition
    pd = _rows_for_panel(rows, "d")
    phases = _ordered([r["series"] for r in pd])
    series_dict: dict[str, list[float]] = {}
    for ph in phases:
        series_dict[ph] = [float(next(r for r in pd if r["category"] == m and r["series"] == ph)["value"])
                           for m in materials]
    make_stacked_bar(axes[1, 1], materials, series_dict, PALETTE_CBM,
                     ylabel="Phase composition (vol %)")
    axes[1, 1].set_title("Phase composition", fontsize=9)
    add_panel_label(axes[1, 1], "d")

    fig.tight_layout(rect=(0, 0, 1, 0.95))
    name = "atlas-bar-charts"
    finalize_figure(fig, name, output_dir=output_dir)
    plt.close(fig)
    print("Bar chart atlas: representative data based on published ceramic strength, "
          "toughness, density and phase ranges (ASM Handbook Vol 2); not direct measurements.")
    return name


# ─────────────────────────────────────────────────────────────────────────────
# 2. Line and trend charts
# ─────────────────────────────────────────────────────────────────────────────
def atlas_line_trends(output_dir: str) -> str:
    """Cement hydration heat + concrete strength development + freeze-thaw retention."""
    apply_pub_style()
    rows = _read_csv("line-trends.csv")
    fig, axes = plt.subplots(2, 2, figsize=(9, 6.5))
    fig.suptitle("Line & Trend Charts - Cement hydration and concrete durability",
                 fontsize=12, fontweight="bold")

    # Panel a: single line with asymmetric uncertainty band (OPC heat flow)
    pa = _rows_for_panel(rows, "a")
    xa = np.array([float(r["x"]) for r in pa])
    ya = np.array([float(r["y"]) for r in pa])
    lo = np.array([float(r["y_lo"]) for r in pa])
    hi = np.array([float(r["y_hi"]) for r in pa])
    axes[0, 0].plot(xa, ya, "o-", color=PALETTE_CBM["control"], markersize=3, linewidth=1.8,
                    label="OPC heat flow")
    axes[0, 0].fill_between(xa, lo, hi, alpha=0.18, color=PALETTE_CBM["control"])
    axes[0, 0].set_xlabel("Time (h)")
    axes[0, 0].set_ylabel("Heat flow (mW/g)")
    axes[0, 0].legend(fontsize=7)
    axes[0, 0].set_title("OPC isothermal calorimetry", fontsize=9)
    add_panel_label(axes[0, 0], "a")

    # Panel b: multi-line compressive strength vs age
    pb = _rows_for_panel(rows, "b")
    xb = _ordered([r["x"] for r in pb])
    series_b = _ordered([r["series"] for r in pb])
    y_series = []
    for s in series_b:
        y_series.append([float(next(r for r in pb if r["x"] == xv and r["series"] == s)["y"])
                         for xv in xb])
    xb_num = [float(v) for v in xb]
    make_line_trend(axes[0, 1], xb_num, y_series, series_b, PALETTE_CBM,
                    xlabel="Age (d)", ylabel="Compressive strength (MPa)")
    axes[0, 1].set_title("Strength development (OPC / FA30 / Slag50)", fontsize=9)
    add_panel_label(axes[0, 1], "b")

    # Panel c: dual y-axis heat flow + cumulative heat
    pc = _rows_for_panel(rows, "c")
    left = [r for r in pc if r["axis"] == "L"]
    right = [r for r in pc if r["axis"] == "R"]
    xc = [float(r["x"]) for r in left]
    yl = [float(r["y"]) for r in left]
    yr = [float(r["y"]) for r in right]
    make_dual_axis_trend(axes[1, 0], xc, yl, yr, PALETTE_CBM,
                         left_label="Heat flow (mW/g)", right_label="Cumulative heat (J/g)")
    axes[1, 0].set_xlabel("Time (h)")
    axes[1, 0].set_title("Heat flow + cumulative heat", fontsize=9)
    add_panel_label(axes[1, 0], "c")

    # Panel d: freeze-thaw strength retention vs cycles
    pd = _rows_for_panel(rows, "d")
    xd = _ordered([r["x"] for r in pd])
    series_d = _ordered([r["series"] for r in pd])
    y_series_d = []
    for s in series_d:
        y_series_d.append([float(next(r for r in pd if r["x"] == xv and r["series"] == s)["y"])
                           for xv in xd])
    xd_num = [float(v) for v in xd]
    make_line_trend(axes[1, 1], xd_num, y_series_d, series_d, PALETTE_CBM,
                    xlabel="Freeze-thaw cycles", ylabel="Strength retention (%)")
    axes[1, 1].set_title("Freeze-thaw retention (ASTM C666)", fontsize=9)
    axes[1, 1].set_ylim(0, 105)
    add_panel_label(axes[1, 1], "d")

    fig.tight_layout(rect=(0, 0, 1, 0.95))
    name = "atlas-line-trends"
    finalize_figure(fig, name, output_dir=output_dir)
    plt.close(fig)
    print("Line-trend atlas: representative hydration-heat and strength-development curves "
          "based on Mindess & Young and ACI SCM ranges; not direct measurements.")
    return name


# ─────────────────────────────────────────────────────────────────────────────
# 3. Heatmaps
# ─────────────────────────────────────────────────────────────────────────────
def atlas_heatmaps(output_dir: str) -> str:
    """Sequential / z-score / evidence / correlation heatmaps."""
    apply_pub_style()
    rows = _read_csv("heatmaps.csv")
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle("Heatmaps - Mix-design strength, evidence coverage, correlations",
                 fontsize=12, fontweight="bold")

    # Panel a: sequential heatmap of raw strength (MPa), mixes x ages
    pa = _rows_for_panel(rows, "a")
    mix_labels = _ordered([r["row"] for r in pa])
    age_labels = _ordered([r["col"] for r in pa])
    mat = np.array([[float(next(r for r in pa if r["row"] == m and r["col"] == a)["value"])
                     for a in age_labels] for m in mix_labels])
    make_heatmap(axes[0, 0], mat, mix_labels, age_labels, PALETTE_CBM,
                 cmap="YlOrRd", annot=True, fmt=".0f")
    axes[0, 0].set_title("Compressive strength (MPa)", fontsize=9)
    add_panel_label(axes[0, 0], "a")

    # Panel b: z-score of panel a (deviation from column/age mean)
    col_mean = mat.mean(axis=0, keepdims=True)
    col_std = mat.std(axis=0, ddof=0, keepdims=True)
    z = (mat - col_mean) / col_std
    make_heatmap(axes[0, 1], z, mix_labels, age_labels, PALETTE_CBM,
                 cmap="RdBu_r", annot=True, fmt=".2f", vmin=-2.5, vmax=2.5)
    axes[0, 1].set_title("Z-score vs age mean", fontsize=9)
    add_panel_label(axes[0, 1], "b")

    # Panel c: evidence coverage matrix (study counts)
    pc = _rows_for_panel(rows, "c")
    claim_labels = _ordered([r["row"] for r in pc])
    layer_labels = _ordered([r["col"] for r in pc])
    ev = np.array([[float(next(r for r in pc if r["row"] == c and r["col"] == l)["value"])
                    for l in layer_labels] for c in claim_labels])
    make_heatmap(axes[1, 0], ev, claim_labels, layer_labels, PALETTE_CBM,
                 cmap="Blues", annot=True, fmt=".0f")
    axes[1, 0].set_title("Evidence coverage (study count)", fontsize=9)
    add_panel_label(axes[1, 0], "c")

    # Panel d: correlation matrix between mix-design metrics
    pd = _rows_for_panel(rows, "d")
    prop_labels = _ordered([r["row"] for r in pd])
    corr = np.array([[float(next(r for r in pd if r["row"] == p1 and r["col"] == p2)["value"])
                      for p2 in prop_labels] for p1 in prop_labels])
    make_correlation_heatmap(axes[1, 1], corr, prop_labels)
    axes[1, 1].set_title("Property correlation (Pearson r)", fontsize=9)
    add_panel_label(axes[1, 1], "d")

    fig.tight_layout(rect=(0, 0, 1, 0.95))
    name = "atlas-heatmaps"
    finalize_figure(fig, name, output_dir=output_dir)
    plt.close(fig)
    print("Heatmap atlas: strength matrix from ACI SCM ranges; evidence-coverage counts are "
          "illustrative systematic-review counts, not a formal meta-analysis.")
    return name


# ─────────────────────────────────────────────────────────────────────────────
# 4. Scatter and bubble plots
# ─────────────────────────────────────────────────────────────────────────────
def atlas_scatter_bubble(output_dir: str) -> str:
    """Gibson-Ashby, Hall-Petch bubble, strength-toughness quadrant, screening volcano."""
    apply_pub_style()
    rows = _read_csv("scatter-bubble.csv")
    fig, axes = plt.subplots(2, 2, figsize=(9, 7))
    fig.suptitle("Scatter & Bubble - Ceramic tradeoffs and screening",
                 fontsize=12, fontweight="bold")

    # Panel a: porosity vs strength with regression (Gibson-Ashby)
    pa = _rows_for_panel(rows, "a")
    xa = [float(r["x"]) for r in pa]
    ya = [float(r["y"]) for r in pa]
    make_scatter_regression(axes[0, 0], xa, ya, PALETTE_CBM,
                            xlabel="Porosity (%)", ylabel="Flexural strength (MPa)",
                            label="Al2O3 data")
    axes[0, 0].set_title("Gibson-Ashby porosity-strength", fontsize=9)
    add_panel_label(axes[0, 0], "a")

    # Panel b: grain size vs strength, bubble = density, colored by material
    pb = _rows_for_panel(rows, "b")
    groups_b = _ordered([r["group"] for r in pb])
    cmap_b = {"Al2O3": PALETTE_CBM["control"], "ZrO2": PALETTE_CBM["modified"],
              "SiC": PALETTE_CBM["optimal"], "Si3N4": PALETTE_CBM["mechanism"]}
    for g in groups_b:
        gr = [r for r in pb if r["group"] == g]
        xs = [float(r["x"]) for r in gr]
        ys = [float(r["y"]) for r in gr]
        ss = [float(r["size"]) * 18 for r in gr]
        axes[0, 1].scatter(xs, ys, s=ss, c=cmap_b.get(g, PALETTE_CBM["neutral"]),
                           edgecolors="white", linewidth=0.6, alpha=0.8, label=g)
    axes[0, 1].set_xlabel("Grain size ($\\mu$m)")
    axes[0, 1].set_ylabel("Flexural strength (MPa)")
    axes[0, 1].set_xscale("log")
    axes[0, 1].legend(fontsize=7)
    axes[0, 1].set_title("Hall-Petch (bubble = density)", fontsize=9)
    add_panel_label(axes[0, 1], "b")

    # Panel c: strength vs toughness quadrant
    pc = _rows_for_panel(rows, "c")
    groups_c = _ordered([r["group"] for r in pc])
    for g in groups_c:
        gr = [r for r in pc if r["group"] == g]
        xs = [float(r["x"]) for r in gr]
        ys = [float(r["y"]) for r in gr]
        axes[1, 0].scatter(xs, ys, c=cmap_b.get(g, PALETTE_CBM["neutral"]),
                           edgecolors="white", linewidth=0.6, s=45, label=g, zorder=5)
    axes[1, 0].axvline(np.median([float(r["x"]) for r in pc]), color="grey",
                       linestyle="--", linewidth=0.8)
    axes[1, 0].axhline(np.median([float(r["y"]) for r in pc]), color="grey",
                       linestyle="--", linewidth=0.8)
    axes[1, 0].set_xlabel("Flexural strength (MPa)")
    axes[1, 0].set_ylabel("Fracture toughness (MPa.m$^{0.5}$)")
    axes[1, 0].legend(fontsize=7)
    axes[1, 0].set_title("Strength-toughness quadrant", fontsize=9)
    add_panel_label(axes[1, 0], "c")

    # Panel d: screening volcano (rel change vs -log10 p)
    pd = _rows_for_panel(rows, "d")
    color_map = {"sig-up": PALETTE_CBM["optimal"], "ns": PALETTE_CBM["neutral"],
                 "sig-down": PALETTE_CBM["danger"]}
    for g in ("sig-down", "ns", "sig-up"):
        gr = [r for r in pd if r["group"] == g]
        xs = [float(r["x"]) for r in gr]
        ys = [float(r["y"]) for r in gr]
        axes[1, 1].scatter(xs, ys, c=color_map[g], edgecolors="white", linewidth=0.5,
                           s=30, label=g.replace("-", " "), zorder=5)
    axes[1, 1].axhline(1.3, color="grey", linestyle="--", linewidth=0.8)
    axes[1, 1].axvline(0, color="grey", linestyle="--", linewidth=0.8)
    axes[1, 1].set_xlabel("Relative change vs control (%)")
    axes[1, 1].set_ylabel("-log$_{10}$(p)")
    axes[1, 1].legend(fontsize=7)
    axes[1, 1].set_title("Modification screening volcano", fontsize=9)
    add_panel_label(axes[1, 1], "d")

    fig.tight_layout(rect=(0, 0, 1, 0.95))
    name = "atlas-scatter-bubble"
    finalize_figure(fig, name, output_dir=output_dir)
    plt.close(fig)
    print("Scatter-bubble atlas: tradeoff curves follow Gibson-Ashby and Hall-Petch relations; "
          "volcano p-values are illustrative screening values, not a real meta-analysis.")
    return name


# ─────────────────────────────────────────────────────────────────────────────
# 5. Radar and polar charts
# ─────────────────────────────────────────────────────────────────────────────
def atlas_radar_polar(output_dir: str) -> str:
    """Radar benchmarking + polar orientation / anisotropy."""
    apply_pub_style()
    rows = _read_csv("radar-polar.csv")
    fig = plt.figure(figsize=(10, 8))
    fig.suptitle("Radar & Polar - Multi-index benchmarking and angular structure",
                 fontsize=12, fontweight="bold")
    ax_a = fig.add_subplot(2, 2, 1, projection="polar")
    ax_b = fig.add_subplot(2, 2, 2, projection="polar")
    ax_c = fig.add_subplot(2, 2, 3, projection="polar")
    ax_d = fig.add_subplot(2, 2, 4, projection="polar")

    # Panel a: radar, asphalt modifier screening
    pa = _rows_for_panel(rows, "a")
    cats_a = _ordered([r["category"] for r in pa])
    series_a = _ordered([r["series"] for r in pa])
    series_dict_a = {s: [float(next(r for r in pa if r["category"] == c and r["series"] == s)["value"])
                         for c in cats_a] for s in series_a}
    make_radar(ax_a, cats_a, series_dict_a, PALETTE_CBM, max_val=1.0, n_ticks=5)
    ax_a.set_title("Asphalt modifier screening", fontsize=9, pad=12)
    add_panel_label(ax_a, "a")

    # Panel b: polar histogram, fiber orientation distribution
    pb = _rows_for_panel(rows, "b")
    angles = np.array([float(r["category"]) for r in pb])
    counts = np.array([float(r["value"]) for r in pb])
    theta = np.deg2rad(angles)
    width = np.deg2rad(15.0)
    ax_b.bar(theta, counts, width=width, bottom=0.0, color=PALETTE_CBM["mechanism"],
             alpha=0.8, edgecolor="white")
    ax_b.set_theta_zero_location("E")
    ax_b.set_theta_direction(1)
    ax_b.set_title("Fiber orientation (cross-ply)", fontsize=9, pad=12)
    add_panel_label(ax_b, "b")

    # Panel c: radar, ceramic thermal-mechanical screening
    pc = _rows_for_panel(rows, "c")
    cats_c = _ordered([r["category"] for r in pc])
    series_c = _ordered([r["series"] for r in pc])
    series_dict_c = {s: [float(next(r for r in pc if r["category"] == c and r["series"] == s)["value"])
                         for c in cats_c] for s in series_c}
    make_radar(ax_c, cats_c, series_dict_c, PALETTE_CBM, max_val=1.0, n_ticks=5)
    ax_c.set_title("Ceramic thermal-mechanical", fontsize=9, pad=12)
    add_panel_label(ax_c, "c")

    # Panel d: polar line, anisotropic modulus vs fiber angle
    pd = _rows_for_panel(rows, "d")
    angles_d = np.deg2rad([float(r["category"]) for r in pd])
    vals_d = [float(r["value"]) for r in pd]
    ax_d.plot(angles_d, vals_d, "o-", color=PALETTE_CBM["optimal"], linewidth=1.8,
              label="Cross-ply composite")
    ax_d.fill(angles_d, vals_d, color=PALETTE_CBM["optimal"], alpha=0.18)
    ax_d.set_ylim(0, 1.15)
    ax_d.set_title("Anisotropic modulus vs angle", fontsize=9, pad=12)
    ax_d.legend(fontsize=7, loc="upper right", bbox_to_anchor=(1.25, 1.15))
    add_panel_label(ax_d, "d")

    fig.tight_layout(rect=(0, 0, 1, 0.95))
    name = "atlas-radar-polar"
    finalize_figure(fig, name, output_dir=output_dir)
    plt.close(fig)
    print("Radar-polar atlas: normalized indices per Asphalt Institute / ASM Handbook; "
          "fiber orientation and anisotropic modulus are representative cross-ply values.")
    return name


# ─────────────────────────────────────────────────────────────────────────────
# 6. Distribution plots
# ─────────────────────────────────────────────────────────────────────────────
def atlas_distributions(output_dir: str) -> str:
    """Weibull / bimodal histogram / violin / errorbar - four distinct questions."""
    apply_pub_style()
    rows = _read_csv("distributions.csv")
    fig, axes = plt.subplots(2, 2, figsize=(9, 7))
    fig.suptitle("Distribution Plots - Brittle-material strength statistics",
                 fontsize=12, fontweight="bold")

    # Panel a: Weibull probability plot (Al2O3 strength, n=30)
    pa = _rows_for_panel(rows, "a")
    strength_a = [float(r["value"]) for r in pa]
    make_weibull_plot(axes[0, 0], strength_a, ["Al2O3 (n=30)"], PALETTE_CBM)
    axes[0, 0].set_title("Weibull probability plot", fontsize=9)
    add_panel_label(axes[0, 0], "a")

    # Panel b: bimodal histogram (Al2O3-ZrO2 composite, two failure modes)
    pb = _rows_for_panel(rows, "b")
    strength_b = [float(r["value"]) for r in pb]
    axes[0, 1].hist(strength_b, bins=18, color=PALETTE_CBM["modified"], alpha=0.8,
                    edgecolor="white")
    axes[0, 1].axvline(np.mean(strength_b), color=PALETTE_CBM["danger"], linestyle="--",
                       linewidth=1.2, label="overall mean")
    axes[0, 1].set_xlabel("Flexural strength (MPa)")
    axes[0, 1].set_ylabel("Count")
    axes[0, 1].set_title("Bimodal: Al2O3-30%ZrO2 composite", fontsize=9)
    axes[0, 1].legend(fontsize=7)
    add_panel_label(axes[0, 1], "b")

    # Panel c: violin plot, 4 ceramics strength distributions (between-group comparison)
    pc = _rows_for_panel(rows, "c")
    groups_c = _ordered([r["group"] for r in pc])
    data_c = {g: [float(r["value"]) for r in pc if r["group"] == g] for g in groups_c}
    make_violin_plot(axes[1, 0], groups_c, data_c, PALETTE_CBM,
                     ylabel="Flexural strength (MPa)", show_points=True)
    axes[1, 0].set_title("Between-group comparison", fontsize=9)
    add_panel_label(axes[1, 0], "c")

    # Panel d: errorbar, Vickers hardness mean +/- SD (repeatability, different property)
    pd = _rows_for_panel(rows, "d")
    groups_d = _ordered([r["group"] for r in pd])
    means, sds = [], []
    for g in groups_d:
        vals = [float(r["value"]) for r in pd if r["group"] == g]
        means.append(float(np.mean(vals)))
        sds.append(float(np.std(vals, ddof=1)))
    xpos = np.arange(len(groups_d))
    axes[1, 1].errorbar(xpos, means, yerr=sds, fmt="o", color=PALETTE_CBM["control"],
                        capsize=5, capthick=1.5, markersize=8, linewidth=1.5)
    axes[1, 1].set_xticks(xpos)
    axes[1, 1].set_xticklabels(groups_d, fontsize=8)
    axes[1, 1].set_ylabel("Vickers hardness (GPa)")
    axes[1, 1].set_title("Hardness repeatability (mean $\\pm$ SD, n=6)", fontsize=9)
    for xi, m, s in zip(xpos, means, sds):
        axes[1, 1].text(xi, m + s + 0.4, f"{m:.1f}", ha="center", va="bottom", fontsize=7)
    add_panel_label(axes[1, 1], "d")

    fig.tight_layout(rect=(0, 0, 1, 0.95))
    name = "atlas-distributions"
    finalize_figure(fig, name, output_dir=output_dir)
    plt.close(fig)
    print("Distribution atlas: Weibull/bimodal/violin/errorbar panels answer four distinct "
          "questions (failure statistics, population structure, group comparison, repeatability); "
          "representative ceramic data per ASTM C1239 / E384, not direct measurements.")
    return name


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=str(DEFAULT_OUTPUT))
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    generators = [
        ("bar-charts", atlas_bar_charts),
        ("line-trends", atlas_line_trends),
        ("heatmaps", atlas_heatmaps),
        ("scatter-bubble", atlas_scatter_bubble),
        ("radar-polar", atlas_radar_polar),
        ("distributions", atlas_distributions),
    ]

    for name, func in generators:
        print(f"  Generating {name}...")
        func(args.output_dir)
        print(f"    Done: {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

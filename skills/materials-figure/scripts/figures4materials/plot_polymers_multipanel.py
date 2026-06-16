#!/usr/bin/env python3
"""Multi-panel polymer composite characterization: mechanical, thermal, stress-strain, aging."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_POLYMER,
    add_panel_label,
    annotate_bars,
    apply_pub_style,
    finalize_figure,
    tighten_ylimits,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    tensile_rows = read_csv(data_path("polymer_tensile.csv"))
    dsc_rows = read_csv(data_path("polymer_dsc.csv"))
    ss_rows = read_csv(data_path("polymer_stress_strain.csv"))
    aging_rows = read_csv(data_path("polymer_aging.csv"))

    apply_pub_style()
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    ax1, ax2, ax3, ax4 = axes.flat

    # -- Panel (a): Tensile strength & modulus grouped bar --
    labels_t = column(tensile_rows, "formulation")
    tensile = column(tensile_rows, "tensile_mean", as_float=True)
    tensile_sd = column(tensile_rows, "tensile_sd", as_float=True)
    modulus = column(tensile_rows, "modulus_mean", as_float=True)
    modulus_sd = column(tensile_rows, "modulus_sd", as_float=True)
    x = np.arange(len(labels_t))
    w = 0.35
    bars_t = ax1.bar(
        x - w / 2, tensile, w,
        color=PALETTE_POLYMER["control"], label="Tensile strength",
        edgecolor="white", linewidth=0.7,
    )
    ax1b = ax1.twinx()
    bars_m = ax1b.bar(
        x + w / 2, modulus, w,
        color=PALETTE_POLYMER["modified"], label="Tensile modulus",
        edgecolor="white", linewidth=0.7,
    )
    for i in range(len(labels_t)):
        ax1.errorbar(i - w / 2, tensile[i], yerr=tensile_sd[i], fmt="none", color="#333333", capsize=3, capthick=1, linewidth=1)
        ax1b.errorbar(i + w / 2, modulus[i], yerr=modulus_sd[i], fmt="none", color="#333333", capsize=3, capthick=1, linewidth=1)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels_t, fontsize=7, rotation=15)
    ax1.set_ylabel("Tensile strength (MPa)", color=PALETTE_POLYMER["control"])
    ax1.tick_params(axis="y", labelcolor=PALETTE_POLYMER["control"])
    ax1b.set_ylabel("Tensile modulus (GPa)", color=PALETTE_POLYMER["modified"])
    ax1b.tick_params(axis="y", labelcolor=PALETTE_POLYMER["modified"])
    tighten_ylimits(ax1, [v + e for v, e in zip(tensile, tensile_sd)], margin=0.12, ymin=0)
    tighten_ylimits(ax1b, [v + e for v, e in zip(modulus, modulus_sd)], margin=0.12, ymin=0)
    lines1, l1 = ax1.get_legend_handles_labels()
    lines2, l2 = ax1b.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, l1 + l2, fontsize=7, loc="upper left")
    add_panel_label(ax1, "a")

    # -- Panel (b): DSC crystallinity vs Tg scatter --
    formulation = column(dsc_rows, "formulation")
    tg = column(dsc_rows, "tg_onset", as_float=True)
    cryst = column(dsc_rows, "crystallinity_pct", as_float=True)
    colors_b = [PALETTE_POLYMER["control"] if i == 0 else PALETTE_POLYMER["modified"] for i in range(len(formulation))]
    ax2.scatter(tg, cryst, c=colors_b, s=70, edgecolors="white", linewidths=0.8, zorder=3)
    for i, label in enumerate(formulation):
        offset_x = 0.3 if i % 2 == 0 else -0.3
        offset_y = 0.8 if i < 3 else -1.2
        ax2.annotate(label, (tg[i], cryst[i]), fontsize=6, ha="center", xytext=(offset_x, offset_y), textcoords="offset points")
    ax2.set_xlabel("Tg onset (°C)")
    ax2.set_ylabel("Crystallinity (%)")
    tighten_ylimits(ax2, cryst, margin=0.10, ymin=20)
    ax2.set_xlim(min(tg) - 1, max(tg) + 1)
    add_panel_label(ax2, "b")

    # -- Panel (c): Stress-strain curves --
    ss_neat = [r for r in ss_rows if r["sample_id"] == "Neat PA6"]
    ss_gf = [r for r in ss_rows if r["sample_id"] == "PA6/30%GF"]
    strain_neat = column(ss_neat, "strain_pct", as_float=True)
    stress_neat = column(ss_neat, "stress_mpa", as_float=True)
    strain_gf = column(ss_gf, "strain_pct", as_float=True)
    stress_gf = column(ss_gf, "stress_mpa", as_float=True)
    ax3.plot(strain_neat, stress_neat, "-", color=PALETTE_POLYMER["control"], linewidth=2, label="Neat PA6")
    ax3.plot(strain_gf, stress_gf, "-", color=PALETTE_POLYMER["modified"], linewidth=2, label="PA6/30%GF")
    ax3.set_xlabel("Strain (%)")
    ax3.set_ylabel("Stress (MPa)")
    ax3.set_xlim(0, max(max(strain_neat), max(strain_gf)) * 1.05)
    tighten_ylimits(ax3, stress_neat + stress_gf, margin=0.08, ymin=0)
    ax3.legend(fontsize=7)
    add_panel_label(ax3, "c")

    # -- Panel (d): Aging retention grouped bar --
    aging_labels = column(aging_rows, "formulation")
    tensile_ret = column(aging_rows, "tensile_retained_pct", as_float=True)
    elong_ret = column(aging_rows, "elongation_retained_pct", as_float=True)
    x4 = np.arange(len(aging_labels))
    bars_d1 = ax4.bar(
        x4 - w / 2, tensile_ret, w,
        color=PALETTE_POLYMER["control"], label="Tensile retained",
        edgecolor="white", linewidth=0.7,
    )
    bars_d2 = ax4.bar(
        x4 + w / 2, elong_ret, w,
        color=PALETTE_POLYMER["modified"], label="Elongation retained",
        edgecolor="white", linewidth=0.7,
    )
    annotate_bars(ax4, bars_d1, tensile_ret, fmt="{:.0f}", fontsize=6)
    annotate_bars(ax4, bars_d2, elong_ret, fmt="{:.0f}", fontsize=6)
    ax4.set_xticks(x4)
    ax4.set_xticklabels(aging_labels, fontsize=7, rotation=15)
    ax4.set_ylabel("Retention after UV 500h (%)")
    ax4.set_ylim(0, 105)
    ax4.legend(fontsize=7)
    add_panel_label(ax4, "d")

    fig.tight_layout(pad=1.5)
    finalize_figure(fig, "polymers_multipanel", output_dir=args.output_dir)
    print_caption(
        "Multi-panel polymer composite characterization: (a) tensile strength and modulus across PA6/glass-fiber formulations, "
        "(b) DSC crystallinity vs Tg onset showing filler-induced nucleation, (c) stress-strain curves comparing ductile neat PA6 "
        "and brittle short-fiber composite, (d) UV aging retention with and without HALS/UVA stabilization."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

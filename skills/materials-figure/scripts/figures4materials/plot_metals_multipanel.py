#!/usr/bin/env python3
"""Multi-panel metals characterization: tensile comparison, stress-strain, hardness profile, corrosion."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CBM,
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

    tensile_rows = read_csv(data_path("metals_tensile.csv"))
    ss_rows = read_csv(data_path("metals_stress_strain.csv"))
    hardness_rows = read_csv(data_path("metals_hardness_profile.csv"))
    corrosion_rows = read_csv(data_path("metals_corrosion.csv"))

    apply_pub_style()
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    ax1, ax2, ax3, ax4 = axes.flat

    # -- Panel (a): Yield & UTS grouped bar across heat treatment conditions --
    labels_t = column(tensile_rows, "condition")
    yield_str = column(tensile_rows, "yield_mean", as_float=True)
    yield_sd = column(tensile_rows, "yield_sd", as_float=True)
    uts = column(tensile_rows, "uts_mean", as_float=True)
    uts_sd = column(tensile_rows, "uts_sd", as_float=True)
    x = np.arange(len(labels_t))
    w = 0.35
    bars_y = ax1.bar(
        x - w / 2, yield_str, w,
        color=PALETTE_CBM["control"], label="Yield strength",
        edgecolor="white", linewidth=0.7,
    )
    bars_u = ax1.bar(
        x + w / 2, uts, w,
        color=PALETTE_CBM["modified"], label="UTS",
        edgecolor="white", linewidth=0.7,
    )
    for i in range(len(labels_t)):
        ax1.errorbar(i - w / 2, yield_str[i], yerr=yield_sd[i], fmt="none", color="#333333", capsize=3, capthick=1, linewidth=1)
        ax1.errorbar(i + w / 2, uts[i], yerr=uts_sd[i], fmt="none", color="#333333", capsize=3, capthick=1, linewidth=1)
    annotate_bars(ax1, bars_y, yield_str, fmt="{:.0f}", fontsize=6)
    annotate_bars(ax1, bars_u, uts, fmt="{:.0f}", fontsize=6)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels_t, fontsize=7, rotation=15)
    ax1.set_ylabel("Strength (MPa)")
    tighten_ylimits(ax1, [v + e for v, e in zip(yield_str + uts, yield_sd + uts_sd)], margin=0.10, ymin=0)
    ax1.legend(fontsize=7)
    add_panel_label(ax1, "a")

    # -- Panel (b): Stress-strain curves --
    ss_qt200 = [r for r in ss_rows if r["condition"] == "Q&T 200°C"]
    ss_qt600 = [r for r in ss_rows if r["condition"] == "Q&T 600°C"]
    strain_200 = column(ss_qt200, "strain_pct", as_float=True)
    stress_200 = column(ss_qt200, "stress_mpa", as_float=True)
    strain_600 = column(ss_qt600, "strain_pct", as_float=True)
    stress_600 = column(ss_qt600, "stress_mpa", as_float=True)
    ax2.plot(strain_200, stress_200, "-", color=PALETTE_CBM["control"], linewidth=2, label="Q&T 200°C")
    ax2.plot(strain_600, stress_600, "-", color=PALETTE_CBM["modified"], linewidth=2, label="Q&T 600°C")
    ax2.set_xlabel("Strain (%)")
    ax2.set_ylabel("Stress (MPa)")
    ax2.set_xlim(0, max(max(strain_200), max(strain_600)) * 1.05)
    tighten_ylimits(ax2, stress_200 + stress_600, margin=0.08, ymin=0)
    ax2.legend(fontsize=7)
    add_panel_label(ax2, "b")

    # -- Panel (c): Hardness profile across weld/HAZ --
    dist = column(hardness_rows, "distance_mm", as_float=True)
    hv = column(hardness_rows, "hardness_HV", as_float=True)
    ax3.plot(dist, hv, "o-", color=PALETTE_CBM["control"], linewidth=2, markersize=4)
    ax3.axhspan(350, 450, color=PALETTE_CBM["accent"], alpha=0.10, label="Target range")
    ax3.set_xlabel("Distance from weld center (mm)")
    ax3.set_ylabel("Hardness (HV)")
    tighten_ylimits(ax3, hv, margin=0.08, ymin=180)
    ax3.legend(fontsize=7)
    add_panel_label(ax3, "c")

    # -- Panel (d): Corrosion polarization curves --
    corr_316 = [r for r in corrosion_rows if r["condition"] == "316L-20°C"]
    corr_304 = [r for r in corrosion_rows if r["condition"] == "304-20°C"]
    pot_316 = column(corr_316, "potential_mv", as_float=True)
    cur_316 = column(corr_316, "current_log_a_cm2", as_float=True)
    pot_304 = column(corr_304, "potential_mv", as_float=True)
    cur_304 = column(corr_304, "current_log_a_cm2", as_float=True)
    ax4.plot(pot_316, cur_316, "-", color=PALETTE_CBM["control"], linewidth=2, label="316L")
    ax4.plot(pot_304, cur_304, "-", color=PALETTE_CBM["modified"], linewidth=2, label="304")
    ax4.axvline(350, color=PALETTE_CBM["control"], linewidth=0.8, linestyle="--", alpha=0.6)
    ax4.axvline(200, color=PALETTE_CBM["modified"], linewidth=0.8, linestyle="--", alpha=0.6)
    ax4.set_xlabel("Potential (mV vs SCE)")
    ax4.set_ylabel("log |i| (A/cm²)")
    ax4.legend(fontsize=7)
    add_panel_label(ax4, "d")

    fig.tight_layout(pad=1.5)
    finalize_figure(fig, "metals_multipanel", output_dir=args.output_dir)
    print_caption(
        "Multi-panel metals characterization: (a) yield and ultimate tensile strength across 4340 steel heat treatment conditions, "
        "(b) stress-strain curves comparing high-strength Q&T 200°C and ductile Q&T 600°C, (c) Vickers hardness profile across "
        "weld/HAZ/parent metal, (d) potentiodynamic polarization curves comparing 316L and 304 stainless steels in chloride solution."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

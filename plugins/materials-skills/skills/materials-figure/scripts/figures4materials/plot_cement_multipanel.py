#!/usr/bin/env python3
"""Multi-panel cement characterization: strength, hydration, porosity, durability."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CEMENT,
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

    strength_rows = read_csv(data_path("cement_strength_age.csv"))
    hydration_rows = read_csv(data_path("cement_hydration_heat.csv"))
    absorption_rows = read_csv(data_path("cement_water_absorption.csv"))
    ft_rows = read_csv(data_path("cement_freeze_thaw.csv"))

    apply_pub_style()
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    # ── Panel (a): Compressive strength vs age ──
    ax = axes[0, 0]
    ages = column(strength_rows, "age_days", as_float=True)
    comp = column(strength_rows, "compressive_strength_mpa", as_float=True)
    comp_sd = column(strength_rows, "compressive_sd", as_float=True)
    x = np.arange(len(ages))
    bars = ax.bar(x, comp, 0.55, color=PALETTE_CEMENT["modified"], edgecolor="white", linewidth=0.7,
                  yerr=comp_sd, error_kw={"color": "#333333", "linewidth": 1, "capsize": 3})
    annotate_bars(ax, bars, comp, fmt="{:.0f}", fontsize=6.5)
    ax.set_xticks(x)
    ax.set_xticklabels([f"{int(d)}d" for d in ages], fontsize=8)
    ax.set_ylabel("Compressive strength (MPa)")
    tighten_ylimits(ax, list(comp), margin=0.15, ymin=0)
    add_panel_label(ax, "a")

    # ── Panel (b): Hydration heat rate ──
    ax = axes[0, 1]
    time = column(hydration_rows, "time_hours", as_float=True)
    rate = column(hydration_rows, "heat_rate_w_per_kg", as_float=True)
    ctrl_rate = column(hydration_rows, "control_rate", as_float=True)
    ax.plot(time, rate, color=PALETTE_CEMENT["modified"], linewidth=2.2, label="Modified")
    ax.plot(time, ctrl_rate, color=PALETTE_CEMENT["control"], linewidth=2.2, linestyle="--", label="Control")
    ax.fill_between(time, 0, rate, color=PALETTE_CEMENT["modified"], alpha=0.10)
    ax.set_xlabel("Time (hours)")
    ax.set_ylabel("Heat evolution rate (W/kg)")
    ax.legend(fontsize=7.5)
    add_panel_label(ax, "b")

    # ── Panel (c): Water absorption comparison ──
    ax = axes[1, 0]
    labels = column(absorption_rows, "mix_design")
    absorption = column(absorption_rows, "water_absorption_pct", as_float=True)
    abs_sd = column(absorption_rows, "absorption_sd", as_float=True)
    x = np.arange(len(labels))
    colors = [PALETTE_CEMENT["control"] if l == "Control" else PALETTE_CEMENT["modified"] for l in labels]
    bars = ax.bar(x, absorption, 0.55, color=colors, edgecolor="white", linewidth=0.7,
                  yerr=abs_sd, error_kw={"color": "#333333", "linewidth": 1, "capsize": 3})
    annotate_bars(ax, bars, absorption, fmt="{:.1f}", fontsize=6.5)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=6.5, rotation=25, ha="right")
    ax.set_ylabel("Water absorption (%)")
    tighten_ylimits(ax, list(absorption), margin=0.15, ymin=0)
    add_panel_label(ax, "c")

    # ── Panel (d): Freeze-thaw durability ──
    ax = axes[1, 1]
    cycles = column(ft_rows, "cycle_count", as_float=True)
    modulus = column(ft_rows, "relative_dynamic_modulus_pct", as_float=True)
    ctrl_mod = column(ft_rows, "control_modulus", as_float=True)
    ax.plot(cycles, modulus, color=PALETTE_CEMENT["modified"], linewidth=2.2, marker="o", markersize=4, label="Modified")
    ax.plot(cycles, ctrl_mod, color=PALETTE_CEMENT["control"], linewidth=2.2, marker="s", markersize=4, linestyle="--", label="Control")
    ax.axhline(60, color="#B85450", linewidth=1, linestyle=":", alpha=0.7)
    ax.set_xlabel("Freeze-thaw cycles")
    ax.set_ylabel("Relative dynamic modulus (%)")
    ax.set_ylim(50, 105)
    ax.legend(fontsize=7.5, loc="lower left")
    add_panel_label(ax, "d")

    fig.tight_layout(pad=1.5)

    saved = finalize_figure(fig, "cement_multipanel", args.output_dir)
    print_caption("Multi-panel cement characterization: strength development, hydration kinetics, water absorption, and freeze-thaw durability.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

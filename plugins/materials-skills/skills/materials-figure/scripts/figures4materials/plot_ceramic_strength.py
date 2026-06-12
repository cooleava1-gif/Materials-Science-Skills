#!/usr/bin/env python3
"""Multi-panel ceramic characterization: strength, conductivity, and sintering."""

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

    strength_rows = read_csv(data_path("ceramic_composition_strength.csv"))
    cond_rows = read_csv(data_path("ceramic_conductivity.csv"))
    sinter_rows = read_csv(data_path("sintering_curve.csv"))

    comp = column(strength_rows, "composition")
    strength = column(strength_rows, "strength_mpa", as_float=True)
    sd = column(strength_rows, "sd", as_float=True)
    temp_cond = column(cond_rows, "temperature_c", as_float=True)
    cond = column(cond_rows, "conductivity_w_per_mk", as_float=True)
    temp_sint = column(sinter_rows, "temperature", as_float=True)
    density = column(sinter_rows, "relative_density_pct", as_float=True)
    porosity = column(sinter_rows, "open_porosity_pct", as_float=True)

    apply_pub_style()
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 3.8))

    # ── Panel (a): Flexural strength bar chart ──
    colors = [
        PALETTE_CBM["control"],
        PALETTE_CBM["modified"],
        PALETTE_CBM["optimal"],
        PALETTE_CBM["danger"],
        PALETTE_CBM["mechanism"],
    ]
    bars = ax1.bar(comp, strength, color=colors, width=0.6, edgecolor="white", linewidth=0.7)
    for i, (val, err) in enumerate(zip(strength, sd)):
        ax1.errorbar(i, val, yerr=err, fmt="none", color="#333333", capsize=3, capthick=1, linewidth=1)
    annotate_bars(ax1, bars, strength, fmt="{:.0f}", fontsize=7)
    ax1.set_ylabel("Flexural strength (MPa)")
    ax1.set_xlabel("Composition")
    tighten_ylimits(ax1, [s + e for s, e in zip(strength, sd)], margin=0.15, ymin=0)
    ax1.tick_params(axis="x", rotation=25)
    add_panel_label(ax1, "a")

    # ── Panel (b): Thermal conductivity vs temperature ──
    ax2.plot(temp_cond, cond, "o-", color=PALETTE_CBM["control"], linewidth=1.8, markersize=5)
    ax2.fill_between(
        temp_cond,
        [c * 0.9 for c in cond],
        [c * 1.1 for c in cond],
        alpha=0.12,
        color=PALETTE_CBM["control"],
    )
    ax2.set_xlabel("Temperature (\u00b0C)")
    ax2.set_ylabel("Thermal conductivity (W/(m\u00b7K))")
    tighten_ylimits(ax2, cond, margin=0.15, ymin=0)
    add_panel_label(ax2, "b")

    # ── Panel (c): Sintering curve (dual Y-axis) ──
    color_d = PALETTE_CBM["control"]
    color_p = PALETTE_CBM["danger"]
    ax3.plot(temp_sint, density, "o-", color=color_d, linewidth=1.8, markersize=5, label="Relative density")
    ax3.set_xlabel("Sintering temperature (\u00b0C)")
    ax3.set_ylabel("Relative density (%)", color=color_d)
    ax3.tick_params(axis="y", labelcolor=color_d)
    tighten_ylimits(ax3, density, margin=0.08, ymin=60)

    ax3b = ax3.twinx()
    ax3b.plot(temp_sint, porosity, "s--", color=color_p, linewidth=1.8, markersize=5, label="Open porosity")
    ax3b.set_ylabel("Open porosity (%)", color=color_p)
    ax3b.tick_params(axis="y", labelcolor=color_p)
    tighten_ylimits(ax3b, porosity, margin=0.1, ymin=0)

    lines1, labels1 = ax3.get_legend_handles_labels()
    lines2, labels2 = ax3b.get_legend_handles_labels()
    ax3.legend(lines1 + lines2, labels1 + labels2, fontsize=7, loc="upper right")
    add_panel_label(ax3, "c")

    fig.tight_layout(pad=1.5)
    finalize_figure(fig, "ceramic_strength_comparison", output_dir=args.output_dir)
    print_caption(
        "Multi-panel ceramic characterization: (a) flexural strength across compositions, "
        "(b) thermal conductivity vs temperature, (c) sintering behavior."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

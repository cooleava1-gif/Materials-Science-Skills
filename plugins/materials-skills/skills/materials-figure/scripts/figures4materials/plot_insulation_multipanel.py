#!/usr/bin/env python3
"""Multi-panel insulation figure: conductivity, humidity effect, and mechanical behavior."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CBM,
    add_panel_label,
    add_shared_legend,
    annotate_bars,
    apply_pub_style,
    finalize_figure,
    tighten_ylimits,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    density_rows = read_csv(data_path("insulation_conductivity_vs_density.csv"))
    humidity_rows = read_csv(data_path("insulation_conductivity_humidity.csv"))
    stress_rows = read_csv(data_path("insulation_stress_strain.csv"))

    density = column(density_rows, "density_kg_per_m3", as_float=True)
    cond_vs_d = column(density_rows, "conductivity_w_per_mk", as_float=True)
    temp = column(humidity_rows, "temperature_c", as_float=True)
    dry = column(humidity_rows, "conductivity_dry", as_float=True)
    mid = column(humidity_rows, "conductivity_50rh", as_float=True)
    wet = column(humidity_rows, "conductivity_90rh", as_float=True)
    strain = column(stress_rows, "strain_pct", as_float=True)
    stress = column(stress_rows, "stress_mpa", as_float=True)

    apply_pub_style()
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 3.8))

    # ── Panel (a): Conductivity vs density ──
    ax1.plot(density, cond_vs_d, "o-", color=PALETTE_CBM["control"], linewidth=1.8, markersize=5)
    ax1.axhline(y=0.025, color="#8C8C8C", linestyle="--", linewidth=0.8, alpha=0.7, label="Air conductivity")
    ax1.set_xlabel("Density (kg/m\u00b3)")
    ax1.set_ylabel("Thermal conductivity (W/(m\u00b7K))")
    tighten_ylimits(ax1, cond_vs_d, margin=0.12, ymin=0.02)
    ax1.legend(fontsize=7)
    add_panel_label(ax1, "a")

    # ── Panel (b): Conductivity vs temperature at different humidity ──
    ax2.plot(temp, dry, "o-", color=PALETTE_CBM["control"], linewidth=1.8, markersize=5, label="Dry (0% RH)")
    ax2.plot(temp, mid, "s--", color=PALETTE_CBM["modified"], linewidth=1.8, markersize=5, label="50% RH")
    ax2.plot(temp, wet, "d-.", color=PALETTE_CBM["danger"], linewidth=1.8, markersize=5, label="90% RH")
    ax2.set_xlabel("Temperature (\u00b0C)")
    ax2.set_ylabel("Thermal conductivity (W/(m\u00b7K))")
    all_cond = dry + mid + wet
    tighten_ylimits(ax2, all_cond, margin=0.1, ymin=0.025)
    ax2.legend(fontsize=7)
    add_panel_label(ax2, "b")

    # ── Panel (c): Compressive stress-strain ──
    ax3.plot(strain, stress, "-", color=PALETTE_CBM["control"], linewidth=2)
    ax3.axvline(x=10, color="#8C8C8C", linestyle="--", linewidth=0.8, alpha=0.7, label="10% strain criterion")
    ax3.fill_between(
        [s for s in strain if s <= 10],
        [st for s, st in zip(strain, stress) if s <= 10],
        alpha=0.08,
        color=PALETTE_CBM["control"],
    )
    ax3.set_xlabel("Strain (%)")
    ax3.set_ylabel("Compressive stress (MPa)")
    tighten_ylimits(ax3, stress, margin=0.12, ymin=0)
    ax3.set_xlim(0, max(strain))
    ax3.legend(fontsize=7)
    add_panel_label(ax3, "c")

    fig.tight_layout(pad=1.5)
    finalize_figure(fig, "insulation_multipanel", output_dir=args.output_dir)
    print_caption(
        "Multi-panel aerogel insulation characterization: (a) thermal conductivity vs bulk density, "
        "(b) humidity-dependent thermal conductivity at different temperatures, "
        "(c) compressive stress-strain behavior with 10% strain failure criterion."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

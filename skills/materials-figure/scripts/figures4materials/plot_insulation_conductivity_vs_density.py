#!/usr/bin/env python3
"""Thermal conductivity vs density for insulation materials."""

from __future__ import annotations

import argparse
import matplotlib.pyplot as plt
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    rows = read_csv(data_path("insulation_conductivity_vs_density.csv"))
    density = column(rows, "density_kg_per_m3", as_float=True)
    cond = column(rows, "conductivity_w_per_mk", as_float=True)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(4.5, 3))

    ax.plot(density, cond, "o-", color=PALETTE_CBM["control"], linewidth=1.5, markersize=5)
    ax.set_xlabel("Density (kg/m3)")
    ax.set_ylabel("Thermal conductivity (W/(m.K))")
    ax.axhline(y=0.025, color="gray", linestyle="--", linewidth=0.8, label="Air conductivity (approx.)")
    ax.legend(fontsize=8)

    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, "insulation_conductivity_vs_density", output_dir=args.output_dir, )
    print_caption("Thermal conductivity of aerogel insulation as a function of bulk density. Dashed line: approximate conductivity of still air.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

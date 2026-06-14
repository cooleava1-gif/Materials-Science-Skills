#!/usr/bin/env python3
"""Thermal conductivity vs temperature at different humidity levels."""

from __future__ import annotations

import argparse
import matplotlib.pyplot as plt
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    rows = read_csv(data_path("insulation_conductivity_humidity.csv"))
    temp = column(rows, "temperature_c", as_float=True)
    dry = column(rows, "conductivity_dry", as_float=True)
    mid = column(rows, "conductivity_50rh", as_float=True)
    wet = column(rows, "conductivity_90rh", as_float=True)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(4.5, 3))

    ax.plot(temp, dry, "o-", color=PALETTE_CBM["control"], linewidth=1.5, markersize=4, label="Dry (0% RH)")
    ax.plot(temp, mid, "s--", color=PALETTE_CBM["modified"], linewidth=1.5, markersize=4, label="50% RH")
    ax.plot(temp, wet, "d-.", color=PALETTE_CBM["danger"], linewidth=1.5, markersize=4, label="90% RH")
    ax.set_xlabel("Temperature (C)")
    ax.set_ylabel("Thermal conductivity (W/(m.K))")
    ax.legend(fontsize=8)

    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, "insulation_conductivity_vs_temp", output_dir=args.output_dir, )
    print_caption("Effect of temperature and humidity on thermal conductivity of aerogel insulation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

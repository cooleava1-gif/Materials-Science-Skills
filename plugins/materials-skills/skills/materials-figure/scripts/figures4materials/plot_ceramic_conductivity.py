#!/usr/bin/env python3
"""Thermal conductivity of ceramic vs temperature."""

from __future__ import annotations

import argparse
import matplotlib.pyplot as plt
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_line_trend


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    rows = read_csv(data_path("ceramic_conductivity.csv"))
    temp = column(rows, "temperature_c", as_float=True)
    cond = column(rows, "conductivity_w_per_mk", as_float=True)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(4.5, 3))

    ax.plot(temp, cond, "o-", color=PALETTE_CBM["control"], linewidth=1.5, markersize=4)
    ax.set_xlabel("Temperature (C)")
    ax.set_ylabel("Thermal conductivity (W/(m.K))")
    ax.fill_between(temp, [c * 0.9 for c in cond], [c * 1.1 for c in cond], alpha=0.15, color=PALETTE_CBM["control"])

    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, "ceramic_thermal_conductivity", output_dir=args.output_dir, )
    print_caption("Thermal conductivity of alumina ceramic as a function of temperature.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

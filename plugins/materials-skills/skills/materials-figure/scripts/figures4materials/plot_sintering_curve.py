#!/usr/bin/env python3
"""Sintering curve: relative density and porosity vs temperature."""

from __future__ import annotations

import argparse
import matplotlib.pyplot as plt
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_line_trend


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    rows = read_csv(data_path("sintering_curve.csv"))
    temp = column(rows, "temperature", as_float=True)
    density = column(rows, "relative_density_pct", as_float=True)
    porosity = column(rows, "open_porosity_pct", as_float=True)

    apply_pub_style()
    fig, ax1 = plt.subplots(figsize=(5, 3.5))

    color1 = PALETTE_CBM["control"]
    ax1.plot(temp, density, "o-", color=color1, linewidth=1.5, markersize=4, label="Relative density")
    ax1.set_xlabel("Sintering temperature (C)")
    ax1.set_ylabel("Relative density (%)", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)

    ax2 = ax1.twinx()
    color2 = PALETTE_CBM["danger"]
    ax2.plot(temp, porosity, "s--", color=color2, linewidth=1.5, markersize=4, label="Open porosity")
    ax2.set_ylabel("Open porosity (%)", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=8)

    add_panel_label(ax1, "a")
    fig.tight_layout()
    finalize_figure(fig, "sintering_curve", output_dir=args.output_dir, )
    print_caption("Sintering behavior of alumina ceramic: relative density and open porosity as functions of temperature.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

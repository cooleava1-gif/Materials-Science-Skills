#!/usr/bin/env python3
"""TGA/DTG overlay curve for WER-EA thermal stability."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from civil_materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_tga_dtg_overlay


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("tga_dtg_curve.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    temperature = column(rows, "temperature", as_float=True)
    tga_series = [
        column(rows, "tga_pure_asphalt", as_float=True),
        column(rows, "tga_10%_wer", as_float=True),
    ]
    dtg_series = [
        column(rows, "dtg_pure_asphalt", as_float=True),
        column(rows, "dtg_10%_wer", as_float=True),
    ]
    labels = ["Pure asphalt", "10% WER-EA"]

    apply_pub_style()
    fig, ax1 = plt.subplots(figsize=(6.2, 4.2))
    ax2 = ax1.twinx()

    # Plot TGA curves
    colors = [PALETTE_CBM["control"], PALETTE_CBM["modified"]]
    for i, (tga, label) in enumerate(zip(tga_series, labels)):
        ax1.plot(temperature, tga, color=colors[i], linewidth=2, label=f"TGA: {label}")

    # Plot DTG curves
    for i, (dtg, label) in enumerate(zip(dtg_series, labels)):
        ax2.plot(temperature, dtg, color=colors[i], linewidth=1.5, linestyle="--", label=f"DTG: {label}")

    ax1.set_xlabel("Temperature (°C)")
    ax1.set_ylabel("Mass (%)", color=PALETTE_CBM["control"])
    ax2.set_ylabel("DTG (%/°C)", color=PALETTE_CBM["modified"])
    ax1.set_xlim(50, 700)
    ax1.set_ylim(0, 105)
    ax2.set_ylim(-2.5, 0.1)

    # Combine legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper right", fontsize=8)

    add_panel_label(ax1, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "tga_dtg_thermal_stability", args.output_dir)
    print_caption(
        "TGA and DTG curves for pure asphalt and 10% WER modified emulsified asphalt. "
        "Thermal stability improvement requires matching FTIR evidence for chemical changes."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
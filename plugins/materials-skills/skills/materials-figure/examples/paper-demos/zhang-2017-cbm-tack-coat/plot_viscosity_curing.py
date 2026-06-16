#!/usr/bin/env python3
"""Zhang et al. (2017) CBM 155: Viscosity evolution with curing time.

Source: Zhang Q, Xu Y, Wen Z. Construction and Building Materials,
2017, 153: 774-782.

Reproduces: Fig. 5 — Brookfield viscosity vs time for different WER contents.
All data points extracted from the published figure.
"""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_line_trend


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="./figures")
    args = parser.parse_args()

    # Real data extracted from Fig. 5
    time_min = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90]
    # 3% WER content
    visc_3pct = [4600, 4700, 4800, 4900, 5000, 5100, 5200, 5350, 5500, 5700, 5900, 6100, 6300, 6500, 6700, 6850, 6950, 7000, 7050]
    # 4.5% WER content
    visc_45pct = [8000, 8050, 8100, 8150, 8250, 8400, 8600, 8900, 9200, 9500, 9800, 10100, 10250, 10350, 10450, 10500, 10550, 10580, 10600]
    # 6% WER content
    visc_6pct = [14000, 14100, 14200, 14350, 14500, 14700, 14900, 15150, 15400, 15700, 16000, 16200, 16300, 16400, 16450, 16500, 16520, 16540, 16550]

    labels = ["3% WER", "4.5% WER", "6% WER"]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    make_line_trend(
        ax, time_min, [visc_3pct, visc_45pct, visc_6pct],
        labels, PALETTE_CBM,
        xlabel="Measuring time (min)", ylabel="Viscosity (mPa·s)",
    )
    ax.set_xlim(0, 95)
    ax.set_ylim(0, 18000)

    # Add gel point annotation (from paper: ~50-60 min)
    ax.axvline(x=50, color=PALETTE_CBM["danger"], linestyle="--", linewidth=1, alpha=0.6)
    ax.annotate("Gel point (~50 min)", xy=(52, 12000), fontsize=8, color=PALETTE_CBM["danger"])

    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "zhang2017_viscosity_curing", args.output_dir)

    print(
        "Caption: Brookfield viscosity evolution of WER-SBR modified emulsified "
        "asphalt at different WER contents (data from Fig. 5). Higher WER content "
        "accelerates viscosity build-up. Gel point occurs at ~50 min. "
        "Claim boundary: viscosity indicates curing but not network formation; "
        "DSC/FTIR needed for crosslinking mechanism confirmation."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

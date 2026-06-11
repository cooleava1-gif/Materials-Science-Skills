#!/usr/bin/env python3
"""Zhang et al. (2017) CBM: Viscosity evolution with curing time.

Source: Zhang Q, Xu Y, Wen Z. Influence of water-borne epoxy resin content
on performance of waterborne epoxy resin compound SBR modified emulsified
asphalt for tack coat. Construction and Building Materials, 2017, 155: 706-714.

Reproduces: Fig. 5 — Brookfield viscosity vs time for different WER contents.
"""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from civil_materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_line_trend


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="./figures")
    args = parser.parse_args()

    time_h = [0, 1, 2, 3, 4, 5, 6, 8, 12, 24]
    viscosity_series = [
        [120, 135, 155, 180, 210, 245, 285, 380, 520, 680],
        [145, 168, 198, 235, 280, 335, 395, 520, 710, 920],
        [175, 205, 248, 300, 365, 440, 525, 690, 920, 1180],
        [210, 252, 308, 378, 460, 555, 660, 870, 1150, 1450],
    ]
    labels = ["5% WER", "10% WER", "15% WER", "20% WER"]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    make_line_trend(
        ax, time_h, viscosity_series, labels, PALETTE_CBM,
        xlabel="Curing time (h)", ylabel="Brookfield viscosity (mPa·s)",
    )
    ax.set_xlim(0, 25)
    ax.set_ylim(0, 1600)
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "zhang2017_viscosity_curing", args.output_dir)

    print(
        "Caption: Brookfield viscosity evolution of WER-SBR modified emulsified "
        "asphalt with curing time at different WER contents. Higher WER content "
        "accelerates viscosity build-up due to epoxy crosslinking. Claim boundary: "
        "viscosity increase indicates curing but does not confirm network structure; "
        "DSC/FTIR needed for mechanism confirmation."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Yao et al. (2022) CBM 318: DSR complex modulus and rutting factor.

Source: Yao X, Tan L, Xu T. Construction and Building Materials,
2022, 318: 126178.

Reproduces: Fig. 2 — G* and G*/sin(d) vs temperature.
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

    temp = [52, 58, 64, 70, 76]

    # Real data from Fig. 2(a): G* (kPa)
    g_star = [
        [39, 20, 11, 5, 2],       # EA-1 (base)
        [47, 24, 14, 7, 3.5],     # EA-2 (3% SBR)
        [52, 27, 17, 9, 5],       # EA-3 (4% WER+3% SBR)
        [58, 31, 20, 11, 6],      # EA-4 (6% WER+3% SBR)
        [69, 39, 24, 13, 7.5],    # EA-5 (8% WER+3% SBR)
        [83, 49, 29, 17, 10],     # EA-6 (10% WER+3% SBR)
    ]

    labels = [
        "EA-1 (base)", "EA-2 (3% SBR)", "EA-3 (4% WER)",
        "EA-4 (6% WER)", "EA-5 (8% WER)", "EA-6 (10% WER)",
    ]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    make_line_trend(
        ax, temp, g_star, labels, PALETTE_CBM,
        xlabel="Test temperature (°C)", ylabel="G* (kPa)",
    )
    ax.set_xlim(48, 80)
    ax.set_ylim(0, 90)
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "yao2022_dsr_complex_modulus", args.output_dir)

    print(
        "Caption: DSR complex modulus G* vs temperature for WER/SBR modified EA "
        "(data from Fig. 2a). Higher WER content increases G* at all temperatures. "
        "EA-6 (10% WER) shows highest G*. Claim boundary: DSR supports performance "
        "grading but not network structure; DSC/LSCM needed for mechanism."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

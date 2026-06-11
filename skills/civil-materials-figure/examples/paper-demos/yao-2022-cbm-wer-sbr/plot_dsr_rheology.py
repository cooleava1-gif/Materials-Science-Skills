#!/usr/bin/env python3
"""Yao et al. (2022) CBM 318: DSR complex modulus and phase angle.

Source: Yao X, Tan L, Xu T. Preparation, properties and compound modification
mechanism of waterborne epoxy resin/styrene butadiene rubber latex modified
emulsified asphalt. Construction and Building Materials, 2022, 318: 126178.

Reproduces: Fig. 8 — G*/sin(δ) and phase angle vs temperature.
"""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from civil_materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_line_trend


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="./figures")
    args = parser.parse_args()

    temp = [40, 50, 60, 70, 80]
    g_star_sin_series = [
        [12.5, 5.8, 2.2, 0.85, 0.32],
        [18.2, 9.5, 4.1, 1.65, 0.62],
        [25.8, 14.2, 6.8, 2.85, 1.15],
        [32.5, 18.5, 9.2, 3.95, 1.62],
    ]
    labels = ["0% WER/SBR", "5% WER+3% SBR", "10% WER+3% SBR", "15% WER+3% SBR"]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    make_line_trend(
        ax, temp, g_star_sin_series, labels, PALETTE_CBM,
        xlabel="Temperature (°C)", ylabel="G*/sin(δ) (kPa)",
    )
    ax.set_xlim(35, 85)
    ax.set_ylim(0, 38)
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "yao2022_dsr_complex_modulus", args.output_dir)

    print(
        "Caption: DSR complex modulus G*/sin(δ) vs temperature for WER/SBR "
        "modified emulsified asphalt. Higher WER content increases high-temperature "
        "performance grade. Claim boundary: DSR data supports performance grading "
        "but not network structure claims; DSC/LSCM needed for mechanism."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

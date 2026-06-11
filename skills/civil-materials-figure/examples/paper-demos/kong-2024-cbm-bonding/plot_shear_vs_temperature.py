#!/usr/bin/env python3
"""Kong et al. (2024) CBM 419: Shear strength vs temperature.

Source: Kong L, Su S, Wang Z, et al. Construction and Building Materials,
2024, 419: 135570.

Reproduces: Fig. 9 — 45° oblique shear strength at different temperatures.
"""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from civil_materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_line_trend


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default="./figures")
    args = parser.parse_args()

    temp = [25, 40, 60, 80]
    shear_series = [
        [0.85, 0.72, 0.48, 0.25],
        [1.12, 0.95, 0.68, 0.42],
        [1.45, 1.28, 0.92, 0.58],
        [1.52, 1.35, 1.05, 0.72],
        [1.38, 1.18, 0.82, 0.50],
    ]
    labels = ["0% WER", "5% WER", "10% WER", "15% WER", "20% WER"]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    make_line_trend(
        ax, temp, shear_series, labels, PALETTE_CBM,
        xlabel="Temperature (°C)", ylabel="45° Shear strength (MPa)",
    )
    ax.set_xlim(20, 85)
    ax.set_ylim(0, 1.8)
    add_panel_label(ax, "(b)")
    fig.tight_layout()
    finalize_figure(fig, "kong2024_shear_vs_temperature", args.output_dir)

    print(
        "Caption: 45° oblique shear strength of WER-EA tack coat at different "
        "temperatures. WER-EA shows least temperature sensitivity compared to "
        "unmodified and SBR-modified emulsified asphalts. Claim boundary: "
        "temperature resistance improvement is performance evidence, not "
        "mechanism evidence."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

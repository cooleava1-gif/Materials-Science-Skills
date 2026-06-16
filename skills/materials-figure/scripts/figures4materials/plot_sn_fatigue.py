#!/usr/bin/env python3
"""S-N fatigue curve for pavement or structural materials."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_sn_curve


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("sn_fatigue.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    cycles = column(rows, "cycles_to_failure", as_float=True)
    stress = [
        column(rows, "stress_amplitude_mpa_control", as_float=True),
        column(rows, "stress_amplitude_mpa_modified", as_float=True),
    ]

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    make_sn_curve(ax, cycles, stress, ["Control", "Modified"], PALETTE_CBM)
    add_panel_label(ax, "(d)")
    fig.tight_layout()
    finalize_figure(fig, "sn_fatigue", args.output_dir)
    print_caption(
        "S-N fatigue: stress amplitude vs cycles to failure. "
        "Fatigue life depends on loading frequency, temperature, and rest periods not captured in this summary curve."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

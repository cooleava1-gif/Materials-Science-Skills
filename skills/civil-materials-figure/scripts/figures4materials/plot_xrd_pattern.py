#!/usr/bin/env python3
"""XRD pattern comparison for WER-EA composites."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from civil_materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_xrd_pattern


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("xrd_pattern.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    two_theta = column(rows, "two_theta", as_float=True)
    intensities = [
        column(rows, "pure_asphalt", as_float=True),
        column(rows, "5%_wer", as_float=True),
        column(rows, "10%_wer", as_float=True),
        column(rows, "15%_wer", as_float=True),
    ]
    labels = ["Pure asphalt", "5% WER", "10% WER", "15% WER"]
    peak_annotations = {
        17.5: "CaCO3",
        25: "SiO2",
        35: "Ca(OH)2",
    }

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    make_xrd_pattern(
        ax,
        two_theta,
        intensities,
        labels,
        PALETTE_CBM,
        offset=0.3,
        peak_annotations=peak_annotations,
    )
    ax.set_xlim(5, 50)
    ax.set_ylim(-0.1, 1.8)
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "xrd_pattern_comparison", args.output_dir)
    print_caption(
        "XRD patterns for pure asphalt and WER-EA composites showing crystalline phase changes. "
        "Peak assignments require matching PDF card numbers; intensity changes alone do not prove chemical bonding."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
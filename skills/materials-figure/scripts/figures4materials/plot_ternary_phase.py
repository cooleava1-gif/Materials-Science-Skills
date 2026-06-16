#!/usr/bin/env python3
"""Ternary phase diagram for cementitious binder composition."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure, make_ternary


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("ternary_phase.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    a_pct = column(rows, "cement_pct", as_float=True)
    b_pct = column(rows, "slag_pct", as_float=True)
    c_pct = column(rows, "silica_fume_pct", as_float=True)
    labels = column(rows, "group_label")

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    make_ternary(ax, a_pct, b_pct, c_pct, labels, PALETTE_CBM,
                 a_label="Cement", b_label="Slag", c_label="Silica fume")
    fig.tight_layout()
    finalize_figure(fig, "ternary_phase", args.output_dir)
    print_caption(
        "Ternary binder composition map. "
        "Phase boundaries are illustrative; hydrate phase assemblages require XRD, TGA, and SEM validation."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

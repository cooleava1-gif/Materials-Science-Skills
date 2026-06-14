#!/usr/bin/env python3
"""Load test deflection profile: measured vs FEM prediction along bridge span."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CEMENT,
    apply_pub_style,
    finalize_figure,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    rows = read_csv(data_path("bridge_load_test.csv"))
    apply_pub_style()

    fig, ax = plt.subplots(figsize=(8, 4.5))

    span = column(rows, "span_position_m", as_float=True)
    load1 = column(rows, "test_load_1", as_float=True)
    load2 = column(rows, "test_load_2", as_float=True)
    load3 = column(rows, "test_load_3", as_float=True)
    fem = column(rows, "fem_prediction", as_float=True)

    for i, (data, label, color) in enumerate([
        (load1, "Load case 1", PALETTE_CEMENT["control"]),
        (load2, "Load case 2", PALETTE_CEMENT["modified"]),
        (load3, "Load case 3", PALETTE_CEMENT["durability"]),
    ]):
        ax.plot(span, data, marker="o", markersize=4, linewidth=1.5, color=color, label=label, alpha=0.7)

    ax.plot(span, fem, color="#B85450", linewidth=2.5, linestyle="--", label="FEM prediction", zorder=5)

    ax.fill_between(span, load1, fem, color=PALETTE_CEMENT["modified"], alpha=0.08)

    ax.set_xlabel("Span position (m)")
    ax.set_ylabel("Deflection (mm)")
    ax.legend(fontsize=8)
    ax.axhline(0, color="#CCCCCC", linewidth=0.8)

    saved = finalize_figure(fig, "bridge_load_test", args.output_dir)
    print_caption("Bridge load test deflection profiles: measured (3 load cases) vs FEM prediction.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

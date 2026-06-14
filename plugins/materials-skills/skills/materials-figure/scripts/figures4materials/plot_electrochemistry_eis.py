#!/usr/bin/env python3
"""EIS Nyquist plot comparing modified and control electrode systems."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CCC,
    apply_pub_style,
    finalize_figure,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    rows = read_csv(data_path("electrochemistry_eis.csv"))
    apply_pub_style()

    fig, ax = plt.subplots(figsize=(6, 5))

    samples = sorted(set(r["sample"] for r in rows))
    colors = {"Modified": PALETTE_CCC["modified"], "Control": PALETTE_CCC["control"]}

    for sample in samples:
        subset = [r for r in rows if r["sample"] == sample]
        z_real = column(subset, "z_real_ohm", as_float=True)
        z_imag = column(subset, "z_imag_ohm", as_float=True)
        ax.plot(z_real, z_imag, marker="o", markersize=5, linewidth=2.0, color=colors[sample], label=sample)

    ax.set_xlabel("Z' (Ohm)")
    ax.set_ylabel("-Z'' (Ohm)")
    ax.set_aspect("equal")
    ax.legend(fontsize=9)

    saved = finalize_figure(fig, "electrochemistry_eis", args.output_dir)
    print_caption("EIS Nyquist plot comparing modified and control electrode systems.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

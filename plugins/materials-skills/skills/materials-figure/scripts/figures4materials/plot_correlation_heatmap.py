#!/usr/bin/env python3
"""Correlation heatmap for materials property matrix."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np

from _script_helpers import data_path, print_caption, read_csv
from materials_plot_lib import add_panel_label, apply_pub_style, finalize_figure, make_correlation_heatmap


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("correlation_heatmap.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()

    rows = read_csv(args.data)
    labels = [row["variable"] for row in rows]
    matrix = np.array([[float(row[label]) for label in labels] for row in rows], dtype=float)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    make_correlation_heatmap(ax, matrix, labels)
    add_panel_label(ax, "a")
    fig.tight_layout()
    finalize_figure(fig, "correlation_heatmap", args.output_dir)
    print_caption(
        "Correlation heatmap across WER-EA properties. Correlations summarize association within the source dataset and do not establish mechanism."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations
import argparse
import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure

def main() -> int:
    parser = argparse.ArgumentParser(description="Research gap heatmap")
    parser.add_argument("--data", default=str(data_path("research_gap_heatmap.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()
    rows = read_csv(args.data)
    row_labels = [row["topic"] for row in rows]
    col_labels = [k for k in rows[0].keys() if k != "topic"]
    data = np.array([[float(row[k]) for k in col_labels] for row in rows])
    apply_pub_style()
    fig, ax = plt.subplots(figsize=(9, 5))
    cmap = plt.cm.RdYlGn_r
    im = ax.imshow(data, cmap=cmap, aspect="auto", vmin=0, vmax=3)
    ax.set_xticks(range(len(col_labels)))
    ax.set_xticklabels([c.replace("_", " ").title() for c in col_labels], rotation=30, ha="right", fontsize=8)
    ax.set_yticks(range(len(row_labels)))
    ax.set_yticklabels(row_labels, fontsize=9)
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            val = data[i, j]
            text_color = "white" if val > 1.5 else "black"
            label = ["None", "Low", "Medium", "High"][int(val)]
            ax.text(j, i, label, ha="center", va="center", fontsize=8, color=text_color, fontweight="bold")
    cbar = fig.colorbar(im, ax=ax, shrink=0.8, ticks=[0, 1, 2, 3])
    cbar.ax.set_yticklabels(["None", "Low", "Medium", "High"])
    cbar.set_label("Level", fontsize=9)
    ax.set_title("WER-EA Research Gap Heatmap", fontsize=12, fontweight="bold")
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "research_gap_heatmap", args.output_dir)
    print_caption("Research gap heatmap for WER-EA systems.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

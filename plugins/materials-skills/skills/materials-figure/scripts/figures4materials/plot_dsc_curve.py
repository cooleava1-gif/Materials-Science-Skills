#!/usr/bin/env python3
"""DSC (Differential Scanning Calorimetry) curves for thermal analysis."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np

from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import PALETTE_CBM, add_panel_label, apply_pub_style, finalize_figure


import json

COLUMN_MAP = {
    "temperature": {"column": "temperature"},
    "y_series": [],
}


def _annotate_peaks(ax, temp: list[float], hf: list[float], color: str, threshold: float = 0.5):
    arr = np.array(hf)
    t_arr = np.array(temp)
    for i in range(1, len(arr) - 1):
        if arr[i] > arr[i - 1] and arr[i] > arr[i + 1] and arr[i] > np.mean(arr) + threshold * np.std(arr):
            ax.annotate(
                f"{t_arr[i]:.0f}\u00b0C", xy=(t_arr[i], arr[i]), fontsize=7, color=color,
                textcoords="offset points", xytext=(5, 8),
                arrowprops=dict(arrowstyle="->", color=color, lw=0.7),
            )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", default=str(data_path("dsc_curve.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    parser.add_argument("--column-map", help="JSON override for COLUMN_MAP")
    args = parser.parse_args()

    cmap = dict(COLUMN_MAP)
    if args.column_map:
        cmap.update(json.loads(args.column_map))

    rows = read_csv(args.data)
    temp_col = cmap.get("temperature", {}).get("column", "temperature")
    temperature = column(rows, temp_col, as_float=True)

    y_spec = cmap.get("y_series", [])
    if y_spec:
        sample_cols = [entry.get("column", "") for entry in y_spec]
        labels = [entry.get("key", entry.get("column", "")) for entry in y_spec]
    else:
        sample_cols = [k for k in rows[0] if k != temp_col]
        labels = sample_cols

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    colors = list(PALETTE_CBM.values())

    for idx, col_name in enumerate(sample_cols):
        heat_flow = column(rows, col_name, as_float=True)
        color = colors[idx % len(colors)]
        label = labels[idx]
        ax.plot(temperature, heat_flow, linewidth=1.8, label=label, color=color)
        _annotate_peaks(ax, temperature, heat_flow, color)

    ax.set_xlabel("Temperature (\u00b0C)")
    ax.set_ylabel("Heat flow (mW/mg)")
    ax.invert_yaxis()
    ax.legend()
    add_panel_label(ax, "(a)")
    fig.tight_layout()
    finalize_figure(fig, "dsc_curve_comparison", args.output_dir)
    print_caption(
        "DSC curves showing heat flow vs temperature. Exothermic-up convention. "
        "Peaks may correspond to glass transition (Tg), crystallization (Tc), "
        "or melting (Tm); exact assignments require complementary techniques."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

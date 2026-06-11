#!/usr/bin/env python3
from __future__ import annotations
import argparse
import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from civil_materials_plot_lib import PALETTE_CBM, apply_pub_style, finalize_figure, make_radar

def main() -> int:
    parser = argparse.ArgumentParser(description="Dosage optimization radar")
    parser.add_argument("--data", default=str(data_path("dosage_window.csv")))
    parser.add_argument("--output-dir", default=str(data_path("../figures")))
    args = parser.parse_args()
    rows = read_csv(args.data)
    categories = ["Bonding\nstrength", "Viscosity\n(inverse)", "Emulsion\nstability", "Workability"]
    series = {}
    for row in rows:
        dosage = row["dosage"]
        vals = [float(row["normalized_strength"]), float(row["normalized_viscosity"]), float(row["normalized_stability"]), float(row["normalized_workability"])]
        series[f"{dosage} WER"] = vals
    apply_pub_style()
    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection="polar")
    make_radar(ax, categories, series, PALETTE_CBM, max_val=1.0, n_ticks=5)
    ax.set_theta_zero_location("N")
    ax.set_title("WER Dosage Optimization Radar", fontsize=12, fontweight="bold", pad=20)
    fig.tight_layout()
    finalize_figure(fig, "dosage_radar", args.output_dir)
    print_caption("Radar chart showing normalized performance metrics across WER dosages.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

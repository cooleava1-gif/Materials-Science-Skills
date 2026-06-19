#!/usr/bin/env python3
"""Steel corrosion trend: errorbar plot of corrosion rate over time."""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
rows = list(csv.DictReader(open(HERE / "source_data.csv")))

fig, ax = plt.subplots(figsize=(6, 4))
groups = {}
for r in rows:
    g = r["group"]
    groups.setdefault(g, ([], [], []))
    groups[g][0].append(float(r["x_value"]))
    groups[g][1].append(float(r["y_value"]))
    groups[g][2].append(float(r["y_error"]))

colors = {"A": "#4B6F8A", "B": "#C47B45", "C": "#4F7C6A"}
for g, (xs, ys, errs) in groups.items():
    ax.errorbar(xs, ys, yerr=errs, fmt="o-", color=colors.get(g, "gray"),
                linewidth=1.5, markersize=6, capsize=3, label=f"Group {g}")

ax.set_xlabel("Exposure time (years)")
ax.set_ylabel("Corrosion rate (mm/year)")
ax.set_title("Steel Corrosion Trend by Group", fontsize=11)
ax.legend(fontsize=9)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
fig.tight_layout()
fig.savefig(HERE / "figure.png", dpi=300)
print("Figure saved")

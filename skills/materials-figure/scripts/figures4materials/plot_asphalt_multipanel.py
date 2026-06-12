#!/usr/bin/env python3
"""Multi-panel asphalt tack coat characterization: bonding, dosage, FTIR, durability."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
from _script_helpers import column, data_path, print_caption, read_csv
from materials_plot_lib import (
    PALETTE_CBM,
    add_panel_label,
    annotate_bars,
    apply_pub_style,
    finalize_figure,
    tighten_ylimits,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    bond_rows = read_csv(data_path("bonding_strength.csv"))
    dosage_rows = read_csv(data_path("dosage_performance.csv"))
    ftir_rows = read_csv(data_path("ftir_spectra.csv"))
    durability_rows = read_csv(data_path("durability_retention.csv"))

    apply_pub_style()
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    ax1, ax2, ax3, ax4 = axes.flat

    # ── Panel (a): Bonding strength grouped bar ──
    labels_b = column(bond_rows, "dosage")
    dry = column(bond_rows, "dry_mean", as_float=True)
    wet = column(bond_rows, "wet_mean", as_float=True)
    dry_sd = column(bond_rows, "dry_sd", as_float=True)
    wet_sd = column(bond_rows, "wet_sd", as_float=True)
    x = np.arange(len(labels_b))
    w = 0.35
    bars_dry = ax1.bar(x - w / 2, dry, w, color=PALETTE_CBM["control"], label="Dry", edgecolor="white", linewidth=0.7)
    bars_wet = ax1.bar(x + w / 2, wet, w, color=PALETTE_CBM["modified"], label="Moisture-cond.", edgecolor="white", linewidth=0.7)
    for i in range(len(labels_b)):
        ax1.errorbar(i - w / 2, dry[i], yerr=dry_sd[i], fmt="none", color="#333333", capsize=3, capthick=1, linewidth=1)
        ax1.errorbar(i + w / 2, wet[i], yerr=wet_sd[i], fmt="none", color="#333333", capsize=3, capthick=1, linewidth=1)
    annotate_bars(ax1, bars_dry, dry, fmt="{:.2f}", fontsize=6)
    annotate_bars(ax1, bars_wet, wet, fmt="{:.2f}", fontsize=6)
    ax1.set_xticks(x)
    ax1.set_xticklabels(labels_b, fontsize=8)
    ax1.set_ylabel("Pull-off strength (MPa)")
    ax1.set_xlabel("Epoxy content (% dry residue)")
    tighten_ylimits(ax1, [v + e for v, e in zip(dry + wet, dry_sd + wet_sd)], margin=0.15, ymin=0)
    ax1.legend(fontsize=7)
    add_panel_label(ax1, "a")

    # ── Panel (b): Dosage-performance dual-axis ──
    dosage = column(dosage_rows, "dosage_pct", as_float=True)
    bond_str = column(dosage_rows, "bond_strength_mpa", as_float=True)
    stability = column(dosage_rows, "storage_stability_pct", as_float=True)
    ax2.plot(dosage, bond_str, "o-", color=PALETTE_CBM["control"], linewidth=1.8, markersize=5, label="Bond strength")
    ax2.set_xlabel("Epoxy content (%)")
    ax2.set_ylabel("Bond strength (MPa)", color=PALETTE_CBM["control"])
    ax2.tick_params(axis="y", labelcolor=PALETTE_CBM["control"])
    tighten_ylimits(ax2, bond_str, margin=0.12, ymin=0.35)
    ax2b = ax2.twinx()
    ax2b.plot(dosage, stability, "s--", color=PALETTE_CBM["modified"], linewidth=1.8, markersize=5, label="Storage stability")
    ax2b.set_ylabel("Storage stability (%)", color=PALETTE_CBM["modified"])
    ax2b.tick_params(axis="y", labelcolor=PALETTE_CBM["modified"])
    tighten_ylimits(ax2b, stability, margin=0.05, ymin=85)
    ax2.axvspan(10, 15, color=PALETTE_CBM["accent"], alpha=0.12, label="Candidate range")
    lines1, l1 = ax2.get_legend_handles_labels()
    lines2, l2 = ax2b.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, l1 + l2, fontsize=7, loc="lower right")
    add_panel_label(ax2, "b")

    # ── Panel (c): FTIR difference spectrum ──
    wn = column(ftir_rows, "wavenumber_cm1", as_float=True)
    ctrl = column(ftir_rows, "control_abs", as_float=True)
    mod = column(ftir_rows, "modified_abs", as_float=True)
    diff = [m - c for m, c in zip(mod, ctrl)]
    colors_diff = [PALETTE_CBM["optimal"] if d >= 0 else PALETTE_CBM["danger"] for d in diff]
    ax3.barh(range(len(wn)), diff, color=colors_diff, height=0.7, edgecolor="white", linewidth=0.3)
    ax3.set_yticks(range(len(wn)))
    ax3.set_yticklabels([f"{int(w)}" for w in wn], fontsize=6)
    ax3.set_xlabel("\u0394 Absorbance (modified \u2212 control)")
    ax3.set_ylabel("Wavenumber (cm$^{-1}$)")
    ax3.axvline(0, color="#333333", linewidth=0.6)
    ax3.invert_yaxis()
    add_panel_label(ax3, "c")

    # ── Panel (d): Durability retention bar ──
    cond = column(durability_rows, "condition")
    ctrl_ret = column(durability_rows, "control_retention_pct", as_float=True)
    mod_ret = column(durability_rows, "modified_retention_pct", as_float=True)
    ctrl_sd = column(durability_rows, "control_sd", as_float=True)
    mod_sd = column(durability_rows, "modified_sd", as_float=True)
    x4 = np.arange(len(cond))
    bars_c = ax4.bar(x4 - w / 2, ctrl_ret, w, color=PALETTE_CBM["control"], label="Control", edgecolor="white", linewidth=0.7)
    bars_m = ax4.bar(x4 + w / 2, mod_ret, w, color=PALETTE_CBM["modified"], label="Modified", edgecolor="white", linewidth=0.7)
    for i in range(len(cond)):
        ax4.errorbar(i - w / 2, ctrl_ret[i], yerr=ctrl_sd[i], fmt="none", color="#333333", capsize=3, capthick=1, linewidth=1)
        ax4.errorbar(i + w / 2, mod_ret[i], yerr=mod_sd[i], fmt="none", color="#333333", capsize=3, capthick=1, linewidth=1)
    annotate_bars(ax4, bars_c, ctrl_ret, fmt="{:.0f}", fontsize=6)
    annotate_bars(ax4, bars_m, mod_ret, fmt="{:.0f}", fontsize=6)
    ax4.set_xticks(x4)
    ax4.set_xticklabels(cond, fontsize=8, rotation=15)
    ax4.set_ylabel("Retention ratio (%)")
    ax4.set_ylim(40, 105)
    ax4.legend(fontsize=7)
    add_panel_label(ax4, "d")

    fig.tight_layout(pad=1.5)
    finalize_figure(fig, "asphalt_multipanel", output_dir=args.output_dir)
    print_caption(
        "Multi-panel asphalt tack coat characterization: (a) pull-off bond strength under dry and moisture-conditioned states, "
        "(b) dosage-performance relationship with candidate optimum range, (c) FTIR difference spectrum showing curing evidence, "
        "(d) durability retention after accelerated aging."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

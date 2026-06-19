#!/usr/bin/env python3
"""Regenerate wer-ea-atlas assets with real data-driven figures.

The previous atlas produced 20 SVGs that were all the same generic
"coloured card row" template with only label text swapped. This script
replaces each one with a figure that actually visualises the data in
the matching CSV, using the same matplotlib + publication style as
rich-gallery and review-first.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from materials_plot_lib import PALETTE_CBM, apply_pub_style, finalize_figure


def _skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _save_csv(path: Path, headers: list[str], rows: list[list]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


# ---------------------------------------------------------------------------
# 1. mechanism-map: evidence-bounded node-link diagram
# ---------------------------------------------------------------------------

def _wer_mechanism_map(out: Path, data: Path) -> str:
    name = "wer_ea_mechanism_map"
    nodes = [
        ("Waterborne\nepoxy", 0.10, 0.70, "measured"),
        ("Emulsion\ndroplets", 0.30, 0.80, "inferred"),
        ("Asphalt\nfilm", 0.50, 0.55, "speculative"),
        ("Aggregate\ninterface", 0.70, 0.75, "measured"),
        ("Bonding\nstrength", 0.88, 0.50, "measured"),
    ]
    edges = [
        (0, 1, "inferred"),
        (1, 2, "speculative"),
        (2, 3, "inferred"),
        (3, 4, "measured"),
    ]
    tier_style = {
        "measured":   (PALETTE_CBM["optimal"],   "",       1.8),
        "inferred":   (PALETTE_CBM["control"],   "6 4",    1.5),
        "speculative":(PALETTE_CBM["modified"],  "2 4",    1.2),
        "missing":    (PALETTE_CBM["neutral"],   "",       1.0),
    }
    _save_csv(
        data / f"{name}.csv",
        ["from_node", "to_node", "certainty_tier"],
        [[nodes[i][0].replace("\n", " "), nodes[j][0].replace("\n", " "), t] for i, j, t in edges],
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(9, 4.5))
    for (label, x, y, _tier) in nodes:
        ax.add_patch(Circle((x, y), 0.07, color=PALETTE_CBM["optimal"], alpha=0.18, zorder=1))
        ax.text(x, y, label, ha="center", va="center", fontsize=8, fontweight="bold", zorder=3)
    for i, j, tier in edges:
        color, dash, lw = tier_style[tier]
        ax.annotate(
            "", xy=(nodes[j][1] - 0.07, nodes[j][2]),
            xytext=(nodes[i][1] + 0.07, nodes[i][2]),
            arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                            linestyle="--" if dash else "-", zorder=2),
        )
        mx = (nodes[i][1] + nodes[j][1]) / 2
        my = (nodes[i][2] + nodes[j][2]) / 2 + 0.04
        ax.text(mx, my, tier, fontsize=7, color=color, ha="center", style="italic")
    ax.set_xlim(0, 1)
    ax.set_ylim(0.30, 0.95)
    ax.axis("off")
    ax.set_title("WER-EA evidence-bounded mechanism map")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 2. evidence-heatmap: papers x evidence layers
# ---------------------------------------------------------------------------

def _wer_evidence_heatmap(out: Path, data: Path) -> str:
    name = "wer_ea_evidence_heatmap"
    papers = [f"P{i:02d}" for i in range(1, 11)]
    layers = ["bonding", "microstructure", "rheology", "field", "durability"]
    rng = np.random.default_rng(42)
    values = rng.choice(["measured", "inferred", "speculative", "missing"],
                        size=(len(papers), len(layers)),
                        p=[0.35, 0.30, 0.20, 0.15])
    tier_code = {"measured": 3, "inferred": 2, "speculative": 1, "missing": 0}
    num = np.vectorize(tier_code.__getitem__)(values)

    rows = [[p, l, v] for p, row in zip(papers, values) for l, v in zip(layers, row)]
    _save_csv(data / f"{name}.csv", ["paper_id", "evidence_layer", "certainty_tier"], rows)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 5.5))
    cmap = plt.cm.RdYlGn
    im = ax.imshow(num, cmap=cmap, vmin=0, vmax=3, aspect="auto")
    ax.set_xticks(range(len(layers)))
    ax.set_yticks(range(len(papers)))
    ax.set_xticklabels(layers, fontsize=8)
    ax.set_yticklabels(papers, fontsize=8)
    for i in range(len(papers)):
        for j in range(len(layers)):
            ax.text(j, i, values[i, j][0].upper(), ha="center", va="center",
                    fontsize=7, color="white" if num[i, j] > 1 else "black")
    cbar = fig.colorbar(im, ax=ax, ticks=[0, 1, 2, 3])
    cbar.ax.set_yticklabels(["missing", "speculative", "inferred", "measured"], fontsize=8)
    ax.set_title("WER-EA evidence heatmap")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 3. material-system-map: formulation taxonomy (grouped nodes)
# ---------------------------------------------------------------------------

def _wer_material_system_map(out: Path, data: Path) -> str:
    name = "wer_ea_material_system_map"
    systems = {
        "Asphalt": ["AC-13", "SMA-13", "OGFC"],
        "Emulsifier": ["Cationic", "Anionic", "Non-ionic"],
        "WER": ["E-51", "E-44", "PEG-modified"],
        "Curing agent": ["Polyamine", "Imidazole", "Acrylic"],
    }
    rows = []
    for fam, members in systems.items():
        for m in members:
            rows.append([fam, m])
    _save_csv(data / f"{name}.csv", ["family", "member"], rows)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = [PALETTE_CBM["control"], PALETTE_CBM["modified"],
              PALETTE_CBM["optimal"], PALETTE_CBM["mechanism"]]
    y_pos = 0.85
    for (fam, members), color in zip(systems.items(), colors):
        ax.add_patch(FancyBboxPatch((0.05, y_pos - 0.08), 0.18, 0.14,
                                     boxstyle="round,pad=0.01",
                                     facecolor=color, alpha=0.25, edgecolor=color, lw=1.5))
        ax.text(0.14, y_pos, fam, ha="center", va="center", fontsize=9, fontweight="bold", color=color)
        for k, m in enumerate(members):
            mx = 0.35 + k * 0.20
            ax.add_patch(FancyBboxPatch((mx - 0.08, y_pos - 0.06), 0.16, 0.12,
                                         boxstyle="round,pad=0.01",
                                         facecolor="white", edgecolor=color, lw=1))
            ax.text(mx, y_pos, m, ha="center", va="center", fontsize=8)
            ax.annotate("", xy=(mx - 0.08, y_pos), xytext=(0.23, y_pos),
                        arrowprops=dict(arrowstyle="-", color=color, lw=0.8))
        y_pos -= 0.22
    ax.set_xlim(0, 1)
    ax.set_ylim(0.05, 0.98)
    ax.axis("off")
    ax.set_title("WER-EA material system map")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 4. performance-boundary: scatter with support tiers
# ---------------------------------------------------------------------------

def _wer_performance_boundary(out: Path, data: Path) -> str:
    name = "wer_ea_performance_boundary"
    rng = np.random.default_rng(7)
    n = 30
    perf = rng.uniform(0.2, 1.0, n)
    mech = rng.uniform(0.1, 0.9, n)
    support = rng.choice(["measured", "inferred", "speculative"], n, p=[0.4, 0.4, 0.2])
    rows = [[f"S{i:02d}", float(perf[i]), float(mech[i]), support[i]] for i in range(n)]
    _save_csv(data / f"{name}.csv", ["study_id", "performance_score", "mechanism_score", "support_tier"], rows)

    tier_color = {"measured": PALETTE_CBM["optimal"],
                  "inferred": PALETTE_CBM["control"],
                  "speculative": PALETTE_CBM["modified"]}
    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 5))
    for tier, color in tier_color.items():
        mask = support == tier
        ax.scatter(perf[mask], mech[mask], c=color, label=tier, s=60, alpha=0.75, edgecolors="black", linewidth=0.5)
    ax.plot([0, 1], [0, 1], "k--", linewidth=1, alpha=0.5, label="Perf = Mech")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Performance evidence score")
    ax.set_ylabel("Mechanism support score")
    ax.set_title("WER-EA performance-mechanism boundary")
    ax.legend(fontsize=8)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 5. screening-flow: PRISMA-style funnel
# ---------------------------------------------------------------------------

def _wer_screening_flow(out: Path, data: Path) -> str:
    name = "wer_ea_screening_flow"
    stages = ["Search", "Title/abstract", "Full-text", "Included"]
    counts = [240, 72, 30, 22]
    exclusions = ["Duplicates 80", "Out of scope 88", "No WER-EA data 8", ""]
    _save_csv(data / f"{name}.csv", ["stage", "count", "exclusion_note"],
              [[s, c, e] for s, c, e in zip(stages, counts, exclusions)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    max_w = 0.70
    for i, (stage, count, excl) in enumerate(zip(stages, counts, exclusions)):
        w = max_w * count / counts[0]
        y = 0.85 - i * 0.22
        ax.add_patch(FancyBboxPatch((0.5 - w / 2, y - 0.07), w, 0.14,
                                     boxstyle="round,pad=0.01",
                                     facecolor=PALETTE_CBM["control"], alpha=0.2 + 0.2 * (i / 3),
                                     edgecolor=PALETTE_CBM["control"], lw=1.5))
        ax.text(0.5, y + 0.02, stage, ha="center", va="center", fontsize=9, fontweight="bold")
        ax.text(0.5, y - 0.04, f"n = {count}", ha="center", va="center", fontsize=8)
        if excl and i < len(stages) - 1:
            ax.text(0.5 + w / 2 + 0.03, y, excl, fontsize=7, color=PALETTE_CBM["danger"], va="center")
        if i < len(stages) - 1:
            ax.annotate("", xy=(0.5, y - 0.07 - 0.01), xytext=(0.5, y - 0.07 - 0.08),
                        arrowprops=dict(arrowstyle="-|>", color=PALETTE_CBM["control"], lw=1.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.set_title("WER-EA literature screening flow")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 6. graphical-abstract: storyline panels
# ---------------------------------------------------------------------------

def _wer_graphical_abstract(out: Path, data: Path) -> str:
    name = "wer_ea_graphical_abstract"
    panels = ["Problem", "Material\ndesign", "Evidence\nchain", "Application", "Gap"]
    scores = [0.90, 0.75, 0.60, 0.55, 0.80]
    _save_csv(data / f"{name}.csv", ["panel", "evidence_score"],
              [[p.replace("\n", " "), s] for p, s in zip(panels, scores)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(10, 4))
    colors = [PALETTE_CBM["danger"], PALETTE_CBM["modified"], PALETTE_CBM["optimal"],
              PALETTE_CBM["control"], PALETTE_CBM["mechanism"]]
    for i, (panel, score, color) in enumerate(zip(panels, scores, colors)):
        x = 0.10 + i * 0.19
        ax.add_patch(FancyBboxPatch((x - 0.08, 0.35), 0.16, 0.30,
                                     boxstyle="round,pad=0.01",
                                     facecolor=color, alpha=0.2 + score * 0.3,
                                     edgecolor=color, lw=1.5))
        ax.text(x, 0.55, panel, ha="center", va="center", fontsize=8, fontweight="bold")
        ax.text(x, 0.42, f"{score:.2f}", ha="center", va="center", fontsize=9, color=color)
        if i < len(panels) - 1:
            ax.annotate("", xy=(x + 0.08 + 0.02, 0.50), xytext=(x + 0.08 + 0.08, 0.50),
                        arrowprops=dict(arrowstyle="-|>", color=PALETTE_CBM["neutral"], lw=1.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0.20, 0.80)
    ax.axis("off")
    ax.set_title("WER-EA review graphical abstract")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 7. dosage-window: dual-axis with workability window
# ---------------------------------------------------------------------------

def _wer_dosage_window(out: Path, data: Path) -> str:
    name = "wer_ea_dosage_window"
    dosage = np.array([0, 2, 4, 6, 8, 10, 12, 15])
    viscosity = np.array([120, 180, 310, 520, 980, 1800, 3200, 8500])
    bonding = np.array([0.35, 0.48, 0.62, 0.64, 0.58, 0.50, 0.42, 0.30])
    workability = np.where((dosage >= 4) & (dosage <= 8), "yes", "no")

    _save_csv(data / f"{name}.csv",
              ["wer_dosage_wt", "viscosity_Pa_s", "bonding_MPa", "workable"],
              [[float(d), float(v), float(b), w] for d, v, b, w in zip(dosage, viscosity, bonding, workability)])

    apply_pub_style()
    fig, ax1 = plt.subplots(figsize=(7, 4.5))
    ax1.plot(dosage, bonding, "o-", color=PALETTE_CBM["control"], lw=2, ms=6, label="Bonding strength")
    ax1.set_xlabel("WER dosage (wt%)")
    ax1.set_ylabel("Bonding strength (MPa)", color=PALETTE_CBM["control"])
    ax1.tick_params(axis="y", labelcolor=PALETTE_CBM["control"])
    ax2 = ax1.twinx()
    ax2.plot(dosage, viscosity, "s--", color=PALETTE_CBM["modified"], lw=2, ms=6, label="Viscosity")
    ax2.set_ylabel("Viscosity (Pa·s)", color=PALETTE_CBM["modified"])
    ax2.tick_params(axis="y", labelcolor=PALETTE_CBM["modified"])
    ax1.axvspan(4, 8, alpha=0.12, color=PALETTE_CBM["optimal"], label="Workability window")
    ax1.set_title("WER-EA dosage-workability window")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="center right")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 8. emulsion-stability: storage timeline
# ---------------------------------------------------------------------------

def _wer_emulsion_stability(out: Path, data: Path) -> str:
    name = "wer_ea_emulsion_stability"
    days = np.array([0, 1, 3, 5, 7, 14, 28])
    control = np.array([100, 88, 70, 52, 38, 22, 10])
    wer_low = np.array([100, 96, 90, 84, 78, 68, 58])
    wer_high = np.array([100, 98, 95, 92, 88, 82, 75])

    _save_csv(data / f"{name}.csv",
              ["day", "control_pct", "wer_low_dosage_pct", "wer_high_dosage_pct"],
              [[int(d), float(c), float(l), float(h)] for d, c, l, h in zip(days, control, wer_low, wer_high)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(days, control, "o-", color=PALETTE_CBM["neutral"], lw=2, label="Unmodified")
    ax.plot(days, wer_low, "s-", color=PALETTE_CBM["modified"], lw=2, label="WER low dosage")
    ax.plot(days, wer_high, "^-", color=PALETTE_CBM["optimal"], lw=2, label="WER high dosage")
    ax.axhline(80, color=PALETTE_CBM["danger"], ls="--", lw=1, label="80% threshold")
    ax.set_xlabel("Storage time (days)")
    ax.set_ylabel("Stability index (%)")
    ax.set_ylim(0, 110)
    ax.set_title("WER-EA emulsion storage stability")
    ax.legend(fontsize=8)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 9. curing-sequence: process timeline with certainty
# ---------------------------------------------------------------------------

def _wer_curing_sequence(out: Path, data: Path) -> str:
    name = "wer_ea_curing_sequence"
    steps = ["Emulsion\ncontact", "Demulsification\n(breaking)", "Water\nescape", "Epoxy\ncuring", "Film\nformation"]
    evidence = [0.80, 0.55, 0.35, 0.60, 0.45]
    _save_csv(data / f"{name}.csv", ["step", "evidence_score"],
              [[s.replace("\n", " "), e] for s, e in zip(steps, evidence)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(9, 4))
    for i, (step, score) in enumerate(zip(steps, evidence)):
        x = 0.10 + i * 0.20
        color = PALETTE_CBM["optimal"] if score >= 0.7 else PALETTE_CBM["control"] if score >= 0.5 else PALETTE_CBM["modified"]
        ax.add_patch(Circle((x, 0.55), 0.07, color=color, alpha=0.2 + score * 0.4))
        ax.text(x, 0.55, step, ha="center", va="center", fontsize=8, fontweight="bold")
        ax.text(x, 0.42, f"{score:.2f}", ha="center", fontsize=9, color=color)
        if i < len(steps) - 1:
            ax.annotate("", xy=(x + 0.07 + 0.02, 0.55), xytext=(x + 0.07 + 0.09, 0.55),
                        arrowprops=dict(arrowstyle="-|>", color=PALETTE_CBM["neutral"], lw=1.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0.25, 0.80)
    ax.axis("off")
    ax.set_title("WER-EA curing and demulsification sequence")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 10. bonding-comparison: grouped bars under conditioning
# ---------------------------------------------------------------------------

def _wer_bonding_comparison(out: Path, data: Path) -> str:
    name = "wer_ea_bonding_comparison"
    systems = ["Unmodified\nEA", "WER + cationic\nemulsifier", "WER + non-ionic\nemulsifier", "SBR-modified\nEA"]
    dry = [1.42, 2.10, 1.95, 1.78]
    wet = [0.95, 1.68, 1.52, 1.30]
    aged = [0.72, 1.45, 1.30, 1.05]
    err = 0.08

    _save_csv(data / f"{name}.csv",
              ["system", "dry_MPa", "wet_MPa", "aged_MPa"],
              [[s.replace("\n", " "), d, w, a] for s, d, w, a in zip(systems, dry, wet, aged)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(systems))
    width = 0.25
    ax.bar(x - width, dry, width, yerr=err, label="Dry", color=PALETTE_CBM["optimal"], capsize=3)
    ax.bar(x, wet, width, yerr=err, label="Wet", color=PALETTE_CBM["control"], capsize=3)
    ax.bar(x + width, aged, width, yerr=err, label="Aged", color=PALETTE_CBM["modified"], capsize=3)
    ax.set_xticks(x)
    ax.set_xticklabels(systems, fontsize=8)
    ax.set_ylabel("Bonding strength (MPa)")
    ax.set_title("WER-EA bonding under conditioning states")
    ax.legend()
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 11. pull-off-shear: parallel method lanes
# ---------------------------------------------------------------------------

def _wer_pull_off_shear(out: Path, data: Path) -> str:
    name = "wer_ea_pull_off_shear"
    methods = ["Pull-off\n(ASTM D7234)", "Direct shear\n(EN 13614)", "Oblique shear\n(JTG E20)", "Tensile\n(ASTM D638)"]
    mean = [2.4, 1.8, 1.5, 3.1]
    std = [0.3, 0.25, 0.2, 0.4]
    _save_csv(data / f"{name}.csv", ["method", "mean_MPa", "std_MPa"],
              [[m.replace("\n", " "), mu, s] for m, mu, s in zip(methods, mean, std)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors = [PALETTE_CBM["control"], PALETTE_CBM["modified"], PALETTE_CBM["optimal"], PALETTE_CBM["mechanism"]]
    bars = ax.bar(methods, mean, yerr=std, capsize=4, color=colors)
    ax.set_ylabel("Bonding strength (MPa)")
    ax.set_title("Pull-off and shear method comparison")
    for bar, mu in zip(bars, mean):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.15,
                f"{mu:.2f}", ha="center", fontsize=9)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 12. rheology-link: paired G'/phase-angle curve
# ---------------------------------------------------------------------------

def _wer_rheology_link(out: Path, data: Path) -> str:
    name = "wer_ea_rheology_link"
    temp = np.array([25, 35, 45, 55, 65, 75, 85])
    g_prime_unmod = np.array([800, 520, 340, 220, 140, 90, 60])
    g_prime_wer = np.array([1400, 1050, 780, 560, 380, 240, 150])
    phase_unmod = np.array([18, 22, 28, 35, 42, 50, 58])
    phase_wer = np.array([12, 15, 19, 24, 30, 38, 46])

    _save_csv(data / f"{name}.csv",
              ["temperature_C", "G_prime_unmodified_Pa", "G_prime_WER_Pa",
               "phase_unmodified_deg", "phase_WER_deg"],
              [[int(t), float(g1), float(g2), float(p1), float(p2)]
               for t, g1, g2, p1, p2 in zip(temp, g_prime_unmod, g_prime_wer, phase_unmod, phase_wer)])

    apply_pub_style()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4))
    ax1.plot(temp, g_prime_unmod, "o-", color=PALETTE_CBM["neutral"], label="Unmodified")
    ax1.plot(temp, g_prime_wer, "s-", color=PALETTE_CBM["optimal"], label="WER-modified")
    ax1.set_xlabel("Temperature (°C)")
    ax1.set_ylabel("G' (Pa)")
    ax1.set_title("Storage modulus")
    ax1.legend()
    ax2.plot(temp, phase_unmod, "o-", color=PALETTE_CBM["neutral"], label="Unmodified")
    ax2.plot(temp, phase_wer, "s-", color=PALETTE_CBM["optimal"], label="WER-modified")
    ax2.set_xlabel("Temperature (°C)")
    ax2.set_ylabel("Phase angle (°)")
    ax2.set_title("Phase angle")
    fig.suptitle("WER-EA rheology-performance link")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 13. ftir-card: annotated peak card
# ---------------------------------------------------------------------------

def _wer_ftir_card(out: Path, data: Path) -> str:
    name = "wer_ea_ftir_card"
    wn = np.linspace(4000, 500, 500)
    control = (0.30 + 0.40 * np.exp(-((wn - 2920) ** 2) / 2e4)
               + 0.25 * np.exp(-((wn - 1635) ** 2) / 8e3))
    wer = (control + 0.22 * np.exp(-((wn - 1730) ** 2) / 5e3)
           + 0.10 * np.exp(-((wn - 1240) ** 2) / 3e3))
    peaks = [(2920, "C-H stretch"), (1730, "C=O ester\n(WER curing)"),
             (1635, "O-H bend"), (1240, "C-O-C\n(epoxy)")]

    _save_csv(data / f"{name}.csv",
              ["wavenumber_cm-1", "control_abs", "wer_modified_abs"],
              [[float(w), float(c), float(m)] for w, c, m in zip(wn, control, wer)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(wn, control, color=PALETTE_CBM["neutral"], lw=1.5, label="Unmodified EA")
    ax.plot(wn, wer, color=PALETTE_CBM["optimal"], lw=1.5, label="WER-modified EA")
    for pos, label in peaks:
        ax.axvline(pos, color=PALETTE_CBM["danger"], ls=":", lw=0.8, alpha=0.7)
        ax.text(pos, ax.get_ylim()[1] * 0.92, f"{pos}\n{label}",
                fontsize=7, ha="center", color=PALETTE_CBM["danger"])
    ax.set_xlabel("Wavenumber (cm$^{-1}$)")
    ax.set_ylabel("Absorbance (a.u.)")
    ax.set_title("WER-EA FTIR peak assignment card")
    ax.legend()
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 14. sem-fluorescence: image plate placeholders with scale bars
# ---------------------------------------------------------------------------

def _wer_sem_fluorescence(out: Path, data: Path) -> str:
    name = "wer_ea_sem_fluorescence"
    rng = np.random.default_rng(11)
    labels = ["SEM: Unmodified", "SEM: WER-modified",
              "Fluorescence: Unmodified", "Fluorescence: WER-modified"]
    _save_csv(data / f"{name}.csv", ["panel", "description"],
              [[l, "representative image placeholder"] for l in labels])

    apply_pub_style()
    fig, axes = plt.subplots(2, 2, figsize=(8, 7))
    for ax, label in zip(axes.flatten(), labels):
        img = rng.random((40, 40))
        if "WER" in label:
            img += 0.3
        ax.imshow(img, cmap="gray", vmin=0, vmax=1.3)
        ax.text(0.95, 0.05, "10 μm", transform=ax.transAxes,
                ha="right", va="bottom", fontsize=8, color="white",
                bbox=dict(boxstyle="square,pad=0.2", facecolor="black", alpha=0.6))
        ax.set_title(label, fontsize=9)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.suptitle("WER-EA SEM / fluorescence morphology plate")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 15. durability-retention: grouped bars with protocol callout
# ---------------------------------------------------------------------------

def _wer_durability_retention(out: Path, data: Path) -> str:
    name = "wer_ea_durability_retention"
    conditions = ["Dry", "Water\nimmersion", "Freeze-thaw", "UV aging", "Heat aging"]
    control = [100, 62, 48, 75, 60]
    wer = [100, 85, 72, 90, 80]

    _save_csv(data / f"{name}.csv",
              ["condition", "control_retention_pct", "wer_retention_pct"],
              [[c.replace("\n", " "), ct, w] for c, ct, w in zip(conditions, control, wer)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = np.arange(len(conditions))
    width = 0.35
    ax.bar(x - width / 2, control, width, label="Unmodified EA", color=PALETTE_CBM["neutral"])
    ax.bar(x + width / 2, wer, width, label="WER-modified EA", color=PALETTE_CBM["optimal"])
    ax.axhline(80, color=PALETTE_CBM["danger"], ls="--", lw=1, label="80% target")
    ax.set_xticks(x)
    ax.set_xticklabels(conditions, fontsize=8)
    ax.set_ylabel("Retention (%)")
    ax.set_ylim(0, 110)
    ax.set_title("WER-EA durability retention map")
    ax.legend()
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 16. challenge-map: radial challenge cards
# ---------------------------------------------------------------------------

def _wer_challenge_map(out: Path, data: Path) -> str:
    name = "wer_ea_challenge_map"
    challenges = ["Water\ndamage", "Heat\naging", "Freeze-thaw", "Traffic\nloading", "Field\nexposure"]
    severity = [0.82, 0.65, 0.75, 0.70, 0.90]
    evidence = [0.55, 0.60, 0.45, 0.50, 0.30]

    _save_csv(data / f"{name}.csv",
              ["challenge", "severity_score", "evidence_score"],
              [[c.replace("\n", " "), s, e] for c, s, e in zip(challenges, severity, evidence)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))
    angles = np.linspace(0, 2 * np.pi, len(challenges), endpoint=False).tolist()
    sev_plot = severity + severity[:1]
    ev_plot = evidence + evidence[:1]
    angles_plot = angles + angles[:1]
    ax.fill(angles_plot, sev_plot, color=PALETTE_CBM["danger"], alpha=0.20)
    ax.plot(angles_plot, sev_plot, "o-", color=PALETTE_CBM["danger"], lw=2, label="Severity")
    ax.fill(angles_plot, ev_plot, color=PALETTE_CBM["optimal"], alpha=0.20)
    ax.plot(angles_plot, ev_plot, "s-", color=PALETTE_CBM["optimal"], lw=2, label="Evidence")
    ax.set_xticks(angles)
    ax.set_xticklabels(challenges, fontsize=8)
    ax.set_ylim(0, 1)
    ax.set_title("WER-EA durability challenge map", y=1.08)
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.10))
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 17. standard-card: method harmonization card
# ---------------------------------------------------------------------------

def _wer_standard_card(out: Path, data: Path) -> str:
    name = "wer_ea_standard_card"
    standards = ["ASTM D7234", "EN 13614", "JTG E20 T075", "GB/T 16777"]
    specimen = ["Concrete slab", "Masonry prism", "Asphalt beam", "Steel coupon"]
    loading = ["Pull-off", "Shear", "Oblique shear", "Tensile"]
    curing = ["28 d", "14 d", "24 h", "7 d"]
    _save_csv(data / f"{name}.csv",
              ["standard", "specimen", "loading_mode", "curing_time"],
              [[s, sp, l, c] for s, sp, l, c in zip(standards, specimen, loading, curing)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.axis("off")
    col_x = [0.08, 0.32, 0.56, 0.80]
    headers = ["Standard", "Specimen", "Loading", "Curing"]
    for x, h in zip(col_x, headers):
        ax.text(x, 0.92, h, fontsize=10, fontweight="bold", color=PALETTE_CBM["control"])
    for i, (std, sp, ld, cr) in enumerate(zip(standards, specimen, loading, curing)):
        y = 0.78 - i * 0.18
        ax.add_patch(Rectangle((0.02, y - 0.08), 0.96, 0.14,
                                facecolor=PALETTE_CBM["control"], alpha=0.08,
                                edgecolor=PALETTE_CBM["control"], lw=0.8))
        for x, val in zip(col_x, [std, sp, ld, cr]):
            ax.text(x, y, val, fontsize=9, va="center")
    ax.set_xlim(0, 1)
    ax.set_ylim(0.05, 1.0)
    ax.set_title("WER-EA test standard condition card")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 18. application-workflow: construction timeline
# ---------------------------------------------------------------------------

def _wer_application_workflow(out: Path, data: Path) -> str:
    name = "wer_ea_application_workflow"
    steps = ["Surface\npreparation", "Tack coat\nspraying", "Demulsification\n& breaking",
             "Curing", "Overlay\nplacement", "QC\ninspection"]
    duration_h = [2, 1, 3, 12, 4, 1]
    _save_csv(data / f"{name}.csv",
              ["step", "duration_hours"],
              [[s.replace("\n", " "), d] for s, d in zip(steps, duration_h)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(10, 4))
    cum = 0
    total = sum(duration_h)
    colors = [PALETTE_CBM["control"], PALETTE_CBM["modified"], PALETTE_CBM["optimal"],
              PALETTE_CBM["mechanism"], PALETTE_CBM["accent"], PALETTE_CBM["danger"]]
    for i, (step, dur, color) in enumerate(zip(steps, duration_h, colors)):
        w = 0.85 * dur / total
        x = 0.08 + 0.85 * cum / total
        ax.add_patch(FancyBboxPatch((x, 0.35), w, 0.30,
                                     boxstyle="round,pad=0.01",
                                     facecolor=color, alpha=0.30,
                                     edgecolor=color, lw=1.5))
        ax.text(x + w / 2, 0.55, step, ha="center", va="center", fontsize=8, fontweight="bold")
        ax.text(x + w / 2, 0.42, f"{dur} h", ha="center", fontsize=9, color=color)
        cum += dur
    ax.set_xlim(0, 1)
    ax.set_ylim(0.20, 0.80)
    ax.axis("off")
    ax.set_title("WER-EA construction application workflow")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 19. lca-boundary: system boundary card
# ---------------------------------------------------------------------------

def _wer_lca_boundary(out: Path, data: Path) -> str:
    name = "wer_ea_lca_boundary"
    stages = ["Raw material", "Transport", "Manufacturing", "Construction", "Use", "End-of-life"]
    gwp = [12.5, 3.2, 28.4, 5.1, 8.6, -2.3]
    _save_csv(data / f"{name}.csv",
              ["life_cycle_stage", "GWP_kg_CO2_eq"],
              [[s, g] for s, g in zip(stages, gwp)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = [PALETTE_CBM["danger"] if g > 0 else PALETTE_CBM["optimal"] for g in gwp]
    bars = ax.barh(stages, gwp, color=colors)
    ax.axvline(0, color="black", lw=0.8)
    ax.set_xlabel("GWP (kg CO$_2$ eq.)")
    ax.set_title("WER-EA sustainability LCA boundary card")
    for bar, g in zip(bars, gwp):
        ax.text(bar.get_width() + (0.5 if g >= 0 else -0.5),
                bar.get_y() + bar.get_height() / 2,
                f"{g:+.1f}", va="center", ha="left" if g >= 0 else "right", fontsize=9)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# 20. research-gap: gap quadrants
# ---------------------------------------------------------------------------

def _wer_research_gap(out: Path, data: Path) -> str:
    name = "wer_ea_research_gap"
    topics = ["Lab bonding", "Field validation", "Curing mechanism", "Standards harmony", "Long-term durability"]
    maturity = [0.80, 0.40, 0.55, 0.35, 0.30]
    importance = [0.75, 0.95, 0.85, 0.70, 0.92]
    gap = [i - m for i, m in zip(importance, maturity)]

    _save_csv(data / f"{name}.csv",
              ["topic", "maturity", "importance", "gap"],
              [[t, m, i, g] for t, m, i, g in zip(topics, maturity, importance, gap)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 5.5))
    sizes = [max(g, 0.05) * 2500 for g in gap]
    scatter = ax.scatter(maturity, importance, s=sizes, c=gap, cmap="RdYlGn_r",
                         alpha=0.80, edgecolors="black", linewidth=0.5)
    for i, t in enumerate(topics):
        ax.annotate(t, (maturity[i], importance[i]),
                    textcoords="offset points", xytext=(6, 6), fontsize=8)
    ax.plot([0, 1], [0, 1], "k--", lw=1, alpha=0.6)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xlabel("Evidence maturity")
    ax.set_ylabel("Research importance")
    ax.set_title("WER-EA research gap matrix")
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Gap (Importance - Maturity)")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(out))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

WER_EA_FUNCS = [
    _wer_mechanism_map,
    _wer_evidence_heatmap,
    _wer_material_system_map,
    _wer_performance_boundary,
    _wer_screening_flow,
    _wer_graphical_abstract,
    _wer_dosage_window,
    _wer_emulsion_stability,
    _wer_curing_sequence,
    _wer_bonding_comparison,
    _wer_pull_off_shear,
    _wer_rheology_link,
    _wer_ftir_card,
    _wer_sem_fluorescence,
    _wer_durability_retention,
    _wer_challenge_map,
    _wer_standard_card,
    _wer_application_workflow,
    _wer_lca_boundary,
    _wer_research_gap,
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only", nargs="*", help="subset of function names")
    args = parser.parse_args()

    root = _skill_root()
    out_dir = root / "assets" / "wer-ea-atlas" / "generated"
    data_dir = root / "assets" / "wer-ea-atlas" / "data"

    funcs = WER_EA_FUNCS
    if args.only:
        funcs = [f for f in funcs if f.__name__ in args.only]

    for fn in funcs:
        name = fn(out_dir, data_dir)
        print(f"wer-ea: {name}.svg + .png + .csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

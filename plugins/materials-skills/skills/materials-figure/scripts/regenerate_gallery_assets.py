#!/usr/bin/env python3
"""Regenerate rich-gallery and review-first assets with real data-driven figures.

Outputs SVG + PNG + CSV for each concept. Run from the skill root or any path.
"""

from __future__ import annotations

# Directory mapping: review figures live under assets/review-first/ to match
# README and manifest references; rich figures live under assets/rich-gallery/.
_DIR_MAP = {"rich": "rich-gallery", "review": "review-first"}

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


def _rich_bonding_performance_matrix(output_dir: Path, data_dir: Path) -> str:
    name = "bonding_performance_matrix"
    formulations = ["Control", "1 wt%", "3 wt%", "5 wt%"]
    dry = [1.85, 2.05, 2.42, 2.30]
    wet = [1.42, 1.68, 2.10, 1.95]
    aged = [1.20, 1.45, 1.88, 1.72]
    err_dry = [0.08, 0.09, 0.10, 0.11]
    err_wet = [0.10, 0.11, 0.12, 0.13]
    err_aged = [0.12, 0.13, 0.14, 0.13]

    _save_csv(
        data_dir / f"{name}.csv",
        ["formulation", "dry_MPa", "wet_MPa", "aged_MPa", "dry_err", "wet_err", "aged_err"],
        [list(r) for r in zip(formulations, dry, wet, aged, err_dry, err_wet, err_aged)],
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    x = np.arange(len(formulations))
    width = 0.25
    ax.bar(x - width, dry, width, yerr=err_dry, label="Dry", color=PALETTE_CBM["control"], capsize=3)
    ax.bar(x, wet, width, yerr=err_wet, label="Wet", color=PALETTE_CBM["modified"], capsize=3)
    ax.bar(x + width, aged, width, yerr=err_aged, label="Aged", color=PALETTE_CBM["mechanism"], capsize=3)
    ax.set_ylabel("Bonding strength (MPa)")
    ax.set_xticks(x)
    ax.set_xticklabels(formulations)
    ax.set_title("Bonding performance matrix")
    ax.legend()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _rich_dosage_workability_window(output_dir: Path, data_dir: Path) -> str:
    name = "dosage_workability_window"
    dosage = np.array([0, 1, 2, 3, 4, 5, 6])
    strength = np.array([1.80, 2.10, 2.45, 2.62, 2.55, 2.30, 1.95])
    viscosity = np.array([2.5, 3.2, 4.8, 7.5, 12.0, 18.5, 26.0])

    _save_csv(
        data_dir / f"{name}.csv",
        ["dosage_wt", "strength_MPa", "viscosity_Pa_s"],
        [[float(d), float(s), float(v)] for d, s, v in zip(dosage, strength, viscosity)],
    )

    apply_pub_style()
    fig, ax1 = plt.subplots(figsize=(7, 4.5))
    color1 = PALETTE_CBM["control"]
    ax1.plot(dosage, strength, "o-", color=color1, linewidth=2, markersize=6, label="Bonding strength")
    ax1.set_xlabel("Modifier dosage (wt%)")
    ax1.set_ylabel("Bonding strength (MPa)", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)
    ax2 = ax1.twinx()
    color2 = PALETTE_CBM["modified"]
    ax2.plot(dosage, viscosity, "s--", color=color2, linewidth=2, markersize=6, label="Viscosity")
    ax2.set_ylabel("Viscosity (Pa·s)", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)
    ax1.axvspan(2.5, 4.0, alpha=0.12, color=PALETTE_CBM["optimal"], label="Workability window")
    ax1.set_title("Dosage-workability window")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _rich_interface_mechanism_map(output_dir: Path, data_dir: Path) -> str:
    name = "interface_mechanism_map"
    nodes = [
        (0.12, 0.65, "Demulsification"),
        (0.32, 0.75, "Curing"),
        (0.52, 0.55, "Morphology"),
        (0.72, 0.70, "Interface\nreaction"),
        (0.88, 0.50, "Bonding"),
    ]
    evidence = [0.45, 0.62, 0.78, 0.55, 0.80]

    _save_csv(
        data_dir / f"{name}.csv",
        ["stage", "evidence_score"],
        [[n[2].replace("\n", " "), float(e)] for n, e in zip(nodes, evidence)],
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for i, (x, y, label) in enumerate(nodes):
        ax.add_patch(Circle((x, y), 0.06, color=PALETTE_CBM["control"], alpha=0.2 + evidence[i] * 0.4))
        ax.text(x, y, label, ha="center", va="center", fontsize=8, fontweight="bold")
        if i < len(nodes) - 1:
            ax.annotate(
                "",
                xy=(nodes[i + 1][0] - 0.06, nodes[i + 1][1]),
                xytext=(x + 0.06, y),
                arrowprops=dict(arrowstyle="->", color=PALETTE_CBM["mechanism"], lw=2),
            )
    ax.set_xlim(0, 1)
    ax.set_ylim(0.35, 0.90)
    ax.axis("off")
    ax.set_title("Interface mechanism map")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _rich_ftir_sem_evidence_pair(output_dir: Path, data_dir: Path) -> str:
    name = "ftir_sem_evidence_pair"
    wavenumber = np.linspace(4000, 500, 500)
    control = 0.3 + 0.4 * np.exp(-((wavenumber - 2920) ** 2) / 2e4) + 0.25 * np.exp(-((wavenumber - 1635) ** 2) / 8e3)
    modified = control + 0.2 * np.exp(-((wavenumber - 1730) ** 2) / 5e3)

    size_bins = np.arange(0.5, 10.5, 1)
    control_size = [2, 8, 15, 22, 28, 18, 10, 5, 2, 1]
    modified_size = [1, 4, 10, 18, 30, 25, 12, 6, 3, 1]

    _save_csv(data_dir / f"{name}_ftir.csv", ["wavenumber_cm-1", "control_abs", "modified_abs"], [[float(w), float(c), float(m)] for w, c, m in zip(wavenumber, control, modified)])
    _save_csv(data_dir / f"{name}_sem.csv", ["size_um", "control_count", "modified_count"], [[float(b), int(c), int(m)] for b, c, m in zip(size_bins, control_size, modified_size)])

    apply_pub_style()
    fig, axes = plt.subplots(1, 2, figsize=(8, 3.8))
    axes[0].plot(wavenumber, control, label="Control", color=PALETTE_CBM["control"])
    axes[0].plot(wavenumber, modified, label="Modified", color=PALETTE_CBM["modified"])
    axes[0].set_xlabel("Wavenumber (cm$^{-1}$)")
    axes[0].set_ylabel("Absorbance (a.u.)")
    axes[0].set_title("FTIR spectra")
    axes[0].legend()
    axes[1].bar(size_bins - 0.2, control_size, 0.4, label="Control", color=PALETTE_CBM["control"])
    axes[1].bar(size_bins + 0.2, modified_size, 0.4, label="Modified", color=PALETTE_CBM["modified"])
    axes[1].set_xlabel(r"Particle size ($\mu$m)")
    axes[1].set_ylabel("Frequency")
    axes[1].set_title("SEM particle size")
    axes[1].legend()
    fig.suptitle("FTIR + SEM evidence pair")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _rich_moisture_aging_retention(output_dir: Path, data_dir: Path) -> str:
    name = "moisture_aging_retention"
    conditions = ["Dry", "Water\nimmersion", "Freeze-thaw", "UV", "Heat aging"]
    control = [100, 72, 58, 80, 65]
    modified = [100, 88, 79, 91, 84]

    _save_csv(data_dir / f"{name}.csv", ["condition", "control_retention_pct", "modified_retention_pct"], [[c, float(ct), float(m)] for c, ct, m in zip(conditions, control, modified)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    x = np.arange(len(conditions))
    width = 0.35
    ax.bar(x - width / 2, control, width, label="Control", color=PALETTE_CBM["control"])
    ax.bar(x + width / 2, modified, width, label="Modified", color=PALETTE_CBM["modified"])
    ax.set_ylabel("Retention (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(conditions)
    ax.set_ylim(0, 110)
    ax.axhline(80, color=PALETTE_CBM["accent"], linestyle="--", linewidth=1, label="Target")
    ax.set_title("Moisture-aging retention")
    ax.legend()
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _rich_storage_stability_timeline(output_dir: Path, data_dir: Path) -> str:
    name = "storage_stability_timeline"
    days = np.array([0, 1, 3, 5, 7, 14])
    control = np.array([98, 92, 82, 68, 52, 30])
    modified = np.array([98, 96, 91, 86, 80, 72])

    _save_csv(data_dir / f"{name}.csv", ["day", "control_stability_pct", "modified_stability_pct"], [[int(d), float(c), float(m)] for d, c, m in zip(days, control, modified)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(days, control, "o-", label="Control", color=PALETTE_CBM["control"])
    ax.plot(days, modified, "s-", label="Modified", color=PALETTE_CBM["modified"])
    ax.set_xlabel("Storage time (days)")
    ax.set_ylabel("Stability index (%)")
    ax.set_ylim(0, 105)
    ax.axhline(80, color=PALETTE_CBM["accent"], linestyle="--", linewidth=1)
    ax.set_title("Storage stability timeline")
    ax.legend()
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _rich_pavement_layer_tackcoat(output_dir: Path, data_dir: Path) -> str:
    name = "pavement_layer_tackcoat"
    rates = [0.2, 0.4, 0.6, 0.8, 1.0]
    shear = [0.55, 0.92, 1.35, 1.48, 1.42]

    _save_csv(data_dir / f"{name}.csv", ["application_rate_L_m2", "shear_strength_MPa"], [[float(r), float(s)] for r, s in zip(rates, shear)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(rates, shear, "o-", color=PALETTE_CBM["optimal"], linewidth=2, markersize=7)
    ax.fill_between(rates, shear, alpha=0.15, color=PALETTE_CBM["optimal"])
    ax.set_xlabel("Tack coat application rate (L/m$^2$)")
    ax.set_ylabel("Shear strength (MPa)")
    ax.set_title("Pavement layer tack coat")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _rich_cement_hydration_evidence(output_dir: Path, data_dir: Path) -> str:
    name = "cement_hydration_evidence"
    time = np.array([0, 2, 4, 8, 12, 24, 48, 72])
    heat = np.array([0, 1.2, 3.5, 5.8, 6.5, 7.1, 7.8, 8.0])
    ch = np.array([0, 5, 12, 22, 30, 38, 44, 48])

    _save_csv(data_dir / f"{name}.csv", ["time_h", "heat_J_g", "CH_content_pct"], [[int(t), float(h), float(c)] for t, h, c in zip(time, heat, ch)])

    apply_pub_style()
    fig, ax1 = plt.subplots(figsize=(7, 4.5))
    ax1.plot(time, heat, "o-", color=PALETTE_CBM["control"], label="Heat release")
    ax1.set_xlabel("Hydration time (h)")
    ax1.set_ylabel("Heat release (J/g)", color=PALETTE_CBM["control"])
    ax1.tick_params(axis="y", labelcolor=PALETTE_CBM["control"])
    ax2 = ax1.twinx()
    ax2.plot(time, ch, "s--", color=PALETTE_CBM["modified"], label="Ca(OH)$_2$ content")
    ax2.set_ylabel("Ca(OH)$_2$ content (%)", color=PALETTE_CBM["modified"])
    ax2.tick_params(axis="y", labelcolor=PALETTE_CBM["modified"])
    ax1.set_title("Cement hydration evidence")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _rich_lca_boundary_card(output_dir: Path, data_dir: Path) -> str:
    name = "lca_boundary_card"
    stages = ["Raw material", "Transport", "Manufacturing", "Construction", "Use", "End-of-life"]
    gwp = [12.5, 3.2, 28.4, 5.1, 8.6, -2.3]

    _save_csv(data_dir / f"{name}.csv", ["life_cycle_stage", "GWP_kg_CO2_eq"], [[s, float(g)] for s, g in zip(stages, gwp)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors = [PALETTE_CBM["danger"] if g > 0 else PALETTE_CBM["optimal"] for g in gwp]
    ax.barh(stages, gwp, color=colors)
    ax.set_xlabel("GWP (kg CO$_2$ eq.)")
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_title("LCA system boundary card")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _rich_review_taxonomy_map(output_dir: Path, data_dir: Path) -> str:
    name = "review_taxonomy_map"
    categories = ["Materials", "Tests", "Mechanisms", "Performance", "Gaps"]
    counts = [42, 28, 19, 35, 14]

    _save_csv(data_dir / f"{name}.csv", ["category", "paper_count"], [[c, int(n)] for c, n in zip(categories, counts)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(categories, counts, color=[PALETTE_CBM["control"], PALETTE_CBM["modified"], PALETTE_CBM["mechanism"], PALETTE_CBM["optimal"], PALETTE_CBM["accent"]])
    ax.set_ylabel("Number of papers")
    ax.set_title("Review taxonomy map")
    for bar, n in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8, str(n), ha="center", fontsize=9)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


# ---------------------------------------------------------------------------
# review-first: data-driven review figures
# ---------------------------------------------------------------------------


def _review_review_framework_map(output_dir: Path, data_dir: Path) -> str:
    name = "review_framework_map"
    dimensions = ["Material scope", "Mechanism depth", "Performance coverage", "Durability evidence", "Gap clarity"]
    scores = [0.75, 0.60, 0.85, 0.55, 0.70]

    _save_csv(data_dir / f"{name}.csv", ["dimension", "coverage_score"], [[d, float(s)] for d, s in zip(dimensions, scores)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    angles = np.linspace(0, 2 * np.pi, len(dimensions), endpoint=False).tolist()
    scores_plot = scores + scores[:1]
    angles += angles[:1]
    ax.fill(angles, scores_plot, color=PALETTE_CBM["control"], alpha=0.25)
    ax.plot(angles, scores_plot, "o-", color=PALETTE_CBM["control"], linewidth=2)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dimensions, fontsize=8)
    ax.set_ylim(0, 1)
    ax.set_title("Review framework map", y=1.08)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _review_material_mechanism_performance_challenges(output_dir: Path, data_dir: Path) -> str:
    name = "material_mechanism_performance_challenges"
    materials = ["SBR", "CR", "EVA", "PU", "Epoxy"]
    mechanism_score = [0.55, 0.62, 0.48, 0.71, 0.80]
    performance = [72, 78, 65, 85, 90]
    challenge = [0.35, 0.28, 0.42, 0.20, 0.15]

    _save_csv(data_dir / f"{name}.csv", ["material", "mechanism_score", "performance_score", "challenge_score"], [[m, float(ms), float(p), float(c)] for m, ms, p, c in zip(materials, mechanism_score, performance, challenge)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 5))
    scatter = ax.scatter(mechanism_score, performance, s=[c * 2000 for c in challenge], c=challenge, cmap="RdYlGn_r", alpha=0.7, edgecolors="black", linewidth=0.5)
    for i, m in enumerate(materials):
        ax.annotate(m, (mechanism_score[i], performance[i]), textcoords="offset points", xytext=(5, 5), fontsize=9)
    ax.set_xlabel("Mechanism understanding score")
    ax.set_ylabel("Performance score")
    ax.set_title("Material-Mechanism-Performance-Challenge map")
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Challenge score")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _review_evidence_chain_map(output_dir: Path, data_dir: Path) -> str:
    name = "evidence_chain_map"
    stages = ["Claim", "Microstructure", "Chemistry", "Interface", "Durability"]
    support = [0.90, 0.75, 0.60, 0.55, 0.40]

    _save_csv(data_dir / f"{name}.csv", ["stage", "evidence_support_score"], [[s, float(v)] for s, v in zip(stages, support)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors = [PALETTE_CBM["optimal"] if s >= 0.7 else PALETTE_CBM["modified"] if s >= 0.55 else PALETTE_CBM["danger"] for s in support]
    ax.barh(stages, support, color=colors)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Evidence support score")
    ax.axvline(0.7, color=PALETTE_CBM["accent"], linestyle="--", linewidth=1, label="Strong evidence threshold")
    ax.set_title("Evidence chain map")
    ax.legend()
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _review_interface_mechanism_boundary(output_dir: Path, data_dir: Path) -> str:
    name = "interface_mechanism_boundary"
    methods = ["Contact angle", "FTIR ester peak", "SEM roughness", "Rheology G'", "Pull-off test"]
    values = [68, 0.35, 2.8, 1450, 2.4]
    normalized = [0.55, 0.70, 0.60, 0.80, 0.75]

    _save_csv(data_dir / f"{name}.csv", ["method", "raw_value", "normalized_score"], [[m, float(v), float(n)] for m, v, n in zip(methods, values, normalized)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors = [PALETTE_CBM["control"], PALETTE_CBM["modified"], PALETTE_CBM["mechanism"], PALETTE_CBM["optimal"], PALETTE_CBM["accent"]]
    bars = ax.barh(methods, normalized, color=colors)
    ax.set_xlim(0, 1)
    ax.set_xlabel("Normalized evidence score")
    ax.set_title("Interface mechanism boundary")
    for bar, v in zip(bars, values):
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2, f"{v:.2g}", va="center", fontsize=8)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _review_bonding_test_method_map(output_dir: Path, data_dir: Path) -> str:
    name = "bonding_test_method_map"
    methods = ["Pull-off", "Shear", "Tensile", "Flexural", "Fracture"]
    factors = ["Substrate", "Rate", "Curing", "Loading", "Metric"]
    data = np.array([
        [1.0, 0.8, 0.9, 0.7, 0.6],
        [0.7, 1.0, 0.8, 0.9, 0.7],
        [0.8, 0.7, 1.0, 0.6, 0.9],
        [0.6, 0.8, 0.7, 1.0, 0.8],
        [0.5, 0.6, 0.6, 0.7, 1.0],
    ])

    rows = []
    for i, m in enumerate(methods):
        for j, f in enumerate(factors):
            rows.append([m, f, float(data[i, j])])
    _save_csv(data_dir / f"{name}.csv", ["method", "factor", "relevance_score"], rows)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 5))
    im = ax.imshow(data, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(np.arange(len(factors)))
    ax.set_yticks(np.arange(len(methods)))
    ax.set_xticklabels(factors)
    ax.set_yticklabels(methods)
    for i in range(len(methods)):
        for j in range(len(factors)):
            ax.text(j, i, f"{data[i, j]:.1f}", ha="center", va="center", color="white" if data[i, j] > 0.5 else "black", fontsize=9)
    ax.set_title("Bonding test method map")
    fig.colorbar(im, ax=ax, label="Relevance")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _review_dosage_viscosity_bonding_window(output_dir: Path, data_dir: Path) -> str:
    name = "dosage_viscosity_bonding_window"
    dosage = np.linspace(1, 6, 30)
    viscosity = 2.0 + 0.8 * dosage + 0.15 * dosage**2
    bonding = 1.6 + 0.45 * dosage - 0.06 * dosage**2 + 0.002 * dosage**3
    bonding = np.clip(bonding, 0, None)

    _save_csv(data_dir / f"{name}.csv", ["dosage_wt", "viscosity_Pa_s", "bonding_MPa"], [[float(d), float(v), float(b)] for d, v, b in zip(dosage, viscosity, bonding)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(dosage, bonding, "o-", color=PALETTE_CBM["control"], label="Bonding strength")
    ax2 = ax.twinx()
    ax2.plot(dosage, viscosity, "s--", color=PALETTE_CBM["modified"], label="Viscosity")
    ax.set_xlabel("Dosage (wt%)")
    ax.set_ylabel("Bonding strength (MPa)", color=PALETTE_CBM["control"])
    ax2.set_ylabel("Viscosity (Pa·s)", color=PALETTE_CBM["modified"])
    ax.axvspan(2.5, 4.0, alpha=0.15, color=PALETTE_CBM["optimal"], label="Optimal window")
    ax.set_title("Dosage-viscosity-bonding window")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _review_ftir_sem_rheology_evidence_panel(output_dir: Path, data_dir: Path) -> str:
    name = "ftir_sem_rheology_evidence_panel"
    wavenumber = np.linspace(4000, 500, 300)
    ftir = 0.25 + 0.35 * np.exp(-((wavenumber - 2920) ** 2) / 2e4) + 0.2 * np.exp(-((wavenumber - 1735) ** 2) / 5e3)
    temp = np.array([30, 40, 50, 60, 70, 80])
    gprime = np.array([1200, 1800, 2600, 3500, 4800, 6200])
    size = np.array([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5])
    freq = np.array([3, 8, 15, 24, 30, 25, 18, 10, 5, 2])

    _save_csv(data_dir / f"{name}_ftir.csv", ["wavenumber", "absorbance"], [[float(w), float(f)] for w, f in zip(wavenumber, ftir)])
    _save_csv(data_dir / f"{name}_rheology.csv", ["temperature_C", "Gprime_Pa"], [[int(t), float(g)] for t, g in zip(temp, gprime)])
    _save_csv(data_dir / f"{name}_sem.csv", ["size_um", "frequency"], [[float(s), int(f)] for s, f in zip(size, freq)])

    apply_pub_style()
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.5))
    axes[0].plot(wavenumber, ftir, color=PALETTE_CBM["control"])
    axes[0].set_xlabel("Wavenumber (cm$^{-1}$)")
    axes[0].set_ylabel("Absorbance")
    axes[0].set_title("FTIR")
    axes[1].bar(size, freq, color=PALETTE_CBM["modified"], width=0.8)
    axes[1].set_xlabel(r"Size ($\mu$m)")
    axes[1].set_ylabel("Frequency")
    axes[1].set_title("SEM/FM")
    axes[2].plot(temp, gprime, "o-", color=PALETTE_CBM["mechanism"])
    axes[2].set_xlabel("Temperature (°C)")
    axes[2].set_ylabel("G' (Pa)")
    axes[2].set_title("Rheology")
    fig.suptitle("FTIR-SEM-Rheology evidence panel")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _review_durability_retention_challenge_map(output_dir: Path, data_dir: Path) -> str:
    name = "durability_retention_challenge_map"
    challenges = ["Water", "Aging", "Freeze-thaw", "Heat", "Traffic"]
    control = [62, 58, 45, 55, 68]
    modified = [85, 80, 72, 78, 82]

    _save_csv(data_dir / f"{name}.csv", ["challenge", "control_retention_pct", "modified_retention_pct"], [[c, float(ct), float(m)] for c, ct, m in zip(challenges, control, modified)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    x = np.arange(len(challenges))
    width = 0.35
    ax.bar(x - width / 2, control, width, label="Control", color=PALETTE_CBM["control"])
    ax.bar(x + width / 2, modified, width, label="Modified", color=PALETTE_CBM["modified"])
    ax.set_ylabel("Retention (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(challenges)
    ax.set_ylim(0, 100)
    ax.axhline(70, color=PALETTE_CBM["accent"], linestyle="--", linewidth=1, label="Acceptance")
    ax.set_title("Durability retention challenge map")
    ax.legend()
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _review_research_gap_matrix(output_dir: Path, data_dir: Path) -> str:
    name = "research_gap_matrix"
    topics = ["Lab\nevidence", "Field\nevidence", "Mechanism", "Standards", "Long-term"]
    maturity = [0.85, 0.45, 0.60, 0.40, 0.30]
    importance = [0.70, 0.90, 0.85, 0.75, 0.95]
    gap = [i - m for i, m in zip(importance, maturity)]

    _save_csv(data_dir / f"{name}.csv", ["topic", "maturity", "importance", "gap"], [[t, float(m), float(i), float(g)] for t, m, i, g in zip(topics, maturity, importance, gap)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 5))
    scatter = ax.scatter(maturity, importance, s=[g * 2000 for g in gap], c=gap, cmap="RdYlGn_r", alpha=0.8, edgecolors="black", linewidth=0.5)
    for i, t in enumerate(topics):
        ax.annotate(t.replace("\n", " "), (maturity[i], importance[i]), textcoords="offset points", xytext=(5, 5), fontsize=8)
    ax.plot([0, 1], [0, 1], "k--", linewidth=1, label="Maturity = Importance")
    ax.set_xlabel("Evidence maturity")
    ax.set_ylabel("Research importance")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_title("Research gap matrix")
    ax.legend()
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label("Gap (Importance - Maturity)")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


def _review_graphical_abstract_review(output_dir: Path, data_dir: Path) -> str:
    name = "graphical_abstract_review"
    years = np.array([2018, 2019, 2020, 2021, 2022, 2023, 2024])
    papers = np.array([12, 18, 25, 34, 45, 58, 72])
    gaps = np.array([5, 6, 8, 10, 12, 15, 18])

    _save_csv(data_dir / f"{name}.csv", ["year", "papers_published", "identified_gaps"], [[int(y), int(p), int(g)] for y, p, g in zip(years, papers, gaps)])

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.bar(years, papers, color=PALETTE_CBM["control"], alpha=0.8, label="Papers")
    ax.plot(years, gaps, "o-", color=PALETTE_CBM["danger"], linewidth=2, markersize=6, label="Identified gaps")
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    ax.set_title("Graphical abstract for review")
    ax.legend()
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    return name


RICH_FUNCS = [
    _rich_bonding_performance_matrix,
    _rich_dosage_workability_window,
    _rich_interface_mechanism_map,
    _rich_ftir_sem_evidence_pair,
    _rich_moisture_aging_retention,
    _rich_storage_stability_timeline,
    _rich_pavement_layer_tackcoat,
    _rich_cement_hydration_evidence,
    _rich_lca_boundary_card,
    _rich_review_taxonomy_map,
]

REVIEW_FUNCS = [
    _review_review_framework_map,
    _review_material_mechanism_performance_challenges,
    _review_evidence_chain_map,
    _review_interface_mechanism_boundary,
    _review_bonding_test_method_map,
    _review_dosage_viscosity_bonding_window,
    _review_ftir_sem_rheology_evidence_panel,
    _review_durability_retention_challenge_map,
    _review_research_gap_matrix,
    _review_graphical_abstract_review,
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rich-only", action="store_true")
    parser.add_argument("--review-only", action="store_true")
    args = parser.parse_args()

    root = _skill_root()
    generated = root / "assets"

    funcs: list = []
    if not args.review_only:
        funcs.extend(("rich", f) for f in RICH_FUNCS)
    if not args.rich_only:
        funcs.extend(("review", f) for f in REVIEW_FUNCS)

    for kind, fn in funcs:
        dir_name = _DIR_MAP[kind]
        out_dir = generated / dir_name / "generated"
        data_dir = generated / dir_name / "data"
        name = fn(out_dir, data_dir)
        print(f"{kind}: {name}.svg + .png + .csv")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

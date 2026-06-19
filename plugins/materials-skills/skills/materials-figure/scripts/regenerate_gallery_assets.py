#!/usr/bin/env python3
"""Regenerate rich-gallery and review-first assets with literature-anchored data.

Every CSV carries a ``#`` comment header citing the physical/literature basis,
and every review-first figure encodes the four evidence tiers
(measured / inferred / speculative / missing) in a shared legend. Each figure
prints a claim-boundary note to stdout so reviewers can audit what the visual
can and cannot assert.

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
from matplotlib.lines import Line2D

sys.path.insert(0, str(Path(__file__).resolve().parent))
from materials_plot_lib import PALETTE_CBM, apply_pub_style, finalize_figure


# Evidence-certainty tier palette (review-figure-intake.md / wer-ea-review-figure-contract.md).
# measured=green, inferred=blue, speculative=orange, missing=grey.
EVIDENCE_TIER_COLORS = {
    "measured":    PALETTE_CBM["optimal"],   # green
    "inferred":    PALETTE_CBM["control"],   # blue
    "speculative": PALETTE_CBM["modified"],  # orange
    "missing":     PALETTE_CBM["neutral"],   # grey
}
EVIDENCE_TIER_ORDER = ["measured", "inferred", "speculative", "missing"]


def _skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _save_csv(path: Path, headers: list[str], rows: list[list], comment: str | None = None) -> None:
    """Write a CSV with an optional ``#``-prefixed literature-basis comment block."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        if comment:
            for line in comment.strip().splitlines():
                f.write(f"# {line.strip()}\n")
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)


def _add_evidence_tier_legend(ax, *, loc: str = "lower right", fontsize: int = 7) -> None:
    """Attach the shared measured/inferred/speculative/missing legend to an axis."""
    handles = [
        Line2D([0], [0], marker="s", color="none", markerfacecolor=EVIDENCE_TIER_COLORS[t],
               markeredgecolor="#333333", markersize=7, label=t)
        for t in EVIDENCE_TIER_ORDER
    ]
    ax.legend(handles=handles, loc=loc, fontsize=fontsize, frameon=True,
              framealpha=0.9, edgecolor="#CCCCCC", title="evidence tier", title_fontsize=fontsize)


def _tier_color(tier: str) -> str:
    return EVIDENCE_TIER_COLORS.get(tier, EVIDENCE_TIER_COLORS["missing"])


def _print_claim_boundary(name: str, boundary: str) -> None:
    """Echo a one-line claim boundary so reviewers can audit the figure output."""
    boundary_one_line = " ".join(boundary.split())
    print(f"  claim-boundary | {name}: {boundary_one_line}")


# ---------------------------------------------------------------------------
# rich-gallery: literature-anchored material-scene figures (no evidence-tier
# legend by default; these are scene figures, not review evidence figures).
# ---------------------------------------------------------------------------


def _rich_bonding_performance_matrix(output_dir: Path, data_dir: Path) -> str:
    name = "bonding_performance_matrix"
    # Literature basis: asphalt-aggregate pull-off bond 0.3-1.5 MPa; WER modification
    # raises bond by 20-60% with an optimum near 3 wt% (above which over-curing/
    # viscosity drops bond). Shear strength tracks pull-off at ~70% magnitude.
    formulations = ["Control", "1 wt%", "3 wt%", "5 wt%"]
    pull_off = [0.85, 1.08, 1.42, 1.23]      # MPa, peak at 3 wt%
    shear    = [0.62, 0.79, 1.05, 0.91]      # MPa, ~70% of pull-off
    pull_err = [0.07, 0.08, 0.09, 0.08]
    shear_err = [0.06, 0.07, 0.08, 0.07]

    comment = (
        "Literature basis: asphalt-aggregate pull-off bond 0.3-1.5 MPa; WER\n"
        "modification raises bond 20-60% with optimum near 3 wt%. Shear tracks\n"
        "pull-off at ~0.7 ratio. Values are synthetic but bounded by reported\n"
        "ranges; errors are typical lab std-dev (n=3-5 replicates)."
    )
    _save_csv(
        data_dir / f"{name}.csv",
        ["formulation", "pull_off_MPa", "shear_MPa", "pull_off_err", "shear_err"],
        [list(r) for r in zip(formulations, pull_off, shear, pull_err, shear_err)],
        comment=comment,
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    x = np.arange(len(formulations))
    width = 0.35
    ax.bar(x - width / 2, pull_off, width, yerr=pull_err, label="Pull-off",
           color=PALETTE_CBM["control"], capsize=3, edgecolor="white", linewidth=0.6)
    ax.bar(x + width / 2, shear, width, yerr=shear_err, label="Shear",
           color=PALETTE_CBM["modified"], capsize=3, edgecolor="white", linewidth=0.6)
    ax.set_ylabel("Bonding strength (MPa)")
    ax.set_xticks(x)
    ax.set_xticklabels(formulations)
    ax.set_title("Bonding performance matrix (pull-off + shear)")
    ax.legend()
    ax.grid(axis="y", color="#E8E2D6", linewidth=0.8, alpha=0.8)
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: WER modification raises asphalt-aggregate bond with an optimum "
        "near 3 wt%. Boundary: synthetic values bounded by literature ranges; "
        "no field pull-off data; substrate/temperature conditions not encoded.",
    )
    return name


def _rich_dosage_workability_window(output_dir: Path, data_dir: Path) -> str:
    name = "dosage_workability_window"
    # Literature basis: WER dosage raises viscosity monotonically but
    # spreadability (workability) peaks then drops; the workable window is the
    # dosage range keeping viscosity < 15 Pa.s AND spreadability > 0.7.
    # This figure is orthogonal to review-first/dosage_viscosity_bonding_window,
    # which tracks bond strength rather than workability.
    dosage = np.array([0, 1, 2, 3, 4, 5, 6], dtype=float)
    viscosity = np.array([2.4, 3.6, 5.8, 9.2, 14.5, 22.0, 31.5])    # Pa.s, monotonic up
    spreadability = np.array([0.55, 0.72, 0.86, 0.90, 0.82, 0.66, 0.48])  # rises then falls

    comment = (
        "Literature basis: WER dosage raises emulsion viscosity monotonically;\n"
        "spreadability (coatability) peaks near 3 wt% then drops as viscosity\n"
        "climbs. Workable window = viscosity < 15 Pa.s AND spreadability > 0.7.\n"
        "Orthogonal to review-first/dosage_viscosity_bonding_window (bond, not\n"
        "workability). Values synthetic, bounded by reported WER-emulsion ranges."
    )
    _save_csv(
        data_dir / f"{name}.csv",
        ["dosage_wt", "viscosity_Pa_s", "spreadability_index"],
        [[float(d), float(v), float(s)] for d, v, s in zip(dosage, viscosity, spreadability)],
        comment=comment,
    )

    apply_pub_style()
    fig, ax1 = plt.subplots(figsize=(7, 4.5))
    c_visc = PALETTE_CBM["control"]
    ax1.plot(dosage, viscosity, "o-", color=c_visc, linewidth=2, markersize=6, label="Viscosity")
    ax1.set_xlabel("WER dosage (wt%)")
    ax1.set_ylabel("Viscosity (Pa·s)", color=c_visc)
    ax1.tick_params(axis="y", labelcolor=c_visc)
    ax2 = ax1.twinx()
    c_spread = PALETTE_CBM["modified"]
    ax2.plot(dosage, spreadability, "s--", color=c_spread, linewidth=2, markersize=6, label="Spreadability")
    ax2.set_ylabel("Spreadability index", color=c_spread)
    ax2.tick_params(axis="y", labelcolor=c_spread)
    ax2.set_ylim(0, 1.05)
    # Workable window: viscosity < 15 AND spreadability > 0.7  -> dosage 1.5-4.2
    ax1.axvspan(1.5, 4.2, alpha=0.12, color=PALETTE_CBM["optimal"], label="Workable window")
    ax1.axhline(15, color=c_visc, linestyle=":", linewidth=1, alpha=0.6)
    ax2.axhline(0.7, color=c_spread, linestyle=":", linewidth=1, alpha=0.6)
    ax1.set_title("Dosage-workability window")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc="center right", fontsize=7)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: a workable WER dosage window exists near 1.5-4.2 wt% bounded by "
        "viscosity < 15 Pa.s and spreadability > 0.7. Boundary: spreadability is "
        "a normalized lab index, not a standardised field metric.",
    )
    return name


def _rich_interface_mechanism_map(output_dir: Path, data_dir: Path) -> str:
    name = "interface_mechanism_map"
    # Literature basis: WER-EA interface formation proceeds by demulsification ->
    # curing -> morphology development -> interface reaction -> bonding. Each stage
    # has a measured evidence strength from FTIR/SEM/rheology. This is a process
    # flow figure, orthogonal to review-first/interface_mechanism_boundary which
    # maps test methods to evidence tiers.
    stages = ["Demulsification", "Curing", "Morphology", "Interface\nreaction", "Bonding"]
    xs = [0.10, 0.30, 0.50, 0.70, 0.90]
    ys = [0.62, 0.74, 0.58, 0.70, 0.55]
    evidence = [0.82, 0.68, 0.75, 0.55, 0.78]  # measured evidence strength

    comment = (
        "Literature basis: WER-EA interface forms via demulsification -> curing\n"
        "-> morphology -> interface reaction -> bonding. Evidence strength from\n"
        "FTIR (curing), SEM/fluorescence (morphology), rheology (demulsification),\n"
        "pull-off (bonding). Interface-reaction step is the least directly measured.\n"
        "Process-flow figure; orthogonal to review-first/interface_mechanism_boundary."
    )
    _save_csv(
        data_dir / f"{name}.csv",
        ["stage", "evidence_score"],
        [[s.replace("\n", " "), float(e)] for s, e in zip(stages, evidence)],
        comment=comment,
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for i, (x, y, label) in enumerate(zip(xs, ys, stages)):
        ax.add_patch(Circle((x, y), 0.055,
                            color=PALETTE_CBM["control"], alpha=0.25 + evidence[i] * 0.45))
        ax.text(x, y, label, ha="center", va="center", fontsize=8, fontweight="bold")
        if i < len(stages) - 1:
            ax.annotate(
                "",
                xy=(xs[i + 1] - 0.055, ys[i + 1]),
                xytext=(x + 0.055, y),
                arrowprops=dict(arrowstyle="->", color=PALETTE_CBM["mechanism"], lw=2),
            )
        ax.text(x, y - 0.10, f"ev={evidence[i]:.2f}", ha="center", fontsize=7,
                color=PALETTE_CBM["danger"])
    ax.set_xlim(0, 1)
    ax.set_ylim(0.35, 0.90)
    ax.axis("off")
    ax.set_title("Interface mechanism map (process flow + evidence strength)")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: interface formation is a five-stage process with measurable "
        "evidence at each stage. Boundary: arrow direction assumes a causal order "
        "that is inferred, not isolated stage-by-stage; interface-reaction evidence "
        "is the weakest link.",
    )
    return name


def _rich_ftir_sem_evidence_pair(output_dir: Path, data_dir: Path) -> str:
    name = "ftir_sem_evidence_pair"
    # Literature basis: WER-EA FTIR peaks anchored to real functional groups:
    #   2920 cm-1  CH2 asym stretch (asphalt)
    #   1730 cm-1  C=O ester stretch (WER epoxy ester)
    #   1240 cm-1  C-O-C ether stretch (WER)
    #    915 cm-1  oxirane ring of epoxy (curing tracker)
    #   1600 cm-1  aromatic C=C (asphalt)
    # SEM: WER modification shifts droplet/particle size finer and tighter.
    wavenumber = np.linspace(4000, 500, 600)
    base = 0.18 + 0.34 * np.exp(-((wavenumber - 2920) ** 2) / 4e4) \
               + 0.20 * np.exp(-((wavenumber - 1600) ** 2) / 6e3)
    control = base + 0.02 * np.random.default_rng(7).normal(0, 1, len(wavenumber))
    modified = base \
        + 0.28 * np.exp(-((wavenumber - 1730) ** 2) / 4e3) \
        + 0.22 * np.exp(-((wavenumber - 1240) ** 2) / 3e3) \
        + 0.16 * np.exp(-((wavenumber - 915) ** 2) / 2e3) \
        + 0.02 * np.random.default_rng(11).normal(0, 1, len(wavenumber))
    modified = np.clip(modified, 0, None)

    size_bins = np.array([0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5])
    control_size = [2, 7, 14, 22, 28, 18, 11, 6, 3, 1]
    modified_size = [1, 5, 12, 24, 32, 22, 9, 4, 2, 1]

    comment_ftir = (
        "Literature basis: FTIR peaks anchored to real functional groups:\n"
        "2920 cm-1 CH2 asym stretch (asphalt); 1730 cm-1 C=O ester (WER);\n"
        "1240 cm-1 C-O-C ether (WER); 915 cm-1 oxirane ring (epoxy curing tracker);\n"
        "1600 cm-1 aromatic C=C (asphalt). Modified spectrum adds the three WER\n"
        "peaks. Absorbance is synthetic Gaussian-broadened, not a real scan."
    )
    comment_sem = (
        "Literature basis: WER modification shifts emulsion droplet size finer\n"
        "and tighter (lower mean, higher peak count near 3-5 um). Counts are\n"
        "synthetic frequency bins from a representative SEM image, not a full PSD."
    )
    _save_csv(data_dir / f"{name}_ftir.csv",
              ["wavenumber_cm-1", "control_abs", "modified_abs"],
              [[float(w), float(c), float(m)] for w, c, m in zip(wavenumber, control, modified)],
              comment=comment_ftir)
    _save_csv(data_dir / f"{name}_sem.csv",
              ["size_um", "control_count", "modified_count"],
              [[float(b), int(c), int(m)] for b, c, m in zip(size_bins, control_size, modified_size)],
              comment=comment_sem)

    apply_pub_style()
    fig, axes = plt.subplots(1, 2, figsize=(9, 3.8))
    axes[0].plot(wavenumber, control, label="Control (asphalt)", color=PALETTE_CBM["control"], lw=1.4)
    axes[0].plot(wavenumber, modified, label="WER-EA modified", color=PALETTE_CBM["modified"], lw=1.4)
    for wn, lbl in [(2920, "CH2"), (1730, "C=O"), (1600, "C=C"), (1240, "C-O-C"), (915, "oxirane")]:
        axes[0].axvline(wn, color=PALETTE_CBM["neutral"], lw=0.6, ls=":", alpha=0.7)
        axes[0].text(wn, axes[0].get_ylim()[1] if False else 0.95, lbl, rotation=90,
                     fontsize=6, color=PALETTE_CBM["danger"], va="top", ha="right")
    axes[0].invert_xaxis()
    axes[0].set_xlabel("Wavenumber (cm$^{-1}$)")
    axes[0].set_ylabel("Absorbance (a.u.)")
    axes[0].set_title("(a) FTIR spectra")
    axes[0].legend(fontsize=7)
    axes[1].bar(size_bins - 0.2, control_size, 0.4, label="Control", color=PALETTE_CBM["control"])
    axes[1].bar(size_bins + 0.2, modified_size, 0.4, label="Modified", color=PALETTE_CBM["modified"])
    axes[1].set_xlabel(r"Particle size ($\mu$m)")
    axes[1].set_ylabel("Frequency count")
    axes[1].set_title("(b) SEM droplet size")
    axes[1].legend(fontsize=7)
    fig.suptitle("FTIR + SEM evidence pair (anchored functional groups)")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: WER-EA adds C=O (1730), C-O-C (1240) and oxirane (915) peaks and "
        "shifts droplet size finer. Boundary: spectra are synthetic Gaussian peaks, "
        "not real scans; peak ratios do not quantify epoxy conversion.",
    )
    return name


def _rich_moisture_aging_retention(output_dir: Path, data_dir: Path) -> str:
    name = "moisture_aging_retention"
    # Literature basis: moisture-conditioned bond retention drops with aging time;
    # WER modification slows the drop. This is a time-series figure (0-30 d),
    # orthogonal to review-first/durability_retention_challenge_map which compares
    # challenge categories with evidence tiers.
    days = np.array([0, 3, 7, 14, 21, 30])
    control = np.array([100, 81, 68, 54, 46, 39])     # steep drop
    modified = np.array([100, 94, 88, 80, 74, 68])    # gentler drop
    control_err = [3, 4, 5, 6, 6, 7]
    modified_err = [2, 3, 3, 4, 4, 5]

    comment = (
        "Literature basis: moisture-conditioned bond retention (%) declines with\n"
        "immersion/aging time; WER modification slows the decline (retention > 80%\n"
        "to ~14 d vs control ~7 d). Time-series figure; orthogonal to\n"
        "review-first/durability_retention_challenge_map (challenge categories).\n"
        "Values synthetic, bounded by reported WER-EA durability ranges."
    )
    _save_csv(
        data_dir / f"{name}.csv",
        ["day", "control_retention_pct", "modified_retention_pct", "control_err", "modified_err"],
        [[int(d), float(c), float(m), float(ce), float(me)]
         for d, c, m, ce, me in zip(days, control, modified, control_err, modified_err)],
        comment=comment,
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.errorbar(days, control, yerr=control_err, fmt="o-", label="Control",
                color=PALETTE_CBM["control"], capsize=3, linewidth=1.8)
    ax.errorbar(days, modified, yerr=modified_err, fmt="s-", label="WER modified",
                color=PALETTE_CBM["modified"], capsize=3, linewidth=1.8)
    ax.set_xlabel("Moisture aging time (d)")
    ax.set_ylabel("Bond retention (%)")
    ax.set_ylim(0, 110)
    ax.axhline(80, color=PALETTE_CBM["accent"], linestyle="--", linewidth=1, label="80% acceptance")
    ax.set_title("Moisture-aging retention (time series)")
    ax.legend(fontsize=8)
    ax.grid(color="#E8E2D6", linewidth=0.7, alpha=0.7)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: WER modification extends moisture-conditioned bond retention above "
        "80% from ~7 d to ~14 d. Boundary: lab immersion only; field moisture and "
        "traffic loading not represented; error bars are synthetic std-dev.",
    )
    return name


def _rich_storage_stability_timeline(output_dir: Path, data_dir: Path) -> str:
    name = "storage_stability_timeline"
    # Literature basis: WER-EA emulsion storage stability (settlement index) must
    # stay > 80% over the storage period; unmodified control settles faster.
    days = np.array([0, 1, 3, 5, 7, 14])
    control = np.array([99, 90, 78, 64, 50, 28])
    modified = np.array([99, 96, 91, 86, 81, 71])

    comment = (
        "Literature basis: WER-EA emulsion storage stability (settlement index, %)\n"
        "must remain > 80% over the storage period. WER slows demulsification/\n"
        "creaming. Control drops below 80% within ~3 d; modified holds to ~7 d.\n"
        "Values synthetic, bounded by reported emulsion stability tests."
    )
    _save_csv(
        data_dir / f"{name}.csv",
        ["day", "control_stability_pct", "modified_stability_pct"],
        [[int(d), float(c), float(m)] for d, c, m in zip(days, control, modified)],
        comment=comment,
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(days, control, "o-", label="Control emulsion", color=PALETTE_CBM["control"])
    ax.plot(days, modified, "s-", label="WER-EA emulsion", color=PALETTE_CBM["modified"])
    ax.set_xlabel("Storage time (d)")
    ax.set_ylabel("Stability index (%)")
    ax.set_ylim(0, 105)
    ax.axhline(80, color=PALETTE_CBM["accent"], linestyle="--", linewidth=1, label="80% threshold")
    ax.set_title("Storage stability timeline")
    ax.legend(fontsize=8)
    ax.grid(color="#E8E2D6", linewidth=0.7, alpha=0.7)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: WER-EA emulsion retains > 80% stability to ~7 d vs ~3 d for control. "
        "Boundary: settlement index is a lab proxy; storage temperature and container "
        "geometry effects not encoded.",
    )
    return name


def _rich_pavement_layer_tackcoat(output_dir: Path, data_dir: Path) -> str:
    name = "pavement_layer_tackcoat"
    # Literature basis: tack coat application rate 0.2-1.0 L/m2; interface shear
    # strength peaks near 0.6 L/m2 then drops as excess binder creates a slip plane.
    rates = [0.2, 0.4, 0.6, 0.8, 1.0]
    shear = [0.55, 0.92, 1.35, 1.18, 0.96]
    shear_err = [0.06, 0.07, 0.09, 0.08, 0.07]

    comment = (
        "Literature basis: tack coat application rate 0.2-1.0 L/m2; interface shear\n"
        "strength peaks near 0.6 L/m2 then drops as excess binder forms a slip\n"
        "plane. Values synthetic, bounded by reported pavement layer shear tests."
    )
    _save_csv(
        data_dir / f"{name}.csv",
        ["application_rate_L_m2", "shear_strength_MPa", "shear_err"],
        [[float(r), float(s), float(e)] for r, s, e in zip(rates, shear, shear_err)],
        comment=comment,
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.errorbar(rates, shear, yerr=shear_err, fmt="o-", color=PALETTE_CBM["optimal"],
                linewidth=2, markersize=7, capsize=3)
    ax.fill_between(rates, shear, alpha=0.12, color=PALETTE_CBM["optimal"])
    ax.axvline(0.6, color=PALETTE_CBM["danger"], linestyle=":", linewidth=1, label="peak ~0.6 L/m2")
    ax.set_xlabel("Tack coat application rate (L/m$^2$)")
    ax.set_ylabel("Interface shear strength (MPa)")
    ax.set_title("Pavement layer tack coat shear")
    ax.legend(fontsize=8)
    ax.grid(color="#E8E2D6", linewidth=0.7, alpha=0.7)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: interface shear peaks near 0.6 L/m2 and drops at higher rates. "
        "Boundary: lab shear test only; substrate texture, temperature and traffic "
        "compaction not encoded.",
    )
    return name


def _rich_cement_hydration_evidence(output_dir: Path, data_dir: Path) -> str:
    name = "cement_hydration_evidence"
    # Literature basis: Portland cement hydration heat-flow curve shows:
    #   - induction period (0-2 h, low heat)
    #   - C3S main hydration peak near 8-12 h (acceleration + deceleration)
    #   - slow C2S contribution after ~24 h-7 d
    # Cumulative heat saturates near ~300-350 J/g by 7 d. Ca(OH)2 grows stepwise.
    time = np.array([0, 1, 3, 6, 8, 12, 18, 24, 48, 72, 168], dtype=float)  # hours
    heat_flow = np.array([0.2, 0.5, 1.2, 3.8, 5.6, 4.2, 2.0, 1.3, 0.9, 0.7, 0.6])  # mW/g, C3S peak ~8-12h
    cum_heat = np.array([0, 1, 6, 24, 58, 110, 160, 195, 250, 290, 330])            # J/g cumulative
    ch = np.array([0, 1, 3, 8, 14, 22, 30, 36, 48, 56, 64])                          # Ca(OH)2 %

    comment = (
        "Literature basis: Portland cement isothermal calorimetry. C3S main\n"
        "hydration peak near 8-12 h (heat flow mW/g); C2S contributes slowly after\n"
        "~24 h. Cumulative heat saturates ~300-350 J/g by 7 d. Ca(OH)2 grows\n"
        "stepwise with C3S hydration. Values synthetic but follow the real curve\n"
        "shape (induction -> acceleration -> deceleration -> slow C2S tail)."
    )
    _save_csv(
        data_dir / f"{name}.csv",
        ["time_h", "heat_flow_mW_g", "cum_heat_J_g", "CH_content_pct"],
        [[float(t), float(hf), float(ch_cum), float(chp)]
         for t, hf, ch_cum, chp in zip(time, heat_flow, cum_heat, ch)],
        comment=comment,
    )

    apply_pub_style()
    fig, ax1 = plt.subplots(figsize=(7.5, 4.8))
    ax1.plot(time, heat_flow, "o-", color=PALETTE_CBM["control"], label="Heat flow (mW/g)")
    ax1.set_xlabel("Hydration time (h)")
    ax1.set_ylabel("Heat flow (mW/g)", color=PALETTE_CBM["control"])
    ax1.tick_params(axis="y", labelcolor=PALETTE_CBM["control"])
    ax2 = ax1.twinx()
    ax2.plot(time, cum_heat, "s--", color=PALETTE_CBM["modified"], label="Cumulative heat (J/g)")
    ax2.plot(time, [c * 5 for c in ch], "^:", color=PALETTE_CBM["mechanism"], label="Ca(OH)$_2$ (x5)")
    ax2.set_ylabel("Cumulative heat (J/g) / CH (%, x5)", color=PALETTE_CBM["modified"])
    ax2.tick_params(axis="y", labelcolor=PALETTE_CBM["modified"])
    ax1.axvspan(6, 14, alpha=0.10, color=PALETTE_CBM["danger"], label="C3S peak window")
    ax1.set_title("Cement hydration evidence (C3S peak + C2S tail)")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=7, loc="right")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: heat-flow curve shows the C3S peak near 8-12 h and a slow C2S tail "
        "to 7 d. Boundary: synthetic curve following the real shape; no admixture "
        "or temperature-cure variation encoded; CH scaled x5 for visibility.",
    )
    return name


def _rich_lca_boundary_card(output_dir: Path, data_dir: Path) -> str:
    name = "lca_boundary_card"
    # Literature basis: asphalt pavement cradle-to-grave GWP by stage. Manufacturing
    # (asphalt mixing, ~150-180 C) dominates; end-of-life recycling gives a credit.
    stages = ["Raw material", "Transport", "Manufacturing", "Construction", "Use", "End-of-life"]
    gwp = [12.5, 3.2, 28.4, 5.1, 8.6, -2.3]  # kg CO2 eq per functional unit

    comment = (
        "Literature basis: asphalt pavement cradle-to-grave GWP (kg CO2 eq per\n"
        "functional unit). Manufacturing (hot mixing at 150-180 C) dominates.\n"
        "End-of-life recycling gives a negative (credit) value. Values synthetic,\n"
        "ordered by typical magnitude from asphalt-pavement LCA reviews."
    )
    _save_csv(
        data_dir / f"{name}.csv",
        ["life_cycle_stage", "GWP_kg_CO2_eq"],
        [[s, float(g)] for s, g in zip(stages, gwp)],
        comment=comment,
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    colors = [PALETTE_CBM["danger"] if g > 0 else PALETTE_CBM["optimal"] for g in gwp]
    ax.barh(stages, gwp, color=colors, edgecolor="white", linewidth=0.6)
    ax.set_xlabel("GWP (kg CO$_2$ eq.)")
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_title("LCA system boundary card (asphalt pavement)")
    ax.grid(axis="x", color="#E8E2D6", linewidth=0.7, alpha=0.7)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: manufacturing is the dominant GWP stage; end-of-life recycling is a "
        "net credit. Boundary: values are per a generic functional unit; actual GWP "
        "depends on mix design, plant energy source and transport distance.",
    )
    return name


def _rich_review_taxonomy_map(output_dir: Path, data_dir: Path) -> str:
    name = "review_taxonomy_map"
    # Literature basis: WER-EA review literature taxonomy. Papers cluster by
    # Materials (formulation), Tests (bonding/durability), Mechanisms (FTIR/SEM),
    # Performance (road performance), Gaps (identified open questions).
    categories = ["Materials", "Tests", "Mechanisms", "Performance", "Gaps"]
    counts = [42, 28, 19, 35, 14]

    comment = (
        "Literature basis: WER-EA review literature taxonomy. Categories reflect\n"
        "how papers cluster: Materials (formulation), Tests (bonding/durability),\n"
        "Mechanisms (FTIR/SEM/rheology), Performance (road performance), Gaps\n"
        "(identified open questions). Counts are illustrative of a ~80-paper review."
    )
    _save_csv(
        data_dir / f"{name}.csv",
        ["category", "paper_count"],
        [[c, int(n)] for c, n in zip(categories, counts)],
        comment=comment,
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7, 4.5))
    bars = ax.bar(categories, counts,
                  color=[PALETTE_CBM["control"], PALETTE_CBM["modified"], PALETTE_CBM["mechanism"],
                         PALETTE_CBM["optimal"], PALETTE_CBM["danger"]],
                  edgecolor="white", linewidth=0.6)
    ax.set_ylabel("Number of papers")
    ax.set_title("Review taxonomy map (WER-EA literature)")
    for bar, n in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.8, str(n),
                ha="center", fontsize=9)
    ax.grid(axis="y", color="#E8E2D6", linewidth=0.7, alpha=0.7)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: WER-EA literature clusters into five categories with Materials the "
        "largest and Gaps the smallest. Boundary: counts are illustrative, not a "
        "systematic review tally; category boundaries are soft.",
    )
    return name


# ---------------------------------------------------------------------------
# review-first: data-driven review figures with evidence-tier encoding.
# Each figure answers a distinct review dimension (framework / evidence chain /
# gap / method / challenge / summary) and carries the four-tier legend.
# ---------------------------------------------------------------------------


def _review_review_framework_map(output_dir: Path, data_dir: Path) -> str:
    name = "review_framework_map"
    # Review dimension: framework coverage. Each axis is a review-coverage score
    # with its evidence tier tagged. Durability evidence is the weakest (missing).
    dimensions = ["Material\nscope", "Mechanism\ndepth", "Performance\ncoverage",
                  "Durability\nevidence", "Gap\nclarity"]
    scores = [0.78, 0.55, 0.82, 0.35, 0.62]
    tiers = ["measured", "inferred", "measured", "missing", "inferred"]

    comment = (
        "Review dimension: framework coverage of a WER-EA mini-review. Each axis\n"
        "score is tagged with an evidence tier: Material scope and Performance\n"
        "coverage are measured (lab data rich); Mechanism depth and Gap clarity\n"
        "are inferred; Durability evidence is missing (long-term data absent).\n"
        "Scores are reviewer judgement, not measured values."
    )
    _save_csv(
        data_dir / f"{name}.csv",
        ["dimension", "coverage_score", "evidence_tier"],
        [[d.replace("\n", " "), float(s), t] for d, s, t in zip(dimensions, scores, tiers)],
        comment=comment,
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(6.2, 6.2), subplot_kw=dict(polar=True))
    angles = np.linspace(0, 2 * np.pi, len(dimensions), endpoint=False).tolist()
    scores_plot = scores + scores[:1]
    angles += angles[:1]
    ax.fill(angles, scores_plot, color=PALETTE_CBM["control"], alpha=0.20)
    ax.plot(angles, scores_plot, "o-", color=PALETTE_CBM["control"], linewidth=2)
    # colour each vertex by its evidence tier
    for ang, sc, tier in zip(angles[:-1], scores, tiers):
        ax.plot(ang, sc, "o", color=_tier_color(tier), markersize=10,
                markeredgecolor="#333333", markeredgewidth=0.8)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dimensions, fontsize=8)
    ax.set_ylim(0, 1)
    ax.set_title("Review framework map (coverage + evidence tier)", y=1.10)
    _add_evidence_tier_legend(ax, loc="lower center", fontsize=7)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: the review covers material scope and performance well but lacks "
        "durability evidence. Boundary: scores are reviewer judgement; tier tags "
        "reflect evidence availability, not score magnitude.",
    )
    return name


def _review_material_mechanism_performance_challenges(output_dir: Path, data_dir: Path) -> str:
    name = "material_mechanism_performance_challenges"
    # Review dimension: material comparison. Each modifier is plotted by mechanism
    # understanding (x), performance (y), challenge (size), and evidence tier (colour).
    materials = ["SBR", "CR", "EVA", "PU", "Epoxy"]
    mechanism = [0.55, 0.48, 0.62, 0.70, 0.80]
    performance = [72, 65, 78, 85, 90]
    challenge = [0.35, 0.42, 0.28, 0.20, 0.15]
    tiers = ["measured", "inferred", "measured", "inferred", "measured"]

    comment = (
        "Review dimension: modifier comparison in asphalt. Mechanism understanding\n"
        "(x, reviewer score), performance (y, normalised road-performance index),\n"
        "challenge (bubble size, lower is better), evidence tier (colour). SBR/EVA\n"
        "performance is measured; CR/PU mechanism is inferred from indirect tests.\n"
        "Scores are reviewer judgement bounded by reported modifier ranges."
    )
    _save_csv(
        data_dir / f"{name}.csv",
        ["material", "mechanism_score", "performance_score", "challenge_score", "evidence_tier"],
        [[m, float(ms), float(p), float(c), t]
         for m, ms, p, c, t in zip(materials, mechanism, performance, challenge, tiers)],
        comment=comment,
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7.2, 5))
    for m, ms, p, c, t in zip(materials, mechanism, performance, challenge, tiers):
        ax.scatter(ms, p, s=[c * 2200], color=_tier_color(t), alpha=0.75,
                   edgecolors="#333333", linewidth=0.7)
        ax.annotate(m, (ms, p), textcoords="offset points", xytext=(6, 6), fontsize=9)
    ax.set_xlabel("Mechanism understanding score")
    ax.set_ylabel("Performance score")
    ax.set_xlim(0.3, 0.95)
    ax.set_ylim(55, 98)
    ax.set_title("Material-Mechanism-Performance-Challenge map")
    ax.grid(color="#E8E2D6", linewidth=0.7, alpha=0.7)
    _add_evidence_tier_legend(ax, loc="lower right", fontsize=7)
    # annotate bubble size meaning
    ax.text(0.04, 0.96, "bubble size = challenge (larger = harder)",
            transform=ax.transAxes, fontsize=7, va="top", color="#555555")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: epoxy has the highest mechanism understanding and performance; CR "
        "the lowest. Boundary: scores are reviewer judgement; performance index is "
        "normalised across non-identical test protocols; bubble size is qualitative.",
    )
    return name


def _review_evidence_chain_map(output_dir: Path, data_dir: Path) -> str:
    name = "evidence_chain_map"
    # Review dimension: evidence chain. Each link in the claim->durability chain is
    # tagged with an evidence tier. Durability is missing; interface is speculative.
    stages = ["Claim", "Microstructure", "Chemistry", "Interface", "Durability"]
    support = [0.90, 0.75, 0.62, 0.40, 0.15]
    tiers = ["measured", "measured", "inferred", "speculative", "missing"]

    comment = (
        "Review dimension: evidence chain from claim to durability for WER-EA.\n"
        "Claim and Microstructure are measured (lab tests); Chemistry is inferred\n"
        "from FTIR peak changes; Interface is speculative (no direct interface\n"
        "probe); Durability is missing (no long-term field data). Support score is\n"
        "reviewer judgement of how strongly each link is backed."
    )
    _save_csv(
        data_dir / f"{name}.csv",
        ["stage", "evidence_support_score", "evidence_tier"],
        [[s, float(v), t] for s, v, t in zip(stages, support, tiers)],
        comment=comment,
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    bars = ax.barh(stages, support, color=[_tier_color(t) for t in tiers],
                   edgecolor="#333333", linewidth=0.6)
    ax.set_xlim(0, 1.05)
    ax.set_xlabel("Evidence support score")
    ax.invert_yaxis()
    for bar, t in zip(bars, tiers):
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2,
                t, va="center", fontsize=8, color="#333333")
    ax.set_title("Evidence chain map (claim -> durability, tiered)")
    ax.axvline(0.7, color=PALETTE_CBM["accent"], linestyle="--", linewidth=1,
               label="strong-evidence threshold")
    _add_evidence_tier_legend(ax, loc="lower right", fontsize=7)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: the evidence chain weakens from measured claim/microstructure to "
        "missing durability. Boundary: support scores are reviewer judgement; "
        "interface and durability tiers mark absence, not negative results.",
    )
    return name


def _review_interface_mechanism_boundary(output_dir: Path, data_dir: Path) -> str:
    name = "interface_mechanism_boundary"
    # Review dimension: interface mechanism evidence by test method. Each method is
    # tagged with an evidence tier. This is a method-evidence figure, orthogonal to
    # rich-gallery/interface_mechanism_map (process flow).
    methods = ["Contact angle", "FTIR ester peak", "SEM roughness", "Rheology G'", "Pull-off test"]
    raw = [68.0, 0.35, 2.8, 1450.0, 2.4]
    units = ["deg", "abs", "um", "Pa", "MPa"]
    normalized = [0.55, 0.70, 0.60, 0.80, 0.75]
    tiers = ["inferred", "measured", "measured", "measured", "measured"]

    comment = (
        "Review dimension: interface-mechanism evidence by test method. FTIR ester\n"
        "peak (1730 cm-1), SEM roughness, rheology G' and pull-off are measured;\n"
        "contact angle is inferred (wettability proxy for adhesion). Normalised\n"
        "score is reviewer judgement of how directly each method probes the\n"
        "interface. Method-evidence figure; orthogonal to rich-gallery process flow."
    )
    _save_csv(
        data_dir / f"{name}.csv",
        ["method", "raw_value", "unit", "normalized_score", "evidence_tier"],
        [[m, float(v), u, float(n), t]
         for m, v, u, n, t in zip(methods, raw, units, normalized, tiers)],
        comment=comment,
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    bars = ax.barh(methods, normalized, color=[_tier_color(t) for t in tiers],
                   edgecolor="#333333", linewidth=0.6)
    ax.set_xlim(0, 1.05)
    ax.set_xlabel("Normalised evidence score")
    ax.invert_yaxis()
    for bar, v, u, t in zip(bars, raw, units, tiers):
        ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height() / 2,
                f"{v:g} {u} [{t}]", va="center", fontsize=7, color="#333333")
    ax.set_title("Interface mechanism boundary (method evidence + tier)")
    _add_evidence_tier_legend(ax, loc="lower right", fontsize=7)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: pull-off, rheology and FTIR directly probe the interface; contact "
        "angle is an inferred wettability proxy. Boundary: normalised scores are "
        "reviewer judgement; no single method isolates the interface reaction.",
    )
    return name


def _review_bonding_test_method_map(output_dir: Path, data_dir: Path) -> str:
    name = "bonding_test_method_map"
    # Review dimension: bonding test-method relevance. Methods x influence factors
    # heatmap. Cells encode how strongly each factor affects each method's result,
    # with an evidence-tier tag per method row.
    methods = ["Pull-off", "Shear", "Tensile", "Flexural", "Fracture"]
    factors = ["Substrate", "Rate", "Curing", "Loading", "Metric"]
    data = np.array([
        [1.0, 0.8, 0.9, 0.7, 0.6],
        [0.7, 1.0, 0.8, 0.9, 0.7],
        [0.8, 0.7, 1.0, 0.6, 0.9],
        [0.6, 0.8, 0.7, 1.0, 0.8],
        [0.5, 0.6, 0.6, 0.7, 1.0],
    ])
    method_tiers = ["measured", "measured", "inferred", "inferred", "speculative"]

    comment = (
        "Review dimension: bonding test-method relevance. Cells encode how strongly\n"
        "each influence factor (substrate, loading rate, curing, loading mode,\n"
        "metric definition) affects each method's result. Pull-off and shear are\n"
        "measured (standardised); tensile and flexural are inferred (adapted);\n"
        "fracture is speculative (no standard for tack coat). Values are reviewer\n"
        "judgement, not measured correlations."
    )
    rows = []
    for i, m in enumerate(methods):
        for j, f in enumerate(factors):
            rows.append([m, f, float(data[i, j]), method_tiers[i]])
    _save_csv(data_dir / f"{name}.csv", ["method", "factor", "relevance_score", "evidence_tier"], rows,
              comment=comment)

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7.5, 5))
    im = ax.imshow(data, cmap="Blues", vmin=0, vmax=1)
    ax.set_xticks(np.arange(len(factors)))
    ax.set_yticks(np.arange(len(methods)))
    ax.set_xticklabels(factors)
    ax.set_yticklabels([f"{m} [{t}]" for m, t in zip(methods, method_tiers)], fontsize=8)
    for i in range(len(methods)):
        for j in range(len(factors)):
            ax.text(j, i, f"{data[i, j]:.1f}", ha="center", va="center",
                    color="white" if data[i, j] > 0.5 else "black", fontsize=9)
    ax.set_title("Bonding test-method map (relevance + method tier)")
    # colour the y-tick labels by tier
    for tick, t in zip(ax.get_yticklabels(), method_tiers):
        tick.set_color(_tier_color(t))
    fig.colorbar(im, ax=ax, label="Relevance")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: substrate and curing dominate pull-off; loading rate dominates "
        "shear. Boundary: relevance scores are reviewer judgement; fracture method "
        "has no tack-coat standard (speculative tier).",
    )
    return name


def _review_dosage_viscosity_bonding_window(output_dir: Path, data_dir: Path) -> str:
    name = "dosage_viscosity_bonding_window"
    # Review dimension: dosage-performance window from a review lens. Bond strength
    # peaks near 3 wt%; viscosity rises monotonically. The optimal window is tagged
    # measured; the over-dosage drop is inferred; the under-dosage tail is measured.
    # Orthogonal to rich-gallery/dosage_workability_window (workability, not bond).
    dosage = np.array([0, 1, 2, 3, 4, 5, 6], dtype=float)
    viscosity = np.array([2.4, 3.6, 5.8, 9.2, 14.5, 22.0, 31.5])
    bonding = np.array([0.85, 1.08, 1.42, 1.45, 1.28, 1.05, 0.82])
    bond_err = np.array([0.07, 0.08, 0.09, 0.09, 0.08, 0.07, 0.07])
    # tier per dosage point
    tiers = ["measured", "measured", "measured", "measured", "inferred", "inferred", "speculative"]

    comment = (
        "Review dimension: WER dosage vs bond strength and viscosity. Bond peaks\n"
        "near 3 wt% then drops (over-curing/viscosity). 0-4 wt% points are measured;\n"
        "5-6 wt% drop is inferred from viscosity trend; 6 wt% is speculative\n"
        "(limited data). Orthogonal to rich-gallery/dosage_workability_window\n"
        "(workability, not bond). Values synthetic, bounded by reported ranges."
    )
    _save_csv(
        data_dir / f"{name}.csv",
        ["dosage_wt", "viscosity_Pa_s", "bonding_MPa", "bond_err", "evidence_tier"],
        [[float(d), float(v), float(b), float(e), t]
         for d, v, b, e, t in zip(dosage, viscosity, bonding, bond_err, tiers)],
        comment=comment,
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    # colour each bond point by tier
    for d, b, be, t in zip(dosage, bonding, bond_err, tiers):
        ax.errorbar(d, b, yerr=be, fmt="o", color=_tier_color(t), markersize=8,
                    capsize=3, markeredgecolor="#333333", markeredgewidth=0.6)
    ax.plot(dosage, bonding, "-", color=PALETTE_CBM["neutral"], linewidth=1, alpha=0.5)
    ax.set_xlabel("WER dosage (wt%)")
    ax.set_ylabel("Bonding strength (MPa)", color=PALETTE_CBM["control"])
    ax.tick_params(axis="y", labelcolor=PALETTE_CBM["control"])
    ax2 = ax.twinx()
    ax2.plot(dosage, viscosity, "s--", color=PALETTE_CBM["modified"], linewidth=1.8, markersize=6,
             label="Viscosity")
    ax2.set_ylabel("Viscosity (Pa·s)", color=PALETTE_CBM["modified"])
    ax2.tick_params(axis="y", labelcolor=PALETTE_CBM["modified"])
    ax.axvspan(2.0, 3.5, alpha=0.12, color=PALETTE_CBM["optimal"], label="optimal bond window")
    ax.set_title("Dosage-viscosity-bonding window (review, tiered)")
    _add_evidence_tier_legend(ax, loc="lower left", fontsize=7)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: bond strength peaks near 3 wt% and drops at over-dosage. Boundary: "
        "0-4 wt% measured; 5-6 wt% inferred/speculative from viscosity trend; "
        "substrate and temperature not encoded.",
    )
    return name


def _review_ftir_sem_rheology_evidence_panel(output_dir: Path, data_dir: Path) -> str:
    name = "ftir_sem_rheology_evidence_panel"
    # Pattern 14 (Clinical triptych): three parallel evidence columns
    # (FTIR / SEM morphology / rheology) with a shared evidence-tier legend
    # strip on top and quantitative summary bars on the bottom. All text uses
    # unicode glyphs (no mathtext) to avoid SVG tspan character-splitting.
    #
    # FTIR peaks anchored to documented functional group wavenumbers:
    # 3400 (-OH), 2920/2850 (CH2), 1730 (C=O ester), 1600 (aromatic C=C),
    # 1240 (C-O-C ether), 915 (oxirane; disappears after epoxy cure).
    # SEM textures are simulated numpy morphology, not real micrographs.
    # Rheology reflects typical WER-EA modified binder frequency-sweep ranges.
    from matplotlib.gridspec import GridSpecFromSubplotSpec
    from matplotlib.transforms import blended_transform_factory

    # ── FTIR: transmittance with Gaussian peak valleys ──
    wavenumber = np.linspace(4000, 1000, 500)

    def _transmittance(peaks, baseline=94.0, oh_depth=14.0):
        t = np.full_like(wavenumber, baseline)
        for cen, dep, wid in peaks:
            t = t - dep * np.exp(-((wavenumber - cen) ** 2) / wid)
        # broad -OH envelope around 3400 cm^-1
        t = t - oh_depth * np.exp(-((wavenumber - 3400) ** 2) / 7e4)
        return np.clip(t, 6, 99)

    ftir_uncured = _transmittance([
        (2920, 13, 2.5e3), (2850, 9, 2.5e3),
        (1730, 21, 1.1e3), (1600, 11, 1.8e3),
        (1240, 19, 1.3e3), (915, 15, 7e2),
    ], oh_depth=14.0)
    # Cured: 915 oxirane peak disappears (epoxy ring opened); -OH grows
    ftir_cured = _transmittance([
        (2920, 13, 2.5e3), (2850, 9, 2.5e3),
        (1730, 21, 1.1e3), (1600, 11, 1.8e3),
        (1240, 19, 1.3e3),
    ], oh_depth=22.0)

    # ── Rheology: frequency sweep G* and phase angle delta ──
    freq = np.logspace(-1, 2, 40)  # 0.1 to 100 rad/s
    gstar_ctrl = 850.0 * freq ** 0.55
    gstar_mod = 3600.0 * freq ** 0.42
    delta_ctrl = np.clip(90 - 11 * np.log10(freq / 0.1), 52, 90)
    delta_mod = np.clip(80 - 32 * np.log10(freq / 0.1), 18, 88)

    # ── SEM: simulated morphology plates (pure numpy) ──
    rng = np.random.default_rng(42)

    def _sem_plate(n_particles, size_range, cluster=False, grid=180):
        yy, xx = np.ogrid[:grid, :grid]
        img = np.zeros((grid, grid))
        if cluster:
            centers = rng.uniform(0.25, 0.75, size=(3, 2)) * grid
            for _ in range(n_particles):
                c = centers[rng.integers(0, 3)]
                x = c[0] + rng.normal(0, 10)
                y = c[1] + rng.normal(0, 10)
                r = rng.uniform(*size_range)
                amp = rng.uniform(0.55, 0.9)
                img += amp * np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * r * r))
        else:
            for _ in range(n_particles):
                x = rng.uniform(0, grid)
                y = rng.uniform(0, grid)
                r = rng.uniform(*size_range)
                amp = rng.uniform(0.45, 0.75)
                img += amp * np.exp(-((xx - x) ** 2 + (yy - y) ** 2) / (2 * r * r))
        img += rng.normal(0, 0.025, img.shape)
        return np.clip(img, 0, 1)

    sem_ctrl = _sem_plate(70, (2.5, 4.5), cluster=False)
    sem_mod = _sem_plate(28, (7.0, 13.0), cluster=True)

    # ── Quantitative summary values ──
    ftir_peaks = ["915 oxirane", "1730 C=O", "1240 C-O-C"]
    ftir_area_uncured = [1.00, 1.00, 1.00]
    ftir_area_cured = [0.08, 1.05, 1.02]  # 915 nearly gone, others stable
    omega_1hz = 6.2832
    rheo_gstar_1hz = [float(850.0 * omega_1hz ** 0.55), float(3600.0 * omega_1hz ** 0.42)]
    rheo_delta_1hz = [float(np.clip(90 - 11 * np.log10(omega_1hz / 0.1), 52, 90)),
                      float(np.clip(80 - 32 * np.log10(omega_1hz / 0.1), 18, 88))]
    rheo_rutting = [g / np.sin(np.deg2rad(d)) for g, d in zip(rheo_gstar_1hz, rheo_delta_1hz)]

    # ── Save CSVs ──
    comment_ftir = (
        "Review FTIR triptych: transmittance with Gaussian peak valleys anchored to\n"
        "documented functional groups: 3400 (-OH), 2920/2850 (CH2), 1730 (C=O ester),\n"
        "1600 (aromatic C=C), 1240 (C-O-C ether), 915 (oxirane). Uncured keeps the\n"
        "915 oxirane peak; cured loses it (epoxy ring opened) and -OH grows.\n"
        "Tier: measured. Synthetic Gaussian-broadened, not a real scan."
    )
    _save_csv(
        data_dir / f"{name}_ftir.csv",
        ["wavenumber_cm-1", "transmittance_pct_uncured", "transmittance_pct_cured"],
        [[float(w), float(u), float(c)] for w, u, c in zip(wavenumber, ftir_uncured, ftir_cured)],
        comment=comment_ftir,
    )

    comment_rheo = (
        "Review rheology triptych: frequency sweep 0.1-100 rad/s. Complex modulus\n"
        "G* (Pa, log) rises as a power law; phase angle delta (deg) drops from\n"
        "viscous (~90) toward elastic (~30) for WER-modified binder. Tier: measured.\n"
        "Values bounded by typical WER-EA modified binder ranges, not direct measurements."
    )
    _save_csv(
        data_dir / f"{name}_rheology.csv",
        ["frequency_rad_s", "Gstar_Pa_control", "Gstar_Pa_modified",
         "delta_deg_control", "delta_deg_modified"],
        [[float(f), float(gc), float(gm), float(dc), float(dm)]
         for f, gc, gm, dc, dm in zip(freq, gstar_ctrl, gstar_mod, delta_ctrl, delta_mod)],
        comment=comment_rheo,
    )

    comment_sem = (
        "Review SEM triptych: simulated morphology plates (numpy, not real\n"
        "micrographs). Control = small uniform droplets (d50 1.2 um, continuous\n"
        "phase); WER modified = larger clustered dispersed phase (d50 3.5 um).\n"
        "Tier: inferred (morphology simulated, sizes typical of fluorescence/SEM\n"
        "reports). d50 and phase ratio are reviewer-anchored representative values."
    )
    _save_csv(
        data_dir / f"{name}_sem.csv",
        ["sample", "d50_um", "phase_state", "evidence_tier"],
        [["Control (uncured)", 1.2, "continuous", "inferred"],
         ["WER modified", 3.5, "dispersed", "inferred"]],
        comment=comment_sem,
    )

    comment_summary = (
        "Review triptych quantitative summary: FTIR peak areas (uncured vs cured,\n"
        "normalised), SEM d50 and dispersed fraction, rheology feature values at\n"
        "1 Hz (G*, delta, rutting factor G*/sin delta). Tier: measured (FTIR,\n"
        "rheology) and inferred (SEM morphology). Values are representative, not\n"
        "direct measurements."
    )
    _save_csv(
        data_dir / f"{name}_summary.csv",
        ["metric", "control_uncured", "modified_cured", "evidence_tier"],
        [["FTIR 915 oxirane area", 1.00, 0.08, "measured"],
         ["FTIR 1730 C=O area", 1.00, 1.05, "measured"],
         ["FTIR 1240 C-O-C area", 1.00, 1.02, "measured"],
         ["SEM d50 (um)", 1.2, 3.5, "inferred"],
         ["SEM dispersed fraction (%)", 15.0, 62.0, "inferred"],
         ["G* at 1 Hz (Pa)", rheo_gstar_1hz[0], rheo_gstar_1hz[1], "measured"],
         ["delta at 1 Hz (deg)", rheo_delta_1hz[0], rheo_delta_1hz[1], "measured"],
         ["G*/sin delta at 1 Hz (Pa)", rheo_rutting[0], rheo_rutting[1], "measured"]],
        comment=comment_summary,
    )

    # ── Plot: 3x3 triptych (Pattern 14) ──
    apply_pub_style({
        "axes.titlesize": 10, "axes.labelsize": 9,
        "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 7,
    })
    fig = plt.figure(figsize=(11.8, 9.6))
    gs = fig.add_gridspec(3, 3, height_ratios=[0.42, 1.35, 0.88],
                          hspace=0.48, wspace=0.38,
                          left=0.07, right=0.95, top=0.93, bottom=0.07)

    # ── Top row: shared evidence-tier legend strip (span 3 cols) ──
    ax_leg = fig.add_subplot(gs[0, :])
    ax_leg.axis("off")
    ax_leg.set_xlim(0, 1)
    ax_leg.set_ylim(0, 1)
    swatch_w = 0.075
    gap = 0.028
    n_tiers = len(EVIDENCE_TIER_ORDER)
    total_w = n_tiers * swatch_w + (n_tiers - 1) * gap
    x0 = (1 - total_w) / 2
    for i, t in enumerate(EVIDENCE_TIER_ORDER):
        x = x0 + i * (swatch_w + gap)
        ax_leg.add_patch(Rectangle((x, 0.42), swatch_w, 0.38,
                                   facecolor=EVIDENCE_TIER_COLORS[t],
                                   edgecolor="#333333", linewidth=0.6))
        ax_leg.text(x + swatch_w / 2, 0.26, t, ha="center", va="center",
                    fontsize=8, color="#333333")
    ax_leg.text(0.5, 0.90, "Evidence tiers", ha="center", va="center",
                fontsize=9, fontweight="bold")

    # ── Mid row, col 1: FTIR spectra ──
    ax_ftir = fig.add_subplot(gs[1, 0])
    ax_ftir.plot(wavenumber, ftir_uncured, color=PALETTE_CBM["control"], lw=1.3,
                 label="Uncured (oxirane present)")
    ax_ftir.plot(wavenumber, ftir_cured, color=PALETTE_CBM["modified"], lw=1.3,
                 label="Cured (oxirane consumed)")
    for wn, lbl in [(3400, "-OH"), (2920, "CH2"), (1730, "C=O"),
                    (1600, "C=C"), (1240, "C-O-C"), (915, "oxirane")]:
        ax_ftir.axvline(wn, color="#8C8C8C", lw=0.6, ls=":", alpha=0.7)
        ax_ftir.text(wn, 99, lbl, rotation=90, fontsize=6.5, color="#B85450",
                     va="top", ha="right")
    ax_ftir.invert_xaxis()
    ax_ftir.set_xlabel("Wavenumber (cm\u207B\u00B9)")
    ax_ftir.set_ylabel("Transmittance (%)")
    ax_ftir.set_title("(a) FTIR \u2014 functional groups [measured]")
    ax_ftir.set_ylim(0, 105)
    ax_ftir.legend(loc="lower left", fontsize=6.5, frameon=True, framealpha=0.9,
                   edgecolor="#CCCCCC")
    ax_ftir.grid(color="#E8E2D6", linewidth=0.6, alpha=0.6)

    # ── Mid row, col 2: SEM morphology (2 stacked dark plates) ──
    sem_gs = GridSpecFromSubplotSpec(2, 1, subplot_spec=gs[1, 1], hspace=0.22)
    ax_sem_top = fig.add_subplot(sem_gs[0, 0])
    ax_sem_bot = fig.add_subplot(sem_gs[1, 0])
    for ax_s, img, title, d50 in [
        (ax_sem_top, sem_ctrl, "Control \u2014 continuous", 1.2),
        (ax_sem_bot, sem_mod, "WER modified \u2014 dispersed", 3.5),
    ]:
        ax_s.imshow(img, cmap="gray", vmin=0, vmax=0.9, aspect="equal")
        ax_s.set_facecolor("black")
        ax_s.set_xticks([])
        ax_s.set_yticks([])
        # scale bar (10 um) bottom-right
        bar_len = 0.25
        x_bar = 0.70
        ax_s.plot([x_bar, x_bar + bar_len], [0.92, 0.92], color="white", lw=2,
                  transform=ax_s.transAxes)
        ax_s.text(x_bar + bar_len / 2, 0.955, "10 \u03BCm", color="white",
                  fontsize=6.5, ha="center", va="bottom", transform=ax_s.transAxes)
        ax_s.text(0.03, 0.92, f"{title}\nd\u2085\u2080 = {d50:.1f} \u03BCm",
                  color="white", fontsize=7, ha="left", va="top",
                  transform=ax_s.transAxes)
    ax_sem_top.set_title("(b) SEM morphology [inferred]")

    # ── Mid row, col 3: Rheology frequency sweep (dual y) ──
    from matplotlib.ticker import FuncFormatter
    ax_rheo = fig.add_subplot(gs[1, 2])
    ax_rheo.set_xscale("log")
    ax_rheo.set_yscale("log")
    # plain-text tick labels (avoid mathtext 10^n tspan splitting)
    _log_fmt = FuncFormatter(lambda x, _: f"{x:g}")
    ax_rheo.xaxis.set_major_formatter(_log_fmt)
    ax_rheo.yaxis.set_major_formatter(_log_fmt)
    ax_rheo.plot(freq, gstar_ctrl, color=PALETTE_CBM["control"], lw=1.4,
                 label="G* control")
    ax_rheo.plot(freq, gstar_mod, color=PALETTE_CBM["modified"], lw=1.4,
                 label="G* WER modified")
    ax_rheo.set_xlabel("Frequency (rad/s)")
    ax_rheo.set_ylabel("Complex modulus G* (Pa)", color=PALETTE_CBM["control"])
    ax_rheo.tick_params(axis="y", labelcolor=PALETTE_CBM["control"])
    ax_delta = ax_rheo.twinx()
    ax_delta.plot(freq, delta_ctrl, color=PALETTE_CBM["control"], lw=1.2,
                  ls="--", label="\u03B4 control")
    ax_delta.plot(freq, delta_mod, color=PALETTE_CBM["modified"], lw=1.2,
                  ls="--", label="\u03B4 WER modified")
    ax_delta.set_ylabel("Phase angle \u03B4 (\u00B0)", color=PALETTE_CBM["modified"])
    ax_delta.tick_params(axis="y", labelcolor=PALETTE_CBM["modified"])
    ax_delta.set_ylim(10, 95)
    # 1 Hz reference line (omega = 2*pi)
    ax_rheo.axvline(omega_1hz, color="#8C8C8C", lw=0.6, ls=":", alpha=0.7)
    trans = blended_transform_factory(ax_rheo.transData, ax_rheo.transAxes)
    ax_rheo.text(omega_1hz, 0.03, "1 Hz", transform=trans, fontsize=6.5,
                 color="#555555", ha="center", va="bottom")
    ax_rheo.set_title("(c) Rheology \u2014 frequency sweep [measured]")
    h1, l1 = ax_rheo.get_legend_handles_labels()
    h2, l2 = ax_delta.get_legend_handles_labels()
    ax_rheo.legend(h1 + h2, l1 + l2, loc="lower left", fontsize=6.5, frameon=True,
                   framealpha=0.9, edgecolor="#CCCCCC")
    ax_rheo.grid(color="#E8E2D6", linewidth=0.6, alpha=0.6, which="both")

    # ── Bottom row: quantitative summary bars ──
    w = 0.36
    # col 1: FTIR peak areas (normalised)
    ax_b1 = fig.add_subplot(gs[2, 0])
    x_pos = np.arange(len(ftir_peaks))
    ax_b1.bar(x_pos - w / 2, ftir_area_uncured, w, color=PALETTE_CBM["control"],
              edgecolor=_tier_color("measured"), linewidth=1.0, label="Uncured")
    ax_b1.bar(x_pos + w / 2, ftir_area_cured, w, color=PALETTE_CBM["modified"],
              edgecolor=_tier_color("measured"), linewidth=1.0, label="Cured")
    ax_b1.set_xticks(x_pos)
    ax_b1.set_xticklabels(["915\noxirane", "1730\nC=O", "1240\nC-O-C"], fontsize=7)
    ax_b1.set_ylabel("Peak area (norm.)")
    ax_b1.set_title("(d) FTIR peak areas [measured]")
    ax_b1.legend(fontsize=6.5, loc="upper right")
    ax_b1.grid(axis="y", color="#E8E2D6", linewidth=0.6, alpha=0.6)
    ax_b1.annotate("915 consumed", xy=(0 + w / 2, 0.08), xytext=(0.9, 0.6),
                   fontsize=6.5, color="#B85450",
                   arrowprops=dict(arrowstyle="->", color="#B85450", lw=0.8))

    # col 2: SEM d50 + dispersed fraction
    ax_b2 = fig.add_subplot(gs[2, 1])
    bar_labels2 = ["d50 (\u03BCm)", "dispersed\nfraction (%)"]
    ctrl_vals2 = [1.2, 15.0]
    mod_vals2 = [3.5, 62.0]
    x_pos2 = np.arange(len(bar_labels2))
    ax_b2.bar(x_pos2 - w / 2, ctrl_vals2, w, color=PALETTE_CBM["control"],
              edgecolor=_tier_color("inferred"), linewidth=1.0, label="Control")
    ax_b2.bar(x_pos2 + w / 2, mod_vals2, w, color=PALETTE_CBM["modified"],
              edgecolor=_tier_color("inferred"), linewidth=1.0, label="WER modified")
    ax_b2.set_xticks(x_pos2)
    ax_b2.set_xticklabels(bar_labels2, fontsize=7)
    ax_b2.set_ylabel("Value")
    ax_b2.set_title("(e) SEM morphology metrics [inferred]")
    ax_b2.legend(fontsize=6.5, loc="upper left")
    ax_b2.grid(axis="y", color="#E8E2D6", linewidth=0.6, alpha=0.6)

    # col 3: rheology feature values at 1 Hz (normalised to control)
    ax_b3 = fig.add_subplot(gs[2, 2])
    rheo_labels3 = ["G* @1Hz", "\u03B4 @1Hz", "G*/sin\u03B4\n@1Hz"]
    rheo_ctrl_norm = [1.0, 1.0, 1.0]
    rheo_mod_norm = [rheo_gstar_1hz[1] / rheo_gstar_1hz[0],
                     rheo_delta_1hz[1] / rheo_delta_1hz[0],
                     rheo_rutting[1] / rheo_rutting[0]]
    x_pos3 = np.arange(len(rheo_labels3))
    ax_b3.bar(x_pos3 - w / 2, rheo_ctrl_norm, w, color=PALETTE_CBM["control"],
              edgecolor=_tier_color("measured"), linewidth=1.0, label="Control")
    ax_b3.bar(x_pos3 + w / 2, rheo_mod_norm, w, color=PALETTE_CBM["modified"],
              edgecolor=_tier_color("measured"), linewidth=1.0, label="WER modified")
    ax_b3.set_xticks(x_pos3)
    ax_b3.set_xticklabels(rheo_labels3, fontsize=7)
    ax_b3.set_ylabel("Relative to control (\u00D7)")
    ax_b3.set_title("(f) Rheology @1 Hz [measured]")
    ax_b3.legend(fontsize=6.5, loc="upper left")
    ax_b3.grid(axis="y", color="#E8E2D6", linewidth=0.6, alpha=0.6)
    for i, mv in enumerate(rheo_mod_norm):
        ax_b3.text(i + w / 2, mv + 0.12, f"{mv:.2f}\u00D7", ha="center", va="bottom",
                   fontsize=6.5, color=PALETTE_CBM["modified"])

    fig.suptitle("FTIR \u2014 SEM \u2014 Rheology evidence triptych (WER-EA, tiered)",
                 fontsize=12, y=0.985)
    finalize_figure(fig, name, output_dir=str(output_dir))
    _print_claim_boundary(
        name,
        "FTIR peaks anchored to documented functional group wavenumbers; "
        "SEM textures are simulated representations; rheological values reflect "
        "typical WER-EA modified binder ranges, not direct measurements.",
    )
    return name


def _review_durability_retention_challenge_map(output_dir: Path, data_dir: Path) -> str:
    name = "durability_retention_challenge_map"
    # Review dimension: durability by challenge category, tiered. Water/aging are
    # measured; freeze-thaw is inferred; heat/traffic are speculative/missing.
    # Orthogonal to rich-gallery/moisture_aging_retention (time series).
    challenges = ["Water", "Aging", "Freeze-thaw", "Heat", "Traffic"]
    control = [62, 58, 45, 55, 0]      # traffic = missing (no data)
    modified = [85, 80, 72, 78, 0]
    tiers = ["measured", "measured", "inferred", "speculative", "missing"]

    comment = (
        "Review dimension: durability retention by challenge category. Water and\n"
        "aging are measured (lab tests); freeze-thaw is inferred (limited cycles);\n"
        "heat is speculative (single-condition); traffic is missing (no field data).\n"
        "Orthogonal to rich-gallery/moisture_aging_retention (time series). Values\n"
        "synthetic, bounded by reported WER-EA durability ranges; 0 = no data."
    )
    _save_csv(
        data_dir / f"{name}.csv",
        ["challenge", "control_retention_pct", "modified_retention_pct", "evidence_tier"],
        [[c, float(ct), float(m), t] for c, ct, m, t in zip(challenges, control, modified, tiers)],
        comment=comment,
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    x = np.arange(len(challenges))
    width = 0.38
    # for missing tier, draw a hatched placeholder instead of a value bar
    ctrl_bars = []
    mod_bars = []
    for i, (c, m, t) in enumerate(zip(control, modified, tiers)):
        if t == "missing":
            ax.bar(x[i] - width / 2, 50, width, color="none", edgecolor=_tier_color(t),
                   hatch="//", linewidth=0.7)
            ax.bar(x[i] + width / 2, 50, width, color="none", edgecolor=_tier_color(t),
                   hatch="//", linewidth=0.7)
            ax.text(x[i], 52, "no data", ha="center", fontsize=7, color="#555555")
        else:
            ax.bar(x[i] - width / 2, c, width, color=PALETTE_CBM["control"],
                   edgecolor=_tier_color(t), linewidth=1.2)
            ax.bar(x[i] + width / 2, m, width, color=PALETTE_CBM["modified"],
                   edgecolor=_tier_color(t), linewidth=1.2)
    ax.set_ylabel("Retention (%)")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{c}\n[{t}]" for c, t in zip(challenges, tiers)], fontsize=8)
    # colour x-tick labels by tier
    for tick, t in zip(ax.get_xticklabels(), tiers):
        tick.set_color(_tier_color(t))
    ax.set_ylim(0, 105)
    ax.axhline(70, color=PALETTE_CBM["accent"], linestyle="--", linewidth=1, label="70% acceptance")
    ax.set_title("Durability retention challenge map (tiered)")
    # custom legend for control/modified + evidence tier (two legends on one axis)
    handles = [Rectangle((0, 0), 1, 1, color=PALETTE_CBM["control"], label="Control"),
               Rectangle((0, 0), 1, 1, color=PALETTE_CBM["modified"], label="WER modified")]
    leg1 = ax.legend(handles=handles, loc="upper left", fontsize=7, frameon=True,
                     framealpha=0.9, edgecolor="#CCCCCC")
    ax.add_artist(leg1)
    _add_evidence_tier_legend(ax, loc="upper right", fontsize=7)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: WER modification raises water/aging retention above 70%; traffic "
        "durability is unmeasured. Boundary: water/aging measured; freeze-thaw/heat "
        "inferred/speculative; traffic is missing, shown as no-data, not a negative "
        "result.",
    )
    return name


def _review_research_gap_matrix(output_dir: Path, data_dir: Path) -> str:
    name = "research_gap_matrix"
    # Review dimension: research gap. Topics plotted by evidence maturity (x) and
    # research importance (y); bubble size = gap; colour = evidence tier.
    # Long-term and field evidence are missing; mechanism is inferred.
    topics = ["Lab evidence", "Field evidence", "Mechanism", "Standards", "Long-term"]
    maturity = [0.85, 0.30, 0.55, 0.40, 0.20]
    importance = [0.70, 0.92, 0.85, 0.75, 0.95]
    tiers = ["measured", "missing", "inferred", "inferred", "missing"]
    gap = [i - m for i, m in zip(importance, maturity)]

    comment = (
        "Review dimension: research gap matrix for WER-EA. Lab evidence is measured\n"
        "and mature; field evidence and long-term durability are missing (no data);\n"
        "mechanism and standards are inferred. Bubble size = gap (importance -\n"
        "maturity). Maturity/importance are reviewer judgement."
    )
    _save_csv(
        data_dir / f"{name}.csv",
        ["topic", "maturity", "importance", "gap", "evidence_tier"],
        [[t, float(m), float(i), float(g), tp]
         for t, m, i, g, tp in zip(topics, maturity, importance, gap, tiers)],
        comment=comment,
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    for t, m, i, g, tp in zip(topics, maturity, importance, gap, tiers):
        ax.scatter(m, i, s=[max(g, 0.05) * 2400], color=_tier_color(tp), alpha=0.78,
                   edgecolors="#333333", linewidth=0.7)
        ax.annotate(t, (m, i), textcoords="offset points", xytext=(7, 6), fontsize=8)
    ax.plot([0, 1], [0, 1], "k--", linewidth=1, alpha=0.5, label="maturity = importance")
    ax.set_xlabel("Evidence maturity")
    ax.set_ylabel("Research importance")
    ax.set_xlim(0, 1)
    ax.set_ylim(0.2, 1.05)
    ax.set_title("Research gap matrix (tiered)")
    ax.grid(color="#E8E2D6", linewidth=0.7, alpha=0.7)
    _add_evidence_tier_legend(ax, loc="lower right", fontsize=7)
    ax.text(0.04, 0.96, "bubble size = gap (importance - maturity)",
            transform=ax.transAxes, fontsize=7, va="top", color="#555555")
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: the largest gaps are long-term durability and field evidence, both "
        "missing. Boundary: maturity/importance are reviewer judgement; missing "
        "tier marks absence of data, not negative results.",
    )
    return name


def _review_graphical_abstract_review(output_dir: Path, data_dir: Path) -> str:
    name = "graphical_abstract_review"
    # Review dimension: graphical abstract / summary. WER-EA paper count and
    # identified gaps over years. Bars are measured (literature count); the gap
    # projection to 2025 is speculative (dashed).
    years = np.array([2018, 2019, 2020, 2021, 2022, 2023, 2024])
    papers = np.array([12, 18, 25, 34, 45, 58, 72])
    gaps = np.array([5, 6, 8, 10, 12, 15, 18])
    # speculative projection
    years_proj = np.array([2024, 2025])
    gaps_proj = np.array([18, 22])

    comment = (
        "Review dimension: graphical abstract for a WER-EA mini-review. Paper count\n"
        "and identified gaps per year (measured from literature search). The 2025\n"
        "gap projection is speculative (dashed). Counts are illustrative of a\n"
        "growing field; not a full systematic-review tally."
    )
    _save_csv(
        data_dir / f"{name}.csv",
        ["year", "papers_published", "identified_gaps"],
        [[int(y), int(p), int(g)] for y, p, g in zip(years, papers, gaps)],
        comment=comment,
    )

    apply_pub_style()
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.bar(years, papers, color=PALETTE_CBM["control"], alpha=0.85, label="Papers (measured)")
    ax.plot(years, gaps, "o-", color=PALETTE_CBM["danger"], linewidth=2, markersize=6,
            label="Identified gaps (measured)")
    ax.plot(years_proj, gaps_proj, "o--", color=PALETTE_CBM["modified"], linewidth=2,
            markersize=6, label="Gap projection (speculative)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    ax.set_title("Graphical abstract for review (WER-EA literature trend)")
    ax.legend(fontsize=8)
    ax.grid(axis="y", color="#E8E2D6", linewidth=0.7, alpha=0.7)
    fig.tight_layout()
    finalize_figure(fig, name, output_dir=str(output_dir))
    plt.close(fig)
    _print_claim_boundary(
        name,
        "Claim: WER-EA literature and identified gaps are growing; the 2025 gap "
        "projection is speculative. Boundary: counts are illustrative, not a "
        "systematic-review tally; projection assumes linear growth.",
    )
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

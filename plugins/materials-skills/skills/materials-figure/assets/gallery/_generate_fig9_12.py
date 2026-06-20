"""Generate gallery entries 9-12 (added in materials-figure upgrade)."""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

PALETTE = {
    "primary": "#3775BA",
    "secondary": "#7AA6D4",
    "accent": "#E07C3E",
    "neutral": "#4D4D4D",
    "highlight": "#B64342",
    "fill": "#C49A6C",
    "green": "#2E9E44",
}

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "DejaVu Sans", "Liberation Sans"],
    "font.size": 14,
    "svg.fonttype": "none",
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 1.8,
    "legend.frameon": False,
})

OUT = Path(__file__).resolve().parent


def _save(fig, base):
    fig.tight_layout()
    fig.savefig(base.with_suffix(".png"), dpi=300)
    fig.savefig(base.with_suffix(".svg"))
    plt.close(fig)


def _panel_label(ax, label):
    ax.text(-0.10, 1.02, label, transform=ax.transAxes, fontsize=18, fontweight="bold")


def fig9_xrd_sem_perf() -> None:
    fig = plt.figure(figsize=(13, 9))
    gs = fig.add_gridspec(2, 2, hspace=0.35, wspace=0.30)
    ax1 = fig.add_subplot(gs[0, 0])
    two_theta = np.linspace(20, 80, 300)
    peaks = np.zeros_like(two_theta)
    for c, w, h in [(28.4, 0.4, 1.0), (47.3, 0.5, 0.6), (56.1, 0.5, 0.4), (69.1, 0.6, 0.5)]:
        peaks += h * np.exp(-0.5 * ((two_theta - c) / w) ** 2)
    ax1.plot(two_theta, peaks, color=PALETTE["primary"], lw=2)
    ax1.fill_between(two_theta, 0, peaks, color=PALETTE["secondary"], alpha=0.4)
    ax1.set_xlabel("2\u03b8 (\u00b0)")
    ax1.set_ylabel("Intensity (a.u.)")
    _panel_label(ax1, "a")

    ax2 = fig.add_subplot(gs[0, 1])
    rng = np.random.default_rng(11)
    yy, xx = np.mgrid[0:64, 0:64]
    image = np.exp(-((xx - 32) ** 2 + (yy - 32) ** 2) / 200) + rng.normal(0, 0.05, xx.shape)
    ax2.imshow(image, cmap="gray", extent=[0, 5, 0, 5])
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax2.set_facecolor("black")
    _panel_label(ax2, "b")
    ax2.text(2.5, -0.10, "SEM (5 \u00b5m scale bar)", ha="center", transform=ax2.transAxes, fontsize=10)

    ax3 = fig.add_subplot(gs[1, :])
    materials = ["Reference", "+ 0.5 wt%", "+ 1.0 wt%", "+ 2.0 wt%"]
    values = [62, 68, 74, 71]
    errors = [2, 2, 2.5, 2.5]
    bars = ax3.bar(materials, values, yerr=errors, color=PALETTE["accent"],
                   edgecolor="black", linewidth=1.5, capsize=6)
    ax3.set_ylabel("Compressive strength (MPa)")
    ax3.set_ylim(0, 90)
    for bar, v in zip(bars, values):
        ax3.text(bar.get_x() + bar.get_width() / 2, v + 1, f"{v}", ha="center", fontsize=11)
    _panel_label(ax3, "c")
    _save(fig, OUT / "fig9-multipanel-xrd-sem-perf")


def fig10_ftir_tg_morph() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.5))
    wn = np.linspace(4000, 400, 200)
    spec = (np.exp(-0.5 * ((wn - 3400) / 100) ** 2) * 0.6
            + np.exp(-0.5 * ((wn - 1620) / 30) ** 2) * 0.4
            + np.exp(-0.5 * ((wn - 1100) / 80) ** 2) * 0.7)
    axes[0].plot(wn, spec, color=PALETTE["primary"], lw=2)
    axes[0].invert_xaxis()
    axes[0].set_xlabel("Wavenumber (cm\u207b\u00b9)")
    axes[0].set_ylabel("Absorbance (a.u.)")
    _panel_label(axes[0], "a")

    t = np.linspace(50, 800, 200)
    tg = 100 - 100 / (1 + np.exp(-(t - 400) / 25))
    axes[1].plot(t, tg, color=PALETTE["accent"], lw=2.2)
    axes[1].set_xlabel("Temperature (\u00b0C)")
    axes[1].set_ylabel("Mass (%)")
    _panel_label(axes[1], "b")

    rng = np.random.default_rng(3)
    yy, xx = np.mgrid[0:48, 0:48]
    blob = (np.exp(-((xx - 24) ** 2 + (yy - 24) ** 2) / 80)
            + np.exp(-((xx - 35) ** 2 + (yy - 15) ** 2) / 40))
    axes[2].imshow(blob + rng.normal(0, 0.05, xx.shape), cmap="magma", extent=[0, 2, 0, 2])
    axes[2].set_xticks([])
    axes[2].set_yticks([])
    _panel_label(axes[2], "c")
    axes[2].text(1, -0.12, "AFM phase (2 \u00b5m scale)", ha="center", transform=axes[2].transAxes, fontsize=10)
    _save(fig, OUT / "fig10-multipanel-ftir-tg-morph")


def fig11_graphical_abstract() -> None:
    fig, ax = plt.subplots(figsize=(10, 5))
    blocks = [
        (0.08, 0.6, "Bitumen", PALETTE["neutral"]),
        (0.30, 0.6, "+ Epoxy resin", PALETTE["secondary"]),
        (0.55, 0.6, "Network IPN", PALETTE["primary"]),
        (0.80, 0.6, "\u2191 28 %\nrutting\nresistance", PALETTE["accent"]),
        (0.30, 0.20, "Compatibility\nwindow\n0.5\u20131.5 wt%", PALETTE["fill"]),
        (0.55, 0.20, "Storage\nstability\nmonitored", PALETTE["fill"]),
    ]
    for x, y, label, c in blocks:
        rect = mpatches.FancyBboxPatch(
            (x - 0.085, y - 0.07), 0.17, 0.14,
            boxstyle="round,pad=0.01", facecolor=c, edgecolor="black", linewidth=1.5,
        )
        ax.add_patch(rect)
        ax.text(x, y, label, ha="center", va="center", fontsize=10,
                color="white" if c not in (PALETTE["fill"], PALETTE["secondary"]) else "black",
                fontweight="bold")
    for x1, x2 in [(0.165, 0.215), (0.385, 0.465), (0.635, 0.715)]:
        ax.annotate("", xy=(x2, 0.6), xytext=(x1, 0.6),
                    arrowprops=dict(arrowstyle="->", lw=2, color=PALETTE["neutral"]))
    ax.annotate("", xy=(0.30, 0.27), xytext=(0.30, 0.53),
                arrowprops=dict(arrowstyle="->", lw=1.5, color=PALETTE["neutral"], ls="--"))
    ax.annotate("", xy=(0.55, 0.27), xytext=(0.55, 0.53),
                arrowprops=dict(arrowstyle="->", lw=1.5, color=PALETTE["neutral"], ls="--"))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.95)
    ax.axis("off")
    _save(fig, OUT / "fig11-graphical-abstract")


def fig12_evidence_chain() -> None:
    """Evidence chain tying figure-handoff -> reader-package -> claim."""
    fig, ax = plt.subplots(figsize=(12, 5))
    nodes = [
        (0.10, 0.6, "Citation\nmatrix", PALETTE["primary"]),
        (0.32, 0.6, "Reader\nextracts", PALETTE["secondary"]),
        (0.54, 0.6, "Figure\ncontract", PALETTE["accent"]),
        (0.76, 0.6, "Plot +\nQA", PALETTE["highlight"]),
        (0.32, 0.20, "Claim\nvalidation", PALETTE["fill"]),
        (0.54, 0.20, "KB\ncross-check", PALETTE["fill"]),
    ]
    for x, y, label, c in nodes:
        circ = plt.Circle((x, y), 0.06, color=c, alpha=0.9)
        ax.add_patch(circ)
        ax.text(x, y, label, ha="center", va="center", fontsize=9,
                color="white" if c != PALETTE["fill"] else "black", fontweight="bold")
    for x1, x2 in [(0.16, 0.26), (0.38, 0.48), (0.60, 0.70)]:
        ax.annotate("", xy=(x2, 0.6), xytext=(x1, 0.6),
                    arrowprops=dict(arrowstyle="->", lw=2, color=PALETTE["neutral"]))
    for x in [0.32, 0.54]:
        ax.annotate("", xy=(x, 0.26), xytext=(x, 0.54),
                    arrowprops=dict(arrowstyle="->", lw=1.5, color=PALETTE["neutral"], ls="--"))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.95)
    ax.axis("off")
    ax.set_title("Evidence chain: handoff -> claim validation", pad=15)
    _save(fig, OUT / "fig12-evidence-chain")


def main() -> None:
    fig9_xrd_sem_perf()
    fig10_ftir_tg_morph()
    fig11_graphical_abstract()
    fig12_evidence_chain()
    print("Generated 4 gallery entries.")


if __name__ == "__main__":
    main()

"""Generate chart-atlas entries 16-21 (added in materials-figure upgrade).

Run from skill root:
    python assets/chart-atlas/_generate_atlas_16_21.py

Outputs PNG (300 dpi) and SVG (editable text) for each new atlas entry.
"""
from __future__ import annotations

import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PALETTE = {
    "primary": "#3775BA",
    "secondary": "#7AA6D4",
    "accent": "#E07C3E",
    "neutral": "#4D4D4D",
    "highlight": "#B64342",
    "fill": "#C49A6C",
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
SIZES = (10, 6)


def _save(fig: plt.Figure, base: Path) -> None:
    fig.tight_layout()
    fig.savefig(base.with_suffix(".png"), dpi=300)
    fig.savefig(base.with_suffix(".svg"))
    plt.close(fig)


def atlas_16_pore_size() -> None:
    """BJH/BET pore-size distribution from a typical mesoporous silica."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=SIZES)
    rng = np.random.default_rng(42)
    diameter = np.linspace(0.5, 50, 200)  # nm
    # dual-peak distribution: mesopore at ~3.5 nm, macropore at ~30 nm
    peak1 = np.exp(-0.5 * ((diameter - 3.5) / 0.8) ** 2) * 0.8
    peak2 = np.exp(-0.5 * ((diameter - 28) / 6) ** 2) * 0.4
    dv_dlogd = peak1 + peak2 + rng.normal(0, 0.005, size=diameter.size)
    cumulative = np.cumsum(dv_dlogd) / np.sum(dv_dlogd) * 100

    ax1.semilogx(diameter, dv_dlogd, color=PALETTE["primary"], lw=2.2)
    ax1.fill_between(diameter, 0, dv_dlogd, color=PALETTE["secondary"], alpha=0.4)
    ax1.set_xlabel("Pore diameter (nm)")
    ax1.set_ylabel("dV/dlogD (cm\u00b3/g)")
    ax1.axvline(3.5, color=PALETTE["accent"], ls="--", lw=1, label="Mesopore peak")
    ax1.axvline(28, color=PALETTE["highlight"], ls="--", lw=1, label="Macropore peak")
    ax1.legend(loc="upper right")

    ax2.semilogx(diameter, cumulative, color=PALETTE["accent"], lw=2.2)
    ax2.set_xlabel("Pore diameter (nm)")
    ax2.set_ylabel("Cumulative pore volume (%)")
    ax2.set_ylim(0, 100)
    _save(fig, OUT / "atlas-16-pore-size-distribution")


def atlas_17_impedance() -> None:
    """Nyquist + Bode plot for a solid-electrolyte interface."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=SIZES)
    f = np.logspace(-1, 6, 80)
    r_s = 12
    r_ct = 240
    z_real = r_s + r_ct / (1 + (2 * math.pi * f * 1e-3) ** 2)
    z_imag = (r_ct * 2 * math.pi * f * 1e-3) / (1 + (2 * math.pi * f * 1e-3) ** 2)
    z_mag = np.sqrt(z_real**2 + z_imag**2)
    phase = np.degrees(np.arctan2(z_imag, z_real))

    ax1.plot(z_real, -z_imag, "o", color=PALETTE["primary"], ms=4, label="Data")
    ax1.plot(z_real, -z_imag, "-", color=PALETTE["secondary"], lw=1, alpha=0.7)
    ax1.set_xlabel("Z' (\u03a9)")
    ax1.set_ylabel("-Z'' (\u03a9)")
    ax1.set_aspect("equal")
    ax1.legend()

    ax2.semilogx(f, z_mag, color=PALETTE["primary"], lw=2, label="|Z|")
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("|Z| (\u03a9)", color=PALETTE["primary"])
    ax2.tick_params(axis="y", labelcolor=PALETTE["primary"])
    ax2b = ax2.twinx()
    ax2b.semilogx(f, -phase, color=PALETTE["accent"], lw=2, ls="--", label="-Phase")
    ax2b.set_ylabel("-Phase (\u00b0)", color=PALETTE["accent"])
    ax2b.tick_params(axis="y", labelcolor=PALETTE["accent"])
    _save(fig, OUT / "atlas-17-electrochemical-impedance")


def atlas_18_mercury_intrusion() -> None:
    """Cumulative + differential MIP curves for a hardened cement paste."""
    fig, ax1 = plt.subplots(figsize=SIZES)
    rng = np.random.default_rng(7)
    pressure = np.logspace(5, 9, 100)  # Pa
    cum_intrusion = 100 * (1 - np.exp(-np.linspace(0, 3, 100) ** 1.6))
    cum_intrusion += rng.normal(0, 0.2, size=100).cumsum() * 0.1
    d_cum = np.gradient(cum_intrusion, np.log10(pressure))

    ax1.semilogx(pressure, cum_intrusion, color=PALETTE["primary"], lw=2.2, label="Cumulative")
    ax1.set_xlabel("Pressure (Pa)")
    ax1.set_ylabel("Cumulative intrusion (mL/g)", color=PALETTE["primary"])
    ax1.tick_params(axis="y", labelcolor=PALETTE["primary"])
    ax1b = ax1.twinx()
    ax1b.semilogx(pressure, d_cum, color=PALETTE["accent"], lw=1.8, label="Differential")
    ax1b.set_ylabel("dV/dlogP (mL/g)", color=PALETTE["accent"])
    ax1b.tick_params(axis="y", labelcolor=PALETTE["accent"])
    _save(fig, OUT / "atlas-18-mercury-intrusion")


def atlas_19_multiscale() -> None:
    """Four-scale architecture diagram: atom -> nano -> micro -> macro."""
    fig, ax = plt.subplots(figsize=(11, 5.5))
    scales = [
        ("Atom", 0.05, 0.5, "Au(111) lattice"),
        ("Nano", 0.30, 0.5, "Au nanoparticle\nD = 8 nm"),
        ("Micro", 0.55, 0.5, "Mesoporous shell\nPore = 4 nm"),
        ("Macro", 0.83, 0.5, "Bulk monolith\n\u03c1 = 0.06 g/cm\u00b3"),
    ]
    for label, x, y, desc in scales:
        circ = plt.Circle((x, y), 0.085, color=PALETTE["primary"], alpha=0.85)
        ax.add_patch(circ)
        ax.text(x, y + 0.12, label, ha="center", fontsize=14, fontweight="bold")
        ax.text(x, y - 0.02, desc, ha="center", va="center", fontsize=9, color="white")
    for x1, x2 in [(0.135, 0.215), (0.385, 0.465), (0.635, 0.745)]:
        ax.annotate("", xy=(x2, 0.5), xytext=(x1, 0.5),
                    arrowprops=dict(arrowstyle="->", lw=2, color=PALETTE["neutral"]))
    scale_labels = ["~0.3 nm", "~10 nm", "~1 \u00b5m", "~1 cm"]
    for (_label, x, _y, _desc), slabel in zip(scales, scale_labels):
        ax.text(x, 0.30, slabel, ha="center", fontsize=10, color=PALETTE["neutral"])
    ax.set_xlim(-0.05, 1.0)
    ax.set_ylim(0.2, 0.8)
    ax.axis("off")
    ax.set_title("Multiscale architecture across four length scales", pad=15)
    _save(fig, OUT / "atlas-19-multiscale-architecture")


def atlas_20_mechanism_flow() -> None:
    """Mechanism flowchart for a WER-EA review."""
    fig, ax = plt.subplots(figsize=(11, 5.5))
    import matplotlib.patches as mpatches
    boxes = [
        ("Binder\nmodification", 0.10, 0.6, PALETTE["primary"]),
        ("Compatibilizer\n(epoxy/SBS)", 0.32, 0.6, PALETTE["secondary"]),
        ("Network\ninterpenetration", 0.55, 0.6, PALETTE["accent"]),
        ("Performance\n\u2191", 0.80, 0.6, PALETTE["highlight"]),
        ("Storage\nstability\u2193", 0.32, 0.18, PALETTE["fill"]),
        ("Cost\n\u2191", 0.55, 0.18, PALETTE["fill"]),
    ]
    for label, x, y, c in boxes:
        rect = mpatches.FancyBboxPatch(
            (x - 0.075, y - 0.05), 0.15, 0.10,
            boxstyle="round,pad=0.01", facecolor=c, edgecolor="black", linewidth=1.5,
        )
        ax.add_patch(rect)
        ax.text(x, y, label, ha="center", va="center", fontsize=10,
                color="white" if c != PALETTE["fill"] else "black", fontweight="bold")
    arrows = [
        (0.175, 0.6, 0.245, 0.6),
        (0.395, 0.6, 0.475, 0.6),
        (0.625, 0.6, 0.725, 0.6),
        (0.32, 0.55, 0.32, 0.23),
        (0.55, 0.55, 0.55, 0.23),
    ]
    for x1, y1, x2, y2 in arrows:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", lw=1.5, color=PALETTE["neutral"]))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 0.8)
    ax.axis("off")
    _save(fig, OUT / "atlas-20-mechanism-flowchart")


def atlas_21_graphical_abstract() -> None:
    """Schematic-style graphical abstract template."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    import matplotlib.patches as mpatches
    # left: challenge icon
    challenge = mpatches.Circle((0.12, 0.5), 0.08, color=PALETTE["highlight"], alpha=0.85)
    ax.add_patch(challenge)
    ax.text(0.12, 0.5, "?", ha="center", va="center", fontsize=22, color="white", fontweight="bold")
    ax.text(0.12, 0.28, "Challenge", ha="center", fontsize=11)
    # center: process arrow
    ax.annotate("", xy=(0.50, 0.5), xytext=(0.22, 0.5),
                arrowprops=dict(arrowstyle="->", lw=3, color=PALETTE["primary"]))
    ax.text(0.36, 0.62, "mechanism-driven\nmaterials design", ha="center", fontsize=10, color=PALETTE["primary"])
    # right: outcome icon
    outcome = mpatches.Rectangle((0.55, 0.42), 0.20, 0.16, color=PALETTE["primary"], alpha=0.85)
    ax.add_patch(outcome)
    ax.text(0.65, 0.5, "\u2191 35 %\nstrength", ha="center", va="center", fontsize=11, color="white", fontweight="bold")
    ax.text(0.65, 0.28, "Outcome", ha="center", fontsize=11)
    ax.text(0.50, 0.85, "Graphical abstract template", ha="center", fontsize=14, fontweight="bold")
    ax.set_xlim(0, 1)
    ax.set_ylim(0.2, 0.9)
    ax.axis("off")
    _save(fig, OUT / "atlas-21-graphical-abstract")


METADATA = {
    16: dict(name="atlas-16-pore-size-distribution", family="thermal-insulation",
             chart_type="distribution+semilog", kb_refs=["Thermal conductivity aerogel (W/mK)"]),
    17: dict(name="atlas-17-electrochemical-impedance", family="functional",
             chart_type="nyquist+bode", kb_refs=["Resistivity semiconductor (\u03a9\u00b7cm)"]),
    18: dict(name="atlas-18-mercury-intrusion", family="civil",
             chart_type="log-scale twin axis", kb_refs=["Concrete 28d compressive strength (MPa)"]),
    19: dict(name="atlas-19-multiscale-architecture", family="all",
             chart_type="schematic", kb_refs=[]),
    20: dict(name="atlas-20-mechanism-flowchart", family="civil",
             chart_type="flowchart", kb_refs=["Asphalt DSR G*/sin \u03b4 @ 64\u00b0C (kPa)"]),
    21: dict(name="atlas-21-graphical-abstract", family="all",
             chart_type="graphical abstract", kb_refs=[]),
}


def write_metadata() -> None:
    import yaml
    for n, meta in METADATA.items():
        path = OUT / f"{meta['name']}-metadata.yaml"
        with path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(
                {
                    "atlas_id": n,
                    "name": meta["name"],
                    "family": meta["family"],
                    "chart_type": meta["chart_type"],
                    "kb_validation_refs": meta["kb_refs"],
                    "qa_gates": ["editable_svg_text", "300_dpi", "no_default_seaborn_palette"],
                },
                f,
                sort_keys=False,
                allow_unicode=True,
            )


def main() -> None:
    atlas_16_pore_size()
    atlas_17_impedance()
    atlas_18_mercury_intrusion()
    atlas_19_multiscale()
    atlas_20_mechanism_flow()
    atlas_21_graphical_abstract()
    write_metadata()
    print("Generated 6 chart-atlas entries + metadata.")


if __name__ == "__main__":
    main()

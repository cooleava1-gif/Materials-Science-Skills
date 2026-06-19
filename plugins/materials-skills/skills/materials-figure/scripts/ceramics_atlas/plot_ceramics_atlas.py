#!/usr/bin/env python3
"""Generate the Ceramics Figure Atlas — literature-anchored data-driven figures.

Figures: sintering, XRD, Weibull, conductivity, grain size, EIS, TGA/DSC,
stress-strain, thermal expansion. All driven by CSV data in
assets/ceramics-atlas/data/. Uses materials_plot_lib for publication style.
"""

import csv
import sys
from pathlib import Path

import numpy as np

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Make materials_plot_lib importable
HERE = Path(__file__).resolve().parent.parent.parent  # skills/materials-figure/
sys.path.insert(0, str(HERE / "scripts"))
from materials_plot_lib import apply_pub_style, PALETTE_CERAMIC  # noqa: E402

apply_pub_style()  # sets svg.fonttype='none', Arial, spines off, etc.

DATA = HERE / "assets" / "ceramics-atlas" / "data"
OUT = HERE / "assets" / "ceramics-atlas" / "generated"
OUT.mkdir(parents=True, exist_ok=True)

PAL = PALETTE_CERAMIC
# series colors for multi-material plots
C_AL = PAL["mechanical"]   # Al2O3
C_ZR = PAL["modified"]     # 3Y-TZP / ZrO2
C_SIC = PAL["optimal"]     # SiC
C_REF = PAL["neutral"]     # reference
C_YSZ = PAL["thermal"]     # 8YSZ

# mathtext labels (avoid Unicode subscript glyphs missing from Arial)
AL2O3 = r"$\mathrm{Al_2O_3}$"
ZRO2 = r"$\mathrm{ZrO_2}$"
SIG0 = r"$\sigma_0$"


def _read_csv(path):
    """Read CSV, skipping # comment header lines."""
    rows = []
    with open(path, newline="") as f:
        for line in f:
            if line.startswith("#"):
                continue
            rows.append(line)
    return list(csv.DictReader(rows))


def _save(fig, name):
    """Save figure as SVG (primary) and PNG."""
    for fmt in ("svg", "png"):
        fig.savefig(OUT / f"{name}.{fmt}")
    plt.close(fig)


# ─────────────────────────────────────────────────────────────────────────────
# 1. Sintering curve — relative density vs temperature
# ─────────────────────────────────────────────────────────────────────────────
def plot_sintering_curve():
    rows = _read_csv(DATA / "sintering_curve.csv")
    T = [int(r["temperature"]) for r in rows]
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(T, [float(r["alumina_density_pct"]) for r in rows], "o-", color=C_AL, lw=1.5, ms=4, label=AL2O3)
    ax.plot(T, [float(r["zirconia_density_pct"]) for r in rows], "s-", color=C_ZR, lw=1.5, ms=4, label="3Y-TZP")
    ax.axhline(100, color=C_REF, ls="--", lw=0.8, label="Theoretical density")
    ax.axhline(98, color=C_REF, ls=":", lw=0.8, alpha=0.6)
    ax.text(T[-1], 98.3, "98% dense", fontsize=7, ha="right", color=C_REF)
    ax.set(xlabel="Sintering Temperature (°C)", ylabel="Relative Density (%)", ylim=(50, 102))
    ax.legend(fontsize=8)
    fig.tight_layout()
    _save(fig, "ceramics_sintering_curve")
    print("  OK sintering curve")
    print("  CLAIM: densification depends on heating rate (5°C/min), dwell (2h), atmosphere (air), and particle size; "
          "values are relative density, not absolute.")


# ─────────────────────────────────────────────────────────────────────────────
# 2. XRD pattern overlay — Al2O3, t-ZrO2, 8YSZ with PDF card reference
# ─────────────────────────────────────────────────────────────────────────────
def plot_xrd_pattern():
    rows = _read_csv(DATA / "xrd_pattern.csv")
    tth = [float(r["two_theta"]) for r in rows]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(tth, [float(r["alumina_intensity"]) for r in rows], color=C_AL, lw=1.0,
            label=f"{AL2O3} sintered (PDF #46-1212)")
    ax.plot(tth, [float(r["alumina_ref_intensity"]) * 0.9 + 60 for r in rows], color=C_REF, lw=0.8, alpha=0.8,
            label="ICDD #46-1212 (ref)")
    ax.plot(tth, [float(r["zro2_intensity"]) * 0.9 + 120 for r in rows], color=C_ZR, lw=1.0,
            label=f"t-{ZRO2} (PDF #79-1769)")
    ax.plot(tth, [float(r["ysz_intensity"]) * 0.9 + 180 for r in rows], color=C_YSZ, lw=1.0,
            label="8YSZ cubic")
    for pos, hkl in [(25.57, "012"), (35.15, "104"), (43.36, "113"), (57.50, "116"), (66.52, "214")]:
        ax.annotate(f"({hkl})", (pos, 95), fontsize=6, rotation=45, ha="center", color=C_AL)
    ax.set(xlabel=r"2$\theta$ (°)", ylabel="Intensity (a.u.)", xlim=(20, 80))
    ax.legend(fontsize=7, loc="upper right")
    fig.tight_layout()
    _save(fig, "ceramics_xrd_pattern")
    print("  OK XRD pattern")
    print("  CLAIM: peak positions match PDF cards #46-1212 (Al2O3) and #79-1769 (t-ZrO2); "
          "phase identification requires full pattern Rietveld refinement, not peak matching alone.")


# ─────────────────────────────────────────────────────────────────────────────
# 3. Weibull probability plot — Al2O3 and 3Y-TZP
# ─────────────────────────────────────────────────────────────────────────────
def plot_weibull():
    rows = _read_csv(DATA / "weibull_data.csv")
    al = sorted([float(r["strength_mpa"]) for r in rows if r["material"] == "Al2O3"])
    zr = sorted([float(r["strength_mpa"]) for r in rows if r["material"] == "3Y-TZP"])

    def _fit(strengths, color, label, ax):
        n = len(strengths)
        P = np.array([(i - 0.5) / n for i in range(1, n + 1)])
        ln_s = np.log(strengths)
        ln_ln = np.log(-np.log(1 - P))
        m, b = np.polyfit(ln_s, ln_ln, 1)
        sigma0 = np.exp(-b / m)
        ax.scatter(ln_s, ln_ln, s=18, color=color, label=f"{label} (m={m:.1f}, {SIG0}={sigma0:.0f})")
        xf = np.linspace(ln_s[0], ln_s[-1], 50)
        ax.plot(xf, m * xf + b, color=color, lw=1.2)
        return m, sigma0

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3.8))
    # left: CDF
    for strengths, color, label in [(al, C_AL, AL2O3), (zr, C_ZR, "3Y-TZP")]:
        n = len(strengths)
        P = [(i - 0.5) / n for i in range(1, n + 1)]
        m, b = np.polyfit(np.log(strengths), np.log(-np.log(1 - np.array(P))), 1)
        s0 = np.exp(-b / m)
        ax1.scatter(strengths, P, s=18, color=color, label=f"{label} (m={m:.1f})")
        xf = np.linspace(min(strengths), max(strengths), 100)
        ax1.plot(xf, 1 - np.exp(-((xf / s0) ** m)), color=color, lw=1.2)
    ax1.set(xlabel="Flexural Strength (MPa)", ylabel="Failure Probability " + r"$P_f$")
    ax1.legend(fontsize=8)

    # right: Weibull plot
    m_al, s0_al = _fit(al, C_AL, AL2O3, ax2)
    m_zr, s0_zr = _fit(zr, C_ZR, "3Y-TZP", ax2)
    ax2.set(xlabel=r"$\ln(\sigma)$", ylabel=r"$\ln[\ln(1/(1-P))]$")
    ax2.legend(fontsize=8)

    fig.tight_layout()
    _save(fig, "ceramics_weibull_plot")
    print(f"  OK Weibull plot (Al2O3 m={m_al:.1f}, σ0={s0_al:.0f}; 3Y-TZP m={m_zr:.1f}, σ0={s0_zr:.0f})")
    print("  CLAIM: Weibull modulus reflects flaw population; valid only for same processing route, "
          "specimen geometry, and test method (n=30 per material).")


# ─────────────────────────────────────────────────────────────────────────────
# 4. Thermal conductivity — Al2O3, 3Y-TZP, SiC
# ─────────────────────────────────────────────────────────────────────────────
def plot_thermal_conductivity():
    rows = _read_csv(DATA / "thermal_conductivity.csv")
    T = [int(r["temperature"]) for r in rows]
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(T, [float(r["alumina_k"]) for r in rows], "o-", color=C_AL, lw=1.5, ms=4, label=AL2O3)
    ax.plot(T, [float(r["zirconia_k"]) for r in rows], "s-", color=C_ZR, lw=1.5, ms=4, label="3Y-TZP")
    ax.plot(T, [float(r["sic_k"]) for r in rows], "^-", color=C_SIC, lw=1.5, ms=4, label="SiC")
    ax.set(xlabel="Temperature (°C)", ylabel=r"Thermal Conductivity (W m$^{-1}$ K$^{-1}$)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _save(fig, "ceramics_thermal_conductivity")
    print("  OK thermal conductivity")
    print("  CLAIM: k depends on density, porosity, and grain size; values are for fully dense samples; "
          "phonon-dominated conduction (k decreases with T).")


# ─────────────────────────────────────────────────────────────────────────────
# 5. Grain size distribution — Al2O3 and ZrO2 lognormal
# ─────────────────────────────────────────────────────────────────────────────
def plot_grain_size_distribution():
    rows = _read_csv(DATA / "grain_size_distribution.csv")
    sizes = [float(r["grain_size_um"]) for r in rows]
    al_freq = [int(r["alumina_freq"]) for r in rows]
    zr_freq = [int(r["zirconia_freq"]) for r in rows]
    fig, ax = plt.subplots(figsize=(5, 3.5))
    width = 0.15
    ax.bar([s - width / 2 for s in sizes], al_freq, width=width, color=C_AL, alpha=0.85,
           label=f"{AL2O3} (median ~3 µm)")
    ax.bar([s + width / 2 for s in sizes], zr_freq, width=width, color=C_ZR, alpha=0.85,
           label="3Y-TZP (median ~0.4 µm)")
    ax.set(xlabel="Grain Size (µm)", ylabel="Frequency")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _save(fig, "ceramics_grain_size_dist")
    print("  OK grain size distribution")
    print("  CLAIM: grain size depends on sintering T and dopants; distribution is from 2D SEM section, "
          "not true 3D size (stereological correction needed for absolute values).")


# ─────────────────────────────────────────────────────────────────────────────
# 6. EIS Nyquist plot — CSV-driven, grain + grain boundary arcs
# ─────────────────────────────────────────────────────────────────────────────
def plot_eis_nyquist():
    rows = _read_csv(DATA / "eis_nyquist.csv")
    zr = [float(r["z_real"]) for r in rows]
    zi = [float(r["z_imag"]) for r in rows]
    fig, ax = plt.subplots(figsize=(5, 4.5))
    ax.plot(zr, [-z for z in zi], "o-", color=C_YSZ, ms=3, lw=1.2)
    ax.set(xlabel=r"$Z'$ (Ω)", ylabel=r"$-Z''$ (Ω)", aspect="equal")
    ax.text(0.55, 0.85, "High-freq arc: grain\nLow-freq arc: grain boundary",
            transform=ax.transAxes, fontsize=8, va="top",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C_REF, alpha=0.8))
    fig.tight_layout()
    _save(fig, "ceramics_eis_nyquist")
    print("  OK EIS Nyquist (CSV-driven)")
    print("  CLAIM: equivalent circuit (R_g-C_g || R_gb-C_gb) fit required for quantitative R_g/R_gb; "
          "Nyquist plot alone is qualitative; temperature and frequency range must be reported.")


# ─────────────────────────────────────────────────────────────────────────────
# 7. TGA + DSC combo — Al2O3 and ZrO2 precursor
# ─────────────────────────────────────────────────────────────────────────────
def plot_tga_dsc():
    rows = _read_csv(DATA / "tga_dsc.csv")
    T = [int(r["temperature"]) for r in rows]
    fig, ax1 = plt.subplots(figsize=(5.5, 3.8))
    ax1.plot(T, [float(r["alumina_mass"]) for r in rows], "-", color=C_AL, lw=1.5, label=f"{AL2O3} TGA")
    ax1.plot(T, [float(r["zirconia_mass"]) for r in rows], "-", color=C_ZR, lw=1.5, label=f"{ZRO2} precursor TGA")
    ax1.set_xlabel("Temperature (°C)")
    ax1.set_ylabel("Mass (%)", color=C_AL)
    ax1.tick_params(axis="y", labelcolor=C_AL)
    ax2 = ax1.twinx()
    ax2.plot(T, [float(r["alumina_dsc"]) for r in rows], "--", color=C_AL, lw=1.2, alpha=0.7, label=f"{AL2O3} DSC")
    ax2.plot(T, [float(r["zirconia_dsc"]) for r in rows], "--", color=C_ZR, lw=1.2, alpha=0.7, label=f"{ZRO2} DSC")
    ax2.set_ylabel("Heat Flow (mW/mg)", color=C_REF)
    ax2.annotate("organics\nburn-off", (400, 2.5), fontsize=7, ha="center", color=C_ZR)
    ax2.annotate("phase\ntransition", (1170, -0.8), fontsize=7, ha="center", color=C_ZR)
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=7, loc="center right")
    fig.tight_layout()
    _save(fig, "ceramics_tga_dsc")
    print("  OK TGA/DSC combo")
    print("  CLAIM: thermal events are literature-supported; exact peak T depends on heating rate (10°C/min), "
          "atmosphere (N₂), and precursor chemistry.")


# ─────────────────────────────────────────────────────────────────────────────
# 8. Stress-strain (compressive) — Al2O3, 3Y-TZP, SiC
# ─────────────────────────────────────────────────────────────────────────────
def plot_stress_strain():
    rows = _read_csv(DATA / "stress_strain.csv")
    strain = [float(r["strain"]) for r in rows]
    fig, ax = plt.subplots(figsize=(5, 3.8))
    ax.plot([s * 100 for s in strain], [float(r["alumina_stress"]) for r in rows], "-", color=C_AL, lw=1.5,
            label=f"{AL2O3} (E=380 GPa)")
    ax.plot([s * 100 for s in strain], [float(r["zirconia_stress"]) for r in rows], "-", color=C_ZR, lw=1.5,
            label="3Y-TZP (E=210 GPa)")
    ax.plot([s * 100 for s in strain], [float(r["sic_stress"]) for r in rows], "-", color=C_SIC, lw=1.5,
            label="SiC (E=410 GPa)")
    ax.set(xlabel="Strain (%)", ylabel="Stress (MPa)", xlim=(0, 0.6))
    ax.legend(fontsize=8)
    ax.text(0.95, 0.05, "Compression (ASTM C773)\nBrittle fracture, no yield",
            transform=ax.transAxes, fontsize=8, va="bottom", ha="right",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C_REF, alpha=0.8))
    fig.tight_layout()
    _save(fig, "ceramics_stress_strain")
    print("  OK stress-strain")
    print("  CLAIM: ceramic fracture strain is 0.1-0.3%, NOT metallic 10%+; "
          "compressive response per ASTM C773; rate-dependent, no macroscopic yield.")


# ─────────────────────────────────────────────────────────────────────────────
# 9. Thermal expansion (dilatometry) — Al2O3, 3Y-TZP, SiC
# ─────────────────────────────────────────────────────────────────────────────
def plot_thermal_expansion():
    rows = _read_csv(DATA / "thermal_expansion.csv")
    T = [int(r["temperature"]) for r in rows]
    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(T, [float(r["alumina_expansion"]) for r in rows], "o-", color=C_AL, lw=1.5, ms=4,
            label=f"{AL2O3} (CTE " + r"$8\times10^{-6}$/K)")
    ax.plot(T, [float(r["zirconia_expansion"]) for r in rows], "s-", color=C_ZR, lw=1.5, ms=4,
            label="3Y-TZP (CTE " + r"$10\times10^{-6}$/K)")
    ax.plot(T, [float(r["sic_expansion"]) for r in rows], "^-", color=C_SIC, lw=1.5, ms=4,
            label="SiC (CTE " + r"$4.5\times10^{-6}$/K)")
    ax.set(xlabel="Temperature (°C)", ylabel=r"$\Delta L/L_0$ (%)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    _save(fig, "ceramics_thermal_expansion")
    print("  OK thermal expansion")
    print("  CLAIM: CTE is temperature-averaged (25-1000°C); true CTE increases slightly with T; "
          "values are engineering averages, not instantaneous.")


if __name__ == "__main__":
    print("Generating Ceramics Figure Atlas (literature-anchored, CSV-driven)...")
    print()
    plot_sintering_curve(); print()
    plot_xrd_pattern(); print()
    plot_weibull(); print()
    plot_thermal_conductivity(); print()
    plot_grain_size_distribution(); print()
    plot_eis_nyquist(); print()
    plot_tga_dsc(); print()
    plot_stress_strain(); print()
    plot_thermal_expansion(); print()
    print(f"All figures saved to {OUT}")

#!/usr/bin/env python3
"""Generate the Ceramics Figure Atlas — sintering, XRD, Weibull, conductivity, grain size, EIS."""

import csv
import os
from pathlib import Path

import numpy as np

# Ensure matplotlib uses non-interactive backend
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent.parent.parent
DATA = HERE / "assets" / "ceramics-atlas" / "data"
OUT = HERE / "assets" / "ceramics-atlas" / "generated"
OUT.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"font.size": 10, "figure.dpi": 150})


def _read_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


# ───────────────────────────
# 1. Sintering curve
# ───────────────────────────
def plot_sintering_curve():
    rows = _read_csv(DATA / "sintering_curve.csv")
    T = [int(r["temperature"]) for r in rows]
    fig, ax = plt.subplots(figsize=(5, 3.5))
    for key, label, marker in [
        ("alumina_density", "Al₂O₃", "o"),
        ("zirconia_density", "3Y-TZP", "s"),
        ("spinel_density", "MgAl₂O₄", "^"),
    ]:
        vals = [float(r[key]) for r in rows]
        ax.plot(T, vals, marker=marker, label=label, lw=1.5)
    ax.axhline(3.96, color="gray", ls="--", lw=0.8, label="Theoretical Al₂O₃")
    ax.set(xlabel="Sintering Temperature (°C)", ylabel="Relative Density (g/cm³)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "ceramics_sintering_curve.png")
    fig.savefig(OUT / "ceramics_sintering_curve.svg")
    plt.close(fig)
    print("  OK sintering curve")


# ───────────────────────────
# 2. XRD pattern overlay
# ───────────────────────────
def plot_xrd_pattern():
    rows = _read_csv(DATA / "xrd_pattern.csv")
    tth = [float(r["two_theta"]) for r in rows]
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(tth, [float(r["alumina_intensity"]) for r in rows], label="Sintered Al₂O₃", lw=1.2)
    ax.plot(tth, [float(r["alumina_ref_intensity"]) for r in rows], label="ICDD 01-075-0782", lw=0.8, alpha=0.7)
    for p in [(25.6, "012"), (35.2, "104"), (43.4, "113"), (52.5, "024"), (57.5, "116"), (68.2, "300")]:
        ax.annotate(f"({p[1]})", (p[0], 10), fontsize=6, rotation=45)
    ax.set(xlabel="2θ (°)", ylabel="Intensity (a.u.)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "ceramics_xrd_pattern.png")
    fig.savefig(OUT / "ceramics_xrd_pattern.svg")
    plt.close(fig)
    print("  OK XRD pattern")


# ───────────────────────────
# 3. Weibull probability plot
# ───────────────────────────
def plot_weibull():
    rows = _read_csv(DATA / "weibull_data.csv")
    strengths = sorted([float(r["strength_mpa"]) for r in rows])
    n = len(strengths)
    P = [(i - 0.5) / n for i in range(1, n + 1)]
    ln_s = np.log(strengths)
    ln_ln = np.log(-np.log(1 - np.array(P)))
    coeffs = np.polyfit(ln_s, ln_ln, 1)
    m, b = coeffs
    sigma0 = np.exp(-b / m)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5))
    ax1.scatter(strengths, P, s=20, c="navy")
    ax1.set(xlabel="Flexural Strength (MPa)", ylabel="Failure Probability")
    x_fit = np.linspace(min(strengths), max(strengths), 100)
    ax1.plot(x_fit, 1 - np.exp(-((x_fit / sigma0) ** m)), "r-", lw=1)
    ax1.text(0.05, 0.95, f"m = {m:.1f}\nσ₀ = {sigma0:.0f} MPa", transform=ax1.transAxes, fontsize=9, va="top")

    ax2.scatter(ln_s, ln_ln, s=20, c="navy")
    ax2.plot(np.linspace(min(ln_s), max(ln_s), 100),
             coeffs[0] * np.linspace(min(ln_s), max(ln_s), 100) + coeffs[1], "r-", lw=1)
    ax2.set(xlabel="ln(σ)", ylabel="ln(-ln(1-P))")
    fig.tight_layout()
    fig.savefig(OUT / "ceramics_weibull_plot.png")
    fig.savefig(OUT / "ceramics_weibull_plot.svg")
    plt.close(fig)
    print(f"  OK Weibull plot (m={m:.1f})")


# ───────────────────────────
# 4. Thermal conductivity
# ───────────────────────────
def plot_thermal_conductivity():
    rows = _read_csv(DATA / "thermal_conductivity.csv")
    T = [int(r["temperature"]) for r in rows]
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    ax.plot(T, [float(r["conductivity_alumina"]) for r in rows], "o-", label="Al₂O₃ (high density)", lw=1.5)
    ax.plot(T, [float(r["conductivity_alumina2"]) for r in rows], "s--", label="Al₂O₃ (low density)", lw=1.5)
    ax.plot(T, [float(r["conductivity_zirconia"]) for r in rows], "^-.", label="3Y-TZP", lw=1.5)
    ax.set(xlabel="Temperature (°C)", ylabel="Thermal Conductivity (W m⁻¹ K⁻¹)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "ceramics_thermal_conductivity.png")
    fig.savefig(OUT / "ceramics_thermal_conductivity.svg")
    plt.close(fig)
    print("  OK thermal conductivity")


# ───────────────────────────
# 5. Grain size distribution
# ───────────────────────────
def plot_grain_size_distribution():
    rows = _read_csv(DATA / "grain_size_distribution.csv")
    sizes = [float(r["grain_size_um"]) for r in rows]
    freqs = [int(r["frequency"]) for r in rows]
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    ax.bar(sizes, freqs, width=0.3, color="steelblue", edgecolor="navy", alpha=0.8)
    ax.set(xlabel="Grain Size (µm)", ylabel="Frequency")
    # lognormal fit curve
    from numpy import exp, log, sqrt, pi
    weighted = np.repeat(sizes, freqs)
    mu, sigma = np.mean(log(weighted)), np.std(log(weighted))
    x_fit = np.linspace(0.2, max(sizes) + 0.5, 200)
    y_fit = 1 / (x_fit * sigma * sqrt(2 * pi)) * exp(-((log(x_fit) - mu) ** 2) / (2 * sigma ** 2))
    y_fit = y_fit / max(y_fit) * max(freqs)
    ax.plot(x_fit, y_fit, "r-", lw=1.5, label="Lognormal fit")
    ax.legend(fontsize=8)
    ax.text(0.95, 0.95, f"Mean: {np.mean(weighted):.2f} µm\nσ: {np.std(weighted):.2f} µm",
            transform=ax.transAxes, fontsize=9, va="top", ha="right")
    fig.tight_layout()
    fig.savefig(OUT / "ceramics_grain_size_dist.png")
    fig.savefig(OUT / "ceramics_grain_size_dist.svg")
    plt.close(fig)
    print("  OK grain size distribution")


# ───────────────────────────
# 6. EIS Nyquist plot (simulated)
# ───────────────────────────
def plot_eis_nyquist():
    np.random.seed(42)
    freq = np.logspace(0, 6, 50)
    R_g, C_g, R_gb, C_gb = 100, 1e-10, 500, 1e-8
    Z_g = R_g / (1 + (2j * np.pi * freq * R_g * C_g))
    Z_gb = R_gb / (1 + (2j * np.pi * freq * R_gb * C_gb))
    Z_total = Z_g + Z_gb

    fig, ax = plt.subplots(figsize=(4.5, 4))
    ax.plot(Z_total.real, -Z_total.imag, "o-", ms=3, lw=1)
    ax.set(xlabel="Z' (Ω)", ylabel="-Z'' (Ω)", aspect="equal")
    ax.text(0.5, 0.9, "Grain\n Grain boundary", transform=ax.transAxes, fontsize=9, va="top")
    fig.tight_layout()
    fig.savefig(OUT / "ceramics_eis_nyquist.png")
    fig.savefig(OUT / "ceramics_eis_nyquist.svg")
    plt.close(fig)
    print("  OK EIS Nyquist (simulated)")


# ───────────────────────────
# 7. TGA + DSC combo (dual axis)
# ───────────────────────────
def plot_tga_dsc():
    rows = _read_csv(DATA / "tga_dsc.csv")
    T = [int(r["temperature"]) for r in rows]
    fig, ax1 = plt.subplots(figsize=(4.5, 3.5))
    ax1.plot(T, [float(r["alumina_hf"]) for r in rows], "b-", lw=1.5, label="TGA (mass %)")
    ax1.set(xlabel="Temperature (°C)", ylabel="Mass (%)")
    ax2 = ax1.twinx()
    ax2.plot(T, [float(r["alumina_dsc"]) for r in rows], "r--", lw=1.5, label="DSC (heat flow)")
    ax2.set(ylabel="Heat Flow (a.u.)")
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, fontsize=8, loc="upper right")
    fig.tight_layout()
    fig.savefig(OUT / "ceramics_tga_dsc.png")
    fig.savefig(OUT / "ceramics_tga_dsc.svg")
    plt.close(fig)
    print("  OK TGA/DSC combo")


# ───────────────────────────
# 8. Stress-strain (compressive)
# ───────────────────────────
def plot_stress_strain():
    rows = _read_csv(DATA / "stress_strain.csv")
    strain = [float(r["strain"]) for r in rows]
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    ax.plot(strain, [float(r["alumina_stress"]) for r in rows], "b-", lw=1.5, label="Al₂O₃ (fine grain)")
    ax.plot(strain, [float(r["alumina2_stress"]) for r in rows], "r--", lw=1.5, label="Al₂O₃ (coarse grain)")
    ax.plot(strain, [float(r["zirconia_stress"]) for r in rows], "g-.", lw=1.5, label="3Y-TZP")
    ax.set(xlabel="Strain", ylabel="Stress (MPa)")
    ax.legend(fontsize=8)
    ax.text(0.95, 0.95, "Compression", transform=ax.transAxes, fontsize=9, va="top", ha="right")
    fig.tight_layout()
    fig.savefig(OUT / "ceramics_stress_strain.png")
    fig.savefig(OUT / "ceramics_stress_strain.svg")
    plt.close(fig)
    print("  OK stress-strain")


# ───────────────────────────
# 9. Thermal expansion
# ───────────────────────────
def plot_thermal_expansion():
    rows = _read_csv(DATA / "thermal_expansion.csv")
    T = [int(r["temperature"]) for r in rows]
    fig, ax = plt.subplots(figsize=(4.5, 3.5))
    ax.plot(T, [float(r["alumina_expansion"]) for r in rows], "o-", lw=1.5, label="Al₂O₃")
    ax.plot(T, [float(r["zirconia_expansion"]) for r in rows], "s--", lw=1.5, label="3Y-TZP")
    ax.set(xlabel="Temperature (°C)", ylabel="dL/L₀ (%)")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "ceramics_thermal_expansion.png")
    fig.savefig(OUT / "ceramics_thermal_expansion.svg")
    plt.close(fig)
    print("  OK thermal expansion")


if __name__ == "__main__":
    print("Generating Ceramics Figure Atlas...")
    plot_sintering_curve()
    plot_xrd_pattern()
    plot_weibull()
    plot_thermal_conductivity()
    plot_grain_size_distribution()
    plot_eis_nyquist()
    plot_tga_dsc()
    plot_stress_strain()
    plot_thermal_expansion()
    print(f"\nAll figures saved to {OUT}")

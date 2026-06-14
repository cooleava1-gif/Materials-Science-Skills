# Paper Demo Reference

This document maps each paper demo to its source publication and explains
the claim boundary discipline enforced by each figure.

## 1. Kong et al. (2024) — Interlayer Bonding

**Full citation**:
Kong L, Su S, Wang Z, Wu P, Zhang Y, Chen Z, Ren D, Ai C.
Microscale mechanism and key factors of waterborne epoxy resin emulsified
asphalt enhancing interlayer bonding performance and shear resistance of
bridge deck pavement.
Construction and Building Materials, 2024, 419: 135570.

**Figures reproduced**:
- `plot_bonding_strength.py` → Fig. 7: Pull-off bonding strength
- `plot_shear_vs_temperature.py` → Fig. 9: 45° shear strength vs temperature

**Key findings**:
- Optimal WER dosage: 15% by evaporation residue
- WER-EA shows least temperature sensitivity
- "Honeycomb" structure observed via SEM

**Claim boundary**:
- ✅ Strength improvement is measured performance evidence
- ❌ Strength alone does not prove mechanism
- 🔍 FTIR + fluorescence + SEM needed for mechanism claims

---

## 2. Zhang et al. (2017) — Tack Coat Performance

**Full citation**:
Zhang Q, Xu Y, Wen Z.
Influence of water-borne epoxy resin content on performance of waterborne
epoxy resin compound SBR modified emulsified asphalt for tack coat.
Construction and Building Materials, 2017, 155: 706-714.

**Figures reproduced**:
- `plot_viscosity_curing.py` → Fig. 5: Brookfield viscosity vs curing time
- `plot_shear_strength.py` → Fig. 10: Shear strength of composite plate

**Key findings**:
- Optimal WER content: 15%
- SBR content: 3% (determined by adhesion and DSC)
- Viscosity build-up indicates epoxy crosslinking

**Claim boundary**:
- ✅ Viscosity increase is measured curing evidence
- ❌ Viscosity alone does not confirm network structure
- 🔍 DSC + FTIR needed for crosslinking mechanism

---

## 3. Yao et al. (2022) — Compound Modification Mechanism

**Full citation**:
Yao X, Tan L, Xu T.
Preparation, properties and compound modification mechanism of waterborne
epoxy resin/styrene butadiene rubber latex modified emulsified asphalt.
Construction and Building Materials, 2022, 318: 126178.

**Figures reproduced**:
- `plot_dsr_rheology.py` → Fig. 8: G*/sin(δ) vs temperature
- `plot_ftir_spectra.py` → Fig. 10: FTIR spectra

**Key findings**:
- SBR forms network film through physical action
- WER forms high-strength network through chemical reaction
- Interpenetrating network structure at sufficient dosage

**Claim boundary**:
- ✅ DSR data supports performance grading
- ✅ FTIR confirms chemical incorporation
- ❌ DSR/FTIR alone do not prove interpenetrating network
- 🔍 DSC + LSCM + ESEM needed for morphology claims

---

## General Claim Boundary Rules

When using these demos for manuscript figures:

1. **Performance claims** (strength, modulus, viscosity): Always include
   error bars, replicate count, and test conditions.

2. **Mechanism claims** (network structure, interpenetrating, crosslinking):
   Must have direct characterization evidence (SEM, LSCM, ESEM, DSC).

3. **Durability claims** (aging resistance, moisture resistance): Must have
   conditioning protocol and retention ratio data.

4. **Temperature claims** (high-temperature performance): Must specify
   test temperature range and loading conditions.

#!/usr/bin/env python3
"""Validate materials science claims in figure_contract.md against materials_kb.yaml.

Extracts materials science entities (XRD peaks, FTIR wavenumbers, performance
values) from a figure contract, then checks each claim against the knowledge
base. This is the materials-domain integrity layer: it catches claims that
contradict known PDF cards, FTIR assignments, or typical property ranges.

Usage:
    python scripts/validate_materials_claims.py figure_contract.md
    python scripts/validate_materials_claims.py figure_contract.md --json

Exit codes: 0 = pass, 1 = warning, 2 = error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.stderr.write("ERROR: PyYAML is required. Install with: pip install pyyaml\n")
    raise

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent
KB_PATH = SCRIPT_DIR.parent / "static" / "core" / "materials_kb.yaml"

XRD_TOLERANCE_DEG = 0.5
FTIR_TOLERANCE_CM1 = 20
PERFORMANCE_TOLERANCE = 0.25  # fractional tolerance for single-value ranges

# Phase aliases -> canonical KB phase name.
# Longer aliases first so "t-ZrO2" matches before "ZrO2".
PHASE_ALIASES: list[tuple[str, str]] = [
    ("alpha-al2o3", "Al2O3 (alpha-corundum)"),
    ("α-al2o3", "Al2O3 (alpha-corundum)"),
    ("al2o3", "Al2O3 (alpha-corundum)"),
    ("corundum", "Al2O3 (alpha-corundum)"),
    ("alumina", "Al2O3 (alpha-corundum)"),
    ("t-zro2", "ZrO2 (tetragonal)"),
    ("tetragonal zro2", "ZrO2 (tetragonal)"),
    ("3y-tzp", "ZrO2 (tetragonal)"),
    ("m-zro2", "ZrO2 (monoclinic)"),
    ("monoclinic zro2", "ZrO2 (monoclinic)"),
    ("zro2", "ZrO2 (tetragonal)"),
    ("zirconia", "ZrO2 (tetragonal)"),
    ("8ysz", "8YSZ (cubic fluorite)"),
    ("ysz", "8YSZ (cubic fluorite)"),
    ("beta-sic", "SiC (3C, beta)"),
    ("3c-sic", "SiC (3C, beta)"),
    ("sic", "SiC (3C, beta)"),
    ("silicon carbide", "SiC (3C, beta)"),
    ("beta-si3n4", "Si3N4 (beta)"),
    ("si3n4", "Si3N4 (beta)"),
    ("silicon nitride", "Si3N4 (beta)"),
    ("ca(oh)2", "Ca(OH)2 (portlandite)"),
    ("portlandite", "Ca(OH)2 (portlandite)"),
    ("quartz", "Quartz (SiO2)"),
    ("sio2", "Quartz (SiO2)"),
    ("tio2 anatase", "TiO2 (anatase)"),
    ("anatase", "TiO2 (anatase)"),
    ("tio2 rutile", "TiO2 (rutile)"),
    ("rutile", "TiO2 (rutile)"),
    ("tio2", "TiO2 (anatase)"),
    ("fe2o3", "Fe2O3 (hematite)"),
    ("hematite", "Fe2O3 (hematite)"),
    ("caco3", "CaCO3 (calcite)"),
    ("calcite", "CaCO3 (calcite)"),
    ("mullite", "Mullite (3Al2O3·2SiO2)"),
]

# FTIR functional group -> category for cross-checking claims.
FTIR_CATEGORIES: list[tuple[str, str]] = [
    ("oxirane", "epoxy"),
    ("epoxy", "epoxy"),
    ("c=o", "carbonyl"),
    ("carbonyl", "carbonyl"),
    ("ester", "carbonyl"),
    ("o-h", "hydroxyl"),
    ("hydroxyl", "hydroxyl"),
    ("oh stretch", "hydroxyl"),
    ("c-h", "methylene_ch"),
    ("ch2", "methylene_ch"),
    ("ch3", "methylene_ch"),
    ("methylene", "methylene_ch"),
    ("c-o-c", "ether"),
    ("ether", "ether"),
    ("c=c", "aromatic"),
    ("aromatic", "aromatic"),
    ("si-o-si", "silicate"),
    ("si-o", "silicate"),
    ("silicate", "silicate"),
    ("c-s-h", "csh"),
    ("csh", "csh"),
    ("so4", "sulfate"),
    ("sulfate", "sulfate"),
    ("ettringite", "sulfate"),
    ("co3", "carbonate"),
    ("carbonate", "carbonate"),
    ("calcite", "carbonate"),
    ("h-o-h", "water"),
    ("water", "water"),
    ("hydration", "water"),
]

# Performance property keywords -> KB property name.
PROPERTY_KEYWORDS: list[tuple[str, str]] = [
    ("flexural strength", "flexural_strength"),
    ("bending strength", "flexural_strength"),
    ("compressive strength", "compressive_strength"),
    ("elastic modulus", "elastic_modulus"),
    ("young's modulus", "elastic_modulus"),
    ("young modulus", "elastic_modulus"),
    ("thermal conductivity", "thermal_conductivity"),
    ("coefficient of thermal expansion", "CTE"),
    ("thermal expansion", "CTE"),
    ("cte", "CTE"),
    ("bond strength", "bond_strength"),
    ("bonding strength", "bond_strength"),
    ("weibull modulus", "weibull_modulus"),
    ("fracture strain", "fracture_strain"),
    ("strain at fracture", "fracture_strain"),
]

# Material aliases for performance claims -> KB material name.
MATERIAL_ALIASES: list[tuple[str, str]] = [
    ("3y-tzp zro2", "3Y-TZP ZrO2"),
    ("3y-tzp", "3Y-TZP ZrO2"),
    ("wer-ea modified", "WER-EA modified"),
    ("wer modified", "WER-EA modified"),
    ("wer-ea", "WER-EA modified"),
    ("asphalt-aggregate", "asphalt-aggregate"),
    ("asphalt aggregate", "asphalt-aggregate"),
    ("base asphalt", "asphalt-aggregate"),
    ("unmodified asphalt", "asphalt-aggregate"),
    ("portland cement", "Portland cement"),
    ("cement", "Portland cement"),
    ("al2o3", "Al2O3"),
    ("alumina", "Al2O3"),
    ("zro2", "ZrO2"),
    ("zirconia", "ZrO2"),
    ("sic", "SiC"),
    ("silicon carbide", "SiC"),
    ("si3n4", "Si3N4"),
    ("silicon nitride", "Si3N4"),
    ("ceramics", "ceramics"),
]


# ---------------------------------------------------------------------------
# KB loading
# ---------------------------------------------------------------------------

def load_kb(kb_path: Path) -> dict[str, Any]:
    """Load the materials knowledge base YAML."""
    with open(kb_path, encoding="utf-8") as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Text splitting
# ---------------------------------------------------------------------------

def split_units(text: str) -> list[str]:
    """Split text into claim units (sentences / list items / table rows).

    A unit is a line or a sentence; we keep both so that peak tables and
    prose paragraphs are both covered.
    """
    units: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        # Split line into sentences on . ; but keep table rows intact.
        if "\t" in line or line.startswith("|") or line.startswith("- {"):
            units.append(line)
        else:
            for sent in re.split(r"[.;]\s+", line):
                sent = sent.strip()
                if sent:
                    units.append(sent)
    return units


# ---------------------------------------------------------------------------
# Entity extraction: XRD
# ---------------------------------------------------------------------------

def find_phases_in_text(text: str) -> list[tuple[str, int]]:
    """Find phase names in text. Returns [(canonical_phase, position), ...]."""
    results: list[tuple[str, int]] = []
    lower = text.lower()
    for alias, canonical in PHASE_ALIASES:
        for m in re.finditer(re.escape(alias), lower):
            results.append((canonical, m.start()))
    return results


def extract_xrd_claims(text: str) -> list[dict[str, Any]]:
    """Extract XRD peak claims: (2θ value, phase) pairs from text."""
    claims: list[dict[str, Any]] = []
    seen: set[tuple[float, str]] = set()

    for unit in split_units(text):
        # Find 2θ values: "35.15°" or "2θ = 35.15" or "2θ=35.15"
        theta_patterns = [
            r"(\d{1,2}\.\d{1,2})\s*°",
            r"2\s*[θθ]\s*[=:]\s*(\d{1,2}\.\d{1,2})",
        ]
        theta_matches: list[tuple[float, int]] = []
        for pat in theta_patterns:
            for m in re.finditer(pat, unit):
                theta_matches.append((float(m.group(1)), m.start()))

        if not theta_matches:
            continue

        phases = find_phases_in_text(unit)
        if not phases:
            continue

        for theta_val, theta_pos in theta_matches:
            # Match with nearest phase in the same unit.
            nearest_phase = None
            min_dist = float("inf")
            for phase_name, phase_pos in phases:
                dist = abs(theta_pos - phase_pos)
                if dist < min_dist:
                    min_dist = dist
                    nearest_phase = phase_name

            key = (theta_val, nearest_phase or "")
            if key in seen:
                continue
            seen.add(key)

            claims.append({
                "two_theta": theta_val,
                "phase": nearest_phase,
                "context": unit[:200],
            })

    return claims


# ---------------------------------------------------------------------------
# Entity extraction: FTIR
# ---------------------------------------------------------------------------

def find_ftir_groups_in_text(text: str) -> list[tuple[str, int]]:
    """Find functional group mentions in text. Returns [(group_text, position), ...]."""
    results: list[tuple[str, int]] = []
    lower = text.lower()
    for alias, _ in FTIR_CATEGORIES:
        for m in re.finditer(re.escape(alias), lower):
            results.append((alias, m.start()))
    return results


def categorise_ftir(group_text: str) -> str | None:
    """Map a functional group text to a category."""
    lower = group_text.lower()
    for alias, category in FTIR_CATEGORIES:
        if alias in lower:
            return category
    return None


def extract_ftir_claims(text: str) -> list[dict[str, Any]]:
    """Extract FTIR claims: (wavenumber, functional_group) pairs from text."""
    claims: list[dict[str, Any]] = []
    seen: set[tuple[int, str | None]] = set()

    for unit in split_units(text):
        # Find wavenumbers: "915 cm-1" or "915cm⁻¹" or "915 cm−1" etc.
        wn_pattern = r"(\d{3,4})\s*cm\s*[-−‐⁻]?\s*[1¹]"
        wn_matches: list[tuple[int, int]] = []
        for m in re.finditer(wn_pattern, unit):
            wn_matches.append((int(m.group(1)), m.start()))

        if not wn_matches:
            continue

        groups = find_ftir_groups_in_text(unit)

        for wn_val, wn_pos in wn_matches:
            # Find nearest functional group mention.
            nearest_group: str | None = None
            min_dist = float("inf")
            for group_text, group_pos in groups:
                dist = abs(wn_pos - group_pos)
                if dist < min_dist:
                    min_dist = dist
                    nearest_group = group_text

            key = (wn_val, nearest_group)
            if key in seen:
                continue
            seen.add(key)

            claims.append({
                "wavenumber": wn_val,
                "functional_group": nearest_group,
                "context": unit[:200],
            })

    return claims


# ---------------------------------------------------------------------------
# Entity extraction: performance
# ---------------------------------------------------------------------------

def find_materials_in_text(text: str) -> list[tuple[str, int]]:
    """Find material names in text. Returns [(canonical_material, position), ...]."""
    results: list[tuple[str, int]] = []
    lower = text.lower()
    for alias, canonical in MATERIAL_ALIASES:
        for m in re.finditer(re.escape(alias), lower):
            results.append((canonical, m.start()))
    return results


def find_properties_in_text(text: str) -> list[tuple[str, int]]:
    """Find property keywords in text. Returns [(kb_property, position), ...].

    Uses word boundaries so that 'cte' does not match inside 'characteristic'.
    """
    results: list[tuple[str, int]] = []
    lower = text.lower()
    for keyword, kb_prop in PROPERTY_KEYWORDS:
        for m in re.finditer(r"(?<!\w)" + re.escape(keyword) + r"(?!\w)", lower):
            results.append((kb_prop, m.start()))
    return results


def find_values_in_text(text: str) -> list[tuple[float, str, int]]:
    """Find numeric values with units. Returns [(value, unit, position), ...].

    The negative lookbehind ``(?<!\\w)`` excludes digits that are part of a
    chemical formula (e.g. the ``2`` and ``3`` in ``Al2O3``), which would
    otherwise be extracted as standalone numbers with an empty unit.
    """
    results: list[tuple[float, str, int]] = []
    # Match "350 MPa", "380 GPa", "120 W/mK", "8e-6 /K", "0.3 %", "12" (dimensionless)
    pattern = r"(?<![\w])(\d+\.?\d*(?:e[-+]?\d+)?)\s*(MPa|GPa|W/mK|W/m\.K|/K|1/K|%|)"
    for m in re.finditer(pattern, text):
        val = float(m.group(1))
        unit = m.group(2).strip()
        results.append((val, unit, m.start()))
    return results


def extract_performance_claims(text: str) -> list[dict[str, Any]]:
    """Extract performance claims: (material, property, value, unit) from text.

    Uses proximity matching instead of a cartesian product: for each property
    keyword found in a sentence, the nearest material and the nearest value
    (preferring values that follow the property, falling back to preceding
    values) are paired with it. This correctly handles sentences like
    "Al2O3 flexural strength is 350 MPa, and the elastic modulus is 380 GPa"
    by assigning 350 to flexural_strength and 380 to elastic_modulus.
    """
    claims: list[dict[str, Any]] = []
    seen: set[tuple[str, str, float]] = set()

    for unit in split_units(text):
        materials = find_materials_in_text(unit)
        if not materials:
            continue

        properties = find_properties_in_text(unit)
        if not properties:
            continue

        values = find_values_in_text(unit)
        if not values:
            continue

        for prop_name, prop_pos in properties:
            # Nearest material (any direction).
            nearest_mat = min(
                materials, key=lambda mp: abs(prop_pos - mp[1])
            )[0]

            # Nearest value that follows the property; fall back to the
            # nearest preceding value if none follow.
            after = [(v, u, p) for v, u, p in values if p >= prop_pos]
            if after:
                nearest_val, nearest_unit, _ = min(
                    after, key=lambda vup: vup[2] - prop_pos
                )
            else:
                nearest_val, nearest_unit, _ = min(
                    values, key=lambda vup: prop_pos - vup[2]
                )

            key = (nearest_mat, prop_name, nearest_val)
            if key in seen:
                continue
            seen.add(key)

            claims.append({
                "material": nearest_mat,
                "property": prop_name,
                "value": nearest_val,
                "unit": nearest_unit,
                "context": unit[:200],
            })

    return claims


# ---------------------------------------------------------------------------
# Validation against KB
# ---------------------------------------------------------------------------

def validate_xrd_claim(
    claim: dict[str, Any], kb: dict[str, Any]
) -> dict[str, Any]:
    """Validate a single XRD claim against KB."""
    theta = claim["two_theta"]
    phase = claim["phase"]

    # Find the phase in KB.
    kb_phase = None
    for card in kb.get("xrd_cards", []):
        if card["phase"] == phase:
            kb_phase = card
            break

    if kb_phase is None:
        return {
            "type": "xrd",
            "claim": claim["context"],
            "extracted": {"two_theta": theta, "phase": phase},
            "kb_match": None,
            "result": "warning",
            "message": f"phase '{phase}' not in KB; cannot verify {theta}°",
        }

    # Check if theta matches any peak.
    for peak in kb_phase["peaks"]:
        if abs(theta - peak["two_theta"]) <= XRD_TOLERANCE_DEG:
            return {
                "type": "xrd",
                "claim": claim["context"],
                "extracted": {"two_theta": theta, "phase": phase},
                "kb_match": {
                    "pdf_card": kb_phase["pdf_card"],
                    "hkl": peak["hkl"],
                    "relative_intensity": peak["relative_intensity"],
                },
                "result": "confirmed",
                "message": (
                    f"{theta}° matches {phase} #{kb_phase['pdf_card']} "
                    f"({peak['hkl']}) peak"
                ),
            }

    # No match: check if this peak belongs to a different phase.
    for card in kb.get("xrd_cards", []):
        for peak in card["peaks"]:
            if abs(theta - peak["two_theta"]) <= XRD_TOLERANCE_DEG:
                return {
                    "type": "xrd",
                    "claim": claim["context"],
                    "extracted": {"two_theta": theta, "phase": phase},
                    "kb_match": {
                        "pdf_card": card["pdf_card"],
                        "hkl": peak["hkl"],
                        "actual_phase": card["phase"],
                    },
                    "result": "error",
                    "message": (
                        f"{theta}° does not match {phase} #{kb_phase['pdf_card']}; "
                        f"it matches {card['phase']} #{card['pdf_card']} ({peak['hkl']})"
                    ),
                }

    return {
        "type": "xrd",
        "claim": claim["context"],
        "extracted": {"two_theta": theta, "phase": phase},
        "kb_match": {"pdf_card": kb_phase["pdf_card"]},
        "result": "warning",
        "message": (
            f"{theta}° not found among {phase} #{kb_phase['pdf_card']} peaks "
            f"(tolerance ±{XRD_TOLERANCE_DEG}°)"
        ),
    }


def validate_ftir_claim(
    claim: dict[str, Any], kb: dict[str, Any]
) -> dict[str, Any]:
    """Validate a single FTIR claim against KB."""
    wn = claim["wavenumber"]
    claimed_group = claim["functional_group"]

    # Find KB entry at this wavenumber (±tolerance).
    kb_match = None
    for entry in kb.get("ftir_groups", []):
        if abs(wn - entry["wavenumber"]) <= FTIR_TOLERANCE_CM1:
            kb_match = entry
            break

    if kb_match is None:
        return {
            "type": "ftir",
            "claim": claim["context"],
            "extracted": {"wavenumber": wn, "functional_group": claimed_group},
            "kb_match": None,
            "result": "warning",
            "message": f"{wn}cm⁻¹ not in KB (tolerance ±{FTIR_TOLERANCE_CM1}cm⁻¹)",
        }

    kb_category = categorise_ftir(
        kb_match["functional_group"] + " " + kb_match["bond_type"]
    )

    if claimed_group is None:
        # No group claimed, just confirm wavenumber.
        return {
            "type": "ftir",
            "claim": claim["context"],
            "extracted": {"wavenumber": wn, "functional_group": None},
            "kb_match": {
                "wavenumber": kb_match["wavenumber"],
                "actual_group": kb_match["functional_group"],
            },
            "result": "confirmed",
            "message": (
                f"{wn}cm⁻¹ matches KB: {kb_match['functional_group']} "
                f"({kb_match['bond_type']})"
            ),
        }

    claimed_category = categorise_ftir(claimed_group)

    if claimed_category is None:
        # Claimed group not in our category map; just confirm wavenumber.
        return {
            "type": "ftir",
            "claim": claim["context"],
            "extracted": {"wavenumber": wn, "functional_group": claimed_group},
            "kb_match": {
                "wavenumber": kb_match["wavenumber"],
                "actual_group": kb_match["functional_group"],
            },
            "result": "confirmed",
            "message": (
                f"{wn}cm⁻¹ matches KB: {kb_match['functional_group']} "
                f"(claimed '{claimed_group}' not categorisable)"
            ),
        }

    if claimed_category == kb_category:
        return {
            "type": "ftir",
            "claim": claim["context"],
            "extracted": {"wavenumber": wn, "functional_group": claimed_group},
            "kb_match": {
                "wavenumber": kb_match["wavenumber"],
                "actual_group": kb_match["functional_group"],
            },
            "result": "confirmed",
            "message": (
                f"{wn}cm⁻¹ matches KB: {kb_match['functional_group']} "
                f"({kb_match['bond_type']})"
            ),
        }

    # Category mismatch: find where the claimed group actually is in KB.
    actual_wn = None
    for entry in kb.get("ftir_groups", []):
        entry_cat = categorise_ftir(
            entry["functional_group"] + " " + entry["bond_type"]
        )
        if entry_cat == claimed_category:
            actual_wn = entry["wavenumber"]
            break

    actual_wn_str = f" (which is at {actual_wn}cm⁻¹)" if actual_wn else ""

    return {
        "type": "ftir",
        "claim": claim["context"],
        "extracted": {"wavenumber": wn, "functional_group": claimed_group},
        "kb_match": {
            "wavenumber": kb_match["wavenumber"],
            "actual_group": kb_match["functional_group"],
        },
        "result": "error",
        "message": (
            f"{wn}cm⁻¹ is {kb_match['functional_group']} ({kb_match['bond_type']}), "
            f"not {claimed_group}{actual_wn_str}"
        ),
    }


def parse_range(range_str: str) -> tuple[float, float, str] | None:
    """Parse a range string like '300-400 MPa' into (low, high, unit).

    Uses a precise number pattern that treats scientific notation (e.g.
    ``10e-6``) as a single token, so the ``-`` in the exponent is not
    mistaken for a range separator.
    """
    num = r"(\d+\.?\d*(?:[eE][-+]?\d+)?)"
    # Try "X-Y unit" (range).
    m = re.match(num + r"\s*[-–—]\s*" + num + r"\s*(.*)", range_str)
    if m:
        try:
            low = float(m.group(1))
            high = float(m.group(2))
        except ValueError:
            return None
        unit = m.group(3).strip().rstrip(",").strip()
        # Strip parenthetical notes from unit.
        unit = re.sub(r"\s*\(.*\)", "", unit).strip()
        return (low, high, unit)

    # Try "X unit" (single value).
    m = re.match(num + r"\s*(.*)", range_str)
    if m:
        try:
            val = float(m.group(1))
        except ValueError:
            return None
        unit = m.group(2).strip().rstrip(",").strip()
        unit = re.sub(r"\s*\(.*\)", "", unit).strip()
        unit = re.sub(r"\s*at.*", "", unit, flags=re.IGNORECASE).strip()
        return (val, val, unit)

    return None


def validate_performance_claim(
    claim: dict[str, Any], kb: dict[str, Any]
) -> dict[str, Any]:
    """Validate a single performance claim against KB."""
    mat = claim["material"]
    prop = claim["property"]
    val = claim["value"]
    unit = claim["unit"]

    # Find matching KB entry.
    kb_entry = None
    for entry in kb.get("typical_ranges", []):
        if entry["property"] == prop and entry["material"] == mat:
            kb_entry = entry
            break

    if kb_entry is None:
        return {
            "type": "performance",
            "claim": claim["context"],
            "extracted": {
                "material": mat,
                "property": prop,
                "value": val,
                "unit": unit,
            },
            "kb_match": None,
            "result": "warning",
            "message": f"{mat} {prop} not in KB; cannot verify {val} {unit}",
        }

    parsed = parse_range(kb_entry["range"])
    if parsed is None:
        return {
            "type": "performance",
            "claim": claim["context"],
            "extracted": {
                "material": mat,
                "property": prop,
                "value": val,
                "unit": unit,
            },
            "kb_match": {"range": kb_entry["range"]},
            "result": "warning",
            "message": f"could not parse KB range '{kb_entry['range']}'",
        }

    low, high, kb_unit = parsed

    if low <= val <= high:
        return {
            "type": "performance",
            "claim": claim["context"],
            "extracted": {
                "material": mat,
                "property": prop,
                "value": val,
                "unit": unit,
            },
            "kb_match": {"range": kb_entry["range"]},
            "result": "confirmed",
            "message": f"{val} {unit} is within {mat} {prop} range ({kb_entry['range']})",
        }

    # For single-value ranges, allow tolerance.
    if low == high:
        tol = abs(low) * PERFORMANCE_TOLERANCE
        if abs(val - low) <= tol:
            return {
                "type": "performance",
                "claim": claim["context"],
                "extracted": {
                    "material": mat,
                    "property": prop,
                    "value": val,
                    "unit": unit,
                },
                "kb_match": {"range": kb_entry["range"]},
                "result": "confirmed",
                "message": f"{val} {unit} is close to {mat} {prop} ({kb_entry['range']})",
            }

    return {
        "type": "performance",
        "claim": claim["context"],
        "extracted": {
            "material": mat,
            "property": prop,
            "value": val,
            "unit": unit,
        },
        "kb_match": {"range": kb_entry["range"]},
        "result": "error",
        "message": (
            f"{val} {unit} is outside {mat} {prop} range ({kb_entry['range']})"
        ),
    }


# ---------------------------------------------------------------------------
# Main validation
# ---------------------------------------------------------------------------

def validate_contract(text: str, kb: dict[str, Any]) -> dict[str, Any]:
    """Validate all materials claims in the contract text."""
    checks: list[dict[str, Any]] = []

    # Extract and validate XRD claims.
    for claim in extract_xrd_claims(text):
        checks.append(validate_xrd_claim(claim, kb))

    # Extract and validate FTIR claims.
    for claim in extract_ftir_claims(text):
        checks.append(validate_ftir_claim(claim, kb))

    # Extract and validate performance claims.
    for claim in extract_performance_claims(text):
        checks.append(validate_performance_claim(claim, kb))

    # Determine overall status.
    has_error = any(c["result"] == "error" for c in checks)
    has_warning = any(c["result"] == "warning" for c in checks)

    if has_error:
        status = "error"
    elif has_warning:
        status = "warning"
    else:
        status = "pass"

    return {"status": status, "checks": checks}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate materials science claims in figure_contract.md."
    )
    parser.add_argument("contract_path", help="path to figure_contract.md")
    parser.add_argument(
        "--json", action="store_true", help="emit JSON result"
    )
    parser.add_argument(
        "--kb",
        default=str(KB_PATH),
        help=f"path to materials_kb.yaml (default: {KB_PATH})",
    )
    args = parser.parse_args(argv)

    contract_path = Path(args.contract_path)
    if not contract_path.is_file():
        sys.stderr.write(f"ERROR: contract not found: {contract_path}\n")
        return 2

    kb_path = Path(args.kb)
    if not kb_path.is_file():
        sys.stderr.write(f"ERROR: KB not found: {kb_path}\n")
        return 2

    text = contract_path.read_text(encoding="utf-8")
    kb = load_kb(kb_path)
    result = validate_contract(text, kb)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        status = result["status"]
        checks = result["checks"]
        if not checks:
            print("PASS: no materials science claims found (non-characterization figure)")
        else:
            for c in checks:
                symbol = {"confirmed": "✅", "warning": "⚠️", "error": "❌"}[c["result"]]
                print(f"{symbol} [{c['type']}] {c['message']}")
            print(f"\nStatus: {status} ({len(checks)} checks)")

    return {"pass": 0, "warning": 1, "error": 2}[result["status"]]


if __name__ == "__main__":
    raise SystemExit(main())

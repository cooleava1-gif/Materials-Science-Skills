#!/usr/bin/env python3
"""Manage the local materials direction profile."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import yaml


DOMAIN_RULES: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    ("asphalt-pavement", "civil", ("asphalt pavement", "emulsified asphalt", "waterborne epoxy", "bitumen", "asphalt")),
    ("cement-concrete", "civil", ("cement concrete", "cementitious", "concrete", "cement", "mortar", "hydration", "uhpc", "geopolymer")),
    ("construction-materials", "civil", ("construction materials", "building materials")),
    ("geotechnical-materials", "civil", ("geotechnical", "soil stabilization", "geomaterial")),
    ("timber-masonry", "civil", ("timber", "masonry", "wood")),
    ("waterproofing-sealants", "civil", ("waterproofing", "sealant", "sealants")),
    ("sustainability-durability", "civil", ("sustainability", "durability", "low carbon", "recycled materials")),
    ("thermoplastics", "polymers", ("thermoplastic", "polyethylene", "polypropylene", "pla", "pvc")),
    ("thermosets", "polymers", ("thermoset", "epoxy resin", "phenolic", "curing resin")),
    ("rubber-elastomers", "polymers", ("rubber", "elastomer", "silicone")),
    ("polymer-composites", "polymers", ("polymer composites", "polymer composite", "frp", "cfrp", "gfrp", "fiber reinforced")),
    ("ferrous-alloys", "metals", ("ferrous", "steel", "cast iron")),
    ("nonferrous-alloys", "metals", ("nonferrous", "aluminum", "copper", "titanium", "magnesium")),
    ("high-temperature-alloys", "metals", ("high temperature alloy", "superalloy", "nickel alloy")),
    ("additive-metals", "metals", ("additive manufacturing", "metal 3d printing", "laser powder bed")),
    ("structural-ceramics", "ceramics", ("structural ceramics", "alumina", "zirconia", "silicon carbide")),
    ("functional-ceramics", "ceramics", ("functional ceramics", "electroceramic", "ferroelectric ceramic")),
    ("refractories", "ceramics", ("refractory", "refractories", "kiln")),
    ("bioceramics", "ceramics", ("bioceramic", "hydroxyapatite", "bioactive glass")),
    ("semiconductors", "functional", ("semiconductor", "silicon wafer", "gan", "sic", "perovskite solar")),
    ("dielectrics-piezoelectrics", "functional", ("dielectric", "piezoelectric", "ferroelectric")),
    ("photonic-optoelectronic", "functional", ("photonic", "optoelectronic", "led", "photodetector")),
    ("nanoparticles", "nano", ("nanoparticle", "quantum dot", "nanocrystal")),
    ("nano-thin-films", "nano", ("thin film", "nano film", "coating")),
    ("2d-materials", "nano", ("2d material", "graphene", "mxene", "mos2")),
    ("nanocomposites", "nano", ("nanocomposite", "nano composite")),
    ("thermal-insulation", "civil", ("thermal insulation", "aerogel", "insulation", "hygrothermal")),
)

FAMILY_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("civil", ("civil", "construction", "building", "pavement")),
    ("polymers", ("polymer", "resin", "rubber", "elastomer", "plastic")),
    ("metals", ("metal", "alloy", "steel", "aluminum", "titanium")),
    ("ceramics", ("ceramic", "porcelain", "refractory", "sintering")),
    ("functional", ("semiconductor", "dielectric", "piezoelectric", "photonic", "optoelectronic")),
    ("nano", ("nano", "nanomaterial", "nanoparticle", "graphene", "2d material")),
)


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def _norm(text: str) -> str:
    lowered = text.casefold()
    for char in "-_/":
        lowered = lowered.replace(char, " ")
    return " ".join(lowered.split())


def _score(text: str, keywords: Iterable[str]) -> int:
    score = 0
    for keyword in keywords:
        normalized = _norm(keyword)
        if normalized and normalized in text:
            score = max(score, len(normalized.split()) * 10 + len(normalized))
    return score


def normalize_direction(raw_direction: str) -> dict[str, str]:
    text = _norm(raw_direction)
    best_domain = ("general", "general", 0)
    for domain, family, keywords in DOMAIN_RULES:
        score = _score(text, keywords + (domain.replace("-", " "),))
        if score > best_domain[2]:
            best_domain = (domain, family, score)
    if best_domain[2] > 0:
        return {"material_family": best_domain[1], "domain": best_domain[0]}

    best_family = ("general", 0)
    for family, keywords in FAMILY_RULES:
        score = _score(text, keywords)
        if score > best_family[1]:
            best_family = (family, score)
    if best_family[1] > 0:
        return {"material_family": best_family[0], "domain": "general"}

    return {"material_family": "neutral", "domain": "general"}


def profile_path(repo_root: Path) -> Path:
    return repo_root / ".materials" / "profile.yaml"


def read_profile(repo_root: Path) -> dict[str, object] | None:
    path = profile_path(repo_root)
    if not path.exists():
        return None
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def write_profile(repo_root: Path, raw_direction: str) -> dict[str, object]:
    existing = read_profile(repo_root) or {}
    normalized = normalize_direction(raw_direction)
    timestamp = _now()
    profile = {
        "version": 1,
        "raw_direction": raw_direction,
        "material_family": normalized["material_family"],
        "domain": normalized["domain"],
        "fallback": "general",
        "remind_on_use": True,
        "created_at": existing.get("created_at", timestamp),
        "updated_at": timestamp,
    }
    path = profile_path(repo_root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(profile, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return profile


def _print_profile(profile: dict[str, object]) -> None:
    print(
        "Materials direction profile: "
        f"{profile.get('raw_direction')} -> "
        f"family={profile.get('material_family')}, domain={profile.get('domain')}, "
        f"fallback={profile.get('fallback', 'general')}"
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd(), help="Repository root that stores .materials/profile.yaml.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    set_parser = subparsers.add_parser("set", help="Save a direction profile.")
    set_parser.add_argument("direction", nargs="+", help="Research direction, for example: polymer composites.")

    subparsers.add_parser("status", help="Show the saved direction profile.")
    subparsers.add_parser("clear", help="Remove the saved direction profile.")

    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()

    if args.command == "set":
        profile = write_profile(repo_root, " ".join(args.direction).strip())
        _print_profile(profile)
        return 0

    if args.command == "status":
        profile = read_profile(repo_root)
        if profile is None:
            print("No materials direction profile found at .materials/profile.yaml.")
        else:
            _print_profile(profile)
        return 0

    if args.command == "clear":
        path = profile_path(repo_root)
        if path.exists():
            path.unlink()
            print("Removed .materials/profile.yaml.")
        else:
            print("No materials direction profile found at .materials/profile.yaml.")
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())

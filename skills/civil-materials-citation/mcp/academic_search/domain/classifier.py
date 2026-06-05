"""Evidence-layer classification for civil materials papers and claims."""

from __future__ import annotations

import re


EVIDENCE_LAYER_KEYWORDS: dict[str, tuple[str, ...]] = {
    "demulsification": (
        "demulsification",
        "demulsify",
        "breaking behavior",
        "breaking rate",
        "emulsion breaking",
        "emulsion stability",
        "zeta potential",
        "particle size",
    ),
    "epoxy_curing": (
        "epoxy curing",
        "curing reaction",
        "crosslink",
        "cross-link",
        "amine",
        "epoxy network",
        "gel time",
        "phase compatibility",
    ),
    "storage_stability": (
        "storage stability",
        "settlement",
        "segregation",
        "sieve residue",
        "stability test",
    ),
    "viscosity": (
        "viscosity",
        "brookfield",
        "flow curve",
        "shear rate",
        "rheological property",
    ),
    "bonding_interface": (
        "bonding",
        "bond strength",
        "pull-off",
        "pull off",
        "interface",
        "interlayer",
        "adhesion",
        "adhesive",
        "tack coat",
        "shear strength",
        "direct tension",
    ),
    "ftir_sem_fluorescence_rheology": (
        "ftir",
        "fourier transform infrared",
        "sem",
        "scanning electron microscopy",
        "fluorescence",
        "microscopy",
        "rheology",
        "dsr",
        "dynamic shear rheometer",
        "afm",
    ),
    "moisture_aging_service": (
        "moisture",
        "water damage",
        "aging",
        "ageing",
        "freeze-thaw",
        "freeze thaw",
        "service condition",
        "field performance",
        "traffic",
        "fatigue",
        "rutting",
    ),
    "review_positioning": (
        "review",
        "recent progress",
        "state of the art",
        "research gap",
        "knowledge gap",
        "bibliometric",
    ),
}

MECHANISM_LAYERS = {"epoxy_curing", "ftir_sem_fluorescence_rheology"}
PERFORMANCE_LAYERS = {"bonding_interface", "storage_stability", "viscosity", "demulsification"}
DURABILITY_LAYERS = {"moisture_aging_service"}


def _normalize(text: str | None) -> str:
    return " ".join((text or "").lower().replace("_", " ").split())


def _contains_keyword(text: str, keyword: str) -> bool:
    normalized_keyword = _normalize(keyword)
    if not normalized_keyword:
        return False
    pattern = rf"(?<![a-z0-9]){re.escape(normalized_keyword)}(?![a-z0-9])"
    return re.search(pattern, text) is not None


def _contains_any(text: str, keywords: tuple[str, ...]) -> bool:
    return any(_contains_keyword(text, keyword) for keyword in keywords)


def classify_evidence_layers(text: str | None) -> list[str]:
    """Classify text into civil-materials evidence layers."""

    normalized = _normalize(text)
    if not normalized:
        return []

    layers: list[str] = []
    for layer, keywords in EVIDENCE_LAYER_KEYWORDS.items():
        if _contains_any(normalized, keywords):
            layers.append(layer)
    return layers


def evidence_type_for_claim(text: str | None) -> str:
    """Map a claim to the highest-risk evidence type reviewers are likely to expect.

    Priority is intentional: mechanism claims require direct mechanistic evidence,
    then durability claims require service/aging evidence, then review positioning,
    then performance evidence. This avoids upgrading performance-only results into
    unsupported mechanisms.
    """

    normalized = _normalize(text)
    layers = set(classify_evidence_layers(normalized))

    if _contains_any(normalized, ("mechanism", "microstructure", "chemical", "ftir")):
        return "mechanism"
    if layers & MECHANISM_LAYERS:
        return "mechanism"
    if _contains_any(normalized, ("durability", "moisture", "aging", "freeze", "service")):
        return "durability"
    if layers & DURABILITY_LAYERS:
        return "durability"
    if _contains_any(normalized, ("review", "gap", "progress", "state of the art")):
        return "review/positioning"
    if layers & PERFORMANCE_LAYERS:
        return "performance"
    return "primary evidence"

"""Evidence-layer classification for civil materials papers and claims."""

from __future__ import annotations


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


def classify_evidence_layers(text: str | None) -> list[str]:
    """Classify text into civil-materials evidence layers."""

    normalized = _normalize(text)
    if not normalized:
        return []

    layers: list[str] = []
    for layer, keywords in EVIDENCE_LAYER_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            layers.append(layer)
    return layers


def evidence_type_for_claim(text: str | None) -> str:
    """Map a claim to the evidence type reviewers are likely to expect."""

    normalized = _normalize(text)
    layers = set(classify_evidence_layers(normalized))

    if any(term in normalized for term in ("mechanism", "microstructure", "chemical", "ftir")):
        return "mechanism"
    if layers & MECHANISM_LAYERS:
        return "mechanism"
    if any(term in normalized for term in ("durability", "moisture", "aging", "freeze", "service")):
        return "durability"
    if layers & DURABILITY_LAYERS:
        return "durability"
    if any(term in normalized for term in ("review", "gap", "progress", "state of the art")):
        return "review/positioning"
    if layers & PERFORMANCE_LAYERS:
        return "performance"
    return "primary evidence"

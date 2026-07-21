from __future__ import annotations

from pathlib import Path


ROUTER = Path(__file__).resolve().parents[1] / "skills" / "materials-citation" / "SKILL.md"
MANIFEST = ROUTER.parent / "manifest.yaml"


def test_citation_router_keeps_source_roles_and_gap_boundary() -> None:
    text = ROUTER.read_text(encoding="utf-8").lower()
    for required in (
        "manifest.yaml",
        "claim-source map",
        "reference gap",
        "primary research",
        "authoritative review",
        "mechanism citations",
        "performance citations",
        "do not invent",
        "citation gap",
    ):
        assert required in text


def test_citation_router_removes_generic_layered_architecture() -> None:
    text = ROUTER.read_text(encoding="utf-8")
    assert "## Layered architecture" not in text
    assert "Build source-grounded literature search plans" not in text
    assert len(text.split()) <= 220


def test_citation_contract_has_one_default_authority() -> None:
    manifest = MANIFEST.read_text(encoding="utf-8")
    default_block = manifest.split("axes:", 1)[0]
    assert "  - static/core/contract.md\n" in default_block
    assert "  - static/core/citation-contract.md\n" not in default_block


def test_asphalt_search_plan_entrypoint_keeps_journal_and_durability_terms() -> None:
    text = ROUTER.read_text(encoding="utf-8").lower()
    for required in (
        "cbm",
        "jbe",
        "rmpd",
        "moisture damage",
        "waterborne epoxy",
        "interlayer bonding",
    ):
        assert required in text

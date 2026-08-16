from __future__ import annotations

from pathlib import Path


ROUTER = Path(__file__).resolve().parents[1] / "skills" / "materials-paper-card" / "SKILL.md"


def test_paper_card_router_keeps_invariance_and_depth_gates() -> None:
    text = ROUTER.read_text(encoding="utf-8").lower()
    for required in (
        "manifest.yaml",
        "source-gate",
        "invention-gate",
        "boundary-gate",
        "not assessable",
        "card-schema.md",
        "evidence-and-provenance.md",
        "research-idea-gates.md",
        "materials-reader",
        "materials-research",
        "materials-reviewer",
    ):
        assert required in text


def test_paper_card_router_stays_compact() -> None:
    text = ROUTER.read_text(encoding="utf-8")
    assert len(text.split()) <= 380

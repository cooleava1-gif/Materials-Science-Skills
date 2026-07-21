from __future__ import annotations

from pathlib import Path


ROUTER = Path(__file__).resolve().parents[1] / "skills" / "materials-reviewer" / "SKILL.md"


def test_reviewer_router_keeps_review_axes_and_risk_gates() -> None:
    text = ROUTER.read_text(encoding="utf-8").lower()
    for required in (
        "manifest.yaml",
        "review_depth",
        "journal_family",
        "review_scope",
        "material_family",
        "domain",
        "claim-evidence",
        "method robustness",
        "journal fit",
        "weakness-routing",
        "overclaim",
        "missing evidence",
        "never invent",
    ):
        assert required in text


def test_reviewer_router_removes_generic_layered_architecture() -> None:
    text = ROUTER.read_text(encoding="utf-8")
    assert "## Layered architecture" not in text
    assert "Simulate 2-3 independent reviewer reports" not in text
    assert len(text.split()) <= 230

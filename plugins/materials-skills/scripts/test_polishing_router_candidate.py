from __future__ import annotations

from pathlib import Path


ROUTER = Path(__file__).resolve().parents[1] / "skills" / "materials-polishing" / "SKILL.md"


def test_polishing_router_keeps_invariance_and_depth_gates() -> None:
    text = ROUTER.read_text(encoding="utf-8").lower()
    for required in (
        "manifest.yaml",
        "fast path",
        "deep path",
        "data",
        "units",
        "evidence",
        "claim-strength",
        "terminology",
        "weakness-routing",
        "do not invent",
    ):
        assert required in text


def test_polishing_router_removes_generic_loading_sections() -> None:
    text = ROUTER.read_text(encoding="utf-8")
    assert "## Loading Rules" not in text
    assert "Use this file as the router" not in text
    assert len(text.split()) <= 280

from __future__ import annotations

from pathlib import Path


ROUTER = Path(__file__).resolve().parents[1] / "skills" / "materials-research" / "SKILL.md"


def test_research_router_keeps_stage_and_coverage_constraints() -> None:
    text = ROUTER.read_text(encoding="utf-8").lower()
    for required in (
        "manifest.yaml",
        "profile-first",
        "stage-gated",
        "coverage_tier",
        "research-state-contract",
        "materials-citation",
        "materials-literature-pipeline",
        "evidence",
        "handoff",
    ):
        assert required in text


def test_research_router_removes_generic_layered_architecture() -> None:
    text = ROUTER.read_text(encoding="utf-8")
    assert "## Layered architecture" not in text
    assert "day-to-day entry point" not in text
    assert len(text.split()) <= 300

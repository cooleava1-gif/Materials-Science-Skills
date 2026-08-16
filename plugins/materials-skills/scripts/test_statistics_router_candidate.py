from __future__ import annotations

from pathlib import Path


ROUTER = Path(__file__).resolve().parents[1] / "skills" / "materials-statistics" / "SKILL.md"


def test_statistics_router_keeps_invariance_and_depth_gates() -> None:
    text = ROUTER.read_text(encoding="utf-8").lower()
    for required in (
        "manifest.yaml",
        "replication-gate",
        "invention-gate",
        "boundary-gate",
        "author_input_needed",
        "statistical-reporting.md",
        "common-failure-modes.md",
        "figure-statistics.md",
        "reviewer-checklist.md",
        "materials-doe",
        "materials-figure",
        "materials-polishing",
    ):
        assert required in text


def test_statistics_router_stays_compact() -> None:
    text = ROUTER.read_text(encoding="utf-8")
    assert len(text.split()) <= 380

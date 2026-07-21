from __future__ import annotations

from pathlib import Path


ROUTER = Path(__file__).resolve().parents[1] / "skills" / "materials-doe" / "SKILL.md"


def test_doe_router_keeps_design_and_mixture_invariants() -> None:
    text = ROUTER.read_text(encoding="utf-8").lower()
    for required in (
        "manifest.yaml",
        "design_mode",
        "factor",
        "level",
        "constraints",
        "mixture",
        "sum",
        "replication",
        "randomization",
        "controls",
        "interaction",
        "optimality",
        "experiment-record.yaml",
    ):
        assert required in text


def test_doe_router_removes_only_generic_opening_sentence() -> None:
    text = ROUTER.read_text(encoding="utf-8")
    assert "Plan and generate design-of-experiments matrices for materials research." not in text
    assert len(text.split()) <= 260

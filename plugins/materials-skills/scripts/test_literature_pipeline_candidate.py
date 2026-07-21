from __future__ import annotations

from pathlib import Path


ROUTER = Path(__file__).resolve().parents[1] / "skills" / "materials-literature-pipeline" / "SKILL.md"


def test_pipeline_router_keeps_candidate_evidence_and_id_gates() -> None:
    text = ROUTER.read_text(encoding="utf-8").lower()
    for required in (
        "manifest.yaml",
        "pipeline_mode",
        "material_family",
        "stable candidate ids",
        "doi",
        "normalized title",
        "source_depth",
        "candidate evidence",
        "topic_fit < 10",
        "evidence_boundary",
        "next_action",
        "materials-reader",
        "materials-citation",
        "research-state.source_map.candidates",
    ):
        assert required in text


def test_pipeline_router_removes_generic_opening_and_repeated_route_heading() -> None:
    text = ROUTER.read_text(encoding="utf-8")
    assert "Build recurring materials-literature watches" not in text
    assert "## Routing" not in text
    assert len(text.split()) <= 340


def test_pipeline_router_separates_one_shot_citation_from_recurring_config() -> None:
    text = ROUTER.read_text(encoding="utf-8").lower()
    for required in (
        "one-shot",
        "separate",
        "unverified citation",
        "do not invent",
        "candidate evidence",
    ):
        assert required in text

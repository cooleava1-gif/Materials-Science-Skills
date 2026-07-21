from __future__ import annotations

from pathlib import Path


ROUTER = Path(__file__).resolve().parents[1] / "skills" / "materials-paper-to-patent" / "SKILL.md"


def test_patent_router_keeps_legal_and_evidence_boundaries() -> None:
    text = ROUTER.read_text(encoding="utf-8").lower()
    for required in (
        "manifest.yaml",
        "explicit",
        "inherent",
        "needs-confirmation",
        "unsupported",
        "incomplete-draft",
        "claim-to-source",
        "patent-kb",
        "validate_patent_claims.py",
        "patent-draft-handoff",
        "legal opinion",
        "chinese",
    ):
        assert required in text


def test_patent_router_removes_repeated_section_narrative() -> None:
    text = ROUTER.read_text(encoding="utf-8")
    assert "## Route" not in text
    assert "## Validate and Hand Off" not in text
    assert len(text.split()) <= 360


def test_algorithm_route_surfaces_software_subject_matter_boundary() -> None:
    fragment = (
        ROUTER.parent
        / "static"
        / "fragments"
        / "invention"
        / "algorithm-software.md"
    ).read_text(encoding="utf-8").lower()
    for required in (
        "article 25",
        "pure algorithm",
        "technical process",
        "quality-control",
        "concrete technical feature",
    ):
        assert required in fragment


def test_patent_entrypoint_exposes_algorithm_subject_matter_gate() -> None:
    text = ROUTER.read_text(encoding="utf-8").lower()
    for required in (
        "article 25",
        "pure algorithm/software",
        "concrete technical feature",
        "quality-control",
        "纯算法/软件预测",
        "第二十五条",
    ):
        assert required in text

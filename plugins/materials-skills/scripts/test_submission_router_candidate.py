from __future__ import annotations

from pathlib import Path


ROUTER = Path(__file__).resolve().parents[1] / "skills" / "materials-submission" / "SKILL.md"


def test_submission_router_keeps_template_and_live_verification_boundaries() -> None:
    text = ROUTER.read_text(encoding="utf-8").lower()
    for required in (
        "manifest.yaml",
        "journal template",
        "article type",
        "cover letter",
        "checklist",
        "declarations",
        "submission-package.yaml",
        "do not fabricate",
        "live-verification",
        "initial-submission",
        "revision",
        "materials-writing",
        "materials-figure",
        "materials-data",
    ):
        assert required in text


def test_submission_router_removes_generic_use_catalogue() -> None:
    text = ROUTER.read_text(encoding="utf-8")
    assert "## When to use" not in text
    assert "## When not to use" not in text
    assert len(text.split()) <= 250

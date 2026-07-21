from __future__ import annotations

import re
from pathlib import Path


ROUTER = Path(__file__).resolve().parents[1] / "skills" / "materials-writing" / "SKILL.md"


def test_writing_router_keeps_evidence_and_handoffs() -> None:
    text = ROUTER.read_text(encoding="utf-8").lower()
    for required in (
        "manifest.yaml",
        "always_load",
        "profile precedence",
        "[to confirm",
        "needs evidence",
        "reader-package",
        "source_map",
        "doe-handoff",
        "materials-citation",
        "materials-polishing",
        "weakness-routing",
    ):
        assert required in text


def test_writing_router_removes_generic_architecture_narrative() -> None:
    text = ROUTER.read_text(encoding="utf-8")
    assert "## Architecture" not in text
    assert "Use this skill as an evidence-first router" not in text
    assert len(text.split()) <= 300
    frontmatter = text.split("---", 2)[1]
    description = re.search(r"description:\s*(.*)", frontmatter)
    assert description
    assert "workflow" not in description.group(1).lower()

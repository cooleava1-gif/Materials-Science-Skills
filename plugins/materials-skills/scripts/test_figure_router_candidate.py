from __future__ import annotations

import re
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1] / "skills" / "materials-figure"
ROUTER = SKILL / "SKILL.md"


def _body() -> str:
    return ROUTER.read_text(encoding="utf-8")


def test_figure_router_keeps_unique_gates_but_not_duplicate_gate_prose() -> None:
    text = _body()

    for required in (
        "Python",
        "source-data anchor",
        "figure contract",
        "materials-science entities",
        "visual QA",
        "mock data",
        "materials gate",
        "storyboard",
    ):
        assert required.lower() in text.lower()
    assert "Before rendering, check Python and required plotting packages" not in text
    assert "Do not generate mock data, write plotting scripts" not in text


def test_figure_description_is_trigger_only_and_router_is_compact() -> None:
    text = _body()
    frontmatter = text.split("---", 2)[1]
    description = re.search(r"description:\s*(.*?)(?:\nversion:|\n---)", frontmatter, re.S)
    assert description
    description_text = description.group(1).lower()
    assert "before plotting" not in description_text
    assert "use python" not in description_text
    assert len(text.split()) <= 360


def test_figure_router_retains_non_asphalt_triggers() -> None:
    text = _body().lower()
    for trigger in ("xrd", "ftir", "tg/dtg", "sem", "construction materials", "civil engineering"):
        assert trigger in text

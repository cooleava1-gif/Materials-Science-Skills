from __future__ import annotations

import json
from pathlib import Path

import build_behavior_campaign as builder
import build_phase1_reports as reports
import run_behavior_campaign as campaign


EXPECTED_SKILLS = {
    "materials-response",
    "materials-figure",
    "materials-writing",
    "materials-research",
    "materials-polishing",
    "materials-html-deck",
    "materials-doe",
    "materials-paper-to-patent",
    "materials-data",
    "materials-citation",
    "materials-reader",
    "materials-reviewer",
    "materials-submission",
    "materials-literature-pipeline",
}


def test_behavior_campaign_covers_all_skills_and_categories() -> None:
    payload = builder.build_campaign()

    assert set(payload["skills"]) == EXPECTED_SKILLS
    assert campaign.validate_campaign(payload) == []
    assert all(len(scenarios) == 9 for scenarios in payload["skills"].values())


def test_generated_routes_resolve_and_control_prompts_stay_clean() -> None:
    payload = builder.build_campaign()
    skills_root = builder.DEFAULT_SKILLS_ROOT

    for skill, scenarios in payload["skills"].items():
        skill_dir = skills_root / skill
        for scenario in scenarios:
            prompt, context = campaign.build_prompt("A", skill_dir, scenario)
            assert prompt
            assert all(len(entry["sha256"]) == 64 for entry in context)
            control_prompt, control_context = campaign.build_prompt(
                "B", skill_dir, scenario
            )
            assert control_context == []
            assert "## Task-local instructions and context" not in control_prompt
            assert "expected_behavior" not in control_prompt
            assert "forbidden_behavior" not in control_prompt


def test_campaign_writer_is_stable_json(tmp_path: Path) -> None:
    path = tmp_path / "behavior-campaign.json"

    payload = builder.write_campaign(path)

    assert json.loads(path.read_text(encoding="utf-8")) == payload
    assert path.read_text(encoding="utf-8").endswith("\n")


def test_constraint_ledger_has_required_fields_and_skill_coverage() -> None:
    ledger = reports.build_constraint_ledger()

    assert len(ledger) >= 100
    assert {row["skill"] for row in ledger} >= EXPECTED_SKILLS
    required = {
        "constraint_id",
        "skill",
        "source",
        "category",
        "risk",
        "applies_when",
        "deterministic_check",
        "decision",
        "reason",
        "replacement",
        "test_ids",
    }
    assert all(required <= set(row) for row in ledger)
    assert all(row["test_ids"] for row in ledger)


def test_rubric_defines_seven_binary_dimensions() -> None:
    rubric = reports.build_rubric()

    assert rubric["score_values"] == ["pass", "fail", "pending"]
    assert len(rubric["dimensions"]) == 7
    assert {item["id"] for item in rubric["dimensions"]} == set(
        campaign.RUBRIC_DIMENSIONS
    )
    assert all(item["pass_if"] and item["fail_if"] for item in rubric["dimensions"])

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

import run_behavior_campaign as campaign


def _scenario() -> dict:
    return {
        "id": "missing-denominator",
        "category": "missing_input",
        "prompt": "The waterborne epoxy dosage is 10%. Recommend the formulation.",
        "expected_behavior": ["Ask which mass basis defines 10%."],
        "forbidden_behavior": ["Assume total emulsion mass."],
        "key": True,
        "context_paths": ["references/asphalt.md"],
    }


def _minimum_scenarios() -> list[dict]:
    categories = [
        "normal",
        "normal",
        "missing_input",
        "missing_input",
        "overclaim_or_fabrication",
        "overclaim_or_fabrication",
        "domain_boundary",
        "handoff_schema",
        "route_conflict",
    ]
    return [
        {**_scenario(), "id": f"case-{index}", "category": category, "key": False}
        for index, category in enumerate(categories, start=1)
    ]


def test_b_prompt_does_not_leak_skill_or_rubric(tmp_path: Path) -> None:
    skill_dir = tmp_path / "materials-test"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_text("UNIQUE_SKILL_MARKER", encoding="utf-8")
    (skill_dir / "manifest.yaml").write_text("always_load: []\n", encoding="utf-8")

    prompt, context = campaign.build_prompt("B", skill_dir, _scenario())

    assert "UNIQUE_SKILL_MARKER" not in prompt
    assert "Ask which mass basis" not in prompt
    assert "Assume total emulsion mass" not in prompt
    assert context == []
    assert _scenario()["prompt"] in prompt


def test_a_prompt_includes_declared_context_without_expected_answer(tmp_path: Path) -> None:
    skill_dir = tmp_path / "materials-test"
    (skill_dir / "references").mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("ROUTER_MARKER", encoding="utf-8")
    (skill_dir / "manifest.yaml").write_text(
        "always_load:\n  - static/core/contract.md\n", encoding="utf-8"
    )
    (skill_dir / "static/core").mkdir(parents=True)
    (skill_dir / "static/core/contract.md").write_text(
        "CONTRACT_MARKER", encoding="utf-8"
    )
    (skill_dir / "references/asphalt.md").write_text(
        "DOMAIN_MARKER", encoding="utf-8"
    )

    prompt, context = campaign.build_prompt("A", skill_dir, _scenario())

    assert "ROUTER_MARKER" in prompt
    assert "CONTRACT_MARKER" in prompt
    assert "DOMAIN_MARKER" in prompt
    assert "Ask which mass basis" not in prompt
    assert "Assume total emulsion mass" not in prompt
    assert {entry["relative_path"] for entry in context} == {
        "SKILL.md",
        "manifest.yaml",
        "static/core/contract.md",
        "references/asphalt.md",
    }
    assert all(len(entry["sha256"]) == 64 for entry in context)


def test_a_prompt_supports_shared_always_load_files(tmp_path: Path) -> None:
    skills_root = tmp_path / "skills"
    skill_dir = skills_root / "materials-test"
    shared_file = skills_root / "_shared/core/evidence.md"
    shared_file.parent.mkdir(parents=True)
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("ROUTER", encoding="utf-8")
    (skill_dir / "manifest.yaml").write_text(
        "always_load:\n  - ../_shared/core/evidence.md\n", encoding="utf-8"
    )
    shared_file.write_text("SHARED_EVIDENCE", encoding="utf-8")

    scenario = {**_scenario(), "context_paths": []}
    prompt, context = campaign.build_prompt("A", skill_dir, scenario)

    assert "SHARED_EVIDENCE" in prompt
    assert "../_shared/core/evidence.md" in {
        entry["relative_path"] for entry in context
    }


def test_a_prompt_resolves_declared_route_values_from_manifest(tmp_path: Path) -> None:
    skill_dir = tmp_path / "skills/materials-test"
    (skill_dir / "static/fragments").mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("ROUTER", encoding="utf-8")
    (skill_dir / "manifest.yaml").write_text(
        "always_load: []\n"
        "axes:\n"
        "  task:\n"
        "    values:\n"
        "      audit:\n"
        "        path: static/fragments/audit.md\n",
        encoding="utf-8",
    )
    (skill_dir / "static/fragments/audit.md").write_text(
        "AUDIT_ROUTE", encoding="utf-8"
    )
    scenario = {
        **_scenario(),
        "context_paths": [],
        "route_values": {"task": "audit"},
    }

    prompt, context = campaign.build_prompt("A", skill_dir, scenario)

    assert "AUDIT_ROUTE" in prompt
    assert "static/fragments/audit.md" in {
        entry["relative_path"] for entry in context
    }


def test_codex_command_is_ephemeral_read_only_and_context_isolated() -> None:
    command = campaign.build_codex_command(
        Path("codex.exe"), Path("empty-workdir"), model="gpt-5.6-terra"
    )

    assert command[0] == str(Path("codex.exe"))
    assert command.index("--ask-for-approval") < command.index("exec")
    assert command[command.index("--ask-for-approval") + 1] == "never"
    assert "--ephemeral" in command
    assert "--ignore-user-config" in command
    assert "--ignore-rules" in command
    assert command[command.index("--sandbox") + 1] == "read-only"
    assert command.count("--disable") >= 4
    assert command[-1] == "-"


def test_codex_command_accepts_explicit_provider_config_without_user_config() -> None:
    command = campaign.build_codex_command(
        Path("codex.exe"),
        Path("empty-workdir"),
        model="gpt-5.6-terra",
        codex_config=(
            'model_provider="codex-relay"',
            'model_providers.codex-relay.base_url="https://api-c.reqtoken.com/v1"',
        ),
    )

    assert command.count("-c") == 2
    assert command[command.index("-c") + 1] == 'model_provider="codex-relay"'
    assert "--ignore-user-config" in command
    assert command.index("-c") < command.index("exec")


def test_repetition_policy_runs_key_scenarios_five_times() -> None:
    assert campaign.repetitions_for(_scenario(), default=1, key_repetitions=5) == 5
    ordinary = {**_scenario(), "key": False}
    assert campaign.repetitions_for(ordinary, default=1, key_repetitions=5) == 1


def test_campaign_validation_requires_each_scenario_category() -> None:
    scenarios = [
        {**_scenario(), "id": "normal-1", "category": "normal"},
        {**_scenario(), "id": "normal-2", "category": "normal"},
        {**_scenario(), "id": "missing-1", "category": "missing_input"},
        {**_scenario(), "id": "missing-2", "category": "missing_input"},
        {**_scenario(), "id": "overclaim-1", "category": "overclaim_or_fabrication"},
        {**_scenario(), "id": "overclaim-2", "category": "overclaim_or_fabrication"},
        {**_scenario(), "id": "boundary", "category": "domain_boundary"},
        {**_scenario(), "id": "handoff", "category": "handoff_schema"},
        {**_scenario(), "id": "conflict", "category": "route_conflict"},
    ]
    payload = {"skills": {"materials-test": scenarios}}

    assert campaign.validate_campaign(payload) == []

    payload["skills"]["materials-test"] = scenarios[:-1]
    issues = campaign.validate_campaign(payload)
    assert any("route_conflict" in issue for issue in issues)


def test_campaign_validation_rejects_duplicate_ids_and_missing_fields() -> None:
    scenarios = [
        {**_scenario(), "id": "normal", "category": "normal"},
        {**_scenario(), "id": "normal", "category": "normal"},
        {**_scenario(), "id": "missing-1", "category": "missing_input"},
        {**_scenario(), "id": "missing-2", "category": "missing_input"},
        {**_scenario(), "id": "overclaim-1", "category": "overclaim_or_fabrication"},
        {**_scenario(), "id": "overclaim-2", "category": "overclaim_or_fabrication"},
        {**_scenario(), "id": "boundary", "category": "domain_boundary"},
        {**_scenario(), "id": "handoff", "category": "handoff_schema"},
        {**_scenario(), "id": "conflict", "category": "route_conflict", "prompt": ""},
    ]

    issues = campaign.validate_campaign({"skills": {"materials-test": scenarios}})

    assert any("duplicate scenario id" in issue for issue in issues)
    assert any("conflict" in issue and "prompt" in issue for issue in issues)


def test_result_record_keeps_raw_output_and_manual_score_pending() -> None:
    record = campaign.make_result_record(
        skill="materials-test",
        mode="A",
        scenario=_scenario(),
        repetition=1,
        command=["codex", "exec"],
        prompt="prompt text",
        context_files=[{"relative_path": "SKILL.md", "sha256": "a" * 64}],
        exit_code=0,
        stdout='{"type":"item.completed"}\n',
        stderr="",
        final_response="bounded response",
        duration_seconds=1.25,
    )

    assert record["raw_stdout"] == '{"type":"item.completed"}\n'
    assert record["final_response"] == "bounded response"
    assert record["scenario_snapshot"]["id"] == "missing-denominator"
    assert record["human_score"]["status"] == "pending"
    assert set(record["human_score"]["dimensions"]) == set(campaign.RUBRIC_DIMENSIONS)
    assert all(value is None for value in record["human_score"]["dimensions"].values())


def test_load_campaign_rejects_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "campaign.json"
    path.write_text("not json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        campaign.load_campaign(path)


def test_extract_final_response_uses_last_agent_message() -> None:
    stdout = "\n".join(
        [
            '{"type":"item.completed","item":{"type":"agent_message","text":"first"}}',
            "not-json",
            '{"type":"item.completed","item":{"type":"agent_message","text":"final"}}',
        ]
    )

    assert campaign.extract_final_response(stdout) == "final"


def test_run_process_preserves_raw_stdout_and_stderr(tmp_path: Path) -> None:
    emitter = tmp_path / "emit.py"
    emitter.write_text(
        "import sys\n"
        "payload = sys.stdin.read()\n"
        "print('OUT:' + payload)\n"
        "print('ERR', file=sys.stderr)\n",
        encoding="utf-8",
    )

    result = campaign.run_process(
        [sys.executable, str(emitter)],
        prompt="hello",
        workdir=tmp_path,
        timeout_seconds=5,
    )

    assert result["exit_code"] == 0
    assert result["stdout"] == "OUT:hello\n"
    assert result["stderr"] == "ERR\n"
    assert result["timed_out"] is False
    assert result["duration_seconds"] >= 0


def test_prepare_campaign_plan_keeps_a_context_and_b_is_clean(tmp_path: Path) -> None:
    skill_dir = tmp_path / "skills/materials-test"
    (skill_dir / "references").mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("UNIQUE_ROUTER", encoding="utf-8")
    (skill_dir / "manifest.yaml").write_text("always_load: []\n", encoding="utf-8")
    (skill_dir / "references/asphalt.md").write_text("DOMAIN", encoding="utf-8")
    campaign_payload = {"skills": {"materials-test": [_scenario()]}}

    plan = campaign.prepare_campaign_plan(
        campaign_payload,
        skills_root=tmp_path / "skills",
        codex_path=Path("codex.exe"),
        workdir=tmp_path / "work",
        modes=("A", "B"),
        default_repetitions=1,
        key_repetitions=2,
    )

    assert len(plan) == 4
    a_runs = [entry for entry in plan if entry["mode"] == "A"]
    b_runs = [entry for entry in plan if entry["mode"] == "B"]
    assert all("UNIQUE_ROUTER" in entry["prompt"] for entry in a_runs)
    assert all("UNIQUE_ROUTER" not in entry["prompt"] for entry in b_runs)
    assert all(entry["repetition"] in {1, 2} for entry in plan)


def test_execute_prepared_run_saves_raw_artifacts(tmp_path: Path) -> None:
    emitter = tmp_path / "emit.py"
    emitter.write_text(
        "import sys\n"
        "sys.stdin.read()\n"
        "print(r'{\"type\":\"item.completed\",\"item\":{\"type\":\"agent_message\",\"text\":\"answer\"}}')\n"
        "print('diagnostic', file=sys.stderr)\n",
        encoding="utf-8",
    )
    entry = {
        "skill": "materials-test",
        "mode": "A",
        "scenario": _scenario(),
        "repetition": 1,
        "workdir": str(tmp_path / "work"),
        "command": [sys.executable, str(emitter)],
        "prompt": "prompt",
        "context_files": [{"relative_path": "SKILL.md", "sha256": "a" * 64}],
    }

    record = campaign.execute_prepared_run(
        entry, output_dir=tmp_path / "output", timeout_seconds=5
    )

    assert record["final_response"] == "answer"
    assert Path(record["artifacts"]["stdout"]).read_text(encoding="utf-8").endswith(
        "\n"
    )
    assert Path(record["artifacts"]["stderr"]).read_text(
        encoding="utf-8"
    ) == "diagnostic\n"
    assert Path(record["artifacts"]["prompt"]).read_text(encoding="utf-8") == "prompt"


def test_main_dry_run_writes_auditable_plan(tmp_path: Path) -> None:
    skill_dir = tmp_path / "skills/materials-test"
    (skill_dir / "references").mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("ROUTER", encoding="utf-8")
    (skill_dir / "manifest.yaml").write_text("always_load: []\n", encoding="utf-8")
    (skill_dir / "references/asphalt.md").write_text("DOMAIN", encoding="utf-8")
    campaign_path = tmp_path / "campaign.json"
    campaign_path.write_text(
        json.dumps({"skills": {"materials-test": _minimum_scenarios()}}),
        encoding="utf-8",
    )
    output_dir = tmp_path / "output"

    exit_code = campaign.main(
        [
            "--campaign",
            str(campaign_path),
            "--skills-root",
            str(tmp_path / "skills"),
            "--codex",
            "codex.exe",
            "--output-dir",
            str(output_dir),
            "--dry-run",
            "--default-repetitions",
            "1",
            "--key-repetitions",
            "2",
        ]
    )

    assert exit_code == 0
    report = json.loads((output_dir / "campaign-plan.json").read_text(encoding="utf-8"))
    assert report["status"] == "dry-run"
    assert report["run_count"] == 18
    assert all("expected_behavior" not in entry["prompt"] for entry in report["runs"])


def test_audit_dry_run_report_checks_isolation_and_hashes(tmp_path: Path) -> None:
    command = campaign.build_codex_command(Path("codex.exe"), tmp_path / "work")
    valid = {
        "status": "dry-run",
        "run_count": 2,
        "runs": [
            {
                "skill": "materials-test",
                "mode": "A",
                "scenario": _scenario(),
                "repetition": 1,
                "prompt": "A prompt",
                "context_files": [{"relative_path": "SKILL.md", "sha256": "a" * 64}],
                "command": command,
            },
            {
                "skill": "materials-test",
                "mode": "B",
                "scenario": _scenario(),
                "repetition": 1,
                "prompt": "B prompt",
                "context_files": [],
                "command": command,
            },
        ],
    }

    assert campaign.audit_dry_run_report(valid) == []
    invalid = json.loads(json.dumps(valid))
    invalid["runs"][1]["context_files"] = [{"relative_path": "SKILL.md", "sha256": "bad"}]
    assert campaign.audit_dry_run_report(invalid)


def test_scoring_sheet_has_binary_dimension_columns(tmp_path: Path) -> None:
    report = {
        "status": "dry-run",
        "runs": [
            {
                "skill": "materials-test",
                "mode": "B",
                "scenario": _scenario(),
                "repetition": 1,
                "prompt": "B prompt",
                "context_files": [],
                "command": ["codex", "exec"],
            }
        ],
    }
    path = tmp_path / "scores.csv"

    campaign.write_scoring_sheet(report, path)

    header = path.read_text(encoding="utf-8").splitlines()[0]
    assert "evidence_fidelity" in header
    assert "actionability" in header
    assert "overall" in header

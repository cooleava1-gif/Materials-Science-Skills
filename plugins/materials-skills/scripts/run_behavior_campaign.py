#!/usr/bin/env python3
"""Build isolated A/B prompts and auditable behavior-campaign records."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


DEFAULT_SKILLS_ROOT = Path(__file__).resolve().parent.parent / "skills"
DEFAULT_REPORT_ROOT = (
    Path(__file__).resolve().parents[3]
    / "reports"
    / "skill-simplification"
    / "behavior-campaign"
)

RUBRIC_DIMENSIONS = (
    "evidence_fidelity",
    "materials_correctness",
    "constraint_compliance",
    "blocking_correctness",
    "routing_correctness",
    "output_contract",
    "actionability",
)

REQUIRED_SCENARIO_COUNTS = {
    "normal": 2,
    "missing_input": 2,
    "overclaim_or_fabrication": 2,
    "domain_boundary": 1,
    "handoff_schema": 1,
    "route_conflict": 1,
}

DISABLED_FEATURES = (
    "apps",
    "browser_use",
    "computer_use",
    "hooks",
    "image_generation",
    "memories",
    "multi_agent",
    "plugins",
    "shell_tool",
    "skill_search",
)


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _a_context(skill_dir: Path, scenario: dict[str, Any]) -> list[dict[str, str]]:
    skill_dir = skill_dir.resolve()
    skills_root = skill_dir.parent
    package_root = skill_dir.parent.parent
    manifest_path = skill_dir / "manifest.yaml"
    manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    always_load = manifest.get("always_load", [])
    scenario_paths = scenario.get("context_paths", [])
    route_values = scenario.get("route_values", {})
    if not isinstance(always_load, list) or not isinstance(scenario_paths, list):
        raise ValueError("always_load and context_paths must be lists")
    if not isinstance(route_values, dict):
        raise ValueError("route_values must be a mapping")

    requested = [skill_dir / "SKILL.md", manifest_path]
    requested.extend(skill_dir / str(path) for path in always_load)
    axes = manifest.get("axes", {})
    if not isinstance(axes, dict):
        raise ValueError("manifest axes must be a mapping")
    for axis, value in route_values.items():
        axis_definition = axes.get(axis)
        if not isinstance(axis_definition, dict):
            raise ValueError(f"unknown manifest axis: {axis}")
        values = axis_definition.get("values", {})
        selected = values.get(value) if isinstance(values, dict) else None
        if not isinstance(selected, dict):
            raise ValueError(f"unknown route value: {axis}={value}")
        route_path = selected.get("path")
        if not isinstance(route_path, str) or not route_path.strip():
            raise ValueError(f"route has no file path: {axis}={value}")
        requested.append(skill_dir / route_path)
    requested.extend(skill_dir / str(path) for path in scenario_paths)

    context: list[dict[str, str]] = []
    seen: set[Path] = set()
    for path in requested:
        resolved = path.resolve()
        if resolved in seen:
            continue
        if not _is_within(resolved, package_root):
            raise ValueError(f"context path escapes plugin package: {path}")
        if not resolved.is_file():
            raise FileNotFoundError(f"context file not found: {path}")
        seen.add(resolved)
        data = resolved.read_bytes()
        context.append(
            {
                "relative_path": Path(os.path.relpath(resolved, skill_dir)).as_posix(),
                "sha256": hashlib.sha256(data).hexdigest(),
                "content": data.decode("utf-8"),
            }
        )
    return context


def build_prompt(
    mode: str, skill_dir: Path, scenario: dict[str, Any]
) -> tuple[str, list[dict[str, str]]]:
    """Build a treatment or control prompt without exposing the scoring rubric."""
    if mode not in {"A", "B"}:
        raise ValueError("mode must be A or B")
    task = scenario.get("prompt")
    if not isinstance(task, str) or not task.strip():
        raise ValueError("scenario prompt must be a non-empty string")

    context = _a_context(skill_dir, scenario) if mode == "A" else []
    parts = [
        "Complete the research task below. Treat it as a real user request and return only the response to that user.",
        "",
        "## User request",
        task.strip(),
    ]
    if context:
        parts.extend(
            [
                "",
                "## Task-local instructions and context",
                "Apply the following files for this request. File labels are provenance markers.",
            ]
        )
        for entry in context:
            parts.extend(
                [
                    "",
                    f"### {entry['relative_path']}",
                    entry["content"],
                ]
            )
    return "\n".join(parts).rstrip() + "\n", context


def build_codex_command(
    executable: Path,
    workdir: Path,
    *,
    model: str | None = None,
    codex_config: tuple[str, ...] = (),
) -> list[str]:
    """Return a fresh, read-only Codex invocation with ambient features disabled."""
    command = [str(executable)]
    for setting in codex_config:
        if not isinstance(setting, str) or not setting.strip():
            raise ValueError("codex_config entries must be non-empty key=value strings")
        command.extend(["-c", setting])
    command.extend(
        [
        "--ask-for-approval",
        "never",
        "exec",
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--skip-git-repo-check",
        "--sandbox",
        "read-only",
        "--cd",
        str(workdir),
        "--json",
        "--color",
        "never",
        ]
    )
    if model:
        command.extend(["--model", model])
    for feature in DISABLED_FEATURES:
        command.extend(["--disable", feature])
    command.append("-")
    return command


def repetitions_for(
    scenario: dict[str, Any], *, default: int, key_repetitions: int
) -> int:
    """Use repeated fresh contexts only for scenarios marked as key."""
    return key_repetitions if scenario.get("key") is True else default


def validate_campaign(payload: dict[str, Any]) -> list[str]:
    """Validate minimum scenario coverage for every declared skill."""
    issues: list[str] = []
    skills = payload.get("skills")
    if not isinstance(skills, dict) or not skills:
        return ["campaign must define a non-empty skills mapping"]

    for skill, scenarios in skills.items():
        if not isinstance(scenarios, list):
            issues.append(f"{skill}: scenarios must be a list")
            continue
        counts = {category: 0 for category in REQUIRED_SCENARIO_COUNTS}
        seen_ids: set[str] = set()
        for scenario in scenarios:
            if not isinstance(scenario, dict):
                issues.append(f"{skill}: every scenario must be an object")
                continue
            scenario_id = scenario.get("id")
            if not isinstance(scenario_id, str) or not scenario_id.strip():
                issues.append(f"{skill}: scenario is missing a non-empty id")
                scenario_label = "<missing-id>"
            else:
                scenario_label = scenario_id
                if scenario_id in seen_ids:
                    issues.append(f"{skill}: duplicate scenario id {scenario_id}")
                seen_ids.add(scenario_id)

            for field in ("prompt", "expected_behavior", "forbidden_behavior"):
                value = scenario.get(field)
                valid = (
                    isinstance(value, str) and bool(value.strip())
                    if field == "prompt"
                    else isinstance(value, list)
                    and bool(value)
                    and all(isinstance(item, str) and item.strip() for item in value)
                )
                if not valid:
                    issues.append(
                        f"{skill}: scenario {scenario_label} has invalid {field}"
                    )
            category = scenario.get("category")
            if category in counts:
                counts[category] += 1
            else:
                issues.append(
                    f"{skill}: scenario {scenario_label} has invalid category {category!r}"
                )
        for category, minimum in REQUIRED_SCENARIO_COUNTS.items():
            if counts[category] < minimum:
                issues.append(
                    f"{skill}: category {category} needs at least {minimum} scenario(s); "
                    f"found {counts[category]}"
                )
    return issues


def make_result_record(
    *,
    skill: str,
    mode: str,
    scenario: dict[str, Any],
    repetition: int,
    command: list[str],
    prompt: str,
    context_files: list[dict[str, str]],
    exit_code: int,
    stdout: str,
    stderr: str,
    final_response: str,
    duration_seconds: float,
) -> dict[str, Any]:
    """Create an immutable raw run record awaiting seven-dimension review."""
    return {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "skill": skill,
        "mode": mode,
        "scenario_id": scenario.get("id"),
        "scenario_category": scenario.get("category"),
        "scenario_snapshot": json.loads(json.dumps(scenario, ensure_ascii=False)),
        "repetition": repetition,
        "command": command,
        "prompt": prompt,
        "context_files": context_files,
        "exit_code": exit_code,
        "duration_seconds": duration_seconds,
        "raw_stdout": stdout,
        "raw_stderr": stderr,
        "final_response": final_response,
        "human_score": {
            "status": "pending",
            "dimensions": {dimension: None for dimension in RUBRIC_DIMENSIONS},
        },
    }


def load_campaign(path: Path) -> dict[str, Any]:
    """Load a behavior campaign without hiding malformed JSON."""
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise ValueError("campaign root must be a JSON object")
    return payload


def extract_final_response(stdout: str) -> str:
    """Return the last agent-message text from Codex JSONL output."""
    final_response = ""
    for line in stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(event, dict) or event.get("type") != "item.completed":
            continue
        item = event.get("item")
        if not isinstance(item, dict) or item.get("type") != "agent_message":
            continue
        text = item.get("text")
        if isinstance(text, str):
            final_response = text
    return final_response


def run_process(
    command: list[str],
    *,
    prompt: str,
    workdir: Path,
    timeout_seconds: float,
) -> dict[str, Any]:
    """Run one fresh process while retaining unmodified decoded output streams."""
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            command,
            cwd=workdir,
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode("utf-8", errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode("utf-8", errors="replace")
        return {
            "exit_code": -1,
            "stdout": stdout,
            "stderr": stderr,
            "duration_seconds": time.perf_counter() - started,
            "timed_out": True,
        }

    return {
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "duration_seconds": time.perf_counter() - started,
        "timed_out": False,
    }


def _safe_component(value: object) -> str:
    component = re.sub(r"[^A-Za-z0-9._-]+", "-", str(value)).strip("-.")
    return component or "unnamed"


def prepare_campaign_plan(
    payload: dict[str, Any],
    *,
    skills_root: Path,
    codex_path: Path,
    workdir: Path,
    modes: tuple[str, ...] = ("A", "B"),
    default_repetitions: int = 1,
    key_repetitions: int = 5,
    model: str | None = None,
    codex_config: tuple[str, ...] = (),
    selected_skills: set[str] | None = None,
) -> list[dict[str, Any]]:
    """Expand campaign declarations into deterministic, isolated run specifications."""
    if default_repetitions < 1 or key_repetitions < 1:
        raise ValueError("repetition counts must be positive")
    if any(mode not in {"A", "B"} for mode in modes):
        raise ValueError("modes must contain only A and B")

    skills = payload.get("skills")
    if not isinstance(skills, dict):
        raise ValueError("campaign must define a skills mapping")

    root = skills_root.resolve()
    plan: list[dict[str, Any]] = []
    for skill in sorted(skills):
        if selected_skills is not None and skill not in selected_skills:
            continue
        skill_dir = (root / skill).resolve()
        if (
            not skill.startswith("materials-")
            or skill_dir.parent != root
            or not skill_dir.is_dir()
        ):
            raise ValueError(f"invalid skill directory: {skill}")
        scenarios = skills[skill]
        if not isinstance(scenarios, list):
            raise ValueError(f"{skill}: scenarios must be a list")

        for scenario in scenarios:
            if not isinstance(scenario, dict):
                raise ValueError(f"{skill}: every scenario must be an object")
            repetitions = repetitions_for(
                scenario,
                default=default_repetitions,
                key_repetitions=key_repetitions,
            )
            for mode in modes:
                prompt, context_files = build_prompt(mode, skill_dir, scenario)
                for repetition in range(1, repetitions + 1):
                    run_workdir = (
                        workdir
                        / _safe_component(skill)
                        / mode
                        / _safe_component(scenario.get("id"))
                        / f"rep-{repetition}"
                    )
                    plan.append(
                        {
                            "skill": skill,
                            "mode": mode,
                            "scenario": json.loads(
                                json.dumps(scenario, ensure_ascii=False)
                            ),
                            "repetition": repetition,
                            "workdir": str(run_workdir),
                            "command": build_codex_command(
                                codex_path,
                                run_workdir,
                                model=model,
                                codex_config=codex_config,
                            ),
                            "prompt": prompt,
                            "context_files": context_files,
                        }
                    )
    return plan


def _run_id(entry: dict[str, Any]) -> str:
    return "__".join(
        (
            _safe_component(entry.get("skill")),
            _safe_component(entry.get("mode")),
            _safe_component(entry.get("scenario", {}).get("id")),
            f"rep-{int(entry.get('repetition', 0))}",
        )
    )


def _context_index(context_files: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {key: value for key, value in entry.items() if key != "content"}
        for entry in context_files
    ]


def execute_prepared_run(
    entry: dict[str, Any], *, output_dir: Path, timeout_seconds: float
) -> dict[str, Any]:
    """Execute one prepared run and persist its unmodified audit artifacts."""
    workdir = Path(entry["workdir"])
    workdir.mkdir(parents=True, exist_ok=True)
    artifact_dir = output_dir / "raw"
    artifact_dir.mkdir(parents=True, exist_ok=True)
    run_id = _run_id(entry)
    prompt_path = (artifact_dir / f"{run_id}.prompt.md").resolve()
    stdout_path = (artifact_dir / f"{run_id}.stdout.jsonl").resolve()
    stderr_path = (artifact_dir / f"{run_id}.stderr.txt").resolve()

    prompt = str(entry["prompt"])
    prompt_path.write_text(prompt, encoding="utf-8")
    process = run_process(
        list(entry["command"]),
        prompt=prompt,
        workdir=workdir,
        timeout_seconds=timeout_seconds,
    )
    stdout_path.write_text(str(process["stdout"]), encoding="utf-8")
    stderr_path.write_text(str(process["stderr"]), encoding="utf-8")

    record = make_result_record(
        skill=str(entry["skill"]),
        mode=str(entry["mode"]),
        scenario=dict(entry["scenario"]),
        repetition=int(entry["repetition"]),
        command=list(entry["command"]),
        prompt=prompt,
        context_files=_context_index(list(entry["context_files"])),
        exit_code=int(process["exit_code"]),
        stdout=str(process["stdout"]),
        stderr=str(process["stderr"]),
        final_response=extract_final_response(str(process["stdout"])),
        duration_seconds=float(process["duration_seconds"]),
    )
    record["timed_out"] = bool(process["timed_out"])
    record["run_id"] = run_id
    record["artifacts"] = {
        "prompt": str(prompt_path),
        "stdout": str(stdout_path),
        "stderr": str(stderr_path),
    }
    return record


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def audit_dry_run_report(report: dict[str, Any]) -> list[str]:
    """Check that a dry-run plan preserves A/B isolation and command invariants."""
    issues: list[str] = []
    if report.get("status") != "dry-run":
        issues.append("report status must be dry-run")
    runs = report.get("runs")
    if not isinstance(runs, list):
        return issues + ["report runs must be a list"]
    if report.get("run_count") != len(runs):
        issues.append("run_count does not equal the number of runs")

    seen: set[str] = set()
    required_tokens = (
        "--ephemeral",
        "--ignore-user-config",
        "--ignore-rules",
        "--sandbox",
        "read-only",
        "--ask-for-approval",
        "never",
    )
    for index, entry in enumerate(runs):
        if not isinstance(entry, dict):
            issues.append(f"run {index}: entry is not an object")
            continue
        run_id = _run_id(entry)
        if run_id in seen:
            issues.append(f"run {index}: duplicate run id {run_id}")
        seen.add(run_id)
        mode = entry.get("mode")
        prompt = entry.get("prompt", "")
        context = entry.get("context_files")
        if not isinstance(prompt, str):
            issues.append(f"run {run_id}: prompt is not text")
        if not isinstance(context, list):
            issues.append(f"run {run_id}: context_files is not a list")
            context = []
        if mode == "B":
            if context:
                issues.append(f"run {run_id}: B mode contains context files")
            if "## Task-local instructions and context" in prompt:
                issues.append(f"run {run_id}: B mode contains the context section")
        elif mode == "A" and not context:
            issues.append(f"run {run_id}: A mode has no context files")
        elif mode not in {"A", "B"}:
            issues.append(f"run {run_id}: invalid mode {mode!r}")
        if "expected_behavior" in prompt or "forbidden_behavior" in prompt:
            issues.append(f"run {run_id}: rubric key leaked into prompt")
        for context_entry in context:
            if not isinstance(context_entry, dict):
                issues.append(f"run {run_id}: malformed context entry")
                continue
            digest = context_entry.get("sha256")
            if not isinstance(digest, str) or len(digest) != 64:
                issues.append(f"run {run_id}: invalid context sha256")
        command = entry.get("command")
        if not isinstance(command, list):
            issues.append(f"run {run_id}: command is not a list")
            continue
        for token in required_tokens:
            if token not in command:
                issues.append(f"run {run_id}: missing command token {token}")
        if command.count("--disable") < 4:
            issues.append(f"run {run_id}: ambient feature disabling is incomplete")
        if not command or command[-1] != "-":
            issues.append(f"run {run_id}: prompt stdin marker is not final")
    return issues


def write_scoring_sheet(report: dict[str, Any], path: Path) -> None:
    """Write a binary pass/fail worksheet with all seven dimensions pending."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "run_id",
        "skill",
        "mode",
        "scenario_id",
        "scenario_category",
        "repetition",
        *RUBRIC_DIMENSIONS,
        "overall",
        "notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for entry in report.get("runs", []):
            scenario = entry.get("scenario", {})
            row = {
                "run_id": _run_id(entry),
                "skill": entry.get("skill", ""),
                "mode": entry.get("mode", ""),
                "scenario_id": scenario.get("id", ""),
                "scenario_category": scenario.get("category", ""),
                "repetition": entry.get("repetition", ""),
                "overall": "",
                "notes": "",
            }
            row.update({dimension: "" for dimension in RUBRIC_DIMENSIONS})
            writer.writerow(row)


def _login_preflight(codex_path: Path) -> dict[str, Any]:
    command = [str(codex_path), "login", "status"]
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "command": command,
            "exit_code": -1,
            "stdout": "",
            "stderr": str(exc),
            "duration_seconds": time.perf_counter() - started,
            "authenticated": False,
        }
    return {
        "command": command,
        "exit_code": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "duration_seconds": time.perf_counter() - started,
        "authenticated": completed.returncode == 0,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run isolated A/B behavior campaigns for materials skills"
    )
    parser.add_argument("--campaign", type=Path, required=True)
    parser.add_argument("--skills-root", type=Path, default=DEFAULT_SKILLS_ROOT)
    parser.add_argument("--codex", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_REPORT_ROOT)
    parser.add_argument("--skill", action="append", dest="skills")
    parser.add_argument("--modes", nargs="+", choices=("A", "B"), default=("A", "B"))
    parser.add_argument("--model", default="gpt-5.6-terra")
    parser.add_argument(
        "--codex-config",
        action="append",
        default=[],
        metavar="KEY=VALUE",
        help="Explicit Codex -c override; repeat for a relay/provider configuration.",
    )
    parser.add_argument("--default-repetitions", type=int, default=1)
    parser.add_argument("--key-repetitions", type=int, default=5)
    parser.add_argument("--timeout-seconds", type=float, default=600)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-login-check", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    payload = load_campaign(args.campaign)
    issues = validate_campaign(payload)
    if issues:
        print(json.dumps({"status": "invalid", "issues": issues}, ensure_ascii=False))
        return 2

    selected_skills = set(args.skills) if args.skills else None
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    plan = prepare_campaign_plan(
        payload,
        skills_root=args.skills_root,
        codex_path=args.codex,
        workdir=output_dir / "workdirs",
        modes=tuple(args.modes),
        default_repetitions=args.default_repetitions,
        key_repetitions=args.key_repetitions,
        model=args.model,
        codex_config=tuple(args.codex_config),
        selected_skills=selected_skills,
    )

    campaign_sha256 = hashlib.sha256(args.campaign.read_bytes()).hexdigest()
    if args.dry_run:
        report = {
            "status": "dry-run",
            "campaign": str(args.campaign.resolve()),
            "campaign_sha256": campaign_sha256,
            "run_count": len(plan),
            "runs": [
                {
                    **entry,
                    "context_files": _context_index(entry["context_files"]),
                }
                for entry in plan
            ],
        }
        audit_issues = audit_dry_run_report(report)
        report["audit_status"] = "pass" if not audit_issues else "fail"
        report["audit_issues"] = audit_issues
        _write_json(output_dir / "campaign-plan.json", report)
        write_scoring_sheet(report, output_dir / "behavior-scoring-sheet.csv")
        if audit_issues:
            print(json.dumps({"status": "dry-run-invalid", "issues": audit_issues}))
            return 2
        print(
            json.dumps(
                {"status": "dry-run", "run_count": len(plan)}, ensure_ascii=False
            )
        )
        return 0

    if not args.skip_login_check:
        preflight = _login_preflight(args.codex)
        if not preflight["authenticated"]:
            blocker = {
                "status": "blocked",
                "reason": "Codex CLI authentication is unavailable",
                "campaign": str(args.campaign.resolve()),
                "campaign_sha256": campaign_sha256,
                "preflight": preflight,
                "reproduction": f'& "{args.codex}" login status',
            }
            _write_json(output_dir / "campaign-blocker.json", blocker)
            print(json.dumps(blocker, ensure_ascii=False))
            return 3

    records: list[dict[str, Any]] = []
    results_jsonl = output_dir / "campaign-results.jsonl"
    with results_jsonl.open("w", encoding="utf-8") as stream:
        for entry in plan:
            record = execute_prepared_run(
                entry, output_dir=output_dir, timeout_seconds=args.timeout_seconds
            )
            records.append(record)
            stream.write(json.dumps(record, ensure_ascii=False) + "\n")
            stream.flush()

    report = {
        "status": "complete"
        if all(record["exit_code"] == 0 for record in records)
        else "execution-failed",
        "campaign": str(args.campaign.resolve()),
        "campaign_sha256": campaign_sha256,
        "run_count": len(records),
        "records": records,
    }
    _write_json(output_dir / "campaign-results.json", report)
    print(json.dumps({"status": report["status"], "run_count": len(records)}))
    return 0 if report["status"] == "complete" else 1


if __name__ == "__main__":
    raise SystemExit(main())

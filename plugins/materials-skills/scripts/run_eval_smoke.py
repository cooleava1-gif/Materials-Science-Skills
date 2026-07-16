#!/usr/bin/env python3
"""Run deterministic offline smoke checks declared by materials skill evals."""

from __future__ import annotations

import argparse
import ast
import json
import locale
import math
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any


DEFAULT_SKILLS_ROOT = Path(__file__).resolve().parent.parent / "skills"
PYTHON_COMMANDS = {"python", "python.exe"}
FORBIDDEN_COMMAND_TOKENS = ("http://", "https://", "&&", "|", ";", "`", "\n", "\r")
QUOTED_TOKEN = r"""(?:"(?:[^"\\]|\\.)*"|'(?:[^'\\]|\\.)*')"""
QUOTED_LIST = re.compile(
    rf"(?P<first>{QUOTED_TOKEN})(?P<rest>(?:\s+and\s+{QUOTED_TOKEN})*)\Z",
    re.IGNORECASE | re.DOTALL,
)
EXIT_CODE = re.compile(r"\bexit code\s+(\d+)\b", re.IGNORECASE)
STREAM_EXPECTATION = re.compile(
    rf"^(?:(?P<exit>exit code\s+\d+)\s+)?"
    rf"(?P<stream>stdout or stderr|stdout|stderr)\s+contains\s+"
    rf"(?P<texts>{QUOTED_TOKEN}(?:\s+and\s+{QUOTED_TOKEN})*)$",
    re.IGNORECASE | re.DOTALL,
)
COMBINED_EXPECTATION = re.compile(
    rf"^(?:(?P<exit>exit code\s+\d+)\s+)?"
    rf"(?P<phrase>dry-run\s+with\s+refusal\s+reason|with|refusal\s+reason)\s+"
    rf"(?P<texts>{QUOTED_TOKEN}(?:\s+and\s+{QUOTED_TOKEN})*)$",
    re.IGNORECASE | re.DOTALL,
)


def _resolve_skill_selector(
    skills_root: Path, skill: str
) -> tuple[Path | None, str | None]:
    """Resolve only a direct materials-* child without following it outside root."""
    selector = Path(skill)
    if selector.is_absolute():
        return None, "--skill must be a direct materials-* child of skills_root"
    if (
        not skill.startswith("materials-")
        or len(selector.parts) != 1
        or selector.name != skill
    ):
        return None, "--skill must be a direct materials-* child of skills_root"

    root = skills_root.resolve()
    resolved = (root / selector).resolve()
    if resolved.parent != root:
        return None, "--skill must stay inside skills_root"
    return resolved, None


def discover_eval_files(skills_root: Path, skill: str | None = None) -> list[Path]:
    """Return tracked eval declarations in stable skill-name order."""
    root = skills_root.resolve()
    if skill is not None:
        skill_dir, issue = _resolve_skill_selector(root, skill)
        if issue is not None or skill_dir is None:
            return []
        skill_dirs = [skill_dir]
    else:
        skill_dirs = sorted(
            path.resolve()
            for path in root.glob("materials-*")
            if path.is_dir()
            and path.resolve().parent == root
            and path.resolve().name.startswith("materials-")
        )

    return [
        (skill_dir / "evals" / "evals.json").resolve()
        for skill_dir in skill_dirs
        if (skill_dir / "evals" / "evals.json").is_file()
        and _is_within(skill_dir / "evals" / "evals.json", root)
    ]


def classify_case(case: dict[str, Any]) -> str:
    """Classify eval declarations without pretending semantic cases are runnable."""
    return "command" if isinstance(case.get("command"), str) else "declarative"


def _parse_quoted_list(value: str) -> list[str] | None:
    match = QUOTED_LIST.fullmatch(value.strip())
    if match is None:
        return None

    tokens = re.findall(QUOTED_TOKEN, value, re.DOTALL)
    try:
        parsed = [ast.literal_eval(token) for token in tokens]
    except (SyntaxError, ValueError):
        return None
    if not all(isinstance(item, str) and item for item in parsed):
        return None
    return parsed


def _expected_oracle(expected: object) -> tuple[int, str, list[str]] | None:
    """Translate the repository's current command-eval prose into checks."""
    if not isinstance(expected, str):
        return None

    expected = expected.strip()
    exit_only = re.fullmatch(r"exit code\s+(\d+)", expected, re.IGNORECASE)
    if exit_only is not None:
        return int(exit_only.group(1)), "combined", []

    stream_match = STREAM_EXPECTATION.fullmatch(expected)
    if stream_match is not None:
        exit_match = EXIT_CODE.search(stream_match.group("exit") or "")
        expected_exit = int(exit_match.group(1)) if exit_match else 0
        required_text = _parse_quoted_list(stream_match.group("texts"))
        if required_text is None:
            return None
        stream = stream_match.group("stream").lower()
        return (
            expected_exit,
            "combined" if stream == "stdout or stderr" else stream,
            required_text,
        )

    combined_match = COMBINED_EXPECTATION.fullmatch(expected)
    if combined_match is not None:
        exit_match = EXIT_CODE.search(combined_match.group("exit") or "")
        expected_exit = int(exit_match.group(1)) if exit_match else 0
        required_text = _parse_quoted_list(combined_match.group("texts"))
        if required_text is None:
            return None
        return expected_exit, "combined", required_text

    return None


def _is_within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
    except ValueError:
        return False
    return True


def _decode_output(value: bytes) -> str:
    """Decode local tool output without discarding the active console encoding."""
    encodings = ("utf-8", locale.getpreferredencoding(False))
    for encoding in dict.fromkeys(encodings):
        try:
            return value.decode(encoding)
        except UnicodeDecodeError:
            continue
    return value.decode("utf-8", errors="replace")


def _command_argv(command: str, skill_dir: Path) -> tuple[list[str], str | None]:
    """Parse an eval command within the trusted repository-local script model.

    The checks below are syntactic restrictions, not an OS-level
    network/filesystem sandbox.
    """
    if (
        any(token in command.lower() for token in ("http://", "https://"))
        or any(token in command for token in FORBIDDEN_COMMAND_TOKENS[2:])
    ):
        return [], "only local Python commands are allowed"

    try:
        argv = shlex.split(command, posix=True)
    except ValueError as exc:
        return [], f"could not parse command: {exc}"

    if len(argv) < 2 or argv[0].lower() not in PYTHON_COMMANDS:
        return [], "only local Python commands are allowed"

    script_path = (skill_dir / argv[1]).resolve()
    if not script_path.is_file() or not _is_within(script_path, skill_dir):
        return [], "command script must be a local file inside the skill directory"

    if any("://" in argument.lower() for argument in argv[2:]):
        return [], "only local Python commands are allowed"

    argv[0] = sys.executable
    return argv, None


def _is_valid_timeout(timeout: object) -> bool:
    try:
        return math.isfinite(timeout) and timeout > 0
    except (TypeError, ValueError):
        return False


def _case_result(
    *,
    skill: str,
    case_id: str,
    kind: str,
    status: str,
    source: Path,
    issues: list[str] | None = None,
    **details: object,
) -> dict[str, object]:
    result: dict[str, object] = {
        "skill": skill,
        "id": case_id,
        "kind": kind,
        "status": status,
        "source": source.as_posix(),
        "issues": issues or [],
    }
    result.update(details)
    return result


def _run_command_case(
    skill: str,
    case: dict[str, Any],
    source: Path,
    skill_dir: Path,
    timeout: float,
) -> dict[str, object]:
    case_id = str(case.get("id", "<missing-id>"))
    command = case.get("command")
    if not isinstance(command, str):
        return _case_result(
            skill=skill,
            case_id=case_id,
            kind="command",
            status="error",
            source=source,
            issues=["command case is missing a command string"],
        )

    oracle = _expected_oracle(case.get("expected"))
    if oracle is None:
        return _case_result(
            skill=skill,
            case_id=case_id,
            kind="command",
            status="error",
            source=source,
            issues=["unsupported command expectation"],
            command=command,
        )

    argv, command_issue = _command_argv(command, skill_dir)
    if command_issue is not None:
        return _case_result(
            skill=skill,
            case_id=case_id,
            kind="command",
            status="error",
            source=source,
            issues=[command_issue],
            command=command,
        )

    try:
        completed = subprocess.run(
            argv,
            cwd=skill_dir,
            capture_output=True,
            timeout=timeout,
            shell=False,
            check=False,
        )
    except subprocess.TimeoutExpired:
        return _case_result(
            skill=skill,
            case_id=case_id,
            kind="command",
            status="error",
            source=source,
            issues=[f"command exceeded {timeout:g} second timeout"],
            command=command,
        )
    except OSError as exc:
        return _case_result(
            skill=skill,
            case_id=case_id,
            kind="command",
            status="error",
            source=source,
            issues=[f"command could not run: {exc}"],
            command=command,
        )

    stdout = _decode_output(completed.stdout or b"")
    stderr = _decode_output(completed.stderr or b"")
    expected_exit, stream, required_text = oracle
    output_by_stream = {
        "stdout": stdout,
        "stderr": stderr,
        "combined": f"{stdout}\n{stderr}",
    }
    actual_output = output_by_stream[stream]
    issues: list[str] = []
    if completed.returncode != expected_exit:
        issues.append(
            f"expected exit code {expected_exit}, got {completed.returncode}"
        )
    for value in required_text:
        if value not in actual_output:
            issues.append(f"expected {stream} to contain {value!r}")

    return _case_result(
        skill=skill,
        case_id=case_id,
        kind="command",
        status="pass" if not issues else "fail",
        source=source,
        issues=issues,
        command=command,
        returncode=completed.returncode,
        stdout=stdout,
        stderr=stderr,
    )


def _declarative_result(
    skill: str, case: dict[str, Any], source: Path
) -> dict[str, object]:
    """Expose semantic eval declarations without claiming an offline oracle."""
    return _case_result(
        skill=skill,
        case_id=str(case.get("id", "<missing-id>")),
        kind="declarative",
        status="not_executable",
        source=source,
        prompt=case.get("prompt"),
        expected_output=case.get("expected_output"),
        assertions=case.get("assertions", []),
        files=case.get("files", []),
    )


def _declarative_issue(case: dict[str, Any]) -> str | None:
    if not isinstance(case.get("prompt"), str):
        return "declarative case must have a prompt string"
    if not isinstance(case.get("expected_output"), str):
        return "declarative case must have an expected_output string"
    if not isinstance(case.get("assertions"), list):
        return "declarative case must have an assertions list"
    if "files" in case and not isinstance(case["files"], list):
        return "declarative case files must be a list"
    return None


def _empty_summary() -> dict[str, int]:
    return {
        "total": 0,
        "pass": 0,
        "fail": 0,
        "error": 0,
        "not_executable": 0,
    }


def json_output(report: dict[str, object]) -> str:
    """Serialize reports safely for Windows consoles with legacy encodings."""
    return json.dumps(report, ensure_ascii=True, indent=2)


def run_smoke_checks(
    skills_root: Path,
    *,
    skill: str | None = None,
    eval_id: str | None = None,
    timeout: float = 30.0,
) -> dict[str, object]:
    """Discover eval declarations and execute the safe deterministic lane."""
    if not _is_valid_timeout(timeout):
        return {
            "status": "fail",
            "summary": _empty_summary(),
            "cases": [],
            "issues": ["timeout must be finite and greater than zero"],
        }

    results: list[dict[str, object]] = []
    issues: list[str] = []
    seen_cases: set[tuple[str, str]] = set()
    selected_case_count = 0
    selector_issue: str | None = None
    if skill is not None:
        _, selector_issue = _resolve_skill_selector(skills_root, skill)

    sources = (
        []
        if selector_issue is not None
        else discover_eval_files(skills_root, skill)
    )
    if selector_issue is not None:
        issues.append(selector_issue)

    if not sources and not issues:
        issues.append("no eval declarations found")

    for source in sources:
        skill_name = source.parents[1].name
        try:
            document = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            result = _case_result(
                skill=skill_name,
                case_id="<document>",
                kind="document",
                status="error",
                source=source,
                issues=[f"could not load eval declaration: {exc}"],
            )
            results.append(result)
            issues.extend(result["issues"])
            continue

        cases = document.get("evals") if isinstance(document, dict) else None
        if not isinstance(cases, list):
            result = _case_result(
                skill=skill_name,
                case_id="<document>",
                kind="document",
                status="error",
                source=source,
                issues=["eval declaration must contain an evals list"],
            )
            results.append(result)
            issues.extend(result["issues"])
            continue

        for raw_case in cases:
            if eval_id is not None:
                if not isinstance(raw_case, dict) or raw_case.get("id") != eval_id:
                    continue
                selected_case_count += 1

            if not isinstance(raw_case, dict):
                result = _case_result(
                    skill=skill_name,
                    case_id="<invalid-case>",
                    kind="document",
                    status="error",
                    source=source,
                    issues=["eval case must be an object"],
                )
                results.append(result)
                issues.extend(result["issues"])
                continue

            case_id = raw_case.get("id")
            if not isinstance(case_id, str) or not case_id:
                result = _case_result(
                    skill=skill_name,
                    case_id="<missing-id>",
                    kind="document",
                    status="error",
                    source=source,
                    issues=["eval case must have a non-empty id"],
                )
                results.append(result)
                issues.extend(result["issues"])
                continue

            if eval_id is not None and case_id != eval_id:
                continue

            key = (skill_name, case_id)
            if key in seen_cases:
                result = _case_result(
                    skill=skill_name,
                    case_id=case_id,
                    kind="document",
                    status="error",
                source=source,
                issues=["duplicate skill/id eval declaration"],
            )
            else:
                seen_cases.add(key)
                if "command" in raw_case and not isinstance(raw_case["command"], str):
                    result = _case_result(
                        skill=skill_name,
                        case_id=case_id,
                        kind="command",
                        status="error",
                        source=source,
                        issues=["command must be a string"],
                    )
                elif classify_case(raw_case) == "command":
                    result = _run_command_case(
                        skill_name,
                        raw_case,
                        source,
                        source.parents[1],
                        timeout,
                    )
                else:
                    declarative_issue = _declarative_issue(raw_case)
                    if declarative_issue is not None:
                        result = _case_result(
                            skill=skill_name,
                            case_id=case_id,
                            kind="declarative",
                            status="error",
                            source=source,
                            issues=[declarative_issue],
                        )
                    else:
                        result = _declarative_result(skill_name, raw_case, source)

            results.append(result)
            if result["status"] in {"fail", "error"}:
                for issue in result["issues"]:
                    issues.append(f"{skill_name}:{case_id}: {issue}")

    if eval_id is not None and selected_case_count == 0:
        issues.append(f"no eval cases matched --eval {eval_id!r}")
    elif not results and not issues:
        issues.append("no eval cases selected")

    summary = _empty_summary()
    for result in results:
        summary["total"] += 1
        summary[str(result["status"])] += 1

    return {
        "status": "pass" if not issues else "fail",
        "summary": summary,
        "cases": results,
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--skills-root",
        type=Path,
        default=DEFAULT_SKILLS_ROOT,
        help="Skill root to inspect (default: plugin skills directory).",
    )
    parser.add_argument("--skill", help="Run one skill's eval declarations.")
    parser.add_argument("--eval", dest="eval_id", help="Run one eval id.")
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Per-command timeout in seconds (default: 30).",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON output.")
    args = parser.parse_args()

    if not _is_valid_timeout(args.timeout):
        parser.error("--timeout must be finite and greater than zero")

    report = run_smoke_checks(
        args.skills_root,
        skill=args.skill,
        eval_id=args.eval_id,
        timeout=args.timeout,
    )
    if args.json:
        print(json_output(report))
    else:
        for case in report["cases"]:
            print(f"[{case['status']}] {case['skill']}:{case['id']}")
        print(json.dumps(report["summary"], ensure_ascii=False))

    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

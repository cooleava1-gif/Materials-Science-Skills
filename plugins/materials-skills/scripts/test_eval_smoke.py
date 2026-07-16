#!/usr/bin/env python3
"""Standalone regression checks for the canonical eval smoke runner."""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from types import ModuleType
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
RUNNER_PATH = SCRIPT_DIR / "run_eval_smoke.py"


def load_runner() -> ModuleType:
    if not RUNNER_PATH.exists():
        raise AssertionError(f"runner does not exist yet: {RUNNER_PATH}")
    spec = importlib.util.spec_from_file_location("run_eval_smoke", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise AssertionError(f"could not load runner: {RUNNER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


EMITTER_SOURCE = (
    "from __future__ import annotations\n"
    "import sys\n"
    "if sys.argv[1] == 'stdout':\n"
    "    print('expected stdout text')\n"
    "elif sys.argv[1] == 'stderr':\n"
    "    print('expected stderr text', file=sys.stderr)\n"
    "    raise SystemExit(1)\n"
    "elif sys.argv[1] == 'replacement':\n"
    "    sys.stdout.buffer.write(b'\\xff')\n"
    "elif sys.argv[1] == 'gbk':\n"
    "    sys.stdout.buffer.write('\\u4e2d\\u6587'.encode('gbk'))\n"
    "elif sys.argv[1] == 'sleep':\n"
    "    import time\n"
    "    time.sleep(float(sys.argv[2]))\n"
    "else:\n"
    "    raise SystemExit(2)\n"
)


def add_fake_skill(
    skills_root: Path,
    cases: list[dict[str, Any]],
    *,
    skill_name: str,
) -> Path:
    skill_dir = skills_root / skill_name
    (skill_dir / "evals").mkdir(parents=True, exist_ok=True)
    (skill_dir / "scripts").mkdir(exist_ok=True)
    (skill_dir / "scripts" / "emit.py").write_text(
        EMITTER_SOURCE,
        encoding="utf-8",
    )
    (skill_dir / "evals" / "evals.json").write_text(
        json.dumps({"skill": skill_name, "evals": cases}),
        encoding="utf-8",
    )
    return skill_dir


def make_fake_skills_root(
    temporary_root: Path,
    cases: list[dict[str, Any]],
    *,
    skill_name: str = "materials-command",
) -> Path:
    skills_root = temporary_root / "skills"
    add_fake_skill(skills_root, cases, skill_name=skill_name)
    return skills_root


def write_eval_document(
    skills_root: Path, skill_name: str, document: object
) -> None:
    path = skills_root / skill_name / "evals" / "evals.json"
    path.write_text(json.dumps(document), encoding="utf-8")


def run_cli(skills_root: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(RUNNER_PATH),
            "--skills-root",
            str(skills_root),
            "--json",
            *arguments,
        ],
        capture_output=True,
        text=True,
        check=False,
    )


def test_discovers_command_and_declarative_cases() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                {
                    "id": "command-pass",
                    "command": "python scripts/emit.py stdout",
                    "expected": "stdout contains 'expected stdout text'",
                },
                {
                    "id": "declarative-case",
                    "prompt": "Provide a bounded response.",
                    "expected_output": "The response must state its evidence boundary.",
                    "assertions": [{"name": "boundary", "description": "Boundary is explicit."}],
                    "files": [],
                },
            ],
        )

        module = load_runner()
        report = module.run_smoke_checks(root)

        assert report["summary"] == {
            "total": 2,
            "pass": 1,
            "fail": 0,
            "error": 0,
            "not_executable": 1,
        }
        assert {case["status"] for case in report["cases"]} == {
            "pass",
            "not_executable",
        }
        assert {case["skill"] for case in report["cases"]} == {
            "materials-command"
        }


def test_rejects_unsafe_or_unknown_commands() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                {
                    "id": "unsafe-command",
                    "command": "bash scripts/emit.py stdout",
                    "expected": "stdout contains 'expected stdout text'",
                }
            ],
        )

        module = load_runner()
        report = module.run_smoke_checks(root)
        result = report["cases"][0]

        assert result["status"] == "error"
        assert "only local Python commands" in result["issues"][0]


def test_matches_exit_codes_and_stream_expectations() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                {
                    "id": "stdout-pass",
                    "command": "python scripts/emit.py stdout",
                    "expected": "stdout contains 'expected stdout text'",
                },
                {
                    "id": "stderr-and-exit-code-pass",
                    "command": "python scripts/emit.py stderr",
                    "expected": "exit code 1 with 'expected stderr text'",
                },
            ],
        )

        module = load_runner()
        report = module.run_smoke_checks(root)

        assert report["summary"]["pass"] == 2
        assert report["summary"]["fail"] == 0


def test_json_output_is_console_safe() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                {
                    "id": "replacement-output",
                    "command": "python scripts/emit.py replacement",
                    "expected": "stdout contains '\ufffd'",
                }
            ],
        )

        module = load_runner()
        report = module.run_smoke_checks(root)
        payload = module.json_output(report)

        assert json.loads(payload)["cases"][0]["stdout"] == "\ufffd"
        assert payload.encode("gbk")


def test_decodes_local_console_output_without_replacement() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                {
                    "id": "gbk-output",
                    "command": "python scripts/emit.py gbk",
                    "expected": "stdout contains '\u4e2d\u6587'",
                }
            ],
        )

        module = load_runner()
        original_preferred_encoding = module.locale.getpreferredencoding
        module.locale.getpreferredencoding = lambda do_setlocale=False: "gbk"
        try:
            report = module.run_smoke_checks(root)
        finally:
            module.locale.getpreferredencoding = original_preferred_encoding

        assert report["summary"]["pass"] == 1
        assert report["cases"][0]["stdout"] == "\u4e2d\u6587"


def test_eval_filter_skips_unselected_malformed_cases() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                "malformed unselected case",
                {
                    "id": "selected",
                    "command": "python scripts/emit.py stdout",
                    "expected": "stdout contains 'expected stdout text'",
                },
            ],
        )

        module = load_runner()
        report = module.run_smoke_checks(root, eval_id="selected")

        assert report["status"] == "pass"
        assert report["summary"] == {
            "total": 1,
            "pass": 1,
            "fail": 0,
            "error": 0,
            "not_executable": 0,
        }
        assert [case["id"] for case in report["cases"]] == ["selected"]


def test_missing_eval_selection_is_failure_not_zero_case_pass() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                {
                    "id": "available",
                    "command": "python scripts/emit.py stdout",
                    "expected": "stdout contains 'expected stdout text'",
                }
            ],
        )

        module = load_runner()
        report = module.run_smoke_checks(root, eval_id="missing")

        assert report["status"] == "fail"
        assert report["summary"] == {
            "total": 0,
            "pass": 0,
            "fail": 0,
            "error": 0,
            "not_executable": 0,
        }
        assert report["cases"] == []
        assert any("no eval cases matched" in issue for issue in report["issues"])


def test_duplicate_ids_only_fail_when_duplicate_id_is_selected() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                {
                    "id": "selected",
                    "command": "python scripts/emit.py stdout",
                    "expected": "stdout contains 'expected stdout text'",
                },
                {
                    "id": "duplicate",
                    "command": "python scripts/emit.py stdout",
                    "expected": "stdout contains 'expected stdout text'",
                },
                {
                    "id": "duplicate",
                    "command": "python scripts/emit.py stdout",
                    "expected": "stdout contains 'expected stdout text'",
                },
            ],
        )

        module = load_runner()
        selected_report = module.run_smoke_checks(root, eval_id="selected")
        duplicate_report = module.run_smoke_checks(root, eval_id="duplicate")

        assert selected_report["status"] == "pass"
        assert selected_report["summary"]["total"] == 1
        assert selected_report["summary"]["error"] == 0
        assert duplicate_report["status"] == "fail"
        assert duplicate_report["summary"]["total"] == 2
        assert duplicate_report["summary"]["error"] == 1
        assert any(
            "duplicate skill/id" in issue for issue in duplicate_report["issues"]
        )


def test_skill_filter_ignores_another_skill_with_malformed_declaration() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                {
                    "id": "selected",
                    "command": "python scripts/emit.py stdout",
                    "expected": "stdout contains 'expected stdout text'",
                }
            ],
        )
        other_skill = root / "materials-other"
        (other_skill / "evals").mkdir(parents=True)
        (other_skill / "evals" / "evals.json").write_text(
            "{ malformed json",
            encoding="utf-8",
        )

        module = load_runner()
        report = module.run_smoke_checks(root, skill="materials-command")

        assert report["status"] == "pass"
        assert report["summary"]["total"] == 1
        assert report["summary"]["error"] == 0


def test_selected_malformed_case_is_error() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [{"id": "selected", "command": 7}],
        )

        module = load_runner()
        report = module.run_smoke_checks(root, eval_id="selected")

        assert report["status"] == "fail"
        assert report["summary"]["error"] == 1
        assert report["cases"][0]["status"] == "error"
        assert "command must be a string" in report["cases"][0]["issues"][0]


def test_malformed_eval_document_is_an_error_when_in_scope() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                {
                    "id": "selected",
                    "command": "python scripts/emit.py stdout",
                    "expected": "stdout contains 'expected stdout text'",
                }
            ],
        )
        eval_path = root / "materials-command" / "evals" / "evals.json"
        eval_path.write_text("{ malformed json", encoding="utf-8")

        module = load_runner()
        report = module.run_smoke_checks(root)

        assert report["status"] == "fail"
        assert report["summary"]["error"] == 1
        assert "could not load eval declaration" in report["cases"][0]["issues"][0]


def test_skill_selector_rejects_absolute_and_traversal_without_execution() -> None:
    with tempfile.TemporaryDirectory() as directory:
        temporary_root = Path(directory)
        root = make_fake_skills_root(
            temporary_root,
            [
                {
                    "id": "inside",
                    "command": "python scripts/emit.py stdout",
                    "expected": "stdout contains 'expected stdout text'",
                }
            ],
        )
        outside_skill = temporary_root / "outside" / "materials-escape"
        (outside_skill / "evals").mkdir(parents=True)
        (outside_skill / "scripts").mkdir()
        marker = outside_skill / "executed.txt"
        (outside_skill / "scripts" / "emit.py").write_text(
            "from pathlib import Path\n"
            f"Path({str(marker)!r}).write_text('executed', encoding='utf-8')\n"
            "print('outside command ran')\n",
            encoding="utf-8",
        )
        (outside_skill / "evals" / "evals.json").write_text(
            json.dumps(
                {
                    "evals": [
                        {
                            "id": "outside",
                            "command": "python scripts/emit.py",
                            "expected": "stdout contains 'outside command ran'",
                        }
                    ]
                }
            ),
            encoding="utf-8",
        )

        module = load_runner()
        selectors = [
            str(outside_skill),
            str(Path("..") / "outside" / "materials-escape"),
            "not-a-materials-skill",
        ]
        for selector in selectors:
            report = module.run_smoke_checks(root, skill=selector)
            assert report["status"] == "fail"
            assert report["cases"] == []
            assert report["summary"]["total"] == 0
            assert any("skill" in issue.lower() for issue in report["issues"])
        assert not marker.exists()


def test_rejects_mixed_stream_predicates_and_unsupported_prose() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                {
                    "id": "mixed-stream",
                    "command": "python scripts/emit.py stdout",
                    "expected": (
                        "stdout contains 'expected stdout text' and "
                        "stderr contains 'expected stderr text'"
                    ),
                },
                {
                    "id": "unsupported-prose",
                    "command": "python scripts/emit.py stdout",
                    "expected": (
                        "stdout contains 'expected stdout text' "
                        "followed by unsupported prose"
                    ),
                },
            ],
        )

        module = load_runner()
        report = module.run_smoke_checks(root)

        assert report["summary"]["error"] == 2
        assert {case["status"] for case in report["cases"]} == {"error"}
        assert all(
            "unsupported command expectation" in issue
            for case in report["cases"]
            for issue in case["issues"]
        )


def test_rejects_urls_and_shell_operators() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                {
                    "id": "url",
                    "command": "python scripts/emit.py stdout https://example.invalid",
                    "expected": "stdout contains 'expected stdout text'",
                },
                {
                    "id": "operator",
                    "command": "python scripts/emit.py stdout | more",
                    "expected": "stdout contains 'expected stdout text'",
                },
            ],
        )

        module = load_runner()
        report = module.run_smoke_checks(root)

        assert report["summary"]["error"] == 2
        assert all(case["status"] == "error" for case in report["cases"])
        assert all(
            "only local Python commands are allowed" in issue
            for case in report["cases"]
            for issue in case["issues"]
        )


def test_timeout_is_reported_as_command_error() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                {
                    "id": "timeout",
                    "command": "python scripts/emit.py sleep 1",
                    "expected": "stdout contains 'never emitted'",
                }
            ],
        )

        module = load_runner()
        report = module.run_smoke_checks(root, timeout=0.01)

        assert report["status"] == "fail"
        assert report["summary"]["error"] == 1
        assert "timeout" in report["cases"][0]["issues"][0].lower()


def test_direct_api_rejects_non_finite_timeout_before_execution() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                {
                    "id": "timeout-validation",
                    "command": "python scripts/emit.py stdout",
                    "expected": "stdout contains 'expected stdout text'",
                }
            ],
        )

        module = load_runner()
        for timeout in (float("nan"), float("inf"), float("-inf")):
            report = module.run_smoke_checks(root, timeout=timeout)

            assert report["status"] == "fail"
            assert report["summary"] == {
                "total": 0,
                "pass": 0,
                "fail": 0,
                "error": 0,
                "not_executable": 0,
            }
            assert report["cases"] == []
            assert report["issues"] == [
                "timeout must be finite and greater than zero"
            ]


def test_cli_rejects_non_finite_timeout_as_usage_error() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                {
                    "id": "timeout-validation",
                    "command": "python scripts/emit.py stdout",
                    "expected": "stdout contains 'expected stdout text'",
                }
            ],
        )

        for timeout in ("nan", "inf"):
            result = run_cli(root, "--timeout", timeout)

            assert result.returncode == 2
            assert result.stdout == ""
            assert "usage:" in result.stderr.lower()
            assert "--timeout must be finite and greater than zero" in result.stderr
            assert "traceback" not in result.stderr.lower()


def test_cli_exit_mapping_and_json_output() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                {
                    "id": "selected",
                    "command": "python scripts/emit.py stdout",
                    "expected": "stdout contains 'expected stdout text'",
                }
            ],
        )

        passing = run_cli(
            root,
            "--skill",
            "materials-command",
            "--eval",
            "selected",
            "--timeout",
            "1.0",
        )
        missing = run_cli(root, "--skill", "materials-command", "--eval", "missing")
        unsafe = run_cli(root, "--skill", str(root.parent / "outside"))

        assert passing.returncode == 0
        assert json.loads(passing.stdout)["status"] == "pass"
        assert missing.returncode == 1
        assert json.loads(missing.stdout)["status"] == "fail"
        assert unsafe.returncode == 1
        assert json.loads(unsafe.stdout)["status"] == "fail"


def test_invalid_utf8_eval_declaration_is_a_structured_error() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                {
                    "id": "available",
                    "command": "python scripts/emit.py stdout",
                    "expected": "stdout contains 'expected stdout text'",
                }
            ],
        )
        eval_path = root / "materials-command" / "evals" / "evals.json"
        eval_path.write_bytes(b'{"evals": "\xff"}')

        module = load_runner()
        report = module.run_smoke_checks(root)

        assert report["status"] == "fail"
        assert report["summary"] == {
            "total": 1,
            "pass": 0,
            "fail": 0,
            "error": 1,
            "not_executable": 0,
        }
        assert len(report["cases"]) == 1
        assert report["cases"][0]["status"] == "error"
        assert "could not load eval declaration" in report["cases"][0]["issues"][0]
        assert report["issues"] == report["cases"][0]["issues"]


def test_rejects_empty_quoted_command_expectation() -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = make_fake_skills_root(
            Path(directory),
            [
                {
                    "id": "empty-expected",
                    "command": "python scripts/emit.py stdout",
                    "expected": "stdout contains ''",
                }
            ],
        )

        module = load_runner()
        report = module.run_smoke_checks(root)

        assert report["status"] == "fail"
        assert report["summary"]["error"] == 1
        assert report["cases"][0]["status"] == "error"
        assert (
            report["cases"][0]["issues"] == ["unsupported command expectation"]
        )


def main() -> int:
    tests = [
        test_discovers_command_and_declarative_cases,
        test_rejects_unsafe_or_unknown_commands,
        test_matches_exit_codes_and_stream_expectations,
        test_json_output_is_console_safe,
        test_decodes_local_console_output_without_replacement,
        test_eval_filter_skips_unselected_malformed_cases,
        test_missing_eval_selection_is_failure_not_zero_case_pass,
        test_duplicate_ids_only_fail_when_duplicate_id_is_selected,
        test_skill_filter_ignores_another_skill_with_malformed_declaration,
        test_selected_malformed_case_is_error,
        test_malformed_eval_document_is_an_error_when_in_scope,
        test_skill_selector_rejects_absolute_and_traversal_without_execution,
        test_rejects_mixed_stream_predicates_and_unsupported_prose,
        test_rejects_urls_and_shell_operators,
        test_timeout_is_reported_as_command_error,
        test_direct_api_rejects_non_finite_timeout_before_execution,
        test_cli_rejects_non_finite_timeout_as_usage_error,
        test_cli_exit_mapping_and_json_output,
        test_invalid_utf8_eval_declaration_is_a_structured_error,
        test_rejects_empty_quoted_command_expectation,
    ]
    for test in tests:
        test()
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

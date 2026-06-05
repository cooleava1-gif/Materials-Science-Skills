#!/usr/bin/env python3
"""Run release checks for the civil-materials skill bundle."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


REQUIRED_SKILLS = [
    "civil-materials-research",
    "civil-materials-reader",
    "civil-materials-citation",
    "civil-materials-polishing",
    "civil-materials-response",
    "civil-materials-paper2ppt",
    "civil-materials-pptx",
    "civil-materials-figure",
    "civil-materials-data",
]

TEXT_EXTENSIONS = {
    ".md",
    ".yaml",
    ".yml",
    ".py",
    ".csv",
    ".json",
    ".txt",
    ".toml",
}

LOCAL_PATH_MARKERS = [
    "C:" + "\\" + "Users" + "\\" + "97218",
    "/".join(["C:", "Users", "97218"]),
]
SECRET_MARKERS = ["yujian" + "wudi"]
SECRET_TOKEN_RE = re.compile("sk-" + r"[A-Za-z0-9]{20,}")


def run(command: list[str], cwd: Path) -> None:
    subprocess.run(command, cwd=str(cwd), check=True)


def clean_generated_artifacts(root: Path) -> None:
    for path in sorted(root.rglob("__pycache__"), reverse=True):
        if path.is_dir():
            shutil.rmtree(path)
    for path in root.rglob("*"):
        if path.is_file() and path.suffix in {".pyc", ".pyo"}:
            path.unlink()


def collect_release_issues(root: Path) -> dict[str, list[str]]:
    issues = {
        "missing_skills": [],
        "openai_yaml_format": [],
        "generated_artifacts": [],
        "local_paths": [],
        "possible_secrets": [],
    }
    for skill in REQUIRED_SKILLS:
        skill_root = root / "skills" / skill
        if not (skill_root / "SKILL.md").exists():
            issues["missing_skills"].append(skill)
        openai_yaml = skill_root / "agents" / "openai.yaml"
        if not openai_yaml.exists():
            issues["openai_yaml_format"].append(f"{skill}: missing agents/openai.yaml")
        else:
            text = openai_yaml.read_text(encoding="utf-8", errors="ignore")
            if "interface:" not in text or "policy:" not in text or "allow_implicit_invocation" not in text:
                issues["openai_yaml_format"].append(f"{skill}: expected interface/policy wrapper")

    for path in root.rglob("*"):
        if path.is_dir() and path.name == "__pycache__":
            issues["generated_artifacts"].append(str(path.relative_to(root)))
        if path.is_file() and path.suffix in {".pyc", ".pyo"}:
            issues["generated_artifacts"].append(str(path.relative_to(root)))
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if any(marker in text for marker in LOCAL_PATH_MARKERS):
            issues["local_paths"].append(str(path.relative_to(root)))
        if any(marker in text for marker in SECRET_MARKERS) or SECRET_TOKEN_RE.search(text):
            issues["possible_secrets"].append(str(path.relative_to(root)))
    return issues


def run_tests(root: Path) -> None:
    test_roots = [
        root / "skills" / "civil-materials-research" / "tests",
        root / "skills" / "civil-materials-data" / "tests",
        root / "skills" / "civil-materials-figure" / "tests",
        root / "skills" / "civil-materials-polishing" / "tests",
        root / "skills" / "civil-materials-response" / "tests",
        root / "skills" / "civil-materials-citation" / "mcp" / "academic_search" / "tests",
    ]
    for test_root in test_roots:
        run([sys.executable, "-m", "unittest", "discover", "-s", str(test_root), "-p", "test_*.py", "-v"], root)

    run(
        [
            sys.executable,
            str(root / "skills" / "civil-materials-research" / "scripts" / "audit_pressure_assets.py"),
            "--skill-root",
            str(root / "skills" / "civil-materials-research"),
            "--json",
        ],
        root,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    clean_generated_artifacts(root)
    run_tests(root)
    clean_generated_artifacts(root)
    issues = collect_release_issues(root)
    status = "pass" if all(not value for value in issues.values()) else "incomplete"
    report = {"status": status, "issues": issues}
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())

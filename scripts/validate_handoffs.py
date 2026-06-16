#!/usr/bin/env python3
"""Validate handoff contracts across all discovered materials skills."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from skill_manifest import iter_skill_manifests, load_yaml
except ModuleNotFoundError:  # pragma: no cover - supports import as scripts.validate_handoffs
    from scripts.skill_manifest import iter_skill_manifests, load_yaml


SKILLS_ROOT = Path(__file__).resolve().parents[1] / "skills"
REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACTS_DIR = REPO_ROOT / "_shared" / "contracts"


def load_contract(name: str) -> dict[str, Any] | None:
    """Load a contract YAML by handoff name."""

    path = CONTRACTS_DIR / f"{name}.yaml"
    if not path.exists():
        return None
    try:
        return load_yaml(path)
    except Exception:
        return None


def _normalize_consumes(consumes: object) -> list[dict[str, Any]]:
    """Normalize manifest handoff consumers to dictionaries."""

    if not isinstance(consumes, list):
        return []
    normalized: list[dict[str, Any]] = []
    for item in consumes:
        if isinstance(item, str) and item:
            normalized.append({"handoff": item})
        elif isinstance(item, dict) and item.get("handoff"):
            normalized.append(dict(item))
    return normalized


def collect_manifest_handoff_topology(
    skills_root: Path = SKILLS_ROOT,
) -> dict[str, object]:
    """Collect providers and consumers from current skill manifests."""

    provides_by_skill: dict[str, list[str]] = {}
    consumes_by_skill: dict[str, list[dict[str, Any]]] = {}
    provider_by_handoff: dict[str, str] = {}
    consumers_by_handoff: dict[str, set[str]] = {}
    issues: dict[str, list[str]] = {}

    for skill_name, _, manifest in iter_skill_manifests(skills_root):
        handoffs = manifest.get("handoffs", {})
        if not isinstance(handoffs, dict):
            if handoffs:
                issues.setdefault(skill_name, []).append("handoffs must be a mapping")
            provides_by_skill[skill_name] = []
            consumes_by_skill[skill_name] = []
            continue

        provides = handoffs.get("provides", {})
        if not isinstance(provides, dict):
            issues.setdefault(skill_name, []).append("handoffs.provides must be a mapping")
            provides = {}

        provides_by_skill[skill_name] = sorted(str(name) for name in provides)
        for handoff_name in provides_by_skill[skill_name]:
            existing_provider = provider_by_handoff.get(handoff_name)
            if existing_provider and existing_provider != skill_name:
                issues.setdefault("handoffs", []).append(
                    f"handoff '{handoff_name}' is provided by both "
                    f"{existing_provider} and {skill_name}"
                )
            provider_by_handoff[handoff_name] = skill_name

        consumes = _normalize_consumes(handoffs.get("consumes", []))
        consumes_by_skill[skill_name] = consumes
        for consume in consumes:
            consumers_by_handoff.setdefault(str(consume["handoff"]), set()).add(skill_name)

    return {
        "provides_by_skill": provides_by_skill,
        "consumes_by_skill": consumes_by_skill,
        "provider_by_handoff": provider_by_handoff,
        "consumers_by_handoff": consumers_by_handoff,
        "issues": issues,
    }


def _contract_names() -> set[str]:
    return {path.stem for path in CONTRACTS_DIR.glob("*.yaml")}


def _contract_consumers(contract: dict[str, Any]) -> set[str]:
    consumed_by = contract.get("consumed_by", [])
    if not isinstance(consumed_by, list):
        return set()
    return {str(item) for item in consumed_by if str(item)}


def _add_issue(issues: dict[str, list[str]], key: str, message: str) -> None:
    issues.setdefault(key, []).append(message)


def _validate_template_paths(
    contract_name: str,
    contract: dict[str, Any],
    issues: dict[str, list[str]],
) -> None:
    templates = contract.get("templates", [])
    if not isinstance(templates, list):
        return
    for template_ref in templates:
        if not isinstance(template_ref, str):
            continue
        template_path = (CONTRACTS_DIR / template_ref).resolve()
        if not template_path.exists():
            _add_issue(
                issues,
                "contracts",
                f"template not found: {template_ref} (referenced by contract '{contract_name}')",
            )


def validate_all() -> dict[str, list[str]]:
    """Run all handoff checks and return {skill_or_category: [issues]}."""

    topology = collect_manifest_handoff_topology()
    issues: dict[str, list[str]] = {
        key: list(values)
        for key, values in (topology["issues"]).items()  # type: ignore[union-attr]
    }
    provides_by_skill = topology["provides_by_skill"]  # type: ignore[assignment]
    consumes_by_skill = topology["consumes_by_skill"]  # type: ignore[assignment]
    provider_by_handoff = topology["provider_by_handoff"]  # type: ignore[assignment]
    consumers_by_handoff = topology["consumers_by_handoff"]  # type: ignore[assignment]

    manifest_handoffs = set(provider_by_handoff) | set(consumers_by_handoff)
    contract_handoffs = _contract_names()

    for name in sorted(manifest_handoffs - contract_handoffs):
        _add_issue(
            issues,
            "contracts",
            f"contract '{name}.yaml' referenced but not found in _shared/contracts/",
        )

    for skill, consumes in consumes_by_skill.items():
        for consume in consumes:
            name = str(consume["handoff"])
            actual_provider = provider_by_handoff.get(name)
            expected_provider = consume.get("from")
            if not actual_provider:
                _add_issue(
                    issues,
                    skill,
                    f"consumes '{name}' but no skill provides it (dangling)",
                )
            elif expected_provider and expected_provider != actual_provider:
                _add_issue(
                    issues,
                    skill,
                    f"consumes '{name}' from {expected_provider} but actual provider is {actual_provider}",
                )

    for name in sorted(manifest_handoffs | contract_handoffs):
        contract = load_contract(name)
        if contract is None:
            continue
        _validate_template_paths(name, contract, issues)

        actual_provider = provider_by_handoff.get(name)
        expected_provider = contract.get("produced_by")
        if expected_provider and actual_provider and expected_provider != actual_provider:
            _add_issue(
                issues,
                "contracts",
                f"contract '{name}' says produced_by={expected_provider} but actual provider is {actual_provider}",
            )
        elif expected_provider and not actual_provider:
            _add_issue(
                issues,
                "contracts",
                f"contract '{name}' says produced_by={expected_provider} but no manifest provides it",
            )

        expected_consumers = _contract_consumers(contract)
        actual_consumers = consumers_by_handoff.get(name, set())
        missing_in_manifests = expected_consumers - actual_consumers
        missing_in_contract = actual_consumers - expected_consumers
        if missing_in_manifests:
            _add_issue(
                issues,
                "contracts",
                f"contract '{name}' consumed_by not declared in manifests: {sorted(missing_in_manifests)}",
            )
        if missing_in_contract:
            _add_issue(
                issues,
                "contracts",
                f"contract '{name}' missing consumed_by entries for manifest consumers: {sorted(missing_in_contract)}",
            )

    for skill, provides in provides_by_skill.items():
        for name in provides:
            if not consumers_by_handoff.get(name):
                _add_issue(
                    issues,
                    skill,
                    f"provides '{name}' is not consumed by any skill (orphan)",
                )

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate handoff contracts across all skills")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    issues = validate_all()

    if args.json:
        print(json.dumps({
            "status": "pass" if not issues else "fail",
            "issues": issues,
        }, indent=2, ensure_ascii=False))
    else:
        if issues:
            for category, cat_issues in issues.items():
                for issue in cat_issues:
                    print(f"[{category}] {issue}")
            print(f"\nFAIL: {sum(len(v) for v in issues.values())} handoff issues found")
        else:
            print("PASS: all handoff contracts valid")

    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())

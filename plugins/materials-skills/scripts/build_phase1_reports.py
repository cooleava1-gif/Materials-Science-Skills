"""Build auditable Phase 1 constraint and behavior-scoring reports."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

import build_behavior_campaign as behavior


REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_SKILLS_ROOT = Path(__file__).resolve().parent.parent / "skills"
DEFAULT_REPORT_ROOT = REPO_ROOT / "reports" / "skill-simplification"

NORMATIVE_RE = re.compile(
    r"\b(must|never|do not|don't|stop|block|required|only|missing|route|handoff|schema|evidence|invent|fabricat|source data|proof|claim|gate|verify|validation|contract)\b",
    re.IGNORECASE,
)


def _scenario_index() -> dict[str, dict[str, list[str]]]:
    payload = behavior.build_campaign()
    index: dict[str, dict[str, list[str]]] = {}
    for skill, scenarios in payload["skills"].items():
        by_category: dict[str, list[str]] = {}
        for scenario in scenarios:
            by_category.setdefault(scenario["category"], []).append(scenario["id"])
        index[skill] = by_category
    return index


def _classify(text: str) -> str:
    lowered = text.lower()
    if any(word in lowered for word in ("handoff", "schema", "contract")):
        return "handoff_schema"
    if any(word in lowered for word in ("evidence", "invent", "fabricat", "citation", "claim", "proof")):
        return "evidence_boundary"
    if any(word in lowered for word in ("stop", "block", "missing", "gate", "verify", "validation")):
        return "blocking"
    if any(word in lowered for word in ("route", "manifest", "axis", "load", "selected")):
        return "routing"
    if any(word in lowered for word in ("output", "package", "format", "deliver")):
        return "output_contract"
    if any(word in lowered for word in ("material", "asphalt", "ceramic", "polymer", "metal", "nano", "domain")):
        return "domain_specificity"
    return "process"


def _risk(category: str) -> str:
    if category in {"evidence_boundary", "blocking", "handoff_schema", "domain_specificity"}:
        return "high"
    if category in {"routing", "output_contract"}:
        return "medium"
    return "low"


def _decision(category: str) -> tuple[str, str, str]:
    if category in {"evidence_boundary", "blocking", "handoff_schema", "domain_specificity"}:
        return (
            "retain_pending_ab",
            "High-risk scientific or workflow boundary; behavior evidence is required before any shortening.",
            "Keep the canonical rule and compress only explanatory repetition after A/B/C verification.",
        )
    return (
        "candidate_compress_after_ab",
        "Potentially compressible instruction, but no deletion is authorized before behavior comparison.",
        "Replace repeated explanation with a canonical reference or deterministic check only if the same behavior remains green.",
    )


def _source_files(skill_dir: Path, manifest: dict[str, Any]) -> list[Path]:
    package_root = skill_dir.parent.parent.resolve()
    requested = [skill_dir / "SKILL.md", skill_dir / "manifest.yaml"]
    always_load = manifest.get("always_load", [])
    if isinstance(always_load, list):
        requested.extend(skill_dir / str(path) for path in always_load)
    result: list[Path] = []
    seen: set[Path] = set()
    for path in requested:
        resolved = path.resolve()
        if resolved in seen:
            continue
        seen.add(resolved)
        if not resolved.is_file():
            continue
        if not _within(resolved, package_root):
            continue
        result.append(resolved)
    return result


def _within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def build_constraint_ledger(
    skills_root: Path = DEFAULT_SKILLS_ROOT,
) -> list[dict[str, Any]]:
    skills_root = Path(skills_root).resolve()
    scenario_index = _scenario_index()
    rows: list[dict[str, Any]] = []
    for skill_dir in sorted(skills_root.glob("materials-*")):
        if not skill_dir.is_dir() or not (skill_dir / "manifest.yaml").is_file():
            continue
        skill = skill_dir.name
        manifest = yaml.safe_load((skill_dir / "manifest.yaml").read_text(encoding="utf-8")) or {}
        for source_path in _source_files(skill_dir, manifest):
            source_text = source_path.read_text(encoding="utf-8")
            source_rel = source_path.relative_to(REPO_ROOT).as_posix()
            source_hash = hashlib.sha256(source_path.read_bytes()).hexdigest()
            for line_number, raw_line in enumerate(source_text.splitlines(), start=1):
                excerpt = raw_line.strip()
                if not excerpt or excerpt.startswith("---") or not NORMATIVE_RE.search(excerpt):
                    continue
                category = _classify(excerpt)
                risk = _risk(category)
                decision, reason, replacement = _decision(category)
                category_ids = scenario_index.get(skill, {}).get(category, [])
                if not category_ids:
                    category_ids = [
                        scenario_id
                        for ids in scenario_index.get(skill, {}).values()
                        for scenario_id in ids
                    ][:3]
                rows.append(
                    {
                        "constraint_id": f"{skill}-{source_path.stem}-{line_number:04d}",
                        "skill": skill,
                        "source": f"{source_rel}#L{line_number}",
                        "source_sha256": source_hash,
                        "source_excerpt": excerpt[:500],
                        "category": category,
                        "risk": risk,
                        "applies_when": "Whenever the task reaches the condition stated by the source rule.",
                        "deterministic_check": (
                            "validate_manifest.py + behavior_campaign"
                            if source_path.name == "manifest.yaml"
                            else f"behavior_campaign:{skill}"
                        ),
                        "decision": decision,
                        "reason": reason,
                        "replacement": replacement,
                        "test_ids": category_ids,
                    }
                )

    # Add explicit review rows for the duplicate candidates discovered in Phase 0.
    duplicate_reviews = [
        ("materials-figure", "figure-default-duplicate", "SKILL.md vs manifest.yaml", "The Python/data blocking gate appears in two default sources."),
        ("materials-figure", "figure-contract-stance-overlap", "static/core/contract.md vs static/core/stance.md", "A repeated figure-description phrase needs an authority decision."),
        ("materials-citation", "citation-contract-duplicate", "_shared/contracts/citation-handoff.yaml vs citation contract", "The handoff schema and local contract overlap and require one authority."),
        ("materials-literature-pipeline", "pipeline-stable-id-overlap", "SKILL.md vs static/core/workflow.md", "Stable candidate ID and deduplication rules repeat across default sources."),
        ("materials-response", "response-contract-overlap", "SKILL.md vs static/core/response-contract.md", "Response package/proof wording may be duplicated; retain until behavior evidence."),
    ]
    for skill, identifier, source, reason in duplicate_reviews:
        test_ids = [
            scenario["id"]
            for scenario in behavior.build_campaign()["skills"].get(skill, [])
            if scenario["category"] in {"overclaim_or_fabrication", "handoff_schema", "route_conflict"}
        ]
        rows.append(
            {
                "constraint_id": f"shared-{identifier}",
                "skill": skill,
                "source": source,
                "source_sha256": "",
                "source_excerpt": reason,
                "category": "authority_review",
                "risk": "high",
                "applies_when": "When two default-activation sources express the same behavior boundary.",
                "deterministic_check": "check_skill_architecture.py + behavior_campaign",
                "decision": "review_shared_authority",
                "reason": reason,
                "replacement": "Choose one canonical authority only after A/B/C evidence; keep a thin pointer at the other location if needed.",
                "test_ids": test_ids,
            }
        )
    return rows


def build_rubric() -> dict[str, Any]:
    return {
        "version": 1,
        "score_values": ["pass", "fail", "pending"],
        "overall_rule": "Overall pass requires pass on all seven dimensions and no forbidden behavior; any critical forbidden behavior is an overall fail.",
        "dimensions": [
            {
                "id": "evidence_fidelity",
                "label": "Evidence fidelity",
                "pass_if": "Every factual or scientific claim is supported by supplied evidence or explicitly marked as a hypothesis, gap, or input-needed item.",
                "fail_if": "The response invents data, citations, DOI, results, locations, or completed actions, or upgrades metadata/proxy evidence into proof.",
            },
            {
                "id": "materials_correctness",
                "label": "Materials correctness",
                "pass_if": "Material identity, units, dosage basis, test conditions, mechanism language, and domain-specific interpretation stay consistent with the scenario.",
                "fail_if": "The response confuses material families, dosage bases, phases, curing/demulsification stages, or transfers unsupported domain claims.",
            },
            {
                "id": "constraint_compliance",
                "label": "Constraint compliance",
                "pass_if": "All applicable source rules and explicit forbidden behaviors are followed, including required markers and no fabricated substitutes.",
                "fail_if": "The response bypasses a stated stop condition, treats a template as measured evidence, or follows a prohibited shortcut.",
            },
            {
                "id": "blocking_correctness",
                "label": "Blocking correctness",
                "pass_if": "Missing, contradictory, unavailable, or invalid inputs trigger a precise block, question, or bounded draft with the exact next input requested.",
                "fail_if": "The response silently assumes the missing input, continues past a failed gate, or reports a blocker without identifying its cause.",
            },
            {
                "id": "routing_correctness",
                "label": "Routing correctness",
                "pass_if": "The response selects the declared route, distinguishes neighboring skills, and names any required handoff without loading unrelated workflows.",
                "fail_if": "The response merges conflicting routes, invokes an unrequested skill, or sends work to a companion skill without a bounded artifact.",
            },
            {
                "id": "output_contract",
                "label": "Output contract",
                "pass_if": "The requested package, IDs, schema fields, provenance, file list, and status markers are present and internally consistent.",
                "fail_if": "Required fields, stable IDs, artifact paths, handoff schema, or status distinctions are missing or contradictory.",
            },
            {
                "id": "actionability",
                "label": "Actionability",
                "pass_if": "The response gives a bounded next action, exact missing input, or reproducible check that a researcher can execute.",
                "fail_if": "The response is only generic advice, leaves the user unable to proceed, or presents an unverified result as the next action.",
            },
        ],
    }


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _markdown_ledger(rows: list[dict[str, Any]]) -> str:
    counts = Counter(row["decision"] for row in rows)
    lines = [
        "# Constraint Ledger (Phase 1)",
        "",
        "This ledger is an audit inventory. `retain_pending_ab` and `candidate_compress_after_ab` are not deletion approvals; each row requires behavior evidence before a Skill is edited.",
        "",
        f"Rows: {len(rows)}; decisions: {dict(counts)}.",
        "",
        "| ID | Skill | Category | Risk | Decision | Source | Tests |",
        "|---|---|---|---|---|---|---|",
    ]
    for row in rows:
        tests = ", ".join(row["test_ids"][:4])
        lines.append(
            f"| {row['constraint_id']} | {row['skill']} | {row['category']} | {row['risk']} | {row['decision']} | {row['source']} | {tests} |"
        )
    return "\n".join(lines) + "\n"


def _markdown_rubric(rubric: dict[str, Any]) -> str:
    lines = [
        "# Behavior Campaign Rubric",
        "",
        rubric["overall_rule"],
        "",
        "Scores are binary (`pass`/`fail`) or `pending`; do not use a fuzzy quality score.",
        "",
        "| Dimension | Pass if | Fail if |",
        "|---|---|---|",
    ]
    for item in rubric["dimensions"]:
        lines.append(f"| {item['label']} (`{item['id']}`) | {item['pass_if']} | {item['fail_if']} |")
    return "\n".join(lines) + "\n"


def write_phase1_reports(report_root: Path = DEFAULT_REPORT_ROOT) -> dict[str, Path]:
    report_root = Path(report_root)
    ledger = build_constraint_ledger()
    rubric = build_rubric()
    paths = {
        "ledger_json": report_root / "constraint-ledger.json",
        "ledger_md": report_root / "constraint-ledger.md",
        "rubric_json": report_root / "behavior-rubric.json",
        "rubric_md": report_root / "behavior-rubric.md",
    }
    _write_json(paths["ledger_json"], {"version": 1, "rows": ledger})
    paths["ledger_md"].parent.mkdir(parents=True, exist_ok=True)
    paths["ledger_md"].write_text(_markdown_ledger(ledger), encoding="utf-8")
    _write_json(paths["rubric_json"], rubric)
    paths["rubric_md"].write_text(_markdown_rubric(rubric), encoding="utf-8")
    return paths


if __name__ == "__main__":
    print(write_phase1_reports())

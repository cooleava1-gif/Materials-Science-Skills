import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
SKILLS_ROOT = REPO_ROOT / "skills"
RESEARCH_ROOT = SKILLS_ROOT / "civil-materials-research"
SHARED_ROOT = SKILLS_ROOT / "_shared" / "paper-production"
WEAKNESS_EXAMPLE = SHARED_ROOT / "examples" / "wer-ea-mini-review-weakness-routing.csv"
GATE_EXAMPLE = SHARED_ROOT / "examples" / "wer-ea-mini-review-gate-report.md"
ROUTE_EXAMPLE = (
    RESEARCH_ROOT
    / "examples"
    / "library"
    / "paper-production-mini-review-example.md"
)


WEAKNESS_FIELDS = [
    "weakness_id",
    "source",
    "severity",
    "weakness_type",
    "evidence_gap",
    "route_to",
    "required_fix",
    "expected_artifact",
    "status",
    "regression_check",
]

GATE_FIELDS = [
    "gate_id",
    "gate_name",
    "status",
    "evidence_checked",
    "missing_inputs",
    "routed_weakness_ids",
    "next_skill",
    "reviewer_risk",
]


def load_audit_module():
    path = SHARED_ROOT / "audit_paper_production.py"
    spec = importlib.util.spec_from_file_location("audit_paper_production", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PaperProductionOrchestratorTest(unittest.TestCase):
    def test_research_manifest_exposes_orchestrator_axes_and_reference(self):
        manifest = yaml.safe_load((RESEARCH_ROOT / "manifest.yaml").read_text(encoding="utf-8"))
        axes = manifest["axes"]

        for axis in ["paper_stage", "workflow_mode", "output_package"]:
            self.assertIn(axis, axes)

        self.assertEqual(
            axes["workflow_mode"]["values"]["paper-production"]["path"],
            "references/paper-production-orchestrator.md",
        )
        self.assertEqual(
            axes["output_package"]["values"]["gate-report"]["path"],
            "../_shared/paper-production/paper-gate-report-template.md",
        )
        self.assertIn("paper-production-orchestrator", manifest["references"]["on_demand"])
        self.assertIn("../_shared/paper-production/weakness-routing.md", manifest["always_load"])

    def test_orchestrator_reference_covers_submission_route_and_gate_contracts(self):
        path = RESEARCH_ROOT / "references" / "paper-production-orchestrator.md"
        self.assertTrue(path.exists())
        text = path.read_text(encoding="utf-8")

        for phrase in [
            "WER-EA mini-review",
            "experimental manuscript",
            "Submission Package",
            "cover letter",
            "graphical abstract",
            "declarations",
            "Literature Coverage",
            "Source Anchoring",
            "Mechanism Boundary",
            "Figure And Table Integrity",
            "Manuscript Logic",
            "Reviewer Simulation",
            "Submission Fit",
            "weakness-routing-template.csv",
            "paper-gate-report-template.md",
        ]:
            self.assertIn(phrase, text)

    def test_shared_templates_have_required_fields_and_routes(self):
        weakness_template = SHARED_ROOT / "weakness-routing-template.csv"
        gate_template = SHARED_ROOT / "paper-gate-report-template.md"
        weakness_reference = SHARED_ROOT / "weakness-routing.md"

        self.assertTrue(weakness_template.exists())
        self.assertTrue(gate_template.exists())
        self.assertTrue(weakness_reference.exists())

        with weakness_template.open("r", encoding="utf-8", newline="") as handle:
            header = next(csv.reader(handle))
        self.assertEqual(header, WEAKNESS_FIELDS)

        gate_text = gate_template.read_text(encoding="utf-8")
        for field in GATE_FIELDS:
            self.assertIn(field, gate_text)

        routing_text = weakness_reference.read_text(encoding="utf-8")
        for skill in [
            "civil-materials-citation",
            "civil-materials-reader",
            "civil-materials-writing",
            "civil-materials-polishing",
            "civil-materials-figure",
            "civil-materials-data",
            "civil-materials-response",
        ]:
            self.assertIn(skill, routing_text)

    def test_filled_paper_production_examples_exist_and_are_linked(self):
        self.assertTrue(WEAKNESS_EXAMPLE.exists())
        self.assertTrue(GATE_EXAMPLE.exists())
        self.assertTrue(ROUTE_EXAMPLE.exists())

        route_doc = (RESEARCH_ROOT / "references" / "paper-production-orchestrator.md").read_text(
            encoding="utf-8"
        )
        for phrase in [
            "paper-production-mini-review-example.md",
            "wer-ea-mini-review-weakness-routing.csv",
            "wer-ea-mini-review-gate-report.md",
        ]:
            self.assertIn(phrase, route_doc)

    def test_audit_script_accepts_valid_files_and_rejects_missing_fields(self):
        audit = load_audit_module()
        valid_weakness = SHARED_ROOT / "weakness-routing-template.csv"
        valid_gate = SHARED_ROOT / "paper-gate-report-template.md"

        report = audit.audit_files(valid_weakness, valid_gate)
        self.assertEqual(report["status"], "pass", report)

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            bad_weakness = tmp_path / "weakness.csv"
            bad_gate = tmp_path / "gate.md"
            bad_weakness.write_text("weakness_id,source\nW001,reviewer\n", encoding="utf-8")
            bad_gate.write_text("| gate_id | gate_name |\n|---|---|\n", encoding="utf-8")

            bad_report = audit.audit_files(bad_weakness, bad_gate)

        self.assertEqual(bad_report["status"], "fail")
        self.assertTrue(bad_report["issues"]["weakness_routing"])
        self.assertTrue(bad_report["issues"]["gate_report"])

    def test_audit_script_rejects_invalid_row_values_and_unknown_links(self):
        audit = load_audit_module()

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            bad_weakness = tmp_path / "weakness.csv"
            bad_gate = tmp_path / "gate.md"
            bad_weakness.write_text(
                "\n".join(
                    [
                        ",".join(WEAKNESS_FIELDS),
                        "W-G2-001,gate:G2,major,source_anchor_missing,gap,civil-materials-reader,fix,reader-package/source_map.json,done,maybe",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            bad_gate.write_text(
                "\n".join(
                    [
                        "# Gate Report",
                        "",
                        "| gate_id | gate_name | status | evidence_checked | missing_inputs | routed_weakness_ids | next_skill | reviewer_risk |",
                        "|---|---|---|---|---|---|---|---|",
                        "| G1 | Literature Coverage | pass | ok | none | none | civil-materials-citation | controlled |",
                        "| G2 | Source Anchoring | review-needed | anchors missing | source_map.json | W-G2-404 | civil-materials-reader | unsupported claim |",
                        "| G3 | Mechanism Boundary | blocked | partial | mechanism evidence table | none | civil-materials-reader; civil-materials-citation | overclaim risk |",
                        "| G4 | Figure And Table Integrity | pass | ok | none | none | civil-materials-figure | controlled |",
                        "| G5 | Manuscript Logic | blocked | partial | claim-evidence-boundary table | none | civil-materials-writing | list-like draft |",
                        "| G6 | Reviewer Simulation | not_applicable | draft missing | manuscript draft | none | civil-materials-reviewer | not yet pressure-tested |",
                        "| G7 | Submission Fit | not_applicable | journal not chosen | target journal | none | civil-materials-research | stale journal facts |",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            report = audit.audit_files(bad_weakness, bad_gate)

        self.assertEqual(report["status"], "fail")
        self.assertTrue(report["issues"]["weakness_routing"])
        self.assertTrue(report["issues"]["gate_report"])
        self.assertTrue(
            any("invalid status" in issue or "unknown weakness id" in issue for issue in report["issues"]["gate_report"]),
            report,
        )

    def test_audit_script_accepts_filled_wer_ea_examples(self):
        audit = load_audit_module()
        report = audit.audit_files(WEAKNESS_EXAMPLE, GATE_EXAMPLE)
        self.assertEqual(report["status"], "pass", report)

    def test_companion_contracts_consume_paper_production_artifacts(self):
        checks = {
            "civil-materials-writing": [
                "reader-package",
                "citation_handoff.csv",
                "claim-evidence-boundary",
                "gate report",
            ],
            "civil-materials-polishing": [
                "evidence_level",
                "weakness route",
                "claim strength",
            ],
            "civil-materials-reviewer": [
                "weakness-routing rows",
                "weakness-routing-template.csv",
                "route_to",
            ],
            "civil-materials-response": [
                "weakness-routing rows",
                "point-by-point",
                "revision proof",
            ],
            "civil-materials-figure": [
                "figure_handoff",
                "caption_boundary",
                "source_anchor",
                "gate report",
            ],
        }
        for skill, phrases in checks.items():
            with self.subTest(skill=skill):
                root = SKILLS_ROOT / skill
                text = "\n".join(
                    path.read_text(encoding="utf-8")
                    for path in [
                        root / "static" / "core" / "contract.md",
                        root / "manifest.yaml",
                    ]
                    if path.exists()
                )
                for phrase in phrases:
                    self.assertIn(phrase, text)

    def test_release_gate_contains_paper_production_bucket(self):
        release_text = (REPO_ROOT / "scripts" / "run_release_checks.py").read_text(encoding="utf-8")
        self.assertIn("paper_production_orchestrator", release_text)
        self.assertIn("collect_paper_production_orchestrator_issues", release_text)
        self.assertIn("paper-production-mini-review-example.md", release_text)
        self.assertIn("wer-ea-mini-review-weakness-routing.csv", release_text)
        self.assertIn("wer-ea-mini-review-gate-report.md", release_text)


if __name__ == "__main__":
    unittest.main()

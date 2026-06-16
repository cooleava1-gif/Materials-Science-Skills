import subprocess
import sys
import tempfile
import unittest
from pathlib import Path



def _find_repo_root():
    p = Path(__file__).resolve()
    for parent in [p] + list(p.parents):
        if (parent / ".git").exists() or (parent / "AGENTS.md").exists():
            return parent
    return p.parents[3]
SKILL_ROOT = Path(__file__).resolve().parents[1]


class ReviewerSkillStructureTest(unittest.TestCase):
    def test_skill_entrypoint_manifest_and_openai_agent_exist(self):
        skill = SKILL_ROOT / "SKILL.md"
        manifest = SKILL_ROOT / "manifest.yaml"
        openai = SKILL_ROOT / "agents" / "openai.yaml"

        self.assertTrue(skill.exists(), "SKILL.md should exist")
        self.assertTrue(manifest.exists(), "manifest.yaml should exist")
        self.assertTrue(openai.exists(), "agents/openai.yaml should exist")

        skill_text = skill.read_text(encoding="utf-8")
        manifest_text = manifest.read_text(encoding="utf-8")
        openai_text = openai.read_text(encoding="utf-8")

        self.assertIn("name: materials-reviewer", skill_text)
        self.assertIn("review", skill_text.lower())
        self.assertIn("cross-review synthesis", skill_text)
        ref_text = (SKILL_ROOT / "references" / "report-structure.md").read_text(encoding="utf-8")
        for recommendation in ["Accept", "Minor Revision", "Major Revision", "Reject"]:
            self.assertIn(recommendation, ref_text)
        for axis in ["journal_family", "review_depth", "quick-scan", "standard", "detailed", "CBM", "CCC", "RMPD", "JBE"]:
            self.assertIn(axis, manifest_text)
        for phrase in ["interface:", "policy:", "allow_implicit_invocation"]:
            self.assertIn(phrase, openai_text)

    def test_core_and_reference_files_cover_reviewer_axes(self):
        expected = {
            "static/core/reviewer-stance.md": ["evidence-driven", "constructive", "referee perspective"],
            "static/core/workflow.md": ["read manuscript", "independent review", "cross-review synthesis"],
            "references/editorial-criteria.md": ["CBM", "CCC", "RMPD", "JBE", "desk rejection"],
            "references/review-axes.md": ["Innovation", "Methodology", "Evidence completeness", "Figure/table quality"],
            "references/report-structure.md": ["Major comments", "Minor comments", "Recommendation"],
            "references/asphalt-reviewer-criteria.md": ["Asphalt", "Emulsified asphalt", "Bonding", "Storage stability"],
            "references/cement-reviewer-criteria.md": ["Cement", "Concrete", "Water-binder ratio", "Compressive strength"],
            "references/ceramics-reviewer-criteria.md": ["Sintering", "Flexural strength", "XRD", "SEM"],
            "references/insulation-reviewer-criteria.md": ["Thermal conductivity", "Density", "Compressive strength", "Moisture"],
            "references/mechanism-evidence-checklist.md": ["FTIR", "SEM", "fluorescence", "rheology"],
            "references/qa-checklist.md": ["overclaim", "missing test conditions", "replicate", "scale bar"],
        }
        for relative, phrases in expected.items():
            path = SKILL_ROOT / relative
            self.assertTrue(path.exists(), f"{relative} should exist")
            text = path.read_text(encoding="utf-8")
            for phrase in phrases:
                self.assertIn(phrase, text)

    def test_examples_and_pressure_test_have_required_sections(self):
        for filename in ["cbm-review-simulation.md", "ccc-review-simulation.md"]:
            path = SKILL_ROOT / "examples" / filename
            self.assertTrue(path.exists(), f"{filename} should exist")
            text = path.read_text(encoding="utf-8")
            for section in ["## Reviewer A", "## Reviewer B", "## Cross-Review Synthesis"]:
                self.assertIn(section, text)

        pressure = SKILL_ROOT / "tests" / "pressure-tests" / "weak-manuscript-review.md"
        self.assertTrue(pressure.exists())
        pressure_text = pressure.read_text(encoding="utf-8")
        for section in ["## Prompt", "## Expected Behavior", "## Failure Signs"]:
            self.assertIn(section, pressure_text)

    def test_release_checks_include_reviewer_skill(self):
        release_script = _find_repo_root() / "scripts" / "run_release_checks.py"
        text = release_script.read_text(encoding="utf-8")

        self.assertIn('"materials-reviewer"', text)
        self.assertIn('"materials-reviewer" / "tests"', text)

    def test_research_router_lists_reviewer_companion_skill(self):
        research_root = SKILL_ROOT.parents[0] / "materials-research"
        skill_text = (research_root / "SKILL.md").read_text(encoding="utf-8")
        manifest_text = (research_root / "manifest.yaml").read_text(encoding="utf-8")
        companion_text = (research_root / "references" / "companion-modules.md").read_text(encoding="utf-8")

        self.assertIn("materials-reviewer", manifest_text)
        self.assertIn("reviewer: materials-reviewer", manifest_text)
        self.assertIn("materials-reviewer", companion_text)
        self.assertIn("simulated peer review", companion_text.lower())


class ReviewerReportScriptTest(unittest.TestCase):
    def test_build_review_report_creates_two_reviews_and_synthesis(self):
        script = SKILL_ROOT / "scripts" / "build_review_report.py"
        self.assertTrue(script.exists(), "build_review_report.py should exist")

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "review.md"
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--title",
                    "Waterborne epoxy modified emulsified asphalt tack coat",
                    "--journal-family",
                    "CBM",
                    "--output",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            self.assertIn(str(output), result.stdout)
            text = output.read_text(encoding="utf-8")
            for phrase in [
                "Reviewer A",
                "Reviewer B",
                "Cross-review synthesis",
                "Major Revision",
                "Innovation and contribution",
                "Evidence completeness",
            ]:
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()

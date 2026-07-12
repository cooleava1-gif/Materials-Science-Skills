import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

def _find_repo_root():
    p = Path(__file__).resolve()
    for parent in [p] + list(p.parents):
        if (parent / ".git").exists() or (parent / "AGENTS.md").exists():
            return parent
    return p.parents[3]

SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = _find_repo_root()
sys.path.insert(0, str(REPO_ROOT / "plugins" / "materials-skills"))

from scripts.skill_manifest import discover_skill_names


class WritingSkillStructureTest(unittest.TestCase):
    def test_slim_router_keeps_profile_and_explicit_fragment_loading(self):
        manifest = yaml.safe_load((SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8"))
        self.assertIn("../_shared/core/direction-profile.md", manifest["always_load"])

        skill_text = (SKILL_ROOT / "SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("for each selected axis", skill_text)
        self.assertIn("read the mapped path", skill_text)
        self.assertIn("profile precedence", skill_text)

    def test_opt_in_qa_references_are_declared_and_exist(self):
        manifest = yaml.safe_load((SKILL_ROOT / "manifest.yaml").read_text(encoding="utf-8"))
        on_demand = manifest["references"]["on_demand"]
        expected = {
            "foundation-files",
            "stopping-rules",
            "evaluation-rubric",
            "validation-checklist",
            "content-first-qa-pipeline",
        }
        self.assertTrue(expected.issubset(on_demand))
        for name in expected:
            path = SKILL_ROOT / on_demand[name]["path"]
            self.assertTrue(path.exists(), f"missing QA reference: {path}")

    def test_core_contract_links_resolve_from_static_core(self):
        contract = (SKILL_ROOT / "static" / "core" / "contract.md").read_text(encoding="utf-8")
        self.assertIn("../../../_shared/core/stance.md", contract)
        self.assertIn("../../../_shared/paper-production/weakness-routing.md", contract)

    def test_readme_documents_tiered_confirmation_gate(self):
        readme = (SKILL_ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("single-section", readme)
        self.assertIn("full-manuscript", readme)
        self.assertIn("confirmation gate", readme)

    def test_skill_entrypoint_manifest_agent_and_release_checks_exist(self):
        skill = SKILL_ROOT / "SKILL.md"
        manifest = SKILL_ROOT / "manifest.yaml"
        openai = SKILL_ROOT / "agents" / "openai.yaml"
        release_script = REPO_ROOT / "scripts" / "run_release_checks.py"
        plugin_release_script = REPO_ROOT / "plugins" / "materials-skills" / "scripts" / "run_release_checks.py"
        readme = REPO_ROOT / "README.md"

        for path in [skill, manifest, openai, release_script, plugin_release_script]:
            self.assertTrue(path.exists(), f"{path.name} should exist")

        skill_text = skill.read_text(encoding="utf-8")
        manifest_text = manifest.read_text(encoding="utf-8")
        openai_text = openai.read_text(encoding="utf-8")
        release_text = release_script.read_text(encoding="utf-8")
        plugin_release_text = plugin_release_script.read_text(encoding="utf-8")
        readme_text = readme.read_text(encoding="utf-8")

        self.assertIn("name: materials-writing", skill_text)
        ref_text = (SKILL_ROOT / "references" / "argument-chain.md").read_text(encoding="utf-8")
        self.assertIn("argument", ref_text)
        for axis in ["paper_type", "section", "language", "journal_family"]:
            self.assertIn(axis, manifest_text)
        for phrase in ["experimental-manuscript", "review-paper", "abstract", "introduction", "results-discussion"]:
            self.assertIn(phrase, manifest_text)
        for phrase in ["interface:", "policy:", "allow_implicit_invocation"]:
            self.assertIn(phrase, openai_text)
        self.assertIn("discover_skill_names", plugin_release_text)
        self.assertIn("materials-writing", discover_skill_names())
        self.assertIn("materials-writing", readme_text)

    def test_core_fragments_references_templates_examples_and_pressure_tests(self):
        expected = {
            "static/core/stance.md": ["Moved to _shared"],
            str(Path("..") / "_shared" / "core" / "stance.md"): ["Never invent", "Placeholder conventions", "claim-evidence chain"],
            "static/core/workflow.md": ["one-sentence argument", "claim-evidence-boundary", "section draft"],
            "static/fragments/paper_type/experimental-manuscript.md": ["waterborne epoxy", "test matrix", "mechanism"],
            "static/fragments/paper_type/review-paper.md": ["small review", "thematic dimensions", "knowledge gap"],
            "static/fragments/section/abstract.md": ["Background", "Gap", "Method", "Result", "Implication"],
            "static/fragments/section/introduction.md": ["gap ladder", "evidence gap", "paper entry"],
            "static/fragments/section/results-discussion.md": ["Result", "Mechanism", "Limitation"],
            "references/argument-chain.md": ["Problem", "Gap", "Hypothesis", "Evidence", "Boundary"],
            "references/waterborne-epoxy-narrative.md": ["emulsified asphalt", "bonding performance", "curing"],
            "references/review-paper-strategy.md": ["mini-review", "taxonomy", "research agenda"],
            "references/reviewer-risk-writing.md": ["overclaim", "missing evidence", "journal fit"],
            "assets/templates/manuscript-argument-template.md": ["Core claim", "Evidence", "Boundary"],
            "assets/templates/section-draft-template.md": ["Section goal", "Input evidence", "Draft"],
            "examples/waterborne-epoxy-abstract-example.md": ["## Input", "## Draft", "## Why It Works"],
            "examples/review-outline-example.md": ["## Topic", "## Outline", "## Contribution Logic"],
            "tests/pressure-tests/missing-data-writing.md": ["## Prompt", "## Expected Behavior", "## Failure Signs"],
        }
        for relative, phrases in expected.items():
            path = SKILL_ROOT / relative
            self.assertTrue(path.exists(), f"{relative} should exist")
            text = path.read_text(encoding="utf-8")
            for phrase in phrases:
                self.assertIn(phrase, text)

    def test_research_router_lists_writing_companion_skill(self):
        research_root = SKILL_ROOT.parents[0] / "materials-research"
        skill_text = (research_root / "SKILL.md").read_text(encoding="utf-8")
        manifest_text = (research_root / "manifest.yaml").read_text(encoding="utf-8")
        companion_text = (research_root / "references" / "companion-modules.md").read_text(encoding="utf-8")

        self.assertIn("materials-writing", manifest_text)
        self.assertIn("writing: materials-writing", manifest_text)
        self.assertIn("materials-writing", companion_text)
        self.assertIn("from-scratch manuscript drafting", companion_text.lower())


class WritingOutlineScriptTest(unittest.TestCase):
    def test_build_manuscript_outline_creates_argument_chain(self):
        script = SKILL_ROOT / "scripts" / "build_manuscript_outline.py"
        self.assertTrue(script.exists(), "build_manuscript_outline.py should exist")

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "outline.md"
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--topic",
                    "waterborne epoxy modified emulsified asphalt bonding performance",
                    "--paper-type",
                    "experimental-manuscript",
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
                "One-sentence argument",
                "Claim-evidence-boundary table",
                "Abstract",
                "Introduction",
                "Results and Discussion",
                "Missing evidence to confirm",
            ]:
                self.assertIn(phrase, text)

    def test_outline_no_hardcoded_content_for_different_topic(self):
        """A different topic must not contain waterborne-epoxy remnants."""
        script = SKILL_ROOT / "scripts" / "build_manuscript_outline.py"

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "outline.md"
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--topic",
                    "ceramic matrix composites",
                    "--output",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            text = output.read_text(encoding="utf-8")
            for forbidden in [
                "waterborne epoxy",
                "tack coat",
                "emulsion",
                "Modified emulsion",
                "emulsified asphalt",
            ]:
                self.assertNotIn(
                    forbidden, text,
                    f"Output should not contain hardcoded remnant: {forbidden!r}",
                )
            # Section headers must still be present
            for phrase in [
                "One-sentence argument",
                "Claim-evidence-boundary table",
                "Abstract",
                "Introduction",
                "Results and Discussion",
                "Missing evidence to confirm",
            ]:
                self.assertIn(phrase, text)

    def test_outline_review_paper_type(self):
        """--paper-type review-paper should produce review/literature text."""
        script = SKILL_ROOT / "scripts" / "build_manuscript_outline.py"

        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "outline.md"
            result = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "--topic",
                    "ceramic matrix composites",
                    "--paper-type",
                    "review-paper",
                    "--output",
                    str(output),
                ],
                check=True,
                capture_output=True,
                text=True,
            )

            text = output.read_text(encoding="utf-8")
            # The one-sentence argument should mention "review"
            self.assertIn("review", text.lower())
            # Missing evidence section should mention literature-related items
            self.assertIn("literature", text.lower())
            # Section headers must still be present
            for phrase in [
                "One-sentence argument",
                "Claim-evidence-boundary table",
                "Abstract",
                "Introduction",
                "Results and Discussion",
                "Missing evidence to confirm",
            ]:
                self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()

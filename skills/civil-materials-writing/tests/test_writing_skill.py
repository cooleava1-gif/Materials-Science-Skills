import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parents[1]


class WritingSkillStructureTest(unittest.TestCase):
    def test_skill_entrypoint_manifest_agent_and_release_checks_exist(self):
        skill = SKILL_ROOT / "SKILL.md"
        manifest = SKILL_ROOT / "manifest.yaml"
        openai = SKILL_ROOT / "agents" / "openai.yaml"
        release_script = REPO_ROOT / "scripts" / "run_release_checks.py"
        readme = REPO_ROOT / "README.md"

        for path in [skill, manifest, openai]:
            self.assertTrue(path.exists(), f"{path.name} should exist")

        skill_text = skill.read_text(encoding="utf-8")
        manifest_text = manifest.read_text(encoding="utf-8")
        openai_text = openai.read_text(encoding="utf-8")
        release_text = release_script.read_text(encoding="utf-8")
        readme_text = readme.read_text(encoding="utf-8")

        self.assertIn("name: civil-materials-writing", skill_text)
        self.assertIn("claim-evidence-boundary", skill_text)
        for axis in ["paper_type", "section", "language", "journal_family"]:
            self.assertIn(axis, manifest_text)
        for phrase in ["experimental-manuscript", "review-paper", "abstract", "introduction", "results-discussion"]:
            self.assertIn(phrase, manifest_text)
        for phrase in ["interface:", "policy:", "allow_implicit_invocation"]:
            self.assertIn(phrase, openai_text)
        self.assertIn('"civil-materials-writing"', release_text)
        self.assertIn('"civil-materials-writing" / "tests"', release_text)
        self.assertIn("civil-materials-writing", readme_text)

    def test_core_fragments_references_templates_examples_and_pressure_tests(self):
        expected = {
            "static/core/stance.md": ["evidence-first", "professional researcher", "no invented data"],
            "static/core/workflow.md": ["one-sentence argument", "claim-evidence-boundary", "section draft"],
            "static/fragments/paper_type/experimental-manuscript.md": ["waterborne epoxy", "test matrix", "mechanism"],
            "static/fragments/paper_type/review-paper.md": ["small review", "thematic logic", "knowledge gap"],
            "static/fragments/section/abstract.md": ["background", "gap", "method", "result", "implication"],
            "static/fragments/section/introduction.md": ["funnel", "gap chain", "contribution"],
            "static/fragments/section/results-discussion.md": ["result", "mechanism", "limitation"],
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
        research_root = REPO_ROOT / "skills" / "civil-materials-research"
        skill_text = (research_root / "SKILL.md").read_text(encoding="utf-8")
        manifest_text = (research_root / "manifest.yaml").read_text(encoding="utf-8")
        companion_text = (research_root / "references" / "companion-modules.md").read_text(encoding="utf-8")

        self.assertIn("civil-materials-writing", skill_text)
        self.assertIn("writing: civil-materials-writing", manifest_text)
        self.assertIn("civil-materials-writing", companion_text)
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


if __name__ == "__main__":
    unittest.main()

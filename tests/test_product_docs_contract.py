import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "civil-materials-skills"
SKILLS = [
    "civil-materials-citation",
    "civil-materials-data",
    "civil-materials-figure",
    "civil-materials-paper2ppt",
    "civil-materials-polishing",
    "civil-materials-pptx",
    "civil-materials-reader",
    "civil-materials-research",
    "civil-materials-response",
    "civil-materials-reviewer",
    "civil-materials-writing",
]
SKILL_README_SECTIONS = [
    "## When To Use",
    "## Inputs",
    "## Outputs",
    "## Example",
    "## Validation",
    "## Boundaries",
]
WORKFLOW_DEMOS = {
    "wer-ea-mini-review": "WER-EA mini-review",
    "experimental-manuscript": "Experimental manuscript",
    "revision-loop": "Revision loop",
    "paper-to-presentation": "Paper to presentation",
}
WORKFLOW_README_SECTIONS = [
    "## Route Summary",
    "## Demo Prompt",
    "## Workflow Steps",
    "## Expected Artifacts",
    "## What Good Looks Like",
]


class ProductDocsContractTests(unittest.TestCase):
    def test_root_docs_present_a_productized_entry_surface(self):
        readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
        install_path = ROOT / "install.md"
        self.assertTrue(install_path.is_file(), "install.md must exist")

        for marker in [
            "## Quick Start",
            "## Four Workflow Entry Points",
            "## Installation Paths",
            "## Skill Status Index",
            "## Guided Demos",
            "## Visual Gallery",
        ]:
            self.assertIn(marker, readme_text)

        install_text = install_path.read_text(encoding="utf-8")
        for marker in [
            "# Install Civil Materials Skills",
            "## Option 1: Codex Plugin",
            "## Option 2: Manual Skills Install",
            "## Verify The Install",
            "## Five-Minute Walkthrough",
            "## Guided Demo Routes",
        ]:
            self.assertIn(marker, install_text)

    def test_workflow_demo_docs_exist_with_concrete_routes(self):
        workflow_index = ROOT / "docs" / "workflows" / "README.md"
        self.assertTrue(workflow_index.is_file(), "docs/workflows/README.md must exist")
        index_text = workflow_index.read_text(encoding="utf-8")
        self.assertIn("# Workflow Demos", index_text)
        self.assertIn("## Workflow Index", index_text)

        for slug, title in WORKFLOW_DEMOS.items():
            path = ROOT / "docs" / "workflows" / f"{slug}.md"
            self.assertTrue(path.is_file(), f"{path} must exist")
            text = path.read_text(encoding="utf-8")
            self.assertIn(f"# {title}", text)
            for marker in WORKFLOW_README_SECTIONS:
                self.assertIn(marker, text, f"{slug} missing section {marker}")

    def test_gallery_doc_uses_real_assets_and_links_to_proof(self):
        gallery_path = ROOT / "docs" / "gallery" / "README.md"
        self.assertTrue(gallery_path.is_file(), "docs/gallery/README.md must exist")
        gallery_text = gallery_path.read_text(encoding="utf-8")

        for marker in [
            "# Civil Materials Gallery",
            "## Screenshot Gallery",
            "## Workflow Proof",
            "## Artifact Deep Dives",
        ]:
            self.assertIn(marker, gallery_text)

        for asset in [
            "wer_ea_mechanism_map.png",
            "wer_ea_evidence_heatmap.png",
            "wer_ea_dosage_window.png",
            "contact_sheet.png",
        ]:
            self.assertIn(asset, gallery_text)

    def test_every_skill_has_a_human_readme_with_core_sections(self):
        for skill in SKILLS:
            readme_path = ROOT / "skills" / skill / "README.md"
            self.assertTrue(readme_path.is_file(), f"{readme_path} must exist")
            readme_text = readme_path.read_text(encoding="utf-8")
            self.assertIn(f"# {skill}", readme_text)
            for marker in SKILL_README_SECTIONS:
                self.assertIn(marker, readme_text, f"{skill} missing section {marker}")

    def test_plugin_metadata_shows_real_assets_and_workflows(self):
        plugin_json = json.loads(
            (PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8")
        )
        interface = plugin_json["interface"]
        screenshots = interface.get("screenshots")
        self.assertIsInstance(screenshots, list)
        self.assertGreaterEqual(len(screenshots), 3)
        for relative_path in screenshots:
            self.assertIsInstance(relative_path, str)
            self.assertTrue(relative_path.endswith(".png"))
            self.assertTrue((PLUGIN_ROOT / relative_path.removeprefix("./")).is_file(), relative_path)

        prompts = interface.get("defaultPrompt")
        self.assertIsInstance(prompts, list)
        self.assertEqual(3, len(prompts))
        self.assertTrue(any("WER-EA" in prompt for prompt in prompts), prompts)
        self.assertTrue(any("manuscript" in prompt.lower() for prompt in prompts), prompts)
        self.assertTrue(any("PPT" in prompt or "ppt" in prompt for prompt in prompts), prompts)


if __name__ == "__main__":
    unittest.main()

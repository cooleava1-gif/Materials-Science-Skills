import json
import re
import unittest
from collections import Counter
from pathlib import Path

import yaml
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "materials-skills"
REGISTRY_ENTRIES = PLUGIN_ROOT / "_shared" / "material-registry" / "entries"
SKILLS = [
    "materials-citation",
    "materials-data",
    "materials-figure",
    "materials-paper2ppt",
    "materials-polishing",
    "materials-pptx",
    "materials-reader",
    "materials-research",
    "materials-response",
    "materials-reviewer",
    "materials-writing",
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
OUTCOME_SHOWCASES = {
    "submission-package": "Submission package",
    "reviewer-response": "Reviewer response",
    "fair-data-package": "FAIR data package",
}
OUTCOME_SHOWCASE_SECTIONS = [
    "## Outcome Snapshot",
    "## Demo Prompt",
    "## Proof Assets",
    "## Build Path",
    "## When To Use This Route",
]
GALLERY_PROOF_ASSETS = {
    "reader_package_proof_wall.png": "Reader-package proof wall",
    "wer_ea_figure_proof_board.png": "WER-EA figure proof board",
    "sbr_wer_performance_proof_board.png": "SBR-WER performance proof board",
    "interlayer_fatigue_proof_board.png": "Interlayer fatigue proof board",
}
SHOWCASE_MANIFEST = "showcase_manifest.json"
LEGACY_PLACEHOLDER_ASSETS = [
    "wer_ea_mechanism_map.png",
    "wer_ea_evidence_heatmap.png",
    "wer_ea_dosage_window.png",
]
REMOVED_GENERAL_ROUTE_MARKERS = [
    "general-materials",
    "general-experiments.md",
    "materials-general-reviewer-criteria.md",
    "default: general",
    "universal fallback",
    "anything not explicitly listed",
]


def image_has_visual_signal(path: Path) -> bool:
    with Image.open(path) as image:
        rgba = image.convert("RGBA")
        extrema = rgba.getextrema()
        return rgba.width >= 1200 and rgba.height >= 700 and any(
            (high - low) >= 40 for low, high in extrema[:3]
        )


def load_registry_entries() -> list[dict]:
    return [
        yaml.safe_load(path.read_text(encoding="utf-8"))
        for path in sorted(REGISTRY_ENTRIES.glob("*.yaml"))
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
            "## Skills",
            "## Guided Demos",
            "## Visual Gallery",
            "## Outcome Showcases",
        ]:
            self.assertIn(marker, readme_text)
        self.assertIn("wer_ea_figure_proof_board.png", readme_text)
        for legacy in LEGACY_PLACEHOLDER_ASSETS:
            self.assertNotIn(legacy, readme_text)

        install_text = install_path.read_text(encoding="utf-8")
        for marker in [
            "# Install Materials Science Skills",
            "## Option 1: Codex Plugin",
            "## Option 2: Manual Skills Install",
            "## Verify The Install",
            "## Five-Minute Walkthrough",
            "## Guided Demo Routes",
            "## Showcase Shortcuts",
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
            "# Materials Science Gallery",
            "## Screenshot Gallery",
            "## Workflow Proof",
            "## Artifact Deep Dives",
            "## Outcome Showcases",
        ]:
            self.assertIn(marker, gallery_text)

        showcase_root = PLUGIN_ROOT / "skills" / "materials-figure" / "assets" / "showcase-proof"
        for asset in GALLERY_PROOF_ASSETS:
            self.assertIn(asset, gallery_text)
            image_refs = re.findall(r"!\[[^\]]*\]\(([^)]+)\)", gallery_text)
            matching_refs = [ref for ref in image_refs if ref.endswith(asset)]
            self.assertTrue(matching_refs, f"{asset} must be linked from gallery")
            for ref in matching_refs:
                resolved_ref = (gallery_path.parent / ref).resolve()
                self.assertTrue(resolved_ref.is_file(), f"{ref} should resolve to a tracked proof asset")
            asset_path = showcase_root / asset
            self.assertTrue(asset_path.is_file(), f"{asset_path} must exist")
            self.assertTrue(image_has_visual_signal(asset_path), f"{asset_path} should be a content-bearing image")
        manifest_path = showcase_root / SHOWCASE_MANIFEST
        self.assertTrue(manifest_path.is_file(), "showcase manifest should exist")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["visual_language"], "editorial-proof-boards")
        self.assertEqual(len(manifest["boards"]), len(GALLERY_PROOF_ASSETS))
        for legacy in LEGACY_PLACEHOLDER_ASSETS:
            self.assertNotIn(legacy, gallery_text)

    def test_outcome_showcase_docs_exist_with_real_proof_assets(self):
        showcase_index = ROOT / "docs" / "showcases" / "README.md"
        self.assertTrue(showcase_index.is_file(), "docs/showcases/README.md must exist")
        index_text = showcase_index.read_text(encoding="utf-8")
        self.assertIn("# Outcome Showcases", index_text)
        self.assertIn("## Outcome Index", index_text)

        for slug, title in OUTCOME_SHOWCASES.items():
            path = ROOT / "docs" / "showcases" / f"{slug}.md"
            self.assertTrue(path.is_file(), f"{path} must exist")
            text = path.read_text(encoding="utf-8")
            self.assertIn(f"# {title}", text)
            for marker in OUTCOME_SHOWCASE_SECTIONS:
                self.assertIn(marker, text, f"{slug} missing section {marker}")

    def test_every_skill_has_a_human_readme_with_core_sections(self):
        for skill in SKILLS:
            readme_path = PLUGIN_ROOT / "skills" / skill / "README.md"
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
            self.assertIn("showcase-proof", relative_path)
            self.assertTrue((PLUGIN_ROOT / relative_path.removeprefix("./")).is_file(), relative_path)

        prompts = interface.get("defaultPrompt")
        self.assertIsInstance(prompts, list)
        self.assertEqual(3, len(prompts))
        self.assertTrue(any("WER-EA" in prompt for prompt in prompts), prompts)
        self.assertTrue(any("manuscript" in prompt.lower() for prompt in prompts), prompts)
        self.assertTrue(any("PPT" in prompt or "ppt" in prompt for prompt in prompts), prompts)

    def test_material_coverage_docs_match_registry(self):
        entries = load_registry_entries()
        entry_ids = {entry["id"] for entry in entries}
        tier_counts = Counter(entry["coverage_tier"] for entry in entries)

        readme_text = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            f"currently covers **{len(entries)} material systems**",
            readme_text,
        )
        for tier, label in {
            "full": "🟢 **full**",
            "partial": "🟡 **partial**",
            "skeleton": "🔵 **skeleton**",
            "generic": "⚪ **generic**",
        }.items():
            self.assertIn(f"| {label} | {tier_counts[tier]} |", readme_text)

        dashboard_text = (ROOT / "docs" / "coverage-dashboard.md").read_text(encoding="utf-8")
        material_table = dashboard_text.split("## Tier Definitions", 1)[0]
        listed_ids = {
            line.split("**", 2)[1]
            for line in material_table.splitlines()
            if line.startswith("| **") and line.count("**") >= 2
        }
        self.assertEqual(entry_ids, listed_ids)

    def test_dashboard_per_row_tier_matches_registry(self):
        """Every dashboard row must show the same tier as the registry entry."""
        entries = {e["id"]: e for e in load_registry_entries()}
        dashboard_text = (ROOT / "docs" / "coverage-dashboard.md").read_text(encoding="utf-8")
        material_table = dashboard_text.split("## Tier Definitions", 1)[0]
        tier_markers = {
            "full": "🟢 **full**",
            "partial": "🟡 **partial**",
            "skeleton": "🔵 **skeleton**",
            "generic": "⚪ **generic**",
        }
        mismatches = []
        for line in material_table.splitlines():
            if not line.startswith("| **") or line.count("**") < 2:
                continue
            domain_id = line.split("**", 2)[1]
            if domain_id not in entries:
                continue
            expected_marker = tier_markers[entries[domain_id]["coverage_tier"]]
            if expected_marker not in line:
                mismatches.append(
                    f"{domain_id}: registry={entries[domain_id]['coverage_tier']}, "
                    f"dashboard line does not contain '{expected_marker}'"
                )
        self.assertEqual([], mismatches, "Dashboard tier drift detected:\n" + "\n".join(mismatches))

    def test_manifest_domain_tiers_match_registry(self):
        """The materials-research manifest domain coverage_tier must match the registry."""
        entries = {e["id"]: e for e in load_registry_entries()}
        manifest_path = PLUGIN_ROOT / "skills" / "materials-research" / "manifest.yaml"
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
        domain_values = manifest["axes"]["domain"]["values"]
        mismatches = []
        for domain_id, config in domain_values.items():
            if domain_id == "general":
                continue
            if domain_id not in entries:
                continue
            manifest_tier = config.get("coverage_tier", "(missing)")
            registry_tier = entries[domain_id]["coverage_tier"]
            if manifest_tier != registry_tier:
                mismatches.append(
                    f"{domain_id}: manifest={manifest_tier}, registry={registry_tier}"
                )
        self.assertEqual(
            [],
            mismatches,
            "Manifest ↔ registry tier drift detected:\n" + "\n".join(mismatches),
        )

    def test_docs_do_not_advertise_removed_general_routes(self):
        # Internal compose/superpowers notes are ignored local planning files.
        # This contract covers the tracked public documentation surface.
        docs_to_check = [
            ROOT / "README.md",
            ROOT / "install.md",
            ROOT / "docs" / "coverage-dashboard.md",
            ROOT / "docs" / "skills-index.md",
            ROOT / "docs" / "gallery" / "README.md",
            ROOT / "docs" / "showcases" / "README.md",
            ROOT / "docs" / "workflows" / "README.md",
        ]
        for path in docs_to_check:
            text = path.read_text(encoding="utf-8")
            for marker in REMOVED_GENERAL_ROUTE_MARKERS:
                with self.subTest(path=path.relative_to(ROOT), marker=marker):
                    self.assertNotIn(marker, text)


if __name__ == "__main__":
    unittest.main()

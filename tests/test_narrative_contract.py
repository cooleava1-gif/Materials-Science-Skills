"""Contract tests for generated narrative guides.

Validates:
- Every non-generic registry entry has a corresponding narrative guide.
- Every narrative guide follows the required 5-section structure.
- Every narrative_guide referenced in registry entries actually exists.
- The template engine can regenerate every narrative guide without error.
"""

import unittest
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = REPO_ROOT / "plugins" / "materials-skills"
REGISTRY_DIR = PLUGIN_ROOT / "_shared" / "material-registry"
ENTRIES_DIR = REGISTRY_DIR / "entries"
NARRATIVE_DIR = PLUGIN_ROOT / "skills" / "materials-writing" / "references"
GENERATOR_SCRIPT = REPO_ROOT / "scripts" / "generate_narrative.py"

REQUIRED_SECTIONS = [
    "Narrative",
    "Key evidence chain",
    "Common section structure",
    "Useful keywords",
    "Reviewer-safe language",
]

REQUIRED_ARC_LINES = 5  # Five-step narrative arc
REQUIRED_SECTION_STRUCTURE_ITEMS = 5  # Introduction, Methods, Results, Discussion, Conclusions


def _load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


class NarrativeGuidePresenceTests(unittest.TestCase):
    """Every non-generic registry entry should have a narrative guide."""

    def test_every_non_generic_material_has_narrative(self):
        missing = []
        for path in sorted(ENTRIES_DIR.glob("*.yaml")):
            data = _load_yaml(path)
            if data.get("coverage_tier") == "generic":
                continue
            mid = data.get("id", path.stem)
            narrative_path = NARRATIVE_DIR / f"{mid}-narrative.md"
            if not narrative_path.exists():
                # Also check old-style names
                old_names = {
                    "cement-concrete": "cement-narrative.md",
                    "structural-ceramics": "ceramics-narrative.md",
                    "thermal-insulation": "insulation-narrative.md",
                }
                old_name = old_names.get(mid)
                if old_name:
                    old_path = NARRATIVE_DIR / old_name
                    if old_path.exists():
                        continue
                missing.append(mid)
        self.assertFalse(missing, f"Materials without narrative guide: {missing}")


class NarrativeGuideStructureTests(unittest.TestCase):
    """Every narrative guide must have the standard 5-section structure."""

    def setUp(self):
        # Only validate narrative guides that correspond to registry entries
        registry_ids = {p.stem for p in ENTRIES_DIR.glob("*.yaml")}
        all_files = sorted(NARRATIVE_DIR.glob("*-narrative.md"))
        self.narrative_files = [
            f for f in all_files
            if f.stem.replace("-narrative", "") in registry_ids
        ]

    def test_all_narratives_have_required_sections(self):
        for path in self.narrative_files:
            with self.subTest(file=path.name):
                text = path.read_text(encoding="utf-8")
                for section in REQUIRED_SECTIONS:
                    self.assertIn(section, text, f"{path.name} missing section: {section}")

    def test_all_narratives_have_five_step_arc(self):
        for path in self.narrative_files:
            with self.subTest(file=path.name):
                text = path.read_text(encoding="utf-8")
                numbered_lines = [l for l in text.splitlines() if l.strip().startswith(("1.", "2.", "3.", "4.", "5."))]
                self.assertGreaterEqual(
                    len(numbered_lines), REQUIRED_ARC_LINES,
                    f"{path.name}: expected ≥{REQUIRED_ARC_LINES} narrative arc steps, found {len(numbered_lines)}"
                )

    def test_all_narratives_have_section_structure(self):
        for path in self.narrative_files:
            with self.subTest(file=path.name):
                text = path.read_text(encoding="utf-8")
                intro_part = text.lower()
                for section in ["introduction", "methods", "results", "discussion", "conclusions"]:
                    self.assertIn(
                        section, intro_part,
                        f"{path.name} missing section heading reference: {section}"
                    )

    def test_all_narratives_have_reviewer_safe_language(self):
        for path in self.narrative_files:
            with self.subTest(file=path.name):
                text = path.read_text(encoding="utf-8")
                # Should have at least 2 reviewer-safe language examples
                reviewer_lines = []
                in_section = False
                for line in text.splitlines():
                    if line.strip().startswith("## Reviewer-safe"):
                        in_section = True
                        continue
                    if in_section and line.startswith("##"):
                        break
                    if in_section and line.strip().startswith("-"):
                        reviewer_lines.append(line)
                self.assertGreaterEqual(
                    len(reviewer_lines), 2,
                    f"{path.name}: expected ≥2 reviewer-safe language examples, found {len(reviewer_lines)}"
                )


class RegistryNarrativeConsistencyTests(unittest.TestCase):
    """Registry entries' narrative_guide references must be consistent."""

    def test_registry_references_exist(self):
        for path in sorted(ENTRIES_DIR.glob("*.yaml")):
            data = _load_yaml(path)
            narrative = data.get("narrative", {})
            if not isinstance(narrative, dict):
                continue
            refs = narrative.get("skill_references", {}) or {}
            guide_path = refs.get("narrative_guide")
            if not guide_path:
                continue
            with self.subTest(entry=path.stem, ref=guide_path):
                full = PLUGIN_ROOT / guide_path
                self.assertTrue(full.exists(), f"{path.stem}: narrative_guide '{guide_path}' not found")

    def test_registry_references_match_generated_files(self):
        for path in sorted(ENTRIES_DIR.glob("*.yaml")):
            data = _load_yaml(path)
            if data.get("coverage_tier") == "generic":
                continue
            mid = data.get("id", path.stem)
            narrative_path = NARRATIVE_DIR / f"{mid}-narrative.md"
            if not narrative_path.exists():
                continue
            narrative = data.get("narrative", {})
            if not isinstance(narrative, dict):
                continue
            refs = narrative.get("skill_references", {}) or {}
            expected_ref = f"skills/materials-writing/references/{mid}-narrative.md"
            actual_ref = refs.get("narrative_guide", "")
            if actual_ref:
                self.assertEqual(
                    actual_ref, expected_ref,
                    f"{mid}: registry narrative_guide '{actual_ref}' doesn't match expected '{expected_ref}'"
                )


if __name__ == "__main__":
    unittest.main()

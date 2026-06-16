import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
PROFILE_SCRIPT = REPO_ROOT / "scripts" / "materials_profile.py"
PLUGIN_PROFILE_SCRIPT = REPO_ROOT / "plugins" / "materials-skills" / "scripts" / "materials_profile.py"
PROFILE_RULE = SKILLS_ROOT / "_shared" / "core" / "direction-profile.md"
MATERIAL_AXIS_NAMES = {"material_family", "domain", "material_domain"}
NEUTRAL_DEFAULTS = {"neutral", "general", "materials"}


class DirectionProfileContractTests(unittest.TestCase):
    def test_local_profile_path_is_gitignored(self):
        gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".materials/", gitignore)

    def test_shared_direction_profile_rule_exists(self):
        text = PROFILE_RULE.read_text(encoding="utf-8")
        self.assertIn(".materials/profile.yaml", text)
        self.assertIn("first use", text.lower())
        self.assertIn("neutral/general", text)

    def test_all_materials_skills_load_profile_rule_and_protocol(self):
        for skill_dir in sorted(SKILLS_ROOT.glob("materials-*")):
            with self.subTest(skill=skill_dir.name):
                manifest = yaml.safe_load((skill_dir / "manifest.yaml").read_text(encoding="utf-8"))
                always_load = manifest.get("always_load", [])
                self.assertIn("../_shared/core/direction-profile.md", always_load)

                skill_text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn(".materials/profile.yaml", skill_text)
                self.assertIn("profile-first", skill_text.lower())

    def test_material_axes_do_not_default_to_civil_domains(self):
        blocked_defaults = {"civil", "civil-generic", "asphalt", "asphalt-emulsion", "cement-concrete"}
        for manifest_path in sorted(SKILLS_ROOT.glob("materials-*/manifest.yaml")):
            manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
            axes = manifest.get("axes", {})
            for axis_name, axis in axes.items():
                if axis_name not in MATERIAL_AXIS_NAMES or not isinstance(axis, dict):
                    continue
                default = axis.get("default")
                with self.subTest(skill=manifest_path.parent.name, axis=axis_name):
                    self.assertNotIn(default, blocked_defaults)
                    self.assertIn(default, NEUTRAL_DEFAULTS)
                    self.assertIn(default, axis.get("values", {}))

    def test_profile_script_writes_normalized_profile(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    str(PROFILE_SCRIPT),
                    "--repo-root",
                    tmp,
                    "set",
                    "polymer composites",
                ],
                capture_output=True,
                text=True,
                check=True,
            )
            self.assertIn("polymer-composites", result.stdout)

            profile_path = Path(tmp) / ".materials" / "profile.yaml"
            profile = yaml.safe_load(profile_path.read_text(encoding="utf-8"))
            self.assertEqual("polymer composites", profile["raw_direction"])
            self.assertEqual("polymers", profile["material_family"])
            self.assertEqual("polymer-composites", profile["domain"])
            self.assertEqual("general", profile["fallback"])
            self.assertTrue(profile["remind_on_use"])

    def test_plugin_package_includes_profile_script(self):
        self.assertTrue(PLUGIN_PROFILE_SCRIPT.exists())
        self.assertEqual(
            PROFILE_SCRIPT.read_text(encoding="utf-8"),
            PLUGIN_PROFILE_SCRIPT.read_text(encoding="utf-8"),
        )

    def test_profile_script_falls_back_to_general_for_unknown_direction(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(
                [
                    sys.executable,
                    str(PROFILE_SCRIPT),
                    "--repo-root",
                    tmp,
                    "set",
                    "unknown frontier topic",
                ],
                capture_output=True,
                text=True,
                check=True,
            )

            profile = yaml.safe_load((Path(tmp) / ".materials" / "profile.yaml").read_text(encoding="utf-8"))
            self.assertEqual("neutral", profile["material_family"])
            self.assertEqual("general", profile["domain"])


if __name__ == "__main__":
    unittest.main()

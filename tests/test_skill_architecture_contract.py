import tempfile
import unittest
from pathlib import Path

from scripts.check_skill_architecture import inspect_all, inspect_skill


REPO_ROOT = Path(__file__).resolve().parents[1]


def _write_minimal_skill(skill_dir: Path, manifest: str) -> None:
    (skill_dir / "agents").mkdir(parents=True)
    (skill_dir / "static" / "core").mkdir(parents=True)
    (skill_dir / "references").mkdir(parents=True)
    (skill_dir / "assets" / "templates").mkdir(parents=True)
    (skill_dir / "scripts").mkdir(parents=True)
    (skill_dir / "tests").mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(
        "---\nname: fake\n---\n# Fake router\n", encoding="utf-8"
    )
    (skill_dir / "agents" / "openai.yaml").write_text("name: fake\n", encoding="utf-8")
    (skill_dir / "static" / "core" / "contract.md").write_text("# Contract\n", encoding="utf-8")
    (skill_dir / "static" / "core" / "workflow.md").write_text("# Workflow\n", encoding="utf-8")
    (skill_dir / "references" / "ok.md").write_text("# Reference\n", encoding="utf-8")
    (skill_dir / "assets" / "templates" / "ok.md").write_text("# Template\n", encoding="utf-8")
    (skill_dir / "scripts" / "ok.py").write_text("print('ok')\n", encoding="utf-8")
    (skill_dir / "tests" / "ok_test.py").write_text("def test_ok():\n    assert True\n", encoding="utf-8")
    (skill_dir / "manifest.yaml").write_text(manifest, encoding="utf-8")


class SkillArchitectureContractTests(unittest.TestCase):
    def test_all_materials_skills_follow_static_dynamic_architecture(self):
        report = inspect_all(Path("skills"))
        self.assertEqual("pass", report["status"], report)
        self.assertFalse(
            report["warnings"]["skills_with_missing_exact_core_files"],
            report["warnings"],
        )
        self.assertFalse(
            report["warnings"]["skills_with_missing_standard_manifest_blocks"],
            report["warnings"],
        )

    def test_architecture_checker_reports_missing_manifest_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "materials-fake"
            _write_minimal_skill(
                skill_dir,
                """
version: "0.0.1"
always_load:
  - static/core/contract.md
axes:
  task:
    values:
      broken:
        path: references/missing.md
        triggers: ["broken"]
assets:
  - assets/templates/ok.md
scripts:
  - scripts/ok.py
tests:
  - tests/ok_test.py
quality_gates: []
handoffs: []
release_checks: []
""",
            )

            report = inspect_skill(skill_dir)

        self.assertIn("references/missing.md", report["missing_manifest_paths"])

    def test_architecture_checker_detects_mojibake_trigger(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "materials-fake"
            _write_minimal_skill(
                skill_dir,
                """
version: "0.0.1"
always_load:
  - static/core/contract.md
axes:
  task:
    values:
      broken:
        path: references/ok.md
        triggers: ["閺傚洨灏濸DF"]
assets:
  - assets/templates/ok.md
scripts:
  - scripts/ok.py
tests:
  - tests/ok_test.py
quality_gates: []
handoffs: []
release_checks: []
""",
            )

            report = inspect_skill(skill_dir)

        self.assertTrue(report["mojibake_triggers"], report)

    def test_architecture_checker_requires_standard_manifest_blocks(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "materials-fake"
            _write_minimal_skill(
                skill_dir,
                """
version: "0.0.1"
always_load:
  - static/core/contract.md
axes:
  task:
    values:
      ok:
        path: references/ok.md
        triggers: ["ok"]
""",
            )

            report = inspect_skill(skill_dir)

        self.assertEqual(
            {
                "assets",
                "scripts",
                "tests",
                "quality_gates",
                "handoffs",
                "release_checks",
            },
            set(report["missing_manifest_blocks"]),
        )

    def test_architecture_checker_fails_on_unexpected_plugin_mirror_extra(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "skills"
            skill_dir = root / "materials-fake"
            _write_minimal_skill(
                skill_dir,
                """
version: "0.0.1"
always_load:
  - static/core/contract.md
axes:
  task:
    values:
      ok:
        path: references/ok.md
        triggers: ["ok"]
assets:
  - assets/templates/ok.md
scripts:
  - scripts/ok.py
tests:
  - tests/ok_test.py
quality_gates: []
handoffs: []
release_checks: []
""",
            )
            plugin_skill = Path(tmp) / "plugins" / "materials-skills" / "skills" / "materials-fake"
            plugin_skill.mkdir(parents=True)
            for source_file in skill_dir.rglob("*"):
                if source_file.is_file():
                    relative = source_file.relative_to(skill_dir)
                    target = plugin_skill / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(source_file.read_bytes())
            (plugin_skill / "plugin-only.md").write_text("stale\n", encoding="utf-8")

            report = inspect_all(root)

        self.assertEqual("fail", report["status"], report)
        self.assertIn("materials-fake/plugin-only.md", report["plugin_mirror"]["extra_plugin_files"])

    def test_release_check_includes_architecture_validation(self):
        release_text = (REPO_ROOT / "scripts" / "run_release_checks.py").read_text(encoding="utf-8")
        self.assertIn("check_skill_architecture.py", release_text)
        self.assertIn("inspect_all", release_text)


if __name__ == "__main__":
    unittest.main()

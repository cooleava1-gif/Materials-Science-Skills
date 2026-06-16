import json
import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATED_EXPORT_EXTENSIONS = {".svg", ".png", ".pdf", ".tif", ".tiff"}


def git_ls_files(*patterns: str) -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", *patterns],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return [line for line in result.stdout.splitlines() if line]


class FigureAssetSlimmingTests(unittest.TestCase):
    def test_figure_package_generated_exports_are_not_tracked(self):
        tracked = git_ls_files(
            "skills/materials-figure/examples/figure-packages/**/figure.*",
            "plugins/materials-skills/skills/materials-figure/examples/figure-packages/**/figure.*",
        )
        generated_exports = [
            path
            for path in tracked
            if Path(path).suffix.lower() in GENERATED_EXPORT_EXTENSIONS
        ]
        self.assertEqual([], generated_exports)

    def test_showcase_proof_screenshots_remain_tracked_for_product_surface(self):
        plugin_json = json.loads(
            (REPO_ROOT / "plugins" / "materials-skills" / ".codex-plugin" / "plugin.json")
            .read_text(encoding="utf-8")
        )
        screenshots = plugin_json["interface"]["screenshots"]
        tracked = set(git_ls_files(
            "skills/materials-figure/assets/showcase-proof/*.png",
            "plugins/materials-skills/skills/materials-figure/assets/showcase-proof/*.png",
        ))

        self.assertGreaterEqual(len(screenshots), 3)
        for screenshot in screenshots:
            plugin_relative = screenshot.removeprefix("./")
            source_relative = plugin_relative.removeprefix("skills/")
            self.assertIn(f"plugins/materials-skills/{plugin_relative}", tracked)
            self.assertIn(f"skills/{source_relative}", tracked)


if __name__ == "__main__":
    unittest.main()

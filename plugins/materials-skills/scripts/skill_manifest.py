"""Shared helpers for discovering materials skills and loading manifests."""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILLS_ROOT = REPO_ROOT / "skills"


def discover_skill_dirs(skills_root: Path = DEFAULT_SKILLS_ROOT) -> list[Path]:
    """Return current materials-* skill directories with manifests in stable order."""

    root = Path(skills_root)
    return sorted(
        path
        for path in root.glob("materials-*")
        if path.is_dir() and (path / "manifest.yaml").exists()
    )


def discover_skill_names(skills_root: Path = DEFAULT_SKILLS_ROOT) -> list[str]:
    """Return current materials-* skill names in stable order."""

    return [path.name for path in discover_skill_dirs(skills_root)]


def load_yaml(path: Path) -> dict[str, Any]:
    """Load a YAML mapping, returning an empty mapping for empty files."""

    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {}


def iter_skill_manifests(
    skills_root: Path = DEFAULT_SKILLS_ROOT,
) -> Iterator[tuple[str, Path, dict[str, Any]]]:
    """Yield (skill_name, skill_dir, manifest) for every current skill."""

    for skill_dir in discover_skill_dirs(skills_root):
        manifest_path = skill_dir / "manifest.yaml"
        if manifest_path.exists():
            yield skill_dir.name, skill_dir, load_yaml(manifest_path)

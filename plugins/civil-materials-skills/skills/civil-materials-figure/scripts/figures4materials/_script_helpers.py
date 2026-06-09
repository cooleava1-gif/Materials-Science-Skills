"""Helpers shared by the figures4materials example scripts."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


SCRIPT_ROOT = Path(__file__).resolve().parent
FIGURE_SKILL_SCRIPTS_ROOT = SCRIPT_ROOT.parent
sys.path.insert(0, str(FIGURE_SKILL_SCRIPTS_ROOT))


def data_path(name: str) -> Path:
    return SCRIPT_ROOT / "data" / name


def read_csv(path: str | Path) -> list[dict[str, str]]:
    with Path(path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def column(rows: list[dict[str, str]], name: str, *, as_float: bool = False):
    values = [row[name] for row in rows]
    if as_float:
        return [float(value) for value in values]
    return values


def print_caption(caption: str) -> None:
    print(f"Caption: {caption}")

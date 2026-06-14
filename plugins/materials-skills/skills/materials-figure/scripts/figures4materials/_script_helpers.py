"""Helpers shared by the figures4materials example scripts.

COLUMN_MAP convention
---------------------
Each figure script declares a COLUMN_MAP that maps semantic data roles
to actual column names in its CSV data file.  This lets any material
system reuse the same script: provide your own CSV with your own column
names, create a thin wrapper that overrides COLUMN_MAP, and the script
works unchanged.

Example COLUMN_MAP (for bonding_strength_bar):
    COLUMN_MAP = {
        "x_labels":    {"column": "dosage"},
        "series":      [
            {"key": "Dry", "column": "dry_mean", "error": "dry_sd"},
            {"key": "Wet", "column": "wet_mean", "error": "wet_sd"},
        ],
        "xlabel":      {"value": "Epoxy content (wt%)"},
        "ylabel":      {"value": "Pull-off strength (MPa)"},
        "caption":     {"value": "..."},
        "figure_name": {"value": "bonding_strength_comparison"},
    }

Load it:
    mapped = load_mapped_data(args.data, COLUMN_MAP)
    # mapped["x_labels"]     → list of str
    # mapped["series"]       → [{"key": "Dry", "values": [...], "errors": [...]}, ...]
    # mapped["xlabel"]       → str
    # mapped["ylabel"]       → str
"""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from typing import Any


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


def load_mapped_data(path: str | Path, column_map: dict[str, Any]) -> dict[str, Any]:
    """Read a CSV and organize its columns according to *column_map*.

    The map keys and their supported forms:

    ``x_labels`` / ``categories``
        ``{"column": "col_name"}``  →  list of str

    ``series``
        ``[{"key": "label", "column": "col", "error": "err_col"}, ...]``
        Each entry yields ``{"key": ..., "values": [float], "errors": [float] | None}``.

    ``y_values``
        ``[{"key": "label", "column": "col", "error": "err_col"}, ...]``
        Same shape as *series*.

    Any key ending in ``_text`` (e.g. ``xlabel``, ``ylabel``, ``caption``)
        ``{"value": "..."}``  →  returns that string literal.
        ``{"column": "col_name"}``  →  reads first row of that column.

    ``figure_name``
        ``{"value": "name"}``  →  used as the output filename.

    Values already present (e.g. pre-loaded lists) pass through unchanged.
    """
    rows = read_csv(path)
    result: dict[str, Any] = {}

    for key, spec in column_map.items():
        # --- series / y_values (list-based specs) -------------------------
        if key in ("series", "y_values") and isinstance(spec, list):
            parsed = []
            for entry in spec:
                item: dict[str, Any] = {"key": entry.get("key", "")}
                col = entry.get("column", "")
                item["values"] = column(rows, col, as_float=True) if col else []
                err_col = entry.get("error")
                if err_col:
                    item["errors"] = column(rows, err_col, as_float=True)
                parsed.append(item)
            result[key] = parsed
            continue

        if not isinstance(spec, dict):
            result[key] = spec  # pass-through literal
            continue

        # --- x_labels / categories ----------------------------------------
        if key in ("x_labels", "categories") and "column" in spec:
            result[key] = column(rows, spec["column"])

        # --- string values (xlabel, ylabel, caption, etc.) ----------------
        elif key.endswith("label") or key == "caption":
            if "value" in spec:
                result[key] = spec["value"]
            elif "column" in spec:
                result[key] = str(column(rows, spec["column"])[0]) if rows else ""

        # --- figure_name --------------------------------------------------
        elif key == "figure_name":
            result[key] = spec.get("value", "figure")

        # --- other --------------------------------------------------------
        else:
            result[key] = spec.get("value") or spec.get("column", "")

    return result


def print_caption(caption: str) -> None:
    print(f"Caption: {caption}")

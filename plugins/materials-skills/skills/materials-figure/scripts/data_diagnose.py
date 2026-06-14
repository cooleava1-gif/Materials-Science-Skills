#!/usr/bin/env python3
"""Diagnose tabular materials figure data for automatic chart generation."""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ERROR_COLUMN_TERMS = ("sd", "std", "se", "sem", "ci", "error", "err", "uncertainty")
GROUP_COLUMN_TERMS = ("group", "condition", "sample", "mix", "treatment", "variant", "material")
X_AXIS_TERMS = (
    "dosage",
    "content",
    "time",
    "temperature",
    "temp",
    "cycle",
    "age",
    "strain",
    "wavenumber",
    "two theta",
    "2theta",
    "2 theta",
    "frequency",
    "density",
    "humidity",
)
Y_AXIS_TERMS = (
    "strength",
    "retention",
    "viscosity",
    "modulus",
    "absorbance",
    "intensity",
    "conductivity",
    "stress",
    "mass",
    "heat flow",
    "current",
    "response",
    "performance",
)


class TableProfile:
    """Small serializable profile for a CSV/TSV table."""

    def __init__(
        self,
        *,
        path: str,
        delimiter: str,
        columns: list[str],
        row_count: int,
        numeric_columns: list[str],
        categorical_columns: list[str],
        error_columns: list[str],
        group_columns: list[str],
        likely_x_columns: list[str],
        likely_y_columns: list[str],
        unit_map: dict[str, str],
        missing_cells: dict[str, int],
        numeric_ranges: dict[str, list[float | None]],
        duplicate_key_count: int,
    ) -> None:
        self.path = path
        self.delimiter = delimiter
        self.columns = columns
        self.row_count = row_count
        self.numeric_columns = numeric_columns
        self.categorical_columns = categorical_columns
        self.error_columns = error_columns
        self.group_columns = group_columns
        self.likely_x_columns = likely_x_columns
        self.likely_y_columns = likely_y_columns
        self.unit_map = unit_map
        self.missing_cells = missing_cells
        self.numeric_ranges = numeric_ranges
        self.duplicate_key_count = duplicate_key_count

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "delimiter": self.delimiter,
            "columns": self.columns,
            "row_count": self.row_count,
            "numeric_columns": self.numeric_columns,
            "categorical_columns": self.categorical_columns,
            "error_columns": self.error_columns,
            "group_columns": self.group_columns,
            "likely_x_columns": self.likely_x_columns,
            "likely_y_columns": self.likely_y_columns,
            "unit_map": self.unit_map,
            "missing_cells": self.missing_cells,
            "numeric_ranges": self.numeric_ranges,
            "duplicate_key_count": self.duplicate_key_count,
        }


def diagnose_table(path: str | Path) -> TableProfile:
    """Read a CSV/TSV file and infer numeric, group, axis, unit, and error columns."""

    table_path = Path(path)
    rows, delimiter = read_table(table_path)
    columns = list(rows[0].keys()) if rows else []
    row_count = len(rows)

    numeric_columns: list[str] = []
    categorical_columns: list[str] = []
    error_columns: list[str] = []
    group_columns: list[str] = []
    likely_x_columns: list[str] = []
    likely_y_columns: list[str] = []
    unit_map: dict[str, str] = {}
    missing_cells: dict[str, int] = {}
    numeric_ranges: dict[str, list[float | None]] = {}

    for column in columns:
        values = [row.get(column, "") for row in rows]
        missing_cells[column] = sum(1 for value in values if str(value).strip() == "")
        unit = extract_unit(column)
        if unit:
            unit_map[column] = unit
        is_numeric = values and all(is_number(value) or str(value).strip() == "" for value in values)
        lower = column.lower()
        if is_numeric:
            numeric_columns.append(column)
            numeric_values = [parse_number(value) for value in values if is_number(value)]
            numeric_ranges[column] = [
                min(numeric_values) if numeric_values else None,
                max(numeric_values) if numeric_values else None,
            ]
        else:
            categorical_columns.append(column)

        if is_error_column(column):
            error_columns.append(column)
        if any(term in lower for term in GROUP_COLUMN_TERMS) or (not is_numeric and unique_count(values) <= max(12, row_count // 2 + 1)):
            group_columns.append(column)
        if any(term in lower for term in X_AXIS_TERMS):
            likely_x_columns.append(column)
        if any(term in lower for term in Y_AXIS_TERMS) and not is_error_column(column):
            likely_y_columns.append(column)

    if not likely_x_columns and numeric_columns:
        likely_x_columns.append(numeric_columns[0])
    if not likely_y_columns:
        likely_y_columns = [column for column in numeric_columns if column not in likely_x_columns and column not in error_columns]
    if not likely_y_columns and numeric_columns:
        likely_y_columns = [numeric_columns[-1]]

    duplicate_key_count = count_duplicate_keys(rows, group_columns[:1])
    if duplicate_key_count == 0:
        duplicate_key_count = count_duplicate_keys(rows, likely_x_columns[:1] + group_columns[:1])

    return TableProfile(
        path=str(table_path),
        delimiter=delimiter,
        columns=columns,
        row_count=row_count,
        numeric_columns=numeric_columns,
        categorical_columns=categorical_columns,
        error_columns=error_columns,
        group_columns=dedupe(group_columns),
        likely_x_columns=dedupe(likely_x_columns),
        likely_y_columns=dedupe(likely_y_columns),
        unit_map=unit_map,
        missing_cells=missing_cells,
        numeric_ranges=numeric_ranges,
        duplicate_key_count=duplicate_key_count,
    )


def read_table(path: Path) -> tuple[list[dict[str, str]], str]:
    if not path.is_file():
        raise FileNotFoundError(f"table not found: {path}")
    text = path.read_text(encoding="utf-8-sig")
    sample = text[:4096]
    if path.suffix.lower() == ".tsv":
        delimiter = "\t"
    else:
        try:
            delimiter = csv.Sniffer().sniff(sample, delimiters=",\t;").delimiter
        except csv.Error:
            delimiter = ","
    reader = csv.DictReader(text.splitlines(), delimiter=delimiter)
    rows = [{key.strip(): (value or "").strip() for key, value in row.items()} for row in reader]
    return rows, delimiter


def is_number(value: object) -> bool:
    if value is None:
        return False
    text = str(value).strip()
    if text == "":
        return False
    try:
        float(text)
    except ValueError:
        return False
    return True


def parse_number(value: object) -> float:
    return float(str(value).strip())


def extract_unit(column: str) -> str | None:
    match = re.search(r"\(([^)]+)\)", column)
    if match:
        return match.group(1).strip()
    return None


def is_error_column(column: str) -> bool:
    lower = column.lower().strip()
    return any(lower == term or term in lower for term in ERROR_COLUMN_TERMS)


def unique_count(values: list[str]) -> int:
    return len({str(value).strip() for value in values if str(value).strip()})


def count_duplicate_keys(rows: list[dict[str, str]], keys: list[str]) -> int:
    active_keys = [key for key in keys if key]
    if not active_keys:
        return 0
    counter = Counter(tuple(row.get(key, "") for key in active_keys) for row in rows)
    return sum(1 for count in counter.values() if count > 1)


def dedupe(items: list[str]) -> list[str]:
    seen = set()
    result: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("table", help="CSV or TSV data table")
    parser.add_argument("--json", action="store_true", help="print JSON profile")
    args = parser.parse_args(argv)

    profile = diagnose_table(args.table)
    if args.json:
        print(json.dumps(profile.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(json.dumps(profile.to_dict(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

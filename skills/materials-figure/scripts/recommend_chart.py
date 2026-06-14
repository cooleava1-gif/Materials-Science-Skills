#!/usr/bin/env python3
"""Recommend a materials figure chart type from a diagnosed table profile."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


class ChartRecommendation:
    """Serializable chart recommendation used by the automatic figure package."""

    def __init__(
        self,
        *,
        chart_type: str,
        title: str,
        x_column: str | None,
        y_column: str | None,
        error_column: str | None,
        group_column: str | None,
        reasons: list[str],
        reviewer_risks: list[str],
        export_formats: list[str],
        claim_boundary: str,
    ) -> None:
        self.chart_type = chart_type
        self.title = title
        self.x_column = x_column
        self.y_column = y_column
        self.error_column = error_column
        self.group_column = group_column
        self.reasons = reasons
        self.reviewer_risks = reviewer_risks
        self.export_formats = export_formats
        self.claim_boundary = claim_boundary

    def to_dict(self) -> dict[str, Any]:
        return {
            "chart_type": self.chart_type,
            "title": self.title,
            "x_column": self.x_column,
            "y_column": self.y_column,
            "error_column": self.error_column,
            "group_column": self.group_column,
            "reasons": self.reasons,
            "reviewer_risks": self.reviewer_risks,
            "export_formats": self.export_formats,
            "claim_boundary": self.claim_boundary,
        }


def recommend_chart(profile: Any, goal: str = "") -> ChartRecommendation:
    """Choose a conservative publication chart type from a table profile."""

    data = profile.to_dict() if hasattr(profile, "to_dict") else dict(profile)
    numeric_columns = data.get("numeric_columns", [])
    categorical_columns = data.get("categorical_columns", [])
    error_columns = data.get("error_columns", [])
    group_columns = data.get("group_columns", [])
    likely_x_columns = data.get("likely_x_columns", [])
    likely_y_columns = data.get("likely_y_columns", [])
    row_count = int(data.get("row_count", 0))
    duplicate_key_count = int(data.get("duplicate_key_count", 0))

    x_column = first(likely_x_columns) or first(numeric_columns)
    y_column = first([column for column in likely_y_columns if column != x_column])
    if y_column is None:
        y_column = first([column for column in numeric_columns if column != x_column])
    if y_column is None and group_columns:
        y_column = first([column for column in numeric_columns if column not in error_columns])
    error_column = first(error_columns)
    group_column = first(group_columns)
    goal_lower = goal.lower()

    reasons: list[str] = []
    risks = [
        "State replicate count (n) in caption or methods before using the figure as manuscript evidence.",
        "Define error bars as SD, SE, CI, or range.",
    ]
    chart_type = "scatter_regression"
    claim_boundary = "Association or trend only; the figure does not prove mechanism without independent evidence."

    if error_column and x_column and y_column:
        chart_type = "errorbar_trend"
        reasons.append(f"Numeric x column `{x_column}`, numeric response `{y_column}`, and error column `{error_column}` support an errorbar trend.")
        claim_boundary = "Supports a measured trend with uncertainty; optimum language needs statistics and durability context."
        if any(term in f"{goal_lower} {x_column.lower()}" for term in ["dosage", "content", "%", "optimum", "optimal"]):
            reasons.append("Dosage/content wording suggests an optimization or dosage-performance claim.")
            risks.append("Do not call a dosage optimum unless the caption names the tested range and supporting durability evidence.")
    elif duplicate_key_count > 0 and group_column and y_column:
        chart_type = "boxplot_points"
        reasons.append("Repeated group keys suggest raw replicate values suitable for boxplot with points.")
        risks.append("Boxplots should show raw points for small n and define outlier rules.")
        claim_boundary = "Supports distribution comparison; do not hide small replicate counts behind summary statistics."
    elif group_column and y_column and row_count <= 60:
        chart_type = "grouped_bar"
        reasons.append(f"Categorical grouping column `{group_column}` with response `{y_column}` supports grouped comparison.")
        risks.append("Grouped bars require clear group definitions and uncertainty when making superiority claims.")
        claim_boundary = "Supports group comparison only; significance requires statistical testing."
    elif len(numeric_columns) >= 4:
        chart_type = "correlation_heatmap"
        reasons.append("Four or more numeric columns can support a property correlation heatmap.")
        risks.append("Correlation heatmaps show association, not causation or mechanism.")
        claim_boundary = "Supports association screening only."
    else:
        reasons.append("Defaulted to scatter/regression because the table has numeric columns but no explicit error or group structure.")

    if chart_type in {"scatter_regression", "errorbar_trend"} and (x_column is None or y_column is None):
        chart_type = "grouped_bar" if categorical_columns else "table_summary"
        risks.append("Insufficient numeric axis structure for a trend plot.")
        claim_boundary = "Needs human review before manuscript use."

    return ChartRecommendation(
        chart_type=chart_type,
        title=make_title(chart_type, y_column),
        x_column=x_column,
        y_column=y_column,
        error_column=error_column,
        group_column=group_column,
        reasons=reasons,
        reviewer_risks=risks,
        export_formats=["SVG", "PNG"],
        claim_boundary=claim_boundary,
    )


def make_title(chart_type: str, y_column: str | None) -> str:
    label = y_column or "materials response"
    labels = {
        "errorbar_trend": f"{label} trend with uncertainty",
        "grouped_bar": f"{label} grouped comparison",
        "boxplot_points": f"{label} replicate distribution",
        "correlation_heatmap": "Materials property correlation heatmap",
        "scatter_regression": f"{label} association plot",
        "table_summary": "Materials data summary",
    }
    return labels.get(chart_type, label)


def first(values: list[str]) -> str | None:
    return values[0] if values else None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile-json", required=True, help="profile JSON file from data_diagnose.py")
    parser.add_argument("--goal", default="", help="figure goal or core conclusion")
    args = parser.parse_args(argv)

    payload = json.loads(Path(args.profile_json).read_text(encoding="utf-8"))
    recommendation = recommend_chart(payload, goal=args.goal)
    print(json.dumps(recommendation.to_dict(), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

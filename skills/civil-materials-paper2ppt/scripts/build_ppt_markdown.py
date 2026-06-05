#!/usr/bin/env python3
"""Create a slide-ready Markdown deck and optionally generate PPTX."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


DECKS = {
    ("project-report", "zh"): [
        ("题目", ["Topic: {title}", "Presenter:", "Date:"]),
        ("工程问题", ["服役中最关键的问题是什么？", "现有材料或工艺为什么不足？", "Slide message:"]),
        ("材料设计", ["材料体系:", "设计变量:", "预期机制:"]),
        ("试验矩阵", ["制备与变量:", "性能测试:", "机理/微观测试:", "耐久或服役测试:"]),
        ("关键结果 1", ["Claim:", "Evidence:", "Figure/table:", "Reviewer-safe takeaway:"]),
        ("关键结果 2", ["Claim:", "Evidence:", "Figure/table:", "Boundary:"]),
        ("机理解释", ["Direct evidence:", "Interpretation:", "Claim strength: direct / inferred / hypothesis"]),
        ("局限与下一步", ["Limitation:", "Next experiment:", "Paper angle:"]),
    ],
    ("journal-club", "zh"): [
        ("文献信息", ["Title: {title}", "Journal/year:", "Why this paper matters:"]),
        ("研究问题", ["Research gap:", "Engineering problem:", "Borrowable angle:"]),
        ("材料体系", ["Base material:", "Modifier:", "Key variable:"]),
        ("试验链条", ["Preparation:", "Performance tests:", "Mechanism tests:", "Durability tests:"]),
        ("图表证据 1", ["Figure/table:", "What it shows:", "Claim supported:", "Caution:"]),
        ("图表证据 2", ["Figure/table:", "What it shows:", "Claim supported:", "Caution:"]),
        ("机理与边界", ["Measured evidence:", "Mechanism inference:", "Boundary:"]),
        ("我能借鉴什么", ["Writing logic:", "Experiment design:", "Reviewer risk:", "Next step:"]),
    ],
    ("review-talk", "zh"): [
        ("综述范围", ["Topic: {title}", "Material family:", "Application boundary:"]),
        ("研究背景", ["Engineering demand:", "Failure/service condition:", "Why this review is needed:"]),
        ("材料分类", ["System 1:", "System 2:", "System 3:"]),
        ("性能证据", ["Key property:", "Comparison logic:", "Evidence gap:"]),
        ("机理证据", ["Chemical evidence:", "Microstructure evidence:", "Unresolved issue:"]),
        ("耐久与服役", ["Moisture/aging:", "Construction condition:", "Field relevance:"]),
        ("研究缺口", ["Gap 1:", "Gap 2:", "Gap 3:"]),
        ("我的选题切入", ["Proposed angle:", "Needed experiments:", "Target journal:"]),
    ],
    ("project-report", "en"): [
        ("Title", ["Topic: {title}", "Presenter:", "Date:"]),
        ("Engineering Problem", ["What fails in service?", "Why current solutions are insufficient?", "Slide message:"]),
        ("Material Design", ["Material system:", "Design variable:", "Expected mechanism:"]),
        ("Experiment Matrix", ["Preparation:", "Performance tests:", "Mechanism tests:", "Durability/service tests:"]),
        ("Key Result 1", ["Claim:", "Evidence:", "Figure/table:", "Reviewer-safe takeaway:"]),
        ("Key Result 2", ["Claim:", "Evidence:", "Figure/table:", "Boundary:"]),
        ("Mechanism", ["Direct evidence:", "Interpretation:", "Claim strength: direct / inferred / hypothesis"]),
        ("Limitations and Next Work", ["Limitation:", "Next experiment:", "Paper angle:"]),
    ],
}


def deck_for(deck_type: str, language: str) -> list[tuple[str, list[str]]]:
    return DECKS.get((deck_type, language)) or DECKS[("project-report", "zh")]


def render_markdown(title: str, deck_type: str, language: str) -> str:
    chunks: list[str] = []
    for idx, (slide_title, bullets) in enumerate(deck_for(deck_type, language), 1):
        chunks.append(f"## Slide {idx} - {slide_title}")
        chunks.extend(f"- {bullet.format(title=title)}" for bullet in bullets)
        chunks.append("")
        chunks.append("Speaker note:")
        chunks.append("")
    return "\n".join(chunks)


def generate_pptx(markdown_path: Path, pptx_output: Path, title: str) -> None:
    skills_root = Path(__file__).resolve().parents[2]
    pptx_script = skills_root / "civil-materials-pptx" / "scripts" / "build_civil_materials_pptx.py"
    if not pptx_script.exists():
        raise FileNotFoundError(f"Cannot find PPTX script: {pptx_script}")
    subprocess.run(
        [sys.executable, str(pptx_script), "--input", str(markdown_path), "--title", title, "--output", str(pptx_output)],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", default="Civil materials presentation")
    parser.add_argument("--deck-type", choices=["project-report", "journal-club", "review-talk"], default="project-report")
    parser.add_argument("--language", choices=["zh", "en"], default="zh")
    parser.add_argument("--output", default="civil-materials-deck.md")
    parser.add_argument("--pptx-output", help="Optional .pptx output path.")
    args = parser.parse_args()

    output = Path(args.output)
    output.write_text(render_markdown(args.title, args.deck_type, args.language), encoding="utf-8")
    print(output)
    if args.pptx_output:
        pptx_output = Path(args.pptx_output)
        generate_pptx(output, pptx_output, args.title)
        print(pptx_output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

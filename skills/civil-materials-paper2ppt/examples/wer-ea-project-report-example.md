# Paper-to-PPT Example: WER-EA Project Report

This example shows how to generate a slide-ready Markdown deck for a WER-EA
project report presentation.

## Input

- **Title**: 水性环氧改性乳化沥青粘结层性能研究
- **Deck type**: project-report
- **Language**: zh

## Command

```powershell
python skills/civil-materials-paper2ppt/scripts/build_ppt_markdown.py `
  --title "水性环氧改性乳化沥青粘结层性能研究" `
  --deck-type project-report `
  --language zh `
  --output wer-ea-project-report.md
```

## Output Structure

The generated Markdown contains 8 slides:

1. **题目** — Title, presenter, date
2. **工程问题** — Engineering problem and current gap
3. **材料设计** — Material system, design variable, expected mechanism
4. **试验矩阵** — Preparation, performance, mechanism, durability tests
5. **关键结果 1** — First key result with claim, evidence, figure reference
6. **关键结果 2** — Second key result with boundary conditions
7. **机理解释** — Mechanism with direct/inferred/hypothesis classification
8. **局限与下一步** — Limitations, next experiments, paper angle

## Slide Message Discipline

Each slide enforces:
- One claim per slide
- Evidence must reference a specific figure or table
- Claim strength must be classified (direct / inferred / hypothesis)
- Boundary conditions must be explicit

## Handoff to PPTX

The Markdown output can be passed to `civil-materials-pptx` for PPTX generation:

```powershell
python skills/civil-materials-pptx/scripts/build_civil_materials_pptx.py `
  --input wer-ea-project-report.md `
  --output wer-ea-project-report.pptx
```

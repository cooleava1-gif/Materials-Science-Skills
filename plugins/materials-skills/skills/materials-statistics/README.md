# materials-statistics / 材料统计报告技能

Version 1.0.0 · status: beta

Audit, revise, and draft statistical reporting for materials-science
manuscripts: replicate and `n` definitions, design-matched tests
(ANOVA / Taguchi S/N / RSM / mixture), multiple-comparison corrections,
effect sizes with uncertainty, figure-statistics alignment, and
reviewer-facing statistical risk.

面向材料科学论文的统计报告审查、修改与起草：重复数与 `n` 定义、与实验设计
匹配的检验（方差分析 / 田口信噪比 / 响应面 / 混料设计）、多重比较校正、
带不确定度的效应量、图注统计对齐，以及审稿人视角的统计风险提示。

## What it does / 功能

- **Replication audit** — separates independent specimens from repeated
  readings, EDS point analyses, SEM fields, and replicate scans
  (pseudoreplication is the top P0 it catches).
- **Design-matched tests** — factorial ANOVA with interactions, Taguchi S/N
  with a stated error term, RSM with lack-of-fit, Scheffé mixture models.
- **Reporting completeness** — Methods Statistical analysis subsections with
  n, unit, test, correction, software + versions, invoked standards
  (ASTM / ISO / GB).
- **Figure statistics** — captions with SD/SEM/CI declared, per-panel n,
  named corrections behind significance markers.
- **Reviewer support** — severity-labelled issues (P0/P1/P2) plus polite
  reply drafts; routes to `materials-response`.

- **重复性审查** —— 区分独立试件与重复读数、EDS 点分析、SEM 视场与重复
  扫描（伪重复是最高频的 P0 问题）。
- **设计匹配检验** —— 含交互作用的析因方差分析、带误差项说明的田口信噪比、
  含失拟检验的响应面、Scheffé 混料模型。
- **报告完整性** —— 统计分析小节须含 n、单元、检验、校正、软件及版本、
  引用的标准（ASTM / ISO / GB）。
- **图注统计** —— 声明 SD/SEM/CI、逐面板 n、显著性标记背后的校正方法。
- **审稿支持** —— P0/P1/P2 分级问题清单与礼貌回复草稿；交接给
  `materials-response`。

## Red lines / 红线

- Never invent p-values, sample sizes, degrees of freedom, intervals,
  software versions, or correction methods — mark `AUTHOR_INPUT_NEEDED`.
  绝不编造 p 值、样本量、自由度、区间、软件版本或校正方法——缺失即标
  `AUTHOR_INPUT_NEEDED`。
- Never treat readings, images, or scans as independent replication without
  an explicit hierarchy. 没有明确的实验层级，读数/图像/扫描不计为独立重复。
- Significance is not importance and not causation. 显著 ≠ 重要 ≠ 因果。

## Handoffs / 交接

`materials-doe` (design changes) · `materials-data` (datasets) ·
`materials-figure` (re-plotting) · `materials-polishing` (language) ·
`materials-response` (reviewer replies)

## Status

Beta — statistics-rule coverage is accumulating; report issues through the
release gate. Beta——统计规则覆盖持续积累中。

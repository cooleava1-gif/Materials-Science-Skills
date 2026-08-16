# materials-paper-card / 材料深读卡技能

Version 1.0.0 · status: beta

Turn one materials-science paper into a source-grounded deep-reading card
with fixed Sections 01-16 — from bibliographic position and core insight to
material system, characterization-chain reading, conclusion boundaries,
critical analysis, and gated testable research ideas.

把一篇材料科学论文变成一张有据可查的深读卡：固定 16 节结构，从书目定位、
核心洞察到材料体系与工艺路线、表征链解读、结论边界、批判性分析，直到
过门槛的可检验研究想法。

## What it does / 功能

- **Fixed 16-section structure** — bibliographic position, research
  question, background route, pain point, core insight, material system
  and processing route, method logic, essential formulas,
  experiment-to-claim evidence chain, characterization-chain reading,
  conclusion boundaries, author-stated limitations, critical analysis,
  learned knowledge, knowledge connections, testable research ideas.
  **固定 16 节**——书目定位、研究问题、背景路线、痛点、核心洞察、材料体系
  与工艺路线、方法模块逻辑、关键公式、实验—结论证据链、表征链解读、结论
  边界、作者自述局限、批判性分析、习得知识、知识连接、可检验研究想法。
- **Source honesty** — page-grounded / structure-grounded /
  source-limited locator modes; unsupported sections are marked
  `Not assessable`, never invented.
  **来源诚实**——三种定位模式；无据可依的节标注 `Not assessable`，绝不编造。
- **Reader reuse** — consumes `materials-reader` evidence packages and
  their IDs instead of re-extracting. **复用 reader 证据包**——直接继承
  证据元组，不重复提取。
- **Materials-first reading** — Section 06 (material system, mix design,
  processing) and Section 10 (XRD/FTIR/SEM/TG chain) give the domain its
  own sections. **材料优先**——材料体系与表征链独立成节。
- **Gated ideas** — Section 16 ideas pass gap/testability/boundary/reuse
  gates and hand off to `materials-research`. **想法过门**——第 16 节想法
  须过四道门，再交给 `materials-research` 路由。

## Red lines / 红线

- No invented data, mechanisms, or citations. 不编造数据、机制或引文。
- Characterization reported, not verified; no inference upgrades
  (SEM morphology is not chemical proof). 表征结果是「论文报告」而非
  「已验证」；表征不越级证明机制。
- The card never grades the paper — that is `materials-reviewer`.
  深读卡不给论文打分——那是 `materials-reviewer` 的事。

## Handoffs / 交接

`materials-reader` (deeper extraction) · `materials-citation`
(bibliographic verification) · `materials-research` (idea routing) ·
`materials-figure` (re-plotting) · `materials-reviewer` (formal review)

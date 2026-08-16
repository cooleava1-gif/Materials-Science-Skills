# Output Format

Fixed structure — every card ships all 16 numbered sections in this order:

```markdown
# Paper Card: <short title>
- Source: <citation / DOI / file>
- Locator mode: page-grounded | structure-grounded | source-limited
- Context mode: paper-only | targeted external check | externally verified
- Evidence base: <supplied text | reader-package ID>

## 01 Bibliographic position 书目定位
venue, year, group, one-sentence field placement; verification status

## 02 Research question 研究问题
the question the paper actually answers (not the claimed one)

## 03 Background route 背景路线
how the field arrived here (paper's narrative, marked as such)

## 04 Pain point 痛点
the specific gap or limitation this paper attacks

## 05 Core insight 核心洞察
the one idea that makes the paper work

## 06 Material system and processing route 材料体系与工艺路线
system, composition/mix design, processing, curing/sintering/synthesis key
parameters, standards invoked

## 07 Method and module logic 方法与模块逻辑
method modules and how they chain into the argument

## 08 Essential formulas 关键公式
the equations that carry the claims, each with its role

## 09 Experiment-to-claim evidence chain 实验—结论证据链
claim → experiment → measurement → inference table with evidence IDs

## 10 Characterization chain reading 表征链解读
XRD / FTIR / SEM-EDS / TG / mechanical / durability results and what each
actually supports (reported, not verified)

## 11 Conclusion boundaries 结论边界
what the evidence supports, hedged where inference exceeds data

## 12 Author-stated limitations 作者自述局限
verbatim-faithful summary of the paper's own limits section

## 13 Critical analysis 批判性分析
analytic strengths/weaknesses with evidence ties (no grading language)

## 14 Learned knowledge 习得知识
transferable takeaways (methods, characterizations, writing moves)

## 15 Knowledge connections 知识连接
links to adjacent papers/topics (context mode noted)

## 16 Testable research ideas 可检验研究想法
each: evidence gap → experiment sketch → boundary respected
```

Rules: `Not assessable` sections carry a one-line reason; no section is
skipped; headings may be localized, numbering stays.

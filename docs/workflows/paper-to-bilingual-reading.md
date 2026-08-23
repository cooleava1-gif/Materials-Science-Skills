# Paper to Bilingual Reading

Turn an English materials paper into a Chinese-first interactive bilingual
reading page where every sentence reveals its aligned English source.

## Prompt

```text
生成这篇英文论文的中文版可交互双语阅读页，保留图表和章节层级。
```

## Expected Shape

1. `materials-reader` detects `source_format` (pdf-text / scanned-pdf / html)
   and routes to `references/bilingual-html-reader.md`.
2. The reader builds `source_map.json` and the terminology ledger first, so
   the HTML stays tied to the evidence chain.
3. Sentences are aligned one-to-one with stable ids; headings, captions, and
   table cells are treated as independent alignment zones.
4. The page is composed from
   `assets/templates/bilingual-reader-template.html`; hover or keyboard focus
   reveals the English source, Esc or pointer-exit hides it.
5. QA verifies no orphan sentence in either direction and intact figures,
   tables, and section hierarchy before delivery.

## Boundary

This is an output format of `materials-reader`, not a separate skill. It does
not trigger for abstract-only or partial translation; those stay in the
Markdown reader path.

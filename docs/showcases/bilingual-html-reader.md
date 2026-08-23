# Bilingual HTML reading page

## Outcome Snapshot

A Chinese-first interactive reading page for a full English paper: every
Chinese sentence reveals its aligned English source on hover or keyboard
focus, with figures, tables, captions, and section hierarchy preserved.

## Demo Prompt

```text
生成这篇英文论文的中文版可交互双语阅读页。
```

## Proof Assets

- `plugins/materials-skills/skills/materials-reader/assets/templates/bilingual-reader-template.html`

## Build Path

1. `materials-reader` parses the PDF and builds the source map and glossary.
2. Sentences are aligned one-to-one with stable ids (`s0001`, …).
3. Each Chinese sentence is wrapped in a `.sentence` span carrying its
   English source in `data-source`.
4. The page is composed from `bilingual-reader-template.html`; the tooltip
   reveals the English source on hover/focus and hides on exit or Esc.
5. QA verifies no orphan sentence in either direction and intact tables.

## When To Use This Route

Use it for full-paper Chinese reading. It is an output format of
`materials-reader`, reusing the same `source_map.json` and terminology ledger;
it does not trigger for abstract-only or partial translation.

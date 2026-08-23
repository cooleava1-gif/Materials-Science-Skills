# Bilingual HTML Reader Output

Use this reference when the user asks for a **Chinese-first, interactive
bilingual reading page** of an English paper — "生成中文版", "全文翻译",
"可交互双语网页", "悬停看原文", or a readable Chinese HTML rendering. This is an
*output format* of `materials-reader`, not a separate skill: it reuses the same
source grounding, terminology ledger, and evidence boundary as the Markdown
reader package, and adds a hover-to-reveal English tooltip layer.

## Scope

- Use this only for a **full-paper** Chinese rendering requested explicitly.
- Do not trigger it for abstract-only translation, a single-sentence gloss, or
  ad hoc questions about the paper — those stay in the Markdown reader path.

## Alignment record

Represent each bilingual unit with stable fields:

- `id`: stable sentence id such as `s0001`
- `block_type`: `heading`, `paragraph`, `caption`, `table-cell`, `footnote`,
  `reference`, or `list-item`
- `page`: source page number
- `source_text`: English sentence
- `target_text`: Chinese sentence
- `context`: optional nearby heading or figure/table id

Keep sentence ids stable across revisions whenever the underlying source
sentence has not changed. Reuse the reader's `source_map.json` anchors where a
unit corresponds to an existing `S001` / `C001` source id, so the HTML stays
connected to the evidence chain.

## Segmentation rules

- Split on true sentence boundaries, not merely on line breaks from PDF
  extraction.
- Merge broken PDF lines before sentence splitting.
- Treat headings, captions, and table cells as independent alignment zones.
- If one English sentence is too dense for readable Chinese, split both
  languages at the same logical clause boundary — never one English sentence
  against several Chinese sentences.
- Keep citations and parenthetical clauses attached to their sentence in both
  languages.
- Numbers, units, chemical formulas, symbols, and equation numbering are
  preserved verbatim; they are never "translated".

## Terminology rules

The reader's `_shared/core/terminology-ledger.md` is the canonical glossary —
build it on first reliable occurrence and reuse the same Chinese term for the
same English technical noun. Additional constraints for HTML output:

- Preserve acronym behavior consistently: if the first occurrence shows both
  Chinese and English, keep that convention stable afterward.
- Prefer domain-correct Chinese terminology over literal word-for-word
  translation.
- Record any new term in `translation_notes.md` so the Markdown package and the
  HTML page stay consistent.

## HTML structure

Use the template at `assets/templates/bilingual-reader-template.html` as the
starting point. Make Chinese the default reading layer; wrap each translated
sentence so it can reveal its English source cleanly:

```html
<span
  class="sentence"
  id="s0001"
  tabindex="0"
  data-source="Original English sentence."
>
  中文译文。
</span>
```

Semantic containers around aligned sentences:

- `section` for paper sections
- `figure` and `figcaption` for figures
- `table` and `caption` for tables
- `aside` for footnotes or translator notes when needed

For tables, wrap sentence-bearing cells individually — do not store an entire
row's English in one tooltip. Keep figures, tables, captions, and section
hierarchy visually clear on both desktop and mobile. Preserve alignment ids in
the DOM so later revisions can target exact sentence pairs. Keep the final HTML
self-contained unless the user asks for split assets.

## Tooltip behavior

- Reveal source text on `hover` and `focus` (the template's JavaScript already
  implements pointer and keyboard events).
- Hide on pointer exit, blur, or `Escape`.
- Keep the tooltip out of normal document flow so reading layout does not jump.
- Limit tooltip width and allow wrapping for long English sentences.

## Quality checks

- Verify every Chinese sentence has a matching English source string.
- Verify the reverse count matches: no orphan English sentence and no orphan
  Chinese sentence.
- Spot-check dense pages with figures or tables after HTML generation.
- Reject output with overlapping captions, clipped tables, or mismatched
  sentence ids.

## Deliverables & cleanup

- Prefer a deterministic final artifact: `dist/{pdf-stem}-zh.html`.
- Keep the original PDF untouched; never copy it into the package.
- Keep the reader's `source_map.json`, `translation_notes.md`, and
  `package_manifest.json` so the HTML stays tied to the evidence chain.
- Clean up only run-specific intermediates (rendered page images, OCR caches,
  raw extraction dumps, temporary alignment manifests, scratch HTML fragments).
  Never delete the source PDF, the final HTML, or user-authored notes.
- Before deleting intermediates, name the exact paths and their effect, and get
  the user's confirmation; if denied, keep the files and report what remains.

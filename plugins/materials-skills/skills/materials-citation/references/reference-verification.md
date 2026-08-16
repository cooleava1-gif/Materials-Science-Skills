# Reference Verification / 参考文献逐条校验

Field-by-field cross-validation of a reference list against multiple
authoritative sources, adapted from nature-skills' ref-verifier patterns
(Apache-2.0) and driven by the `materials-academic-search` MCP (Crossref,
OpenAlex, Semantic Scholar, PubMed, arXiv, Scopus, ScienceDirect).

## Procedure

1. **Parse the list** into entries: authors, title, year, journal, volume,
   issue, pages, DOI. Note the citation style in use.
2. **Query per entry** via the MCP — DOI lookup first when a DOI exists;
   otherwise title + first author. Record which sources answered
   (multi-source beats single-source).
3. **Compare field by field** and classify:
   - `OK` — all fields match at least one authoritative source.
   - `WARN` — recoverable anomaly (see patterns below), with the fix.
   - `ERROR` — no source confirms the entry, or the first author differs
     entirely (possible hallucinated reference).
4. **Report** a structured table + per-entry fix suggestions + Zotero-style
   field corrections; never auto-apply silent fixes.

## Common anomaly patterns 常见异常模式

- **卷年 vs DOI 年**: the DOI string's year is often the manuscript year;
  cite the journal volume year. DOI 2024 + volume 2025 → cite **2025**;
  online 2024-12-31 in a 2025 volume → cite **2025**. Prefer the official
  volume year; fall back to the online year when no volume exists.
- **第一作者完全编造** (AI-hallucinated references): authors differ
  entirely from the DOI's registered authors → ERROR, the most severe
  class. Detect by comparing surnames against Crossref/OpenAlex records.
- **作者顺序颠倒**: order disagrees with the official record → WARN with
  the corrected order.
- **中文作者形近字**: 廷/延、健/建、浩/皓 → verify against CNKI/Wanfang
  official records when available.
- **双姓缩写** (Spanish/Portuguese): `Álvarez López Y` = `López Y Á` =
  `Alvarez Lopez Y` — all acceptable, not an anomaly.
- **"等" vs full author list**: acceptable in Chinese citation; when all
  authors are listed (3-5), order must match the original.
- **页码偏差**: preprint vs published pages; conference early vs final
  version; same paper paginated differently in journal vs proceedings →
  cite the version actually used, note the other.
- **期刊更名/转刊**: old journal name in the reference, new name in the
  source → cite the name at publication time.
- **卷期号对调** and **DOI 前缀错配**（publisher prefix doesn't match the
  journal）→ WARN/ERROR respectively.

## Output format

```text
Reference verification report
- Entries checked: N (sources consulted per entry: Crossref/OpenAlex/...)
- OK: n1  WARN: n2  ERROR: n3

| # | Field(s) | Severity | Finding | Suggested fix |
|---|---|---|---|---|

Zotero sync suggestions
- per entry: field corrections as key=value pairs

Unresolved
- entries no source confirmed; recommend manual check on the journal page
```

## Red lines

- Never mark an entry OK on a single fuzzy title match; require DOI or
  strong multi-field agreement.
- Never rewrite author names to "fix" legitimate transliteration
  variants; only correct against authoritative records.
- Full-text claims (content of the paper) are out of scope — this route
  verifies metadata, not findings.

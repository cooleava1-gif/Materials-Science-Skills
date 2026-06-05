---
name: civil-materials-polishing
description: Use when polishing, translating, tightening, restructuring, or risk-auditing English manuscript prose for civil engineering and construction materials research, especially claim-strength control, Chinese-to-English academic writing, CBM, CBM in Transportation, CCC, CSCM, JBE, RMPD, IJPE, JRE, asphalt pavement materials, cement/concrete, durability, sustainability, abstracts, highlights, introductions, results, discussions, and cover letters.
---

# Civil Materials Polishing

Polish civil materials prose while preserving scientific responsibility.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect the section, journal family, and language direction.
3. Load only the matching fragments.
4. Apply the language rulebook, claim-strength ladder, and domain language fragment.
5. Preserve facts, evidence strength, units, citations, and author intent.
6. Return polished text plus a short risk note when claims are too strong.

## Core Rule

Do not make weak evidence sound strong. Civil materials writing should be clear, engineering-grounded, and reviewer-safe.

Use `references/language-rulebook.md` for general manuscript language, `references/claim-strength-ladder.md` when causality or novelty is risky, and `references/chinese-to-english-patterns.md` for Chinese-to-English polishing.

Use this module for English polishing. Use `civil-materials-research` first when the argument, journal fit, or evidence chain is unclear.

Use `examples/claim-strength-polishing-example.md` as a concrete model. Use `tests/pressure-tests/overclaim-and-literal-translation.md` to check that polishing improves language without inflating weak evidence.

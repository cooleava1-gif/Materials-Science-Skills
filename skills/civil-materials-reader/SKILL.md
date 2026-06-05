---
name: civil-materials-reader
description: Use when reading, translating, extracting, auditing, or structuring civil engineering and construction materials papers, especially for source-grounded notes, evidence-chain reading, claim-evidence-mechanism matrices, Chinese-English paper notes, figure/table-aware reading, literature matrices, journal-club preparation, asphalt pavement materials, cement/concrete, durability, sustainability, and waterborne epoxy modified emulsified asphalt.
---

# Civil Materials Reader

Build source-grounded civil materials reading artifacts, not shallow summaries.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect the `source_type` and `output_type`.
3. Load only the matching fragments and references.
4. Produce a Markdown reader, matrix, or evidence-chain audit that preserves the paper's evidence chain.
5. Keep all numbers, figures, tables, mechanisms, and limitations tied to the source.

## Default Output

Use `assets/templates/literature-reading-template.md` as the base structure unless the user requests another format.

The output should include:

- paper identity,
- research question,
- material system,
- experiment matrix,
- figure/table evidence map,
- mechanism chain,
- limitations,
- what the user can borrow for their own topic.
- claim-evidence-mechanism-boundary audit when the paper will inform a manuscript or review.

## Civil Materials Reading Rules

- Extract test conditions and standards when present.
- Do not convert figure captions into unsupported conclusions.
- Separate measured results from inferred mechanisms.
- For asphalt/pavement papers, always capture binder/emulsion, interface, mixture, and service-condition evidence separately.
- For cement/concrete papers, always capture fresh properties, strength, durability, hydration/microstructure, and sustainability boundary separately.
- For review writing, convert each borrowable idea into: claim -> evidence -> mechanism -> boundary -> citation role.
- Flag reviewer risks when a conclusion is stronger than the measurements.

If the user asks for a PPT after reading, hand off to `civil-materials-paper2ppt`. If the user asks for polished English after reading, hand off to `civil-materials-polishing`.

Use `examples/waterborne-epoxy-evidence-chain-example.md` as a concrete model for evidence-chain reading. Use `tests/pressure-tests/overclaim-from-figure-caption.md` to check that figure captions are not converted into unsupported conclusions.

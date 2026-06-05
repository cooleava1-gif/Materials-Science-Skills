---
name: civil-materials-citation
description: Use when searching, screening, organizing, or mapping literature and citations for civil engineering and construction materials manuscripts, especially CBM, CCC, JBE, RMPD, IJPE, asphalt pavement materials, emulsified asphalt, waterborne epoxy, cement/concrete, durability, mechanisms, citation matrices, reference gaps, and claim-source alignment.
---

# Civil Materials Citation

Build source-grounded literature search plans and claim-citation maps for civil materials manuscripts.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Detect `task`, `journal_family`, and `material_domain`.
3. Load only the matching reference files.
4. Produce one of these outputs: search strategy, citation matrix, claim-source map, reference gap audit, or journal-specific source plan.
5. Do not invent papers, DOIs, impact factors, journal rules, or citation counts. Use live search or user-provided sources for current facts.

## Default Output

Use `assets/templates/citation-matrix-template.csv` as the matrix schema and `assets/templates/search-plan-template.md` for search planning.

For each claim, include:

- exact claim or knowledge gap,
- search query and database route,
- target journal family,
- evidence type needed,
- candidate source status,
- manuscript location,
- risk if uncited or weakly cited.

## Civil Materials Citation Rules

- Prefer primary research and authoritative review articles over generic web summaries.
- Separate mechanism citations from performance citations.
- For asphalt and pavement manuscripts, keep binder/emulsion, aggregate-interface, mixture, construction, and service-condition evidence separate.
- For cement/concrete manuscripts, keep fresh properties, strength, durability, hydration/microstructure, and sustainability boundary citations separate.
- For CBM/JBE/CSCM-style manuscripts, emphasize applied material performance and reviewer-safe engineering evidence.
- For CCC-style manuscripts, emphasize mechanism depth and composite-material logic.
- For RMPD/IJPE-style manuscripts, emphasize pavement performance, field relevance, test standards, and traffic/environment service conditions.

Use `scripts/build_citation_matrix.py` to create a CSV search-and-citation matrix from a topic, claims, and target journals.

Use `references/academic-search-mcp.md` when explaining or planning a future civil-materials academic-search MCP.

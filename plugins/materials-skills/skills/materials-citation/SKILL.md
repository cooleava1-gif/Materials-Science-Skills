---
name: materials-citation
version: "1.1.0"
stability: stable
description: Use when searching, screening, organizing, or mapping literature and citations for materials science and engineering manuscripts.
---

# Materials Science Citation Router

Read `manifest.yaml` and `always_load` files. Apply profile-first routing, detect `task`, `journal_family`, `material_domain`, and `material_family`, then load only mapped fragments.

Return the requested search strategy, citation matrix, claim-source map, reference gap audit, or journal-specific source plan. Keep a citation gap visible when a source, DOI, full text, or claim anchor is unresolved.

Evidence boundary:

- Do not invent papers, DOIs, impact factors, journal rules, citation counts, page locations, or experimental support.
- Prefer primary research and authoritative reviews according to the claim's evidence role; metadata or a review is not direct proof of a mechanism or measured performance.
- Separate mechanism citations from performance citations, and distinguish literature fact, source interpretation, and author data.

Asphalt search-plan minimum: for CBM-oriented waterborne-epoxy/emulsified-
asphalt requests, keep CBM, JBE, and RMPD; include `waterborne epoxy`,
`interlayer bonding`, and `moisture damage`; separate binder/emulsion,
interface, mixture, construction, and service-condition layers; never replace
a missing source with a plausible citation.

Route intensive reading to `materials-reader`; recurring discovery/scoring/digest
to `materials-literature-pipeline`. Return stable IDs, evidence roles, gaps, and
the selected output contract.

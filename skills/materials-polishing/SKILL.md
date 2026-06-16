---
name: materials-polishing
version: "1.1.0"
stability: stable
description: Use when polishing, translating, tightening, or risk-auditing English manuscript prose for civil engineering and construction materials research.
---

# Materials Science Polishing

Polish materials prose while preserving scientific responsibility.

## Protocol

1. Read [manifest.yaml](manifest.yaml), then load every `always_load` file.
2. Apply profile-first routing from `.materials/profile.yaml`; on first use, ask for direction once and save it locally.
3. Detect `section`, `journal_family`, `language_mode`, and `paper_type`.
4. Load only the matching fragments.
5. Apply the language rulebook, claim-strength ladder, and domain language fragment.
6. Preserve facts, evidence strength, units, citations, and author intent.

## Gates

- Do not make weak evidence sound strong.
- Limit sentences to <=35 words.
- Return polished text plus a short risk note when claims are too strong.

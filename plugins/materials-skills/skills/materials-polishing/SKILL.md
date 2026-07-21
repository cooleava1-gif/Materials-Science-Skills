---
name: materials-polishing
version: "1.3.0"
stability: stable
description: >-
  Use when polishing, restructuring, proofreading, translating, or calibrating materials-science and engineering manuscript prose while preserving data, units, evidence strength, author meaning, and journal terminology. Trigger for academic writing, Chinese-to-English, claim-strength, grammar, clarity, section, and weakness-routing requests.
---

# Materials Science Polishing Router

Read `manifest.yaml` and its `always_load` files. Apply explicit direction > saved `.materials/profile.yaml` > neutral fallback, then load only the selected section, language, paper-type, journal, material-family, domain, and on-demand paths.

Choose the fast path for a bounded sentence, title, paragraph, or direct translation. Choose the deep path for document-scale work, structural repair, terminology consistency, risky claims, citation review, or paper-production handoffs; when depth is ambiguous, use the deep path. Follow the workflow and output contract declared by the manifest.

Non-negotiable invariants:

- Preserve data, units, test conditions, standards, citations, notation, uncertainty, limitations, and author meaning.
- Do not invent experiments, evidence, mechanisms, statistics, novelty, applicability, journal facts, or citations; do not make weak evidence sound strong.
- Keep unsupported claims visible through a claim-strength note or explicit revision marker. Load evidence, terminology, ethics, failure-mode, and `weakness-routing` references only when the edit needs them.
- Do not run a full manuscript workflow for a bounded local edit.

For paper-production weaknesses, emit the bounded polished text plus the claim-evidence map, terminology ledger, and missing-input status required by the receiving skill. Do not silently upgrade a draft from language-polished to scientifically verified.

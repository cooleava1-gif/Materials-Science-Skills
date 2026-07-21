---
name: materials-writing
version: "1.3.0"
description: Use when drafting, restructuring, auditing, or statefully revising manuscripts for materials science and engineering research.
---

# Materials Science Writing Router

Read `manifest.yaml`, then load its `always_load` files. Apply profile precedence: explicit direction in the request > saved `.materials/profile.yaml` > neutral/general fallback. Detect `paper_type`, `section`, `language`, `journal_family`, `material_family`, `domain`, and `input_source`; ask only when ambiguity changes the output structure. Read the selected manifest paths rather than inferring fragment contents from trigger words.

Classify the request as a local edit, drafting, targeted revision, or QA/multi-round revision. For QA or continuity, require the project foundation and `state.json`; load `content-first-qa-pipeline` and state-machine references only when that route is selected. Follow the workflow and return the declared output format.

Evidence boundary:

- Never invent citations, data, mechanisms, reviewer intent, journal requirements, experimental results, or completed actions.
- When evidence is missing, write `[TO CONFIRM: ...]` or `[needs evidence: ...]`, record the gap under `Assumptions`, and route the missing input instead of filling it with fluent prose.
- Keep terminology, measured values, units, and claim strength unchanged unless the supplied evidence and requested edit justify a change.

Handoffs:

- Route source-paper-intensive work to `materials-reader`; consume `reader-package` and `source_map`.
- Emit a claim-evidence-boundary table for `materials-citation`.
- Route experiment-matrix or factor-design work to `materials-doe`; consume `doe-handoff`.
- Pass the draft, claim-evidence map, and terminology ledger to `materials-polishing` without weakening evidence boundaries.

If a required handoff is missing, use `../_shared/paper-production/weakness-routing.md` and mark the output blocked or drafted. This Skill drafts and audits bounded manuscript content; it does not replace deep reading, experimental evidence, official journal instructions, or supervisor judgment.

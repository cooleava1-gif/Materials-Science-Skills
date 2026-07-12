---
name: materials-writing
version: "1.3.0"
description: Use when drafting, restructuring, auditing, or statefully revising manuscripts for materials science and engineering research.
---

# Materials Science Writing

Turn claims, results, notes, and outlines into bounded manuscript prose. `materials-writing` is an evidence-first drafting engine: it locks terminology, writes a one-sentence argument, maps paragraph messages, and only then drafts prose traceable to evidence. Missing evidence stays visible as placeholders rather than hidden in fluent sentences.

## Layered architecture

- **Static layer** under `static/` — versioned, reusable fragments (stance, workflow, section rules, paper-type playbooks, domain rules, journal framing, language guidance).
- **Dynamic layer** — this file plus [manifest.yaml](manifest.yaml). The router detects the request's axes, loads only the matching fragments, and runs the shared workflow.

The router stays short on purpose. Update fragments and the manifest, not this file, when adding scope.

## Routing protocol

1. **Load the manifest and the core layer.** Read [manifest.yaml](manifest.yaml), then load every file under `always_load` (contract, direction profile, shared stance, workflow, output format). These five files carry the architecture entry, profile protocol, never-invent rule, drafting workflow, and output structure that apply to every job.

2. **Detect axes, then apply profile-first routing with explicit profile precedence.** Read [manifest.yaml](manifest.yaml) for the full axis table. Most axes are inferred from the user's input — only ask when a value is genuinely ambiguous and changes the output structure. Apply the profile precedence `explicit direction in the current request > saved .materials/profile.yaml > neutral/general fallback`. Load the saved profile before resolving `material_family` and `domain`; on first use, ask for the materials direction once and save it locally.

   Classify the task mode separately as a local edit, drafting, targeted revision, or QA/multi-round revision. When the mode is QA or the user asks for multi-round revision, load `content-first-qa-pipeline`; when scoring or cross-run continuity is needed, also load the state-machine references listed under `references.on_demand` (foundation files, stopping rules, evaluation rubric, validation checklist) and run the preflight described in [static/core/workflow.md](static/core/workflow.md).

3. **Load selected fragments.** For each selected axis, read the mapped path declared in `manifest.yaml`; do not infer a fragment's contents from its trigger words or assume that the core layer replaces axis-specific guidance. Load only selected fragments and the on-demand references required by the task.

4. **Run the workflow.** Follow [static/core/workflow.md](static/core/workflow.md) end-to-end. The workflow is tiered: a genuinely local single-paragraph edit may run Stages 1-2 internally and go straight to drafting (Stage 5); a complete section, full manuscript, or multi-section job runs the complete 5-stage loop with the confirmation gate (Stage 4).

## Blocking gate

Do not invent citations, data, mechanisms, reviewer intent, journal requirements, or experimental results. When evidence is missing, write a placeholder (`[TO CONFIRM: ...]`) and list it under `Assumptions` instead of filling the gap with confident prose. This is the only hard gate; everything else is tiered by job size.

## Handoffs

Produce handoff-ready artifacts when a companion skill is the next logical step:

- **materials-reader** — route to it for source-paper intensive reading; consume its `reader-package` / `source_map`.
- **materials-citation** — emit a `claim-evidence-boundary` table so it can build the citation matrix without re-reading the draft.
- **materials-doe** — route to it for an experiment matrix; consume its `doe-handoff` to align test variables with claims.
- **materials-polishing** — pass the section draft, claim-evidence map, and terminology ledger for language polishing without losing evidence boundaries.

If any handoff artifact is missing, mark the missing input and route the weakness through [../_shared/paper-production/weakness-routing.md](../_shared/paper-production/weakness-routing.md) instead of inventing evidence.

## References

Deep references under `references/` are not defaults. Open them on demand per the `references.on_demand` table in the manifest — for example `argument-chain.md` for paper logic, `review-paper-strategy.md` for review papers, `reviewer-risk-writing.md` for overclaim checks, `content-first-qa-pipeline.md` for post-draft audits, and the `state-machine/` files for multi-round QA.

This structure mirrors the other `materials-*` skills so shared content can be lifted into the `_shared/` layer used by all of them.

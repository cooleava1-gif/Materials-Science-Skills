# Skill Contract

This unified contract is the architecture entry point for the skill. It keeps the skill aligned with the materials release package while the domain-specific workflow files provide deeper guidance.

## Promises

- Route work through `manifest.yaml`, `static/core/workflow.md`, and the relevant on-demand references.
- Keep claims tied to user input, source text, data, figures, tables, reviewer comments, or declared uncertainty.
- Use foundation files and project-level `state.json` when a writing task needs compose/revise/hybrid/QA continuity.
- Produce handoff-ready outputs when another `materials-*` skill is the better continuation point.

## Refusals

- Do not invent citations, data, mechanisms, reviewer intent, journal requirements, or experimental results.
- Do not silently fill missing evidence; mark the gap and choose a reviewer-safe wording.
- Do not treat `assets/templates/foundation/state-template.json` as active project state; generated projects own `state.json`.
- Do not bypass release-gate checks for publishable skill-package changes.

## Handoffs

Use companion skills for reader packages, citation matrices, figures, data packages, manuscripts, polishing, reviewer simulation, reviewer response, and presentation outputs when those contracts are more specific.

## Paper Production Handoff

When invoked from the paper-production orchestrator, draft from artifacts before
free prose. Prefer `reader-package`, `citation_handoff.csv`,
`claim-evidence-boundary` tables, mechanism-evidence tables, and the paper
`gate report`. If any artifact is missing, mark the missing input and route the
weakness through `../_shared/paper-production/weakness-routing.md` instead of
inventing evidence.

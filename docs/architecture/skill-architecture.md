# Materials Science Skill Architecture

This document defines the final static/dynamic architecture for every
`materials-*` skill. The root `skills/<skill>/` directory is the source of
truth, and `plugins/materials-skills/skills/<skill>/` is the installed
plugin mirror.

For day-to-day maintenance, extension workflows, and current technical-debt
warnings, read [Maintainer Handoff Guide](maintenance-handoff.md).

## Architecture Contract

| Layer | Required files | Responsibility | Release gate |
|---|---|---|---|
| Router | SKILL.md | Trigger and route only | frontmatter + links checked |
| Manifest | manifest.yaml | Axes, always_load, trigger routing, assets, scripts, tests, handoffs, release checks | path, schema, and UTF-8 checks |
| Static core | static/core/contract.md, static/core/workflow.md | Stable promises and base workflow | required terms checked |
| References | references/*.md | Heavy domain guidance | linked paths checked |
| Templates | assets/templates/* | Output schemas | required fields checked |
| Scripts | scripts/*.py | Reusable production helpers | targeted tests |
| Tests | tests/* | Regression and contract checks | release gate |
| Plugin mirror | plugins/materials-skills/skills/<skill>/ | Installed package copy | byte identity check |

## Router

`SKILL.md` is the short entry point. It should describe when the skill applies,
the invocation protocol, the default output, and where to load further guidance.
It should not carry long domain playbooks when those can live in `static/core/`
or `references/`.

The router may mention important defaults, but it should route by manifest
concepts instead of duplicating every trigger list. For example, full-paper
reading belongs in the reader manifest axis and the relevant reference file, not
as a long embedded procedure inside the router.

## Manifest

`manifest.yaml` is the routing and release metadata contract. Each production
skill must declare:

- `version`
- `always_load`
- `axes`
- `assets`
- `scripts`
- `tests`
- `quality_gates`
- `handoffs`
- `release_checks`

`always_load` paths are loaded for every invocation and must point to stable,
small files. `axes.*.values.*.path` entries route user intent to on-demand
references. Paths under `assets`, `scripts`, and `tests` should be explicit
enough for release checks to prove that the declared deliverables exist.

Trigger strings must be valid UTF-8. Chinese triggers are allowed and useful,
but mojibake markers such as corrupted GBK text must be treated as release
warnings or failures depending on the gate phase.

## Static Core

`static/core/contract.md` defines what the skill promises to produce, what it
will not invent, and what evidence boundaries it enforces. `static/core/workflow.md`
defines the stable workflow used on every invocation.

During the migration, older domain-specific contract names such as
`reader-contract.md`, `citation-contract.md`, or `figure-contract.md` may be
reported as compatible core files. The final target remains the normalized
`contract.md` plus `workflow.md` pair.

## Dynamic Guidance

`references/*.md` files hold heavy domain guidance, journal-specific workflows,
evidence maps, figure rules, reviewer response patterns, and other material that
should be loaded only when the manifest route selects it.

`assets/templates/*` holds reusable Markdown, CSV, JSON, or schema contracts for
handoffs and generated packages. Templates should encode fields and boundaries,
not just examples.

`scripts/*.py` contains deterministic helpers for package building, validation,
search conversion, figure generation, or QA. Scripts should emit JSON for
automation-facing operations when practical.

`tests/*` proves structure and behavior for routes, templates, scripts, and
anti-overclaim constraints. Skills may also declare nested test folders, such as
the citation MCP test suite.

## Plugin Mirror

Root skill files are source-of-truth files. The plugin mirror must match changed
skill files byte-for-byte unless a documented exception applies. The mirror lets
the installed plugin package behave exactly like the root development copy.

The architecture checker compares router files and static core files between
root and plugin mirror as a first-pass identity gate. Later release gates can
expand the comparison to all touched skill assets, references, scripts, and
tests.

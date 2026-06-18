# Maintainer Handoff Guide

This guide is for any engineer or agent taking over maintenance of the
Materials Science Skills repository. It focuses on operational rules, source of
truth, release checks, and the places where a small unsynchronized change can
break the package.

## Branch Policy

- `main` is the authoritative branch.
- Start every task from a fresh `origin/main`: `git fetch origin` followed by
  `git checkout main` and `git pull --ff-only origin main`.
- `gemini` and `mimo` are audit/comparison branches only. Do not treat them as
  sources of truth unless a human maintainer explicitly promotes a change.
- Do not recreate retired experimental branches such as `deepseek` or `codex`.
- Do not rewrite `main` history unless the coordinated history slimming plan is
  explicitly approved for execution.

## First Ten Minutes

1. Run `git status --short --branch` and understand every local change before
   editing.
2. Read `AGENTS.md`.
3. Read `README.md` for product intent and public workflow entry points.
4. Read `docs/skills-index.md` to understand the 12 `materials-*` skills.
5. Read `docs/architecture/skill-architecture.md` for the static/dynamic skill
   contract.
6. Read this file for maintenance rules.
7. Read `docs/architecture/release-gate-contract.md` before changing gates.
8. If changing history or repository size, read
   `docs/architecture/git-history-slimming-plan.md` first.

## Source Of Truth

The repository is a Codex skill bundle, not a single Python application.

- `plugins/materials-skills/skills/materials-*` is the source skill tree and the
  installable plugin package.
- `manifest.yaml` is the source of truth for routing axes, loaded files,
  assets, scripts, tests, quality gates, handoffs, and release checks.
- `plugins/materials-skills/_shared/contracts/*.yaml` is the source of truth for
  cross-skill artifact handoff schemas.
- `scripts/run_release_checks.py` is the release gate entry point.
- `scripts/check_skill_architecture.py` validates manifest structure.

When in doubt, prefer making structure discoverable from manifests and contracts
instead of adding hard-coded skill lists to scripts.

## Agent Work Rules

- Never discard user work. If the tree is dirty, inspect it and preserve
  unrelated changes.
- Keep generated work products out of Git. Root `outputs/`, local run
  artifacts, desktop metadata, and internal planning notes are ignored.
- Use synthetic/example data only. Do not commit real paper data or private
  user data.
- For template or handoff field changes, update the producer, consumer,
  `plugins/materials-skills/_shared/contracts`, and tests together.
- For public docs changes, run the product docs tests or the full root test
  suite when practical.
- Before claiming completion, run `python scripts\run_release_checks.py --json`
  from the repository root.

## Figure Asset Rules

Bundled figure packages under `examples/figure-packages/` are source-only
examples. They should track source files such as README, storyboard, caption
boundary, QA report, manifest, plot script, and source data. They should not
track regenerated `figure.svg`, `figure.png`, `figure.pdf`, `figure.tif`, or
`figure.tiff` exports.

Production figure packages still must generate SVG, PDF, PNG, and TIFF exports
before being called production-ready. Use:

```powershell
python plugins\materials-skills\skills\materials-figure\scripts\audit_figure_package.py --package-dir <package>
```

Use source-only audit only for bundled examples:

```powershell
python plugins\materials-skills\skills\materials-figure\scripts\audit_figure_package.py --package-dir <package> --source-only
```

Do not delete `plugins/materials-skills/skills/materials-figure/assets/showcase-proof/*.png`.
Those are product screenshots referenced by README, gallery docs, and plugin metadata.

## Validation Matrix

| Change type | Minimum validation |
|---|---|
| Any release candidate | `python scripts\run_release_checks.py --json` |
| Root contracts | `python -m unittest discover -s tests -p "test_*.py" -v` |
| One skill | `python -m unittest discover -s plugins\materials-skills\skills\materials-<name>\tests -p "test_*.py" -v` |
| Plugin manifests | `python scripts\check_skill_architecture.py --json` |
| Citation MCP | `python -m unittest discover -s plugins\materials-skills\skills\materials-citation\mcp\academic_search\tests -p "test_*.py" -v` |
| Product docs/gallery/showcases | `python -m unittest tests.test_product_docs_contract -v` |
| Figure package behavior | `python -m unittest discover -s plugins\materials-skills\skills\materials-figure\tests -p "test_*.py" -v` |

Broaden the validation when touching shared contracts, scripts, MCP surfaces,
release gates, or plugin metadata.

## High-Risk Areas

| Area | Risk | Control |
|---|---|---|
| Shared contracts | Producer and consumer schemas drift | Update `plugins/materials-skills/_shared/contracts` and manifests together |
| Release gates | One-off exceptions hide drift | Keep validators manifest-driven |
| Figure assets | Generated exports bloat Git | Track source-only examples and ignore exports |
| Public docs | Product surface contradicts registry | Run product docs contract tests |

## Handoff Packet Template

When handing work to another agent, include:

- Current branch and latest commit.
- Files changed and whether any synchronized files were updated.
- Commands run and their exit status.
- Any known skipped checks and why they were skipped.
- Whether generated assets were created locally and whether they are ignored.
- Next recommended task.

Keep the packet factual. Do not say a change is complete unless the relevant
checks were run and passed.

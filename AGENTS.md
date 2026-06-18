# Materials Science Skills

Full-cycle Codex skill bundle for materials science research. Covers seven
material families with dual-axis domain routing, and routes work across
research, citation, reader, writing, figure, data, polishing, reviewer,
response, paper-to-PPT, and PPTX generation.

## Project

- **Stack**: Python 3.11+, YAML skill manifests, tests with `unittest`
- **Entry**: any `materials-*` skill; start with `materials-research` for workflow routing
- **Plugin package**: `plugins/materials-skills/` is the installable Codex plugin
- **Public docs**: `README.md`, `install.md`, `docs/skills-index.md`, `docs/workflows/`, `docs/showcases/`, `docs/gallery/`

## Commands

| Purpose | Command |
|---|---|
| Root contract tests | `python -m unittest discover -s tests -p "test_*.py" -v` |
| Single skill tests | `python -m unittest discover -s plugins/materials-skills/skills/materials-<name>/tests -p "test_*.py" -v` |
| Citation MCP tests | `python -m unittest discover -s plugins/materials-skills/skills/materials-citation/mcp/academic_search/tests -p "test_*.py" -v` |
| Release checks | `python scripts/run_release_checks.py --json` |
| Install | `.\scripts\install.ps1` |

## Architecture

- 12 skill modules under `plugins/materials-skills/skills/materials-*/`, each with `SKILL.md`, `manifest.yaml`, `agents/openai.yaml`, `tests/`, and `README.md`
- `plugins/materials-skills/skills/_shared/` contains cross-skill core guidance, journal formats, and paper-production handoffs
- `plugins/materials-skills/_shared/` contains cross-skill contracts, material registry entries, and trigger metadata
- Dual-axis domain routing uses `material_family` plus fine-grained `domain`
- `manifest.yaml` declares routing axes, `always_load` fragments, assets, scripts, tests, quality gates, handoffs, and release checks
- Output handoffs use standardized CSV/MD artifacts such as `reader-package`, `citation_handoff.csv`, `figure_handoff.csv`, gate reports, and DOE handoffs

## Agent Handoff Rules

- Treat `main` as the source-of-truth branch. Start by fetching `origin/main`, checking out `main`, and pulling with `--ff-only`.
- Treat `gemini` and `mimo` as audit/comparison branches only unless a maintainer explicitly promotes a change.
- Check `git status --short --branch` before editing and never discard unrelated user or agent work.
- Edit skills directly under `plugins/materials-skills/skills/materials-*`.
- Do not commit generated work products. Bundled `plugins/materials-skills/skills/materials-figure/examples/figure-packages` examples are source-only; regenerated `figure.svg/png/pdf/tif/tiff` exports are ignored.
- Keep `plugins/materials-skills/skills/materials-figure/assets/showcase-proof/*.png` tracked because README, gallery docs, and plugin metadata use them as product screenshots.
- Do not rewrite Git history unless following `docs/architecture/git-history-slimming-plan.md` during an approved freeze window.
- Run `python scripts/run_release_checks.py --json` before declaring any change complete.

## Conventions

- Skills are named `materials-*`; plugin directory is `plugins/materials-skills/`
- Import plotting helpers as `materials_plot_lib`
- Test files are `test_*.py` and use `unittest.TestCase`
- Citation MCP tests live under `mcp/academic_search/tests/`
- Use synthetic/example data only; do not commit real paper data
- Keep generated work products out of Git. Root-level `outputs/`, local run artifacts, desktop metadata, and internal planning notes are ignored
- Prefer `pathlib.Path` in scripts
- On PowerShell, use `; if ($?) { }` instead of `&&`
- Run `python scripts/run_release_checks.py --json` before declaring a change complete

## Key Files

| File | Purpose |
|---|---|
| `plugins/materials-skills/skills/materials-research/manifest.yaml` | Master routing manifest |
| `plugins/materials-skills/skills/_shared/core/stance.md` | Writing stance and operating principles |
| `plugins/materials-skills/skills/_shared/core/evidence-contract.md` | Evidence standards |
| `plugins/materials-skills/skills/_shared/paper-production/weakness-routing.md` | Weakness routing rules |
| `scripts/run_release_checks.py` | Release validation |
| `scripts/check_skill_architecture.py` | Manifest and plugin validation |
| `docs/workflows/` | Public guided workflow demos |
| `docs/showcases/` | Public outcome examples |

## Dependencies

`httpx`, `matplotlib`, `numpy`, `pillow`, `pymupdf`

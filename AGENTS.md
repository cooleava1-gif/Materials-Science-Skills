# Materials Science Skills

Full-cycle Codex skill bundle for materials science research. Covers seven
material families with dual-axis domain routing, and routes work across
research, citation, reader, writing, figure, data, polishing, reviewer,
response, paper-to-PPT, and PPTX generation.

## Project

- **Stack**: Python 3.11+, YAML skill manifests, tests with `unittest`
- **Entry**: any `materials-*` skill; start with `materials-research` for workflow routing
- **Plugin mirror**: `plugins/materials-skills/` mirrors the installable skill package
- **Public docs**: `README.md`, `install.md`, `docs/skills-index.md`, `docs/workflows/`, `docs/showcases/`, `docs/gallery/`

## Commands

| Purpose | Command |
|---|---|
| Root contract tests | `python -m unittest discover -s tests -p "test_*.py" -v` |
| Single skill tests | `python -m unittest discover -s skills/materials-<name>/tests -p "test_*.py" -v` |
| Citation MCP tests | `python -m unittest discover -s skills/materials-citation/mcp/academic_search/tests -p "test_*.py" -v` |
| Release checks | `python scripts/run_release_checks.py --json` |
| Install | `.\scripts\install.ps1` |

## Architecture

- 12 skill modules under `skills/materials-*/`, each with `SKILL.md`, `manifest.yaml`, `agents/openai.yaml`, `tests/`, and `README.md`
- `_shared/` contains cross-skill contracts, paper-production handoffs, material registry entries, and trigger metadata
- Dual-axis domain routing uses `material_family` plus fine-grained `domain`
- `manifest.yaml` declares routing axes, `always_load` fragments, assets, scripts, tests, quality gates, handoffs, and release checks
- Output handoffs use standardized CSV/MD artifacts such as `reader-package`, `citation_handoff.csv`, `figure_handoff.csv`, gate reports, and DOE handoffs
- `plugins/materials-skills/` should stay synchronized with source skills before release

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
| `skills/materials-research/manifest.yaml` | Master routing manifest |
| `skills/_shared/core/stance.md` | Writing stance and operating principles |
| `skills/_shared/core/evidence-contract.md` | Evidence standards |
| `skills/_shared/paper-production/weakness-routing.md` | Weakness routing rules |
| `scripts/run_release_checks.py` | Release validation |
| `scripts/check_skill_architecture.py` | Manifest and plugin mirror validation |
| `docs/workflows/` | Public guided workflow demos |
| `docs/showcases/` | Public outcome examples |

## Dependencies

`httpx`, `matplotlib`, `numpy`, `pillow`, `pymupdf`

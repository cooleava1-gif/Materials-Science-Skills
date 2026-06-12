# Materials Science Skills

Full-cycle Codex skill bundle for materials science research. Covers 7 material families (civil/construction, polymers, metals, ceramics, functional/electronic, nanomaterials, general) with dual-axis domain routing. Routes work across research, citation, reader, writing, figure, data, polishing, reviewer, response, paper-to-PPT, and PPTX generation.

## Project

- **Stack**: Python 3.11+, skill manifests in YAML, tests with `unittest`
- **Entry**: any of 12 `materials-*` skills; start with `materials-research` for workflow routing
- **Plugin mirror**: `plugins/materials-skills/` — installed package mirrored from `skills/`
- **Design docs**: `docs/superpowers/specs/`

## Commands

| Purpose | Command |
|---|---|
| **Root contract tests** | `python -m unittest discover -s tests -p "test_*.py" -v` |
| **Single skill tests** | `python -m unittest discover -s skills/materials-<name>/tests -p "test_*.py" -v` |
| **Citation MCP tests** | `python -m unittest discover -s skills/materials-citation/mcp/academic_search/tests -p "test_*.py" -v` |
| **Release checks** | `python scripts/run_release_checks.py --json` |
| **Install** | `.\scripts\install.ps1` (Windows PowerShell) |

## Architecture

- **12 skill modules** under `skills/materials-*/`, each with `SKILL.md`, `manifest.yaml`, `agents/openai.yaml`, `tests/`, `README.md`
- **_shared/** — cross-skill assets: `core/` (stance, ethics, evidence-contract, claim-strength-ladder, source-basis, terminology-ledger), `journal-formats/` (~17 journal format files), `paper-production/` (routing, gate report, weakness templates)
- **Dual-axis domain routing**: `material_family` (7 coarse: civil/polymers/metals/ceramics/functional/nano/general) + `domain` (29 fine-grained values)
- **manifest.yaml** — routing axes (`task`, `material_family`, `domain`, `journal`, `paper_stage`, `workflow_mode`, `output_package`) with `always_load`, `detect` triggers, and fragment paths
- **Output handoffs** — standardized CSV/MD artifacts: `reader-package`, `citation_handoff.csv`, `figure_handoff.csv`, gate reports, doe-handoff
- **scripts/** — `run_release_checks.py`, `install.ps1`, figure generators, pressure tests
- **plugins/** — Codex plugin mirror of the source tree

## Conventions

- **Naming**: Skills are `materials-*` (not `civil-materials-*`). Plugin dir: `plugins/materials-skills/`. Import: `materials_plot_lib`.
- Each skill has: `SKILL.md`, `manifest.yaml`, `agents/openai.yaml`, `tests/`, `README.md`
- Each manifest must include: `assets`, `scripts`, `tests`, `quality_gates`, `handoffs`, `release_checks` blocks
- Test files: `test_*.py` in `tests/` per skill, using `unittest.TestCase`
- Citation MCP tests live under `mcp/academic_search/tests/` — separate discovery path
- No real paper data committed — use synthetic/example data only
- Paths in scripts use `pathlib.Path`; prefer relative to repo root
- PowerShell: use `; if ($?) { }` instead of `&&` for command chaining
- Run `python scripts/run_release_checks.py --json` before declaring any change complete
- When modifying skills, sync to plugin mirror: `plugins/materials-skills/skills/`

## Key Files

| File | Purpose |
|---|---|
| `skills/materials-research/manifest.yaml` | Master routing manifest (all 7 axes) |
| `skills/_shared/core/stance.md` | Writing stance and operating principles |
| `skills/_shared/core/evidence-contract.md` | Evidence standards |
| `skills/_shared/paper-production/weakness-routing.md` | Weakness routing rules |
| `scripts/run_release_checks.py` | Architecture validation |
| `scripts/check_skill_architecture.py` | Manifest lint + mojibake detection |
| `docs/superpowers/specs/` | Design documents |

## Dependencies

`httpx`, `matplotlib`, `numpy`, `pillow`, `pymupdf`

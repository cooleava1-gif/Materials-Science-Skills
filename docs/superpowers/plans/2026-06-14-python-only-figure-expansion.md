# Python-Only Figure Expansion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove R as a supported plotting backend and expand `materials-figure` with ten additional Python publication-chart families.

**Architecture:** Keep the existing `materials-figure` structure. Update router docs/manifests to make Python the only plotting backend, remove R backend assets, add matplotlib helpers to `materials_plot_lib.py`, and add focused `figures4materials` scripts plus CSV examples.

**Tech Stack:** Python 3, matplotlib, numpy, unittest, repository release checks.

---

### Task 1: Python-Only Contract

**Files:**
- Modify: `skills/materials-figure/tests/test_figure_hard_workflow.py`
- Modify: `skills/materials-figure/SKILL.md`
- Modify: `skills/materials-figure/manifest.yaml`
- Modify: `skills/materials-figure/static/core/contract.md`
- Modify: `skills/materials-figure/static/core/figure-contract.md`
- Modify: `skills/materials-figure/static/core/workflow.md`
- Modify: `skills/materials-figure/static/fragments/backend/python.md`
- Delete: `skills/materials-figure/static/fragments/backend/r.md`
- Delete: `skills/materials-figure/references/r-workflow.md`
- Delete: `skills/materials-figure/references/r-template-index.md`
- Delete: `skills/materials-figure/scripts/r/palettes.R`
- Delete: `skills/materials-figure/scripts/r/theme_materials.R`

- [ ] Write failing tests requiring Python-only wording and absence of R backend files.
- [ ] Run the hard workflow test and verify it fails before production edits.
- [ ] Update source files to remove R backend routing and make Python the default backend.
- [ ] Delete R backend files from source.
- [ ] Run the hard workflow test and verify it passes.

### Task 2: Expanded Python Chart Helpers

**Files:**
- Modify: `skills/materials-figure/tests/test_matplotlib_production.py`
- Modify: `skills/materials-figure/scripts/materials_plot_lib.py`

- [ ] Write failing tests for ten helpers: scatter regression, boxplot with points, violin plot, contour map, 3D surface, polar plot, errorbar trend, dual-axis trend, correlation heatmap, and stacked composition bar.
- [ ] Run the matplotlib production test and verify it fails.
- [ ] Implement helpers in `materials_plot_lib.py`.
- [ ] Run the matplotlib production test and verify it passes.

### Task 3: Expanded Python Script Gallery

**Files:**
- Modify: `skills/materials-figure/tests/test_matplotlib_production.py`
- Create: ten `skills/materials-figure/scripts/figures4materials/plot_*.py` scripts.
- Create: ten CSV files under `skills/materials-figure/scripts/figures4materials/data/`.
- Modify: `skills/materials-figure/references/chart-atlas.md`
- Modify: `skills/materials-figure/references/tutorials.md`

- [ ] Write failing tests that require each new script/data pair and assert each script emits one SVG, one PNG, and a caption.
- [ ] Run the script test and verify it fails.
- [ ] Add the new scripts and synthetic example CSV data.
- [ ] Update chart atlas and tutorials with the Python-only expanded gallery.
- [ ] Run the script test and verify it passes.

### Task 4: Plugin Mirror And Verification

**Files:**
- Mirror all changed `skills/materials-figure/**` files to `plugins/materials-skills/skills/materials-figure/**`.

- [ ] Copy source changes to plugin mirror.
- [ ] Run `python scripts/check_skill_architecture.py --json`.
- [ ] Run `python -m unittest discover -s skills/materials-figure/tests -p "test_*.py" -v`.
- [ ] Run `python -m unittest discover -s tests -p "test_*.py" -v`.
- [ ] Run `python scripts/run_release_checks.py --json`.

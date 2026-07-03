---
name: materials-figure
description: >-
  Submission-grade scientific figure workflow for materials science and engineering research. Use whenever the user asks to create, revise, audit, or polish manuscript figures, multi-panel materials science plots, or journal-ready SVG/PDF/TIFF outputs for materials journals, construction materials research, or civil engineering publications. Before plotting, define the figure's conclusion, evidence logic, export needs, and review risks. Use Python (matplotlib/seaborn) for all figure generation, previewing, exporting, and QA. Supports materials characterization plots (XRD, FTIR, TG/DTG), performance curves, mechanism schematics, and review evidence maps. Not for dashboards or Illustrator/Figma-first infographics. Also trigger on materials science figure needs such as 材料科学配图、土木材料论文图、XRD/FTIR光谱图、性能曲线图、机理示意图、综述证据图.
version: 2.0.0
author: Community contribution, refactored into static/dynamic layers
---

# Materials Science Figure Making — Router

## Layered architecture

This skill is split into two layers:

- A **static layer** under `static/` that holds reusable content fragments.
- A **dynamic layer** (this file plus [manifest.yaml](manifest.yaml)) that detects the request's axes and loads only the fragments needed for the current job.

Do not try to apply the figure logic from memory or from this router. Always load fragments from disk as described below.

## Routing protocol

Follow these five steps every time the skill is invoked.

Before axis routing, apply profile-first routing from `.materials/profile.yaml`.
On first use, ask for the user's materials direction once, save it locally, and
use the saved profile to set the default material family/domain.

### 1. Load the manifest and the core layer

Read [manifest.yaml](manifest.yaml). It declares the `backend` axis (Python-only), the `always_load` files, and the on-demand references.

Also read every file listed under `always_load`:
- `static/core/contract.md` — the five-point figure contract
- `static/core/stance.md` — the default operating stance for materials science figures
- `static/core/materials_kb.yaml` — the materials knowledge graph for claim validation

These hold the figure contract, the backend gate, and the materials science knowledge base that apply to every figure job.

### 2. Resolve the backend — Python-only gate

The Python backend is mandatory for all figure drawing, previewing, exporting, and visual QA. Before rendering, check Python and required plotting packages (matplotlib, numpy, PIL; seaborn for heatmaps/statistical plots). If the runtime or packages are unavailable, stop before rendering and report the exact blocker.

Do not generate mock data, write plotting scripts, create previews, or render placeholder figures until the claim, source-data anchor, and figure contract are clear.

### 3. Load the Python backend fragment

After confirming Python backend readiness, read `static/fragments/backend/python.md`. It carries the Python-only execution rule and the publication quick-start (rcParams and export helper).

### 4. Build the figure using the loaded material

Apply the loaded material in this order:

1. **Figure contract** (`static/core/contract.md`) — write the core conclusion, map the evidence chain, classify the archetype, set the journal/export contract, before any code.
2. **Default stance** (`static/core/stance.md`) — materials science priorities, reviewer-safe defaults, restrained palettes, evidence hierarchy.
3. **Backend fragment** (`static/fragments/backend/python.md`) — the Python quick-start and execution rule.

The chart serves the scientific logic; aesthetic polish is subordinate to making the core conclusion clear, defensible, and reviewable.

**Optional materials knowledge validation.** If the figure contains materials-science entities (XRD peaks/phases, FTIR wavenumbers/functional groups, performance values), validate claims against `static/core/materials_kb.yaml`. Claims that contradict known material relations are errors and must be corrected before plotting. Figures without materials-science entities (e.g. pure flowcharts) pass with no checks.

**Optional multi-figure storyboard.** When a task spans more than one figure (e.g. a manuscript), write `figure_storyboard.yaml` defining the narrative arc, each figure's role, and cross-figure evidence dependencies. The storyboard gate sits above individual figure contracts: validate the storyboard first, then each figure's contract.

### 5. Reach for references only when needed

The files under `references/` are deep references, not defaults. Open them on demand per the `references.on_demand` table in the manifest — for example:
- `references/figure-package-protocol.md` to build a complete figure package
- `references/characterization-figures.md` for XRD/FTIR/TG/SEM plotting patterns
- `references/performance-figures.md` for strength/bonding/viscosity curves
- `references/mechanism-figures.md` for mechanism schematics and interface figures
- `references/figure-qa-contract.md` before final delivery
- `references/figure-production-spec.md` for export DPI, TIFF/EPS/PDF, final size
- `references/tutorials.md` for end-to-end walkthroughs
- `references/materials-figure-atlas.md` for fixed materials figure archetypes

## Why this split

- The static layer is versioned and reviewable. The Python backend gate is explicit in the manifest.
- The dynamic layer keeps each invocation cheap: only the Python quick-start enters context, and the 2,000+ lines of reference depth load only when a step needs them.
- The router itself is short on purpose. Update fragments and references, not this file, when adding scope.
- This structure mirrors `nature-figure` and separates the "LLM as artist" execution model from the deep reference material.

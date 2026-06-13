# Golden Sample: Asphalt-Pavement (WER-EA)

> **Coverage Tier**: 🟢 full  
> **Registry entry**: `_shared/material-registry/entries/asphalt-pavement.yaml`  
> **Domain fragment**: `skills/materials-research/static/fragments/domain/asphalt-pavement.md`  
> **Narrative guide**: `skills/materials-writing/references/asphalt-pavement-narrative.md`  
> **Reviewer criteria**: `skills/materials-reviewer/references/asphalt-reviewer-criteria.md`

This is the most deeply supported material system in the bundle. It covers
waterborne epoxy modified emulsified asphalt (WER-EA) for pavement tack coats,
waterproofing, and maintenance applications.

---

## 🔍 1. Search Strategy

When the user asks about WER-EA, the router detects `asphalt-pavement` and
loads the domain fragment + narrative guide. Key search queries:

| Layer | Boolean query | Target databases |
|---|---|---|
| Performance | `("waterborne epoxy" OR "WER") AND "emulsified asphalt" AND bond*` | Scopus, Web of Science, TRID |
| Mechanism | `("waterborne epoxy" OR "WER") AND FTIR AND curing AND asphalt` | Scopus, Google Scholar |
| Durability | `("emulsified asphalt" OR "tack coat") AND (freeze-thaw OR moisture) AND bond*` | Scopus, TRID, ASCE |
| Sustainability | `("emulsified asphalt") AND LCA AND ("cold mix" OR "cold recycling")` | Scopus, ScienceDirect |

The **materials-citation** MCP server runs these across CrossRef, PubMed,
OpenAlex, and Semantic Scholar in parallel, merging results with confidence
scoring.

## 📖 2. Reader Package Structure

After search, `materials-reader` produces a reader package:

```
reader-package/
├── source_map.json              # Source → claim mapping
├── evidence-chain-matrix.csv    # Claim → evidence → mechanism → boundary
├── citation-handoff.csv         # For materials-writing
└── figure-handoff.csv           # For materials-figure
```

Key columns in the evidence chain:
- **Claim type**: performance / mechanism / durability / sustainability
- **Evidence needed**: control group, FTIR peaks, SEM morphology, aging data
- **Reviewer risk**: overclaim from FTIR-alone mechanism assertions

## 📊 3. Evidence Matrix

| Claim | Evidence required | Typical data | Figure archetype |
|---|---|---|---|
| Epoxy improves bonding | Pull-off bond with dry & wet conditioning | 0.3–1.5 MPa, n≥3 | `bonding_strength_bar` |
| Curing mechanism | FTIR epoxide peak decay at 915 cm⁻¹ | Spectra at 0/3/7 days | `ftir_overlay` |
| Optimum dosage | Bonding + viscosity + stability vs. dosage | 10–15% epoxy range | `dosage_performance_curve` |
| Durability | Freeze-thaw cycling retention ≥80% | 5–25 cycles | `freeze_thaw_durability` |
| Morphology | SEM sea-island → co-continuous | Images at 5/10/15% | `sem_image` |

## 🧪 4. Experiment Design (DOE)

| Factor | Levels | Response variables |
|---|---|---|
| Epoxy content (% wt) | 0, 5, 10, 15, 20 | Bond strength, viscosity, stability |
| Curing time (days) | 1, 3, 7, 14 | FTIR conversion, bond development |
| Conditioning | Dry, wet (24h), freeze-thaw (5cy) | Retention ratio |

A full-factorial 5×4×3 = 60 runs, or a Taguchi L16 for screening.

## 📈 5. Typical Figures

Available figure scripts in `skills/materials-figure/scripts/figures4materials/`:

| Script | Output | Column roles |
|---|---|---|
| `plot_bonding_strength_comparison.py` | Grouped bar: dry vs. wet | `x_labels`, `series` |
| `plot_ftir_curing_evidence.py` | FTIR overlay with peak annotations | `x_values`, `absorbances` |
| `plot_dosage_performance_curve.py` | Dual-axis: bond + stability vs. dosage | `x_labels`, `series` |
| `plot_rheology_curve.py` | Viscosity vs. shear rate | `x_values`, `y_series` |
| `plot_sem_analysis.py` | Particle size histogram | `x_values`, `y_series` |
| `plot_durability_retention.py` | Retention ratio grouped bar | `x_labels`, `series` |
| `plot_tga_dtg_curve.py` | TGA/DTG overlay | `x_values`, `tga`, `dtg` |

All scripts accept `--column-map` for material-agnostic reuse.

## ⚠️ 6. Reviewer Risks

From `asphalt-reviewer-criteria.md` and registry `claim_types`:

| Risk | How to avoid |
|---|---|
| "FTIR confirms mechanism" without SEM/rheology | Say "FTIR suggests" and pair with at least one complementary technique |
| "Significantly improves" without p-value | Report p-value or use "notably / markedly" |
| "Durability proven" from lab-only test | Specify conditions: "after 5 freeze-thaw cycles, retention was X%" |
| "Field-ready" without constructability data | Report viscosity, open time, storage stability |
| "Green / sustainable" without LCA boundary | State functional unit and scope (cradle-to-gate) |

## 📝 7. Submission Advice

| Journal | Fit | Evidence emphasis |
|---|---|---|
| CBM (Constr. Build. Mater.) | 🟢 Strong | Bonding + mechanism + durability |
| CCC (Cem. Concr. Compos.) | 🟡 If cement-related | Hydration + microstructure |
| RMPD (Road Mater. Pavement) | 🟢 Strong | Pavement performance + field relevance |
| JBE (J. Build. Eng.) | 🟡 Waterproofing | Moisture resistance + adhesion |

---

## Key Files Summary

```
_shared/material-registry/entries/asphalt-pavement.yaml  # Structured registry
_shared/triggers/domain/asphalt-pavement.yaml            # Routing triggers
skills/materials-writing/references/asphalt-pavement-narrative.md
skills/materials-reviewer/references/asphalt-reviewer-criteria.md
skills/materials-figure/scripts/figures4materials/
├── plot_bonding_strength_comparison.py
├── plot_ftir_curing_evidence.py
├── plot_dosage_performance_curve.py
├── ... (+18 more WER-EA scripts)
skills/materials-figure/examples/figure-packages/
├── wer-ea-dosage-window/
├── wer-ea-evidence-heatmap/
└── wer-ea-mechanism-map/
```

Total: **21 figure scripts, 3 example packages, full end-to-end pipeline**.

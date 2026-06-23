## Design Method Selection Guide

Choose the right DOE approach based on your stage of research and number of factors.

### Decision Tree

```
Start
  │
  ├─ Are factors independent (not summing to 100%)?
  │    │
  │    ├─ YES → Factorial / RSM path
  │    │    │
  │    │    ├─ How many factors?
  │    │    │    ├─ 1 factor → Single-factor design (classical)
  │    │    │    ├─ 2-3 factors → Full factorial (classical)
  │    │    │    ├─ 4-6 factors → Orthogonal array / Taguchi
  │    │    │    ├─ 5-20 factors, screening phase → Plackett-Burman (screening)
  │    │    │    ├─ 4-8 factors, know some are important → Fractional factorial (screening)
  │    │    │    └─ 2-5 key factors, want optimum → RSM (CCD or BBD)
  │    │    │
  │    │    └─ Already have a design?
  │    │         ├─ Have screening results → Augment to full factorial or RSM
  │    │         └─ Have factorial with curvature → Augment to CCD
  │    │
  │    └─ NO → Mixture path
  │         │
  │         ├─ Components sum to 100%?
  │         │    ├─ YES → Mixture design (simplex lattice / centroid)
  │         │    └─ NO → Mix design guide (engineering approach)
  │         │
  │         └─ Component constraints?
  │              ├─ All components 0-100% → Standard simplex
  │              └─ Bounded components → Extreme vertices design
  │
  └─ Mixed: formulation + process factors?
       → Combined mixture-process design
```

### Recommended sequential strategy

1. **Screening** (many factors → few key factors): Plackett-Burman or 2^(k-p)
2. **Characterization** (understand key factors and interactions): Full factorial
3. **Optimization** (find best settings): RSM (CCD or BBD)
4. **Confirmation** (verify results): 3-5 replicate runs at optimum

### Quick reference table

| Design Type | Factors | Runs | Outputs | Use Case |
|-------------|---------|------|---------|----------|
| Single-factor | 1 | 3-5 levels × replicates | Main effect, trend | One variable study |
| Full factorial | 2-4 | 2^k or 3^k | All main effects + interactions | Detailed study of few factors |
| Taguchi L9/L16 | 3-6 | 9 or 16 | Main effects + some interactions | Robust design, quality engineering |
| Plackett-Burman | 7-23 | 12, 20, 24... | Main effects only (screening) | Initial factor screening |
| Fractional factorial | 4-8 | 8, 16, 32... | Main effects + some 2FI | Efficient screening with known resolution |
| CCD (RSM) | 2-5 | 13, 20, 30+ | Full quadratic model, optimum | Optimization with known key factors |
| Box-Behnken (RSM) | 3-5 | 15, 27... | Full quadratic model | Optimization, no extreme points |
| Simplex lattice {q,2} | 3-6 components | 6, 10, 15... | Quadratic mixture model | Formulation optimization |
| Simplex centroid | 3-4 components | 7, 15 | Up to special cubic | Comprehensive mixture study |

---

# Workflow

General workflow for design-of-experiments planning.

## Steps

1. Identify the material system and domain.
2. Choose the design mode (classical, orthogonal, or mix-design).
3. List factors and levels.
4. Generate the experimental matrix.
5. Define the analysis strategy.

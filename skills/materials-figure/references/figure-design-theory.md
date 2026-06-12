# Figure Design Theory for Materials Science

## Color Theory and Semantic Mapping

### Core principle
Color in scientific figures is not decoration — it is a semantic encoding channel.
Every color must carry meaning that is consistent across all panels of a figure.

### Semantic roles for materials science

| Role | Use case | Recommended hue |
|---|---|---|
| Control / baseline | Unmodified material, reference group | Neutral blue-grey |
| Modified / experimental | Formulation variant, treatment | Warm orange-brown |
| Optimal / best performer | Selected composition, peak performance | Green |
| Mechanism evidence | Characterization, microstructure | Brown / earth |
| Comparison / competitor | Literature data, commercial product | Grey |
| Danger / warning | Failed group, degradation, risk | Red |
| Accent | Annotation, highlight, callout | Gold / amber |

### Palette system

```python
# Primary semantic palette
PALETTE_SEMANTIC = {
    "control":      "#4B6F8A",   # blue-grey
    "modified":     "#C47B45",   # warm orange
    "optimal":      "#4F7C6A",   # forest green
    "mechanism":    "#8B6F47",   # earth brown
    "comparison":   "#8C8C8C",   # neutral grey
    "danger":       "#B85450",   # muted red
    "accent":       "#D4A574",   # gold
}
```

### Unified low-saturation palette (Nature Machine Intelligence style)

When comparing related variants of the same material system (e.g., 3 epoxy dosages),
use a **single hue family** with increasing saturation/darkness:

```python
PALETTE_SINGLE_HUE = {
    "variant_1": "#B4C0E4",   # light
    "variant_2": "#7884B4",   # medium
    "variant_3": "#484878",   # dark
}
```

### Practical rules

- Design for **colorblind accessibility**: avoid red-green contrast alone. Use marker shapes, hatching, or labels alongside color.
- Test figures in grayscale: if information is lost, add pattern or shape cues.
- Colorblind-friendly palettes use blue-orange instead of red-green for contrast.

- The **same** material variant keeps the **same** color in every panel of a figure.
- Do not recolor "15% epoxy" from orange in panel (a) to green in panel (c).
- Reserve green/red for signed semantics: improvement vs decline, pass vs fail.
- For bar charts with >4 groups, use a single-hue gradient rather than rainbow.
- Always check color accessibility: avoid red-green contrast alone. Add marker shapes or patterns.

## Typography and Fonts

### Font stack

```python
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
plt.rcParams['svg.fonttype'] = 'none'
```

**Why `svg.fonttype = 'none'`**: keeps text as editable SVG `<text>` nodes, not bezier paths.
Without this, no one can edit axis labels, legends, or annotations after export.

### Font size hierarchy

| Context | Publication (single-column) | Presentation / poster |
|---|---|---|
| Axis labels | 8-10 pt | 14-18 pt |
| Tick labels | 7-9 pt | 12-14 pt |
| Panel labels (a, b, c) | 10-12 pt bold | 16-20 pt bold |
| Legend | 7-8 pt | 12-14 pt |
| In-bar annotation | 6-7 pt | 10-12 pt |

### Panel label placement

```python
ax.text(-0.08, 1.05, "a", transform=ax.transAxes,
        fontsize=12, fontweight="bold", va="top", ha="left")
```

Use **bold lowercase** (a, b, c). Place at top-left via transAxes.

## Layout Rules

### Figure size recommendations

| Chart type | figsize (inches) | Aspect ratio |
|---|---|---|
| Single grouped bar | (4.5, 3.5) | 1.3:1 |
| Multi-panel (2 panels) | (8, 4) | 2:1 |
| Multi-panel (3-4 panels) | (10, 6) | 1.7:1 |
| Line/trend | (5, 3) | 1.7:1 |
| Heatmap | (5, 4) | 1.25:1 |
| XRD pattern | (6, 3) | 2:1 |
| TGA/DTG overlay | (5, 3.5) | 1.4:1 |
| Radar | (5, 5) | 1:1 |

### Axes

- Top and right spines: always off.
- Left and bottom spines: 1.5-2 pt linewidth.
- No gridlines by default. Use sparse y-ticks for guidance.
- Y-limits tightened to data range — never 0-100 when data sits in 80-95.

### Legend

- `frameon=False`.
- Place inside plot only if it does not obscure data.
- For multi-panel figures, give legend its own subplot axis.

### Multi-panel information hierarchy and architecture

Each panel in a multi-panel figure must answer a **different** scientific question.
Recommended 3-level progression:

| Level | Question | Encoding |
|---|---|---|
| 1. Overview | "What is the overall trend?" | Grouped bar, composition |
| 2. Deviation | "What is different per group?" | Z-score heatmap, diverging cmap |
| 3. Relationship | "How do variables co-vary?" | Scatter, bubble plot |

### Anti-redundancy checklist

- [ ] Each panel answers a different question.
- [ ] No panel is a subset of another (e.g., ranked bar of one column from a stacked bar).
- [ ] If two panels show the same trend from different angles, merge or replace one.
- [ ] Color assignments are consistent across panels.

## Export Policy

- Primary output: **SVG** with `bbox_inches='tight'`.
- Raster preview: PNG at 300 dpi.
- For submission: follow journal requirements (TIFF 300 dpi, EPS, or PDF).
- Always `plt.close(fig)` after save to free memory.

## Figure QA Checklist

Before marking a figure as publication-ready:

- [ ] svg.fonttype = 'none' is set.
- [ ] Text is editable in Illustrator/Inkscape (open SVG and check).
- [ ] All axis labels, tick labels, and legend text are legible at final print size.
- [ ] Color assignments are consistent across all panels.
- [ ] Panel labels (a, b, c) are present, bold, lowercase.
- [ ] No top/right spines. Bottom/left spines are visible.
- [ ] Legend has no frame.
- [ ] Y-limits are tightened to data range.
- [ ] Error bars or confidence intervals are present where applicable.
- [ ] Statistical annotations (p-values, n) are included if relevant.
- [ ] Figure caption describes the conclusion, not just the axis labels.
- [ ] Source data is accessible (CSV or table in supplement).

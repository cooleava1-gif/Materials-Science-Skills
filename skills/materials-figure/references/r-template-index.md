# R Template Index for Materials Figures

This file indexes reusable R code templates for common materials-science
figure types. Each template references the `r-workflow.md` theme and palettes.

---

## Template Index

| # | Template | File | Chart type | Packages |
|---|---|---|---|---|
| 1 | Grouped bar | `r/grouped_bar.R` | `geom_col` + `geom_errorbar` | ggplot2 |
| 2 | Dosage curve | `r/dosage_curve.R` | `geom_line` + `geom_ribbon` | ggplot2 |
| 3 | FTIR overlay | `r/ftir_overlay.R` | `geom_line` + reversed x | ggplot2 |
| 4 | XRD stacked | `r/xrd_stacked.R` | `geom_line` + offset | ggplot2, dplyr |
| 5 | Evidence heatmap | `r/evidence_heatmap.R` | `ComplexHeatmap` | ComplexHeatmap |
| 6 | Radar chart | `r/radar_chart.R` | `coord_polar` + `geom_polygon` | ggplot2 |
| 7 | Box plot | `r/boxplot_with_points.R` | `geom_boxplot` + `geom_jitter` | ggplot2 |
| 8 | TGA/DTG dual-axis | `r/tga_dtg.R` | `sec_axis` dual y | ggplot2 |
| 9 | 2×2 multi-panel | `r/multipanel_2x2.R` | patchwork | patchwork |
| 10 | Durability retention | `r/durability_retention.R` | grouped bar with facets | ggplot2 |

---

## Template 1: Grouped Bar

```r
# r/grouped_bar.R
source("r/theme_materials.R")
source("r/palettes.R")

data <- data.frame(
  condition = rep(c("Dry", "Moisture"), each = 4),
  formulation = rep(c("Control", "10% WER", "15% WER", "20% WER"), 2),
  strength = c(0.45, 0.62, 0.78, 0.71, 0.32, 0.51, 0.68, 0.55),
  sd = c(0.04, 0.05, 0.06, 0.05, 0.03, 0.04, 0.05, 0.04)
)

p <- ggplot(data, aes(x = condition, y = strength, fill = formulation)) +
  geom_col(position = position_dodge(width = 0.7), width = 0.6,
           colour = "white", linewidth = 0.3) +
  geom_errorbar(aes(ymin = strength - sd, ymax = strength + sd),
                position = position_dodge(width = 0.7), width = 0.15) +
  scale_fill_manual(values = palette_materials) +
  labs(y = "Bond strength (MPa)", x = NULL) +
  theme_materials()

ggsave("bonding_strength.svg", p, device = svglite::svglite,
       width = 6, height = 4, dpi = 300)
```

---

## Template 2: Dosage Curve

```r
# r/dosage_curve.R
source("r/theme_materials.R")
source("r/palettes.R")

data <- data.frame(
  dosage = c(0, 5, 10, 15, 20, 25),
  strength = c(0.45, 0.58, 0.72, 0.78, 0.71, 0.63),
  sd = c(0.04, 0.05, 0.05, 0.06, 0.05, 0.04)
)

p <- ggplot(data, aes(x = dosage, y = strength)) +
  geom_ribbon(aes(ymin = strength - sd, ymax = strength + sd),
              fill = palette_materials[["control"]], alpha = 0.18) +
  geom_line(linewidth = 1.2, colour = palette_materials[["control"]]) +
  geom_point(size = 3, colour = palette_materials[["control"]]) +
  annotate("rect", xmin = 12, xmax = 18, ymin = -Inf, ymax = Inf,
           fill = palette_materials[["optimal"]], alpha = 0.12) +
  annotate("text", x = 15, y = 0.82, label = "Optimum range",
           colour = palette_materials[["optimal"]], size = 3.5) +
  labs(x = "WER content (%)", y = "Bond strength (MPa)") +
  theme_materials()

ggsave("dosage_curve.svg", p, device = svglite::svglite,
       width = 6, height = 4, dpi = 300)
```

---

## Template 3: FTIR Overlay

```r
# r/ftir_overlay.R
source("r/theme_materials.R")
source("r/palettes.R")

# Load spectral data (wavenumber, absorbance, sample)
data <- read.csv("ftir_data.csv")

peaks <- data.frame(
  position = c(915, 1240, 1730, 3400),
  label = c("Epoxide", "C-O-C", "C=O", "O-H")
)

p <- ggplot(data, aes(x = wavenumber, y = absorbance, colour = sample)) +
  geom_line(linewidth = 0.8) +
  scale_x_reverse() +
  geom_vline(data = peaks, aes(xintercept = position),
             linetype = "dashed", colour = "#B85450", linewidth = 0.5) +
  geom_text(data = peaks, aes(x = position, y = Inf, label = label),
            vjust = 1.5, size = 3, colour = "#B85450", angle = 90) +
  scale_color_manual(values = palette_materials) +
  labs(x = expression(Wavenumber~(cm^{-1})), y = "Absorbance (a.u.)") +
  theme_materials()

ggsave("ftir_overlay.svg", p, device = svglite::svglite,
       width = 7, height = 4, dpi = 300)
```

---

## Template 4: XRD Stacked

```r
# r/xrd_stacked.R
source("r/theme_materials.R")
source("r/palettes.R")

data <- read.csv("xrd_data.csv")  # columns: two_theta, intensity, sample

offset <- 1.0
data <- data %>%
  group_by(sample) %>%
  mutate(y_offset = intensity + (cur_group_id() - 1) * offset) %>%
  ungroup()

peaks <- data.frame(
  position = c(18.0, 26.6, 29.4, 34.1),
  label = c("CH", "Quartz", "C3S", "C-S-H")
)

p <- ggplot(data, aes(x = two_theta, y = y_offset, colour = sample)) +
  geom_line(linewidth = 0.7) +
  geom_vline(data = peaks, aes(xintercept = position),
             linetype = "dashed", colour = "#8C8C8C", linewidth = 0.5) +
  geom_text(data = peaks, aes(x = position, y = Inf, label = label),
            vjust = 1.5, size = 3, colour = "#8C8C8C") +
  scale_color_manual(values = palette_materials) +
  labs(x = expression(2*theta~(degree)), y = "Intensity (a.u.)") +
  theme_materials()

ggsave("xrd_pattern.svg", p, device = svglite::svglite,
       width = 7, height = 5, dpi = 300)
```

---

## Template 5: Evidence Heatmap

```r
# r/evidence_heatmap.R
library(ComplexHeatmap)
library(circlize)

mat <- matrix(c(
  1.0, 0.5, 0.0, 1.0, 0.5, 0.0,
  0.5, 0.0, 0.0, 0.5, 1.0, 0.0,
  1.0, 0.5, 0.5, 0.0, 0.0, 0.0,
  0.0, 0.0, 0.0, 1.0, 0.5, 0.0,
  0.0, 0.0, 0.0, 0.0, 0.0, 0.0
), nrow = 5, byrow = TRUE)

rownames(mat) <- c(
  "Epoxy improves bond strength",
  "WER improves moisture resistance",
  "Curing mechanism is crosslinking",
  "Optimal dosage is 12-18%",
  "Field performance validated"
)
colnames(mat) <- c("FTIR", "SEM", "XRD", "Mechanical", "Durability", "Field")

symbols <- matrix(ifelse(mat == 1, "\u2713",
                  ifelse(mat == 0.5, "~",
                  ifelse(mat == 0, "\u2717", "?"))),
                  nrow = nrow(mat))

ht <- Heatmap(mat, name = "Evidence",
  col = colorRamp2(c(-1, 0, 0.5, 1),
                   c("#F6CFCB", "#F6CFCB", "#FFD700", "#4F7C6A")),
  cluster_rows = FALSE, cluster_columns = FALSE,
  cell_fun = function(j, i, x, y, w, h, col) {
    grid.text(symbols[i, j], x, y,
              gp = gpar(fontsize = 12, fontface = "bold"))
  }
)

svg("evidence_heatmap.svg", width = 8, height = 5)
draw(ht)
dev.off()
```

---

## Template 6: Radar Chart

```r
# r/radar_chart.R
source("r/theme_materials.R")
source("r/palettes.R")

categories <- c("Bond strength", "Tensile", "Flexural",
                "Impact", "Hardness", "Workability")

data <- data.frame(
  formulation = rep(c("Control", "15% WER"), each = 6),
  category = rep(categories, 2),
  value = c(0.45, 0.60, 0.55, 0.30, 0.70, 0.85,
            0.78, 0.82, 0.75, 0.55, 0.68, 0.70)
)

# Create angle for radar
data <- data %>%
  group_by(formulation) %>%
  mutate(angle = seq(0, 2 * pi, length.out = n() + 1)[1:n()]) %>%
  ungroup()

# Close polygons
closed <- data %>%
  group_by(formulation) %>%
  slice(1) %>%
  mutate(angle = 2 * pi) %>%
  bind_rows(data) %>%
  arrange(formulation, angle)

p <- ggplot(closed, aes(x = angle, y = value,
                         colour = formulation, fill = formulation)) +
  geom_polygon(alpha = 0.15, linewidth = 1) +
  geom_point(size = 2) +
  coord_polar() +
  scale_y_continuous(limits = c(0, 1)) +
  scale_x_continuous(
    breaks = seq(0, 2 * pi, length.out = length(categories) + 1)[1:length(categories)],
    labels = categories
  ) +
  scale_color_manual(values = palette_materials) +
  scale_fill_manual(values = palette_materials) +
  theme(axis.title = element_blank())

ggsave("radar_chart.svg", p, device = svglite::svglite,
       width = 6, height = 6, dpi = 300)
```

---

## Template 7: Box Plot with Points

```r
# r/boxplot_with_points.R
source("r/theme_materials.R")
source("r/palettes.R")

set.seed(42)
data <- data.frame(
  formulation = rep(c("Control", "10% WER", "15% WER"), each = 20),
  strength = c(rnorm(20, 0.45, 0.08), rnorm(20, 0.62, 0.06),
               rnorm(20, 0.78, 0.07))
)

p <- ggplot(data, aes(x = formulation, y = strength, fill = formulation)) +
  geom_boxplot(alpha = 0.7, outlier.shape = NA, width = 0.5) +
  geom_jitter(width = 0.15, size = 1.5, alpha = 0.7, colour = "#333333") +
  scale_fill_manual(values = palette_materials) +
  labs(x = NULL, y = "Bond strength (MPa)") +
  theme_materials() +
  theme(legend.position = "none")

ggsave("boxplot.svg", p, device = svglite::svglite,
       width = 5, height = 4, dpi = 300)
```

---

## Template 8: TGA/DTG Dual-Axis

```r
# r/tga_dtg.R
source("r/theme_materials.R")
source("r/palettes.R")

data <- read.csv("tga_data.csv")  # columns: temp, mass, dtg, sample

p <- ggplot(data, aes(x = temp)) +
  geom_line(aes(y = mass, colour = sample), linewidth = 0.8) +
  geom_line(aes(y = dtg * 100, colour = sample), linewidth = 0.6,
            linetype = "dashed") +
  scale_y_continuous(
    name = "Mass (%)",
    sec.axis = sec_axis(~ . / 100, name = "DTG (%/°C)")
  ) +
  scale_color_manual(values = palette_materials) +
  labs(x = "Temperature (°C)") +
  theme_materials() +
  theme(axis.title.y.right = element_text(angle = 90))

ggsave("tga_dtg.svg", p, device = svglite::svglite,
       width = 6, height = 4, dpi = 300)
```

---

## Template 9: 2×2 Multi-Panel

```r
# r/multipanel_2x2.R
source("r/theme_materials.R")
source("r/palettes.R")
library(patchwork)

# Build individual panels (p1, p2, p3, p4 from templates above)
combined <- p1 + p2 + p3 + p4 +
  plot_layout(ncol = 2, nrow = 2, guides = "collect") +
  plot_annotation(tag_levels = "a", tag_prefix = "(", tag_suffix = ")") &
  theme(plot.tag = element_text(face = "bold", size = 14))

ggsave("multipanel_2x2.svg", plot = combined, device = svglite::svglite,
       width = 12, height = 10, dpi = 300)
```

---

## Template 10: Durability Retention

```r
# r/durability_retention.R
source("r/theme_materials.R")
source("r/palettes.R")

data <- data.frame(
  formulation = rep(c("Control", "10% WER", "15% WER", "20% WER"), 3),
  condition = rep(c("Before", "After 5 cycles", "Retention (%)"), each = 4),
  value = c(0.45, 0.62, 0.78, 0.71,   # before
            0.28, 0.52, 0.66, 0.55,   # after
            62, 84, 85, 78)            # retention
)

p_retention <- ggplot(data %>% filter(condition == "Retention (%)"),
                      aes(x = formulation, y = value, fill = formulation)) +
  geom_col(width = 0.6, colour = "white") +
  scale_fill_manual(values = palette_materials) +
  labs(x = NULL, y = "Retention (%)") +
  coord_cartesian(ylim = c(0, 100)) +
  theme_materials() +
  theme(legend.position = "none")

ggsave("durability_retention.svg", p_retention, device = svglite::svglite,
       width = 5, height = 4, dpi = 300)
```

---

## Shared Files

Create these as reusable source files:

### `r/theme_materials.R`

Contains the `theme_materials()` function from `r-workflow.md` §2.

### `r/palettes.R`

Contains all palette definitions from `r-workflow.md` §3.

---

## Usage Notes

1. Source the shared files at the top of each script.
2. Load data from CSV (never hardcode in production scripts).
3. Export SVG as primary, PNG as preview, TIFF for submission.
4. Use `patchwork` for multi-panel composition.
5. Follow the QA checklist in `r-workflow.md` §7 after every export.

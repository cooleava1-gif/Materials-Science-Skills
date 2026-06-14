# R Workflow for Materials Science Figures

Use this reference when the user selects R as the plotting backend. This file
governs the complete R workflow: setup, theme, palettes, chart patterns, export,
and QA.

---

## 1. Setup

### Required packages

```r
# Core
library(ggplot2)       # primary plotting
library(patchwork)     # multi-panel composition
library(svglite)       # editable SVG export
library(ragg)          # high-quality TIFF/PNG

# Optional (for specific chart types)
library(ComplexHeatmap)  # large heatmaps, review matrices
library(ggrepel)         # non-overlapping text labels
library(scales)          # axis formatting
library(RColorBrewer)    # color palettes
library(dplyr)           # data manipulation
library(tidyr)           # data reshaping
```

### Runtime check

```powershell
Rscript -e "library(ggplot2); library(patchwork); library(svglite); library(ragg)"
```

If any package is missing, stop and report the blocker. Do not fall back to
Python.

---

## 2. Publication Theme

Every materials figure starts with this theme:

```r
theme_materials <- function(base_size = 12) {
  theme_minimal(base_size = base_size, base_family = "Arial") +
    theme(
      # Spines
      axis.line = element_line(linewidth = 0.6, colour = "#333333"),
      axis.line.x.top = element_blank(),
      axis.line.y.right = element_blank(),

      # Grid
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),

      # Text
      axis.title = element_text(size = base_size, colour = "#333333"),
      axis.text = element_text(size = base_size - 2, colour = "#333333"),
      plot.title = element_text(size = base_size + 2, face = "bold", hjust = 0),

      # Legend
      legend.position = "right",
      legend.key = element_blank(),
      legend.background = element_blank(),
      legend.text = element_text(size = base_size - 2),

      # Panel
      panel.background = element_blank(),
      plot.background = element_blank(),
      strip.text = element_text(size = base_size - 1, face = "bold")
    )
}

# Apply globally
theme_set(theme_materials())
```

### Font size hierarchy

| Context | base_size |
|---|---|
| Compact subfigure | 10–11 |
| Standard single-column | 12 |
| Large multi-panel | 13–14 |
| Poster / presentation | 16–18 |

---

## 3. Color Palettes

### Semantic palette (materials science)

```r
palette_materials <- c(
  control    = "#4B6F8A",
  modified   = "#C47B45",
  optimal    = "#4F7C6A",
  mechanism  = "#8B6F47",
  comparison = "#8C8C8C",
  danger     = "#B85450",
  accent     = "#D4A574"
)
```

### Single-hue gradient (related variants)

```r
palette_single_hue <- c(
  "#B4C0E4",  # light
  "#7884B4",  # medium
  "#484878",  # dark
  "#2C2C58"   # darkest
)
```

### Domain-specific palettes

```r
palette_asphalt <- c(
  control   = "#6B7B8D",
  modified  = "#8B6914",
  optimal   = "#4A7C59",
  moisture  = "#5B8FA8",
  aging     = "#C47B45",
  mechanism = "#8B6F47",
  danger    = "#B85450",
  neutral   = "#8C8C8C"
)

palette_cement <- c(
  control   = "#7A7A7A",
  modified  = "#4B6F8A",
  optimal   = "#4F7C6A",
  hydration = "#C47B45",
  mechanism = "#8B6F47",
  durability = "#5B8FA8",
  danger    = "#B85450",
  neutral   = "#9E9E9E"
)

palette_polymer <- c(
  control   = "#4B6F8A",
  modified  = "#9A4D8E",
  optimal   = "#4F7C6A",
  mechanism = "#C47B45",
  thermal   = "#B85450",
  mechanical = "#5B8FA8",
  danger    = "#D4574E",
  neutral   = "#8C8C8C"
)

palette_ceramic <- c(
  control   = "#8C8C8C",
  modified  = "#C47B45",
  optimal   = "#4F7C6A",
  mechanism = "#8B6F47",
  thermal   = "#B85450",
  mechanical = "#4B6F8A",
  danger    = "#D4574E",
  neutral   = "#9E9E9E"
)
```

### NMI pastel palette (editorial multi-panel)

```r
palette_nmi_pastel <- c(
  baseline_dark  = "#484878",
  baseline_mid   = "#7884B4",
  baseline_soft  = "#B4C0E4",
  ours_tiny      = "#E4E4F0",
  ours_base      = "#E4CCD8",
  ours_large     = "#F0C0CC",
  delta_up       = "#2E9E44",
  delta_down     = "#E53935"
)
```

### Usage

```r
# Scale fill
scale_fill_manual(values = palette_materials)

# Scale color
scale_color_manual(values = palette_materials)

# For 3+ groups, use the palette as a named vector
groups <- c("Control", "10% WER", "15% WER", "20% WER")
colors <- setNames(palette_materials[1:4], groups)
```

---

## 4. Chart Patterns

### 4.1 Grouped bar chart

```r
make_grouped_bar <- function(data, x, y, fill, facet = NULL,
                              error_col = NULL, ylabel = NULL) {
  p <- ggplot(data, aes(x = .data[[x]], y = .data[[y]],
                         fill = .data[[fill]])) +
    geom_col(position = position_dodge(width = 0.7), width = 0.6,
             colour = "white", linewidth = 0.3)

  if (!is.null(error_col)) {
    p <- p + geom_errorbar(
      aes(ymin = .data[[y]] - .data[[error_col]],
          ymax = .data[[y]] + .data[[error_col]]),
      position = position_dodge(width = 0.7), width = 0.15, linewidth = 0.4
    )
  }

  if (!is.null(facet)) {
    p <- p + facet_wrap(as.formula(paste("~", facet)))
  }

  p + labs(y = ylabel) +
    scale_fill_manual(values = palette_materials)
}
```

### 4.2 Line trend with uncertainty band

```r
make_line_trend <- function(data, x, y, group = NULL, sd_col = NULL,
                             xlabel = NULL, ylabel = NULL) {
  p <- ggplot(data, aes(x = .data[[x]], y = .data[[y]]))

  if (!is.null(sd_col)) {
    p <- p + geom_ribbon(
      aes(ymin = .data[[y]] - .data[[sd_col]],
          ymax = .data[[y]] + .data[[sd_col]],
          fill = if (!is.null(group)) .data[[group]] else NULL),
      alpha = 0.18, colour = NA
    )
  }

  if (!is.null(group)) {
    p <- p + geom_line(aes(colour = .data[[group]]), linewidth = 1.2) +
      geom_point(aes(colour = .data[[group]]), size = 2) +
      scale_color_manual(values = palette_materials)
  } else {
    p <- p + geom_line(linewidth = 1.2, colour = palette_materials[["control"]]) +
      geom_point(size = 2, colour = palette_materials[["control"]])
  }

  p + labs(x = xlabel, y = ylabel)
}
```

### 4.3 FTIR overlay

```r
make_ftir_overlay <- function(data, wavenumber_col, absorbance_col,
                               sample_col, peaks = NULL) {
  p <- ggplot(data, aes(x = .data[[wavenumber_col]],
                         y = .data[[absorbance_col]],
                         colour = .data[[sample_col]])) +
    geom_line(linewidth = 0.8) +
    scale_x_reverse() +
    scale_color_manual(values = palette_materials) +
    labs(x = expression(Wavenumber~(cm^{-1})), y = "Absorbance (a.u.)")

  if (!is.null(peaks)) {
    peak_df <- data.frame(x = peaks$position, label = peaks$label)
    p <- p + geom_vline(data = peak_df, aes(xintercept = x),
                         linetype = "dashed", colour = "#B85450", linewidth = 0.5) +
      geom_text(data = peak_df, aes(x = x, y = Inf, label = label),
                vjust = 1.5, hjust = 0, size = 3, colour = "#B85450",
                angle = 90)
  }

  p
}
```

### 4.4 XRD stacked pattern

```r
make_xrd_stacked <- function(data, two_theta_col, intensity_col,
                              sample_col, offset = 1.0, peaks = NULL) {
  data <- data %>%
    group_by(.data[[sample_col]]) %>%
    mutate(intensity_offset = .data[[intensity_col]] +
             (cur_group_id() - 1) * offset) %>%
    ungroup()

  p <- ggplot(data, aes(x = .data[[two_theta_col]],
                         y = intensity_offset,
                         colour = .data[[sample_col]])) +
    geom_line(linewidth = 0.7) +
    scale_color_manual(values = palette_materials) +
    labs(x = expression(2*theta~(degree)), y = "Intensity (a.u.)")

  if (!is.null(peaks)) {
    peak_df <- data.frame(x = peaks$position, label = peaks$label)
    p <- p + geom_vline(data = peak_df, aes(xintercept = x),
                         linetype = "dashed", colour = "#8C8C8C", linewidth = 0.5) +
      geom_text(data = peak_df, aes(x = x, y = Inf, label = label),
                vjust = 1.5, size = 3, colour = "#8C8C8C")
  }

  p
}
```

### 4.5 Heatmap (sequential)

```r
make_heatmap <- function(data, row_labels, col_labels, cmap = "YlOrRd",
                          annot = TRUE) {
  mat <- as.matrix(data)
  rownames(mat) <- row_labels
  colnames(mat) <- col_labels

  ComplexHeatmap::Heatmap(
    mat, name = "Value",
    col = circlize::colorRamp2(
      seq(min(mat), max(mat), length.out = 9),
      RColorBrewer::brewer.pal(9, cmap)
    ),
    cluster_rows = FALSE, cluster_columns = FALSE,
    cell_fun = if (annot) function(j, i, x, y, w, h, col) {
      grid::grid.text(sprintf("%.2f", mat[i, j]), x, y,
                       gp = grid::gpar(fontsize = 8))
    } else NULL
  )
}
```

### 4.6 Radar chart

```r
make_radar <- function(data, categories, values_col, group_col,
                        max_val = 1.0) {
  # Prepare data: each category needs to close the polygon
  radar_data <- data %>%
    mutate(angle = seq(0, 2 * pi, length.out = n() + 1)[1:n()]) %>%
    bind_rows(data %>% slice(1) %>% mutate(angle = 2 * pi))

  ggplot(radar_data, aes(x = angle, y = .data[[values_col]],
                          colour = .data[[group_col]],
                          fill = .data[[group_col]])) +
    geom_polygon(alpha = 0.15, linewidth = 1) +
    geom_point(size = 2) +
    coord_polar() +
    scale_y_continuous(limits = c(0, max_val)) +
    scale_x_continuous(
      breaks = seq(0, 2 * pi, length.out = length(categories) + 1)[1:length(categories)],
      labels = categories
    ) +
    scale_color_manual(values = palette_materials) +
    scale_fill_manual(values = palette_materials) +
    theme(axis.title = element_blank())
}
```

### 4.7 Box plot with individual points

```r
make_boxplot <- function(data, x, y, fill = NULL, show_points = TRUE) {
  p <- ggplot(data, aes(x = .data[[x]], y = .data[[y]]))

  if (!is.null(fill)) {
    p <- p + geom_boxplot(aes(fill = .data[[fill]]), alpha = 0.7,
                           outlier.shape = NA, width = 0.5) +
      scale_fill_manual(values = palette_materials)
  } else {
    p <- p + geom_boxplot(fill = palette_materials[["control"]],
                           alpha = 0.7, outlier.shape = NA, width = 0.5)
  }

  if (show_points) {
    p <- p + geom_jitter(width = 0.15, size = 1.5, alpha = 0.7,
                          colour = "#333333")
  }

  p
}
```

### 4.8 TGA/DTG dual-axis

```r
make_tga_dtg <- function(data, temp_col, tga_col, dtg_col,
                          sample_col = NULL) {
  p <- ggplot(data, aes(x = .data[[temp_col]]))

  if (!is.null(sample_col)) {
    p <- p +
      geom_line(aes(y = .data[[tga_col]], colour = .data[[sample_col]]),
                linewidth = 0.8) +
      geom_line(aes(y = .data[[dtg_col]] * 100, colour = .data[[sample_col]]),
                linewidth = 0.6, linetype = "dashed") +
      scale_color_manual(values = palette_materials)
  } else {
    p <- p +
      geom_line(aes(y = .data[[tga_col]]), linewidth = 0.8,
                colour = palette_materials[["control"]]) +
      geom_line(aes(y = .data[[dtg_col]] * 100), linewidth = 0.6,
                linetype = "dashed", colour = palette_materials[["modified"]])
  }

  p + scale_y_continuous(
    name = "Mass (%)",
    sec.axis = sec_axis(~ . / 100, name = "DTG (%/°C)")
  ) +
    labs(x = "Temperature (°C)") +
    theme(axis.title.y.right = element_text(angle = 90))
}
```

---

## 5. Multi-Panel Composition

Use `patchwork` for multi-panel figures:

```r
library(patchwork)

# Standard 2x2
p1 + p2 + p3 + p4 +
  plot_layout(ncol = 2, nrow = 2, guides = "collect") +
  plot_annotation(tag_levels = "a", tag_prefix = "(", tag_suffix = ")") &
  theme(plot.tag = element_text(face = "bold", size = 14))

# Full-width header + 3 panels
p_header / (p1 | p2 | p3) +
  plot_layout(heights = c(1.2, 1)) +
  plot_annotation(tag_levels = "a")

# Sidebar legend
p_main + plot_spacer() +
  plot_layout(widths = c(4, 1))
```

### Panel label style

```r
# Add to each plot
p + labs(tag = "a") +
  theme(plot.tag = element_text(face = "bold", size = 14, hjust = 0))
```

---

## 6. Export

### SVG (primary)

```r
ggsave("figure.svg", plot = last_plot(), device = svglite::svglite,
       width = 8, height = 5, dpi = 300)
```

### PNG (raster preview)

```r
ggsave("figure.png", plot = last_plot(), device = ragg::agg_png,
       width = 8, height = 5, dpi = 300)
```

### TIFF (submission)

```r
ggsave("figure.tiff", plot = last_plot(), device = ragg::agg_tiff,
       width = 8, height = 5, dpi = 300, compression = "lzw")
```

### PDF (vector alternative)

```r
ggsave("figure.pdf", plot = last_plot(), device = cairo_pdf,
       width = 8, height = 5)
```

### Multi-panel export

```r
combined <- p1 + p2 + p3 + p4 +
  plot_layout(ncol = 2, guides = "collect") +
  plot_annotation(tag_levels = "a")

ggsave("figure_combined.svg", plot = combined, device = svglite::svglite,
       width = 12, height = 10, dpi = 300)
```

---

## 7. QA Checklist

After every R figure export:

- [ ] SVG opens in Illustrator/Inkscape with editable text.
- [ ] Font is Arial (or journal-safe sans-serif).
- [ ] No top/right spines (handled by `theme_materials()`).
- [ ] Legend has no frame.
- [ ] Panel labels (a, b, c) are bold, lowercase.
- [ ] Y-limits are tightened to data range.
- [ ] Colors are consistent across panels.
- [ ] Export at 300+ dpi for raster formats.
- [ ] `dev.off()` called after base R plots (not needed for ggplot2/ggsave).

# Materials Science Publication Theme for ggplot2
# Source this file at the top of every materials figure script.

theme_materials <- function(base_size = 12) {
  ggplot2::theme_minimal(base_size = base_size, base_family = "Arial") +
    ggplot2::theme(
      # Spines
      axis.line = ggplot2::element_line(linewidth = 0.6, colour = "#333333"),
      axis.line.x.top = ggplot2::element_blank(),
      axis.line.y.right = ggplot2::element_blank(),

      # Grid
      panel.grid.major = ggplot2::element_blank(),
      panel.grid.minor = ggplot2::element_blank(),

      # Text
      axis.title = ggplot2::element_text(size = base_size, colour = "#333333"),
      axis.text = ggplot2::element_text(size = base_size - 2, colour = "#333333"),
      plot.title = ggplot2::element_text(size = base_size + 2, face = "bold", hjust = 0),

      # Legend
      legend.position = "right",
      legend.key = ggplot2::element_blank(),
      legend.background = ggplot2::element_blank(),
      legend.text = ggplot2::element_text(size = base_size - 2),

      # Panel
      panel.background = ggplot2::element_blank(),
      plot.background = ggplot2::element_blank(),
      strip.text = ggplot2::element_text(size = base_size - 1, face = "bold"),

      # Panel labels (a, b, c)
      plot.tag = ggplot2::element_text(face = "bold", size = 14, hjust = 0)
    )
}

# Materials Science Color Palettes
# Source this file at the top of every materials figure script.

# Semantic palette
palette_materials <- c(
  control    = "#4B6F8A",
  modified   = "#C47B45",
  optimal    = "#4F7C6A",
  mechanism  = "#8B6F47",
  comparison = "#8C8C8C",
  danger     = "#B85450",
  accent     = "#D4A574"
)

# Single-hue gradient (related variants)
palette_single_hue <- c(
  "#B4C0E4",  # light
  "#7884B4",  # medium
  "#484878",  # dark
  "#2C2C58"   # darkest
)

# Asphalt / pavement
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

# Cement / concrete
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

# Polymer / composites
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

# Ceramics / structural
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

# NMI pastel (editorial multi-panel)
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

# Helper: get palette by domain name
get_domain_palette <- function(domain = "materials") {
  palettes <- list(
    materials = palette_materials,
    asphalt = palette_asphalt,
    cement = palette_cement,
    polymer = palette_polymer,
    ceramic = palette_ceramic,
    nmi = palette_nmi_pastel
  )
  palettes[[domain]] %||% palette_materials
}

# Null-coalescing operator
`%||%` <- function(a, b) if (!is.null(a)) a else b

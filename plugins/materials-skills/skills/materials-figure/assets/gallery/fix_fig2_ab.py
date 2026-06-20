"""Regenerate fig2 with realistic EBSD IPF-ND and grain boundary panels.
Pure numpy/matplotlib - no scipy dependency."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.size': 10,
    'axes.linewidth': 1.0,
    'axes.spines.right': False,
    'axes.spines.top': False,
    'xtick.major.width': 0.8,
    'ytick.major.width': 0.8,
    'xtick.major.size': 4,
    'ytick.major.size': 4,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

PALETTE = {
    'blue': '#4477AA',
    'cyan': '#66CCEE',
    'purple': '#AA3377',
    'red': '#CC3311',
    'orange': '#EE7733',
    'green': '#228833',
    'gray': '#BBBBBB',
    'dark': '#332288',
}

np.random.seed(42)

# ── Panel (a): EBSD IPF-ND map ─
# Use a grid-based approach with random grain seeds
def generate_ebsd_ipf(size=300, n_grains=80):
    """Generate realistic EBSD IPF-ND colored map."""
    # Generate grain seeds
    seeds_x = np.random.uniform(0, size, n_grains)
    seeds_y = np.random.uniform(0, size, n_grains)
    
    # Assign random IPF colors (RGB)
    # IPF-ND: red=<001>, green=<101>, blue=<111>
    colors = np.random.random((n_grains, 3))
    colors = colors / colors.sum(axis=1, keepdims=True)  # normalize
    
    # Create pixel grid - use vectorized distance calculation
    yy, xx = np.mgrid[0:size, 0:size]
    
    # For efficiency, use a coarser grid then upscale
    coarse = 3  # 3x3 blocks
    size_coarse = size // coarse
    yy_c, xx_c = np.mgrid[0:size_coarse, 0:size_coarse]
    
    # Calculate distances to all seeds (vectorized)
    grain_map = np.zeros((size_coarse, size_coarse), dtype=int)
    
    for i in range(n_grains):
        dist = (xx_c - seeds_x[i]/coarse)**2 + (yy_c - seeds_y[i]/coarse)**2
        mask = (grain_map == 0) | (dist < np.array([(xx_c - seeds_x[grain_map]/coarse)**2 + 
                    (yy_c - seeds_y[grain_map]/coarse)**2][0]))
        # Simpler: just find minimum distance
        pass
    
    # Even simpler: use broadcasting
    seeds_x_c = seeds_x / coarse
    seeds_y_c = seeds_y / coarse
    
    # Reshape for broadcasting: seeds (n, 1, 1, 2), pixels (1, h, w, 2)
    seeds_arr = np.stack([seeds_x_c, seeds_y_c], axis=1)  # (n, 2)
    pixels_arr = np.stack([xx_c.ravel(), yy_c.ravel()], axis=1)  # (h*w, 2)
    
    # Calculate all distances: (n, h*w)
    dists = np.sqrt(((seeds_arr[:, np.newaxis, :] - pixels_arr[np.newaxis, :, :])**2).sum(axis=2))
    grain_indices = np.argmin(dists, axis=0).reshape(size_coarse, size_coarse)
    
    # Build color map
    color_map = colors[grain_indices]
    
    # Upscale to full size
    from numpy import repeat
    color_map_full = repeat(repeat(color_map, coarse, axis=0), coarse, axis=1)
    # Crop to exact size
    color_map_full = color_map_full[:size, :size]
    
    # Add realistic EBSD noise
    noise = np.random.normal(0, 0.06, color_map_full.shape)
    # Smooth noise
    from numpy.lib.stride_tricks import as_strided
    # Simple box blur for noise
    kernel_size = 3
    noise_smooth = np.zeros_like(noise)
    for c in range(3):
        noise_c = noise[:, :, c]
        # Simple 3x3 average
        padded = np.pad(noise_c, 1, mode='edge')
        for i in range(3):
            for j in range(3):
                noise_smooth[:, :, c] += padded[i:i+size, j:j+size]
        noise_smooth[:, :, c] /= 9
    
    color_map_full = np.clip(color_map_full + noise_smooth * 0.5, 0, 1)
    
    # Add unindexed pixels (~2%)
    unindexed = np.random.random((size, size)) < 0.02
    color_map_full[unindexed] = 0.05
    
    return color_map_full

print("Generating EBSD IPF-ND map...")
ebsd_map = generate_ebsd_ipf(size=300, n_grains=80)

# ── Panel (b): Grain boundary network ──
def draw_grain_boundaries(ax, size=300, n_grains=40, seed=42):
    """Draw realistic grain boundary network using random polygons."""
    np.random.seed(seed)
    
    # Generate grain centers
    centers = []
    for _ in range(n_grains):
        cx = np.random.uniform(30, size-30)
        cy = np.random.uniform(30, size-30)
        centers.append((cx, cy))
    
    # Assign colors
    colors_list = plt.cm.Pastel1(np.linspace(0, 1, n_grains))
    
    # Draw grains as irregular polygons
    for i, (cx, cy) in enumerate(centers):
        n_vertices = np.random.randint(5, 10)
        angles = np.sort(np.random.uniform(0, 2*np.pi, n_vertices))
        base_r = np.random.uniform(20, 50)
        radii = base_r * (1 + 0.3 * np.random.randn(n_vertices))
        radii = np.clip(radii, base_r * 0.5, base_r * 1.5)
        
        verts_x = cx + radii * np.cos(angles)
        verts_y = cy + radii * np.sin(angles)
        
        # Clip to bounds
        verts_x = np.clip(verts_x, 0, size)
        verts_y = np.clip(verts_y, 0, size)
        
        polygon = plt.Polygon(list(zip(verts_x, verts_y)), 
                             facecolor=colors_list[i % len(colors_list)], 
                             edgecolor='none', alpha=0.5)
        ax.add_patch(polygon)
        
        # Draw edges
        for j in range(n_vertices):
            x1, y1 = verts_x[j], verts_y[j]
            x2, y2 = verts_x[(j+1) % n_vertices], verts_y[(j+1) % n_vertices]
            ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1.5, alpha=0.7)
    
    ax.set_xlim(0, size)
    ax.set_ylim(0, size)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])

# ── Create full fig2 ──
print("Creating full fig2...")
fig = plt.figure(figsize=(18, 24))
gs = gridspec.GridSpec(4, 2, height_ratios=[1.2, 1.2, 1, 1], hspace=0.35, wspace=0.3)

# Panel (a): EBSD IPF-ND
ax_a = fig.add_subplot(gs[0, 0])
ax_a.imshow(ebsd_map, interpolation='nearest')
ax_a.set_title('(a) EBSD IPF-ND', fontsize=10, pad=8)
ax_a.set_xticks([])
ax_a.set_yticks([])

# Panel (b): Grain boundary network
ax_b = fig.add_subplot(gs[0, 1])
draw_grain_boundaries(ax_b, size=300, n_grains=40, seed=42)
ax_b.set_title('(b) Grain boundary network', fontsize=10, pad=8)

# Panel (c): {100} Pole figure
ax_c = fig.add_subplot(gs[1, 0], projection='polar')
np.random.seed(100)
n_points = 80
theta = np.random.uniform(0, 2*np.pi, n_points)
r = np.random.rayleigh(0.3, n_points)
r = np.clip(r, 0, 0.75)
ax_c.scatter(theta, r, c=PALETTE['red'], s=15, alpha=0.7, edgecolors='none')
ax_c.set_title('(c) {100} Pole figure', fontsize=10, pad=8, y=1.05)
ax_c.set_rticks([0.25, 0.50, 0.75])
ax_c.set_rlabel_position(0)
ax_c.grid(True, alpha=0.3)

# Panel (d): Stress-strain curves
ax_d = fig.add_subplot(gs[1, 1])
strain = np.linspace(0, 0.3, 200)
for label, color, sigma_y, sigma_uts in [
    ('Sample A', PALETTE['blue'], 450, 520),
    ('Sample B', PALETTE['red'], 500, 560),
    ('Sample C', PALETTE['green'], 420, 620),
]:
    elastic = strain * 200000
    yield_strain = sigma_y / 200000
    stress = np.where(
        strain < yield_strain,
        elastic,
        sigma_y + (sigma_uts - sigma_y) * np.sin(np.pi/2 * np.clip((strain - yield_strain) / 0.15, 0, 1))
    )
    uts_strain = yield_strain + 0.15
    stress = np.where(strain > uts_strain, sigma_uts * np.exp(-2 * (strain - uts_strain)), stress)
    stress = np.clip(stress, 0, None)
    ax_d.plot(strain, stress, color=color, linewidth=1.5, label=label)

ax_d.set_xlabel('Strain', fontsize=9)
ax_d.set_ylabel('Stress (MPa)', fontsize=9)
ax_d.legend(fontsize=8, loc='lower right')
ax_d.set_title('(d) Stress-strain curves', fontsize=10, pad=8)
ax_d.set_ylim(0, 700)

# Panel (e): Work hardening rate
ax_e = fig.add_subplot(gs[2, 0])
true_strain = np.linspace(0.01, 0.2, 200)
for label, color, K, n_val in [
    ('Sample A', PALETTE['blue'], 1500, 0.15),
    ('Sample B', PALETTE['red'], 1400, 0.18),
    ('Sample C', PALETTE['green'], 1300, 0.20),
]:
    whr = n_val * K * true_strain ** (n_val - 1)
    ax_e.plot(true_strain, whr, color=color, linewidth=1.5, label=label)

ax_e.set_xlabel('True strain', fontsize=9)
ax_e.set_ylabel('Work hardening rate (MPa)', fontsize=9)
ax_e.legend(fontsize=8, loc='upper right')
ax_e.set_title('(e) Work hardening rate', fontsize=10, pad=8)

# Panel (f): Strength-elongation Ashby map
ax_f = fig.add_subplot(gs[2, 1])
materials = [
    ('Al alloy', 200, 20, PALETTE['orange']),
    ('Steel A', 520, 25, PALETTE['blue']),
    ('Steel B', 650, 18, PALETTE['red']),
    ('Steel C', 800, 12, PALETTE['green']),
    ('Ti alloy', 900, 10, PALETTE['purple']),
]
for name, ys, ue, color in materials:
    ax_f.scatter(ys, ue, c=color, s=80, zorder=5, edgecolors='black', linewidth=0.5)
    ax_f.annotate(name, (ys, ue), textcoords="offset points", xytext=(5, 5), fontsize=8)

ax_f.set_xlabel('Yield strength (MPa)', fontsize=9)
ax_f.set_ylabel('Uniform elongation (%)', fontsize=9)
ax_f.set_title('(f) Strength-ductility map', fontsize=10, pad=8)

# Panel (g): Fracture surface (dimple rupture)
ax_g = fig.add_subplot(gs[3, :])
np.random.seed(77)
n_dimples = 200
for _ in range(n_dimples):
    cx = np.random.uniform(0, 18)
    cy = np.random.uniform(0, 4)
    r = np.random.exponential(0.3) + 0.1
    r = min(r, 0.8)
    
    theta_ring = np.linspace(0, 2*np.pi, 30)
    x_ring = cx + r * np.cos(theta_ring)
    y_ring = cy + r * np.sin(theta_ring) * 0.6
    
    for frac in np.linspace(1, 0.3, 5):
        alpha = 0.15 * (1 - frac)
        circle = plt.Circle((cx, cy), r * frac * 0.9, 
                           facecolor='gray', alpha=alpha, edgecolor='none')
        ax_g.add_patch(circle)
    
    ax_g.plot(x_ring, y_ring, 'k-', linewidth=0.5, alpha=0.3)

ax_g.set_xlim(0, 18)
ax_g.set_ylim(0, 4)
ax_g.set_aspect('equal')
ax_g.set_xticks([])
ax_g.set_yticks([])
ax_g.set_title('(g) Fracture surface (dimple rupture)', fontsize=10, pad=8)

plt.savefig(r'c:\Users\97218\Desktop\civil-materials-skills-release\plugins\materials-skills\skills\materials-figure\assets\gallery\fig2-steel-microstructure-property.png', 
            dpi=300, bbox_inches='tight')
plt.close()
print("Saved fig2-steel-microstructure-property.png")

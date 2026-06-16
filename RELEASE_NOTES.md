# Materials Science Skills v1.0.0

**A research companion built by a materials researcher, for materials researchers.**

---

## What is this?

Eleven Codex skills that walk with you through the entire journey of a materials research paper -- from picking a topic all the way to responding to Reviewer 2's third round of comments. Everything here was shaped by real peer-review experience in asphalt emulsions, waterborne epoxy systems, and cementitious composites.

This is not a generic academic writing tool. It knows that "significantly improved" needs a p-value, that FTIR alone cannot prove a mechanism, and that your GB/T test results need an ASTM translation before an editor at CBM will take them seriously.

---

## What's inside

| Skill | What it does |
|---|---|
| **materials-research** | The router. Detects your task, material domain, and target journal, then loads only what you need. Start here. |
| **materials-reader** | Turns a paper into structured evidence-chain notes, not shallow summaries. Flags claims that outrun the data. |
| **materials-citation** | Builds claim-citation matrices, runs multi-source academic search (Crossref + PubMed + OpenAlex + Semantic Scholar), audits reference gaps. |
| **materials-writing** | Drafts manuscript sections from claims, results, or Chinese notes. Claim first, evidence second, boundary always visible. |
| **materials-polishing** | Polishes English prose without inflating weak evidence. Includes a claim-strength ladder that downgrades "proves" to "suggests" when the data only supports trends. |
| **materials-response** | Structures reviewer response packages. 12 high-frequency reviewer comment patterns with ready-to-adapt templates. |
| **materials-reviewer** | Simulates two independent peer reviewers plus a cross-review synthesis. Use before you submit, not after you get rejected. |
| **materials-figure** | Plans figures, enforces DPI/format/width specs per journal, includes 5 matplotlib production scripts for bonding strength bars, FTIR overlays, dosage-performance curves, durability retention, and multi-property radar charts. |
| **materials-paper2ppt** | Converts papers into Chinese slide decks for group meetings, journal clubs, and thesis reports. |
| **materials-pptx** | Generates real `.pptx` files from structured outlines -- with speaker notes, figure embedding, and crop settings. |
| **materials-data** | Builds FAIR dataset packages with metadata, audit reports, and data availability statements. Scaffolds everything so you can fill in real values. |

---

## Highlights of this release

### Academic search now covers four sources

The citation skill's MCP server connects to **Crossref**, **PubMed**, **OpenAlex**, and **Semantic Scholar** -- all queried in parallel, results merged with confidence scoring and deduplication. New: a `lookup_mesh` tool that finds standardized MeSH terms for your topic (handy for cross-disciplinary searches).

### Five matplotlib scripts you can actually run

A new `materials_plot_lib.py` provides publication-ready helper functions (`make_grouped_bar`, `make_ftir_overlay`, `make_xrd_pattern`, `make_radar`, etc.) with journal-specific color palettes (CBM, CCC). Five complete example scripts under `scripts/figures4materials/`:

- **Bonding strength comparison** -- grouped bar chart, dry vs. moisture-conditioned, with error bars
- **FTIR curing evidence** -- overlaid spectra with peak annotations at 915, 1240, 1730 cm-1
- **Dosage-performance curve** -- trend line with optimum identification
- **Durability retention** -- multi-condition retention ratio comparison
- **Mechanical property radar** -- normalized multi-index radar chart with constructability trade-off

Each script reads from CSV data and exports SVG + PNG at 300 DPI.

### A reviewer simulator you didn't know you needed

`materials-reviewer` generates exactly two independent review reports (different lenses: Reviewer A checks novelty and journal fit; Reviewer B checks mechanism evidence and statistics) plus a cross-review synthesis. Scoring across six axes: innovation, methodology, evidence completeness, writing, figures, journal fit. Use it to find the holes in your manuscript before a real reviewer does.

### Statistical methods guidance

A new reference file covering: which test to use when (decision tree), how to handle n=3 samples (Shapiro-Wilk has no power at n=3 -- just show the data), how to write ANOVA + Tukey HSD results in a manuscript paragraph, and a Kruskal-Wallis + Dunn template for non-normal data.

### GB/T to ASTM/EN standard mapping

Your lab runs GB/T 50081. The journal wants ASTM C39. The cube-vs-cylinder difference is 15-25%. Now you have a lookup table with the mapping, the key difference to report, and a ready-to-paste manuscript sentence.

### Twelve reviewer response patterns

From "English needs major revision" to "the novelty claim is not justified" to "Reviewer 1 and Reviewer 2 contradict each other" -- each pattern includes a strategy, a diplomatic template, and guidance on what to do when you genuinely cannot run the experiment the reviewer asked for.

### Figure production specs

Elsevier wants 300 DPI TIFF at 85 mm single-column width. Taylor & Francis wants EPS at 82 mm. ASCE wants 7.2 inches. Now you have a table per publisher, a caption formula with a worked example, and a pre-submission export checklist.

### And everything else

- 4 data schemas with field types, allowed values, typical ranges, and sanity checks
- Characterization guide with FTIR peak assignments, SEM parameters, XRD settings, and copy-paste methods paragraphs
- Microstructure interpretation guide (what sea-island vs. co-continuous morphology looks like and how to describe it)
- Sustainability claims decision tree (can you do LCA? then simplified screening then safe wording)
- 12-month thesis timeline with weekly rhythm and a one-semester rescue plan
- 213 reference and documentation files, 52 Python scripts, 15 test files, 12 CSV templates, and a release check script that scans for leaked local paths and API keys

---

## Installation

```powershell
# Copy skills into your Codex skills directory
Copy-Item -Recurse .\skills\materials-* "$env:CODEX_HOME\skills\"

# Install root dependencies for figure/data workflows
pip install -r requirements.txt

# Install the local academic-search MCP dependencies when using the repo MCP server
pip install -r .\mcp-server\materials-academic-search\requirements.txt
```

Optional: configure the academic-search MCP server in your Codex config:

```toml
[mcp_servers."materials-academic-search"]
command = "python"
args = ["server.py"]
cwd = "mcp-server/materials-academic-search"

# Optional environment variables
# OPENALEX_API_KEY=...
# SEMANTIC_SCHOLAR_API_KEY=...
# NCBI_API_KEY=...           # speeds up PubMed from 3 to 10 requests/sec
# CIVIL_MATERIALS_CONTACT_EMAIL=your@email.com
```

---

## What this is not

This skill bundle helps structure your research work. It does not replace deep reading, experimental evidence, supervisor judgment, official journal instructions, or the ethical requirements of your institution. The claim-strength ladder will tell you to write "suggests" instead of "proves" -- but only you can run the experiment that makes the claim true.

---

## Acknowledgments

Architectural patterns inspired by [nature-skills](https://github.com/Yuan1z0825/nature-skills) by Yizhe Yuan.

---

**Full changelog:** See `REVIEW_REPORT.md` and `UPGRADE_REVIEW.md` for the complete audit trail from initial code review through three rounds of iteration.

# Civil Materials Skills

Civil Materials Skills is a Codex skill bundle for civil engineering and construction-materials research. It is adapted for asphalt pavement materials, waterborne epoxy modified emulsified asphalt, cement/concrete, durability, sustainability, journal targeting, literature work, manuscript writing, figures, PPTX, data/FAIR packaging, and reviewer responses.

## Included Skills

| Skill | Purpose |
|---|---|
| `civil-materials-research` | Research router, topic positioning, manuscript strategy, journal fit, pressure tests, example library |
| `civil-materials-reader` | Evidence-chain reading, paper notes, claim-evidence-mechanism-boundary audits |
| `civil-materials-citation` | Literature search planning, citation matrices, reference gap audits, academic-search MCP |
| `civil-materials-polishing` | English polishing, Chinese-to-English academic rewriting, claim-strength control |
| `civil-materials-response` | Reviewer response packages and point-by-point rebuttal drafting |
| `civil-materials-paper2ppt` | Paper-to-PPT outlines and slide-ready Markdown |
| `civil-materials-pptx` | Real `.pptx` generation from structured outlines |
| `civil-materials-figure` | Figure planning, gallery examples, SVG demos, caption boundaries |
| `civil-materials-data` | Dataset packages, metadata, FAIR audits, data availability statements |

## Install

Copy the skill folders into your Codex skills directory:

```powershell
Copy-Item -Recurse .\skills\civil-materials-* "$env:CODEX_HOME\skills\"
```

If `CODEX_HOME` is not set, use your Codex home directory, commonly `~/.codex`.

## Optional Academic Search MCP

The citation skill includes a local academic-search MCP server.

Example Codex config:

```toml
[mcp_servers."civil-materials-academic-search"]
command = "python"
args = ["$CODEX_HOME/skills/civil-materials-citation/mcp/academic_search/server.py"]
```

Optional environment variables:

- `OPENALEX_API_KEY`
- `SEMANTIC_SCHOLAR_API_KEY`
- `CIVIL_MATERIALS_CONTACT_EMAIL`

No secrets or local Codex config files are included in this repository.

## Verify

Run the release check script:

```powershell
python .\scripts\run_release_checks.py
```

The script checks core tests, pressure-test coverage, generated-artifact cleanup, and accidental local-path or secret leakage.

## Scope

This bundle helps structure research work. It does not replace deep reading, experimental evidence, supervisor/co-author judgment, official journal instructions, or ethical/institutional requirements.

## License

MIT License. See [LICENSE](LICENSE).

# Materials Science Academic Search MCP Server

Python stdio JSON-RPC MCP server for civil engineering and construction-materials literature search.

## Tools

| Tool | Description |
|---|---|
| `list_academic_sources` | List enabled and disabled academic metadata sources. |
| `search_civil_materials` | Search for papers with journal family and material domain filters. |
| `fetch_paper_metadata` | Resolve DOI/title to full metadata. |
| `resolve_paper_ids` | Normalize DOI, PMID, PMCID, arXiv, OpenAlex, Semantic Scholar, Scopus EID, and PII identifiers. |
| `suggest_search_queries` | Generate journal-aware Boolean search queries. |
| `lookup_mesh` | Look up PubMed MeSH terms for materials topics. |
| `convert_citation_records` | Convert RIS, BibTeX, NBIB, or CSV records. |
| `deduplicate_citation_records` | Deduplicate citation records by DOI, IDs, title, and year. |
| `build_claim_source_map` | Map manuscript claims to evidence sources. |
| `audit_reference_gaps` | Flag missing evidence types. |
| `export_citation_matrix` | Export rows compatible with the citation matrix template. |
| `get_formatted_citation` | Generate formatted citations and export records. |

## Sources

- **CrossRef** - open metadata.
- **PubMed / MeSH** - biomedical and chemistry-adjacent records.
- **arXiv** - open e-prints.
- **OpenAlex** - open scholarly index.
- **Semantic Scholar** - academic metadata with optional API key for higher rate limits.
- **Scopus** - Elsevier abstract database with optional API key.
- **ScienceDirect** - Elsevier platform with optional API key.

## Quick Start

The `.mcp.json` at the repository root registers this server with Codex.

Install the local MCP dependencies:

```powershell
python -m pip install -r .\mcp-server\materials-academic-search\requirements.txt
```

Run the server manually:

```powershell
python server.py
```

Then send JSON-RPC messages over stdin:

```json
{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"test","version":"0.1.0"}}}
{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}
```

## Tests

```powershell
python -m unittest discover -s academic_search/tests -p "test_*.py" -v
```

## Environment Variables

- `OPENALEX_API_KEY` - enables OpenAlex searches.
- `SEMANTIC_SCHOLAR_API_KEY` - higher rate limits for Semantic Scholar.
- `CIVIL_MATERIALS_CONTACT_EMAIL` - polite Crossref and PubMed requests.
- `NCBI_API_KEY` - higher PubMed E-utilities rate limits.

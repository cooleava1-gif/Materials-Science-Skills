# Materials Science Academic-Search MCP

Local stdio MCP server for materials science and engineering literature search.

## Run Tests

```powershell
python -m unittest discover -s "$CODEX_HOME/skills/materials-citation/mcp/academic_search/tests" -p "test_*.py" -v
```

## Smoke Test

```powershell
'{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python "$CODEX_HOME/skills/materials-citation/mcp/academic_search/server.py"
```

## Optional Environment Variables

- `OPENALEX_API_KEY`: enables OpenAlex searches.
- `SEMANTIC_SCHOLAR_API_KEY`: increases Semantic Scholar rate limits.
- `CIVIL_MATERIALS_CONTACT_EMAIL`: enables polite Crossref and PubMed E-utilities requests.
- `NCBI_API_KEY`: optional PubMed E-utilities key for higher rate limits.

## PubMed and MeSH

PubMed search is included as a candidate-source adapter for biomedical, chemistry-adjacent, sustainability, and materials papers that are indexed by NCBI. Returned records are still candidates, not validated evidence.

Use `lookup_mesh` to check standardized MeSH terms for topics such as `epoxy resin`, `emulsion`, `cement hydration`, or other chemistry/materials terms before building a search strategy.

## Core Rule

Treat returned papers as candidates. Use `materials-reader` for deep reading before making novelty, mechanism, or durability claims.

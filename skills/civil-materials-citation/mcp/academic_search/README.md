# Civil Materials Academic-Search MCP

Local stdio MCP server for civil engineering and construction-materials literature search.

## Run Tests

```powershell
python -m unittest discover -s "$CODEX_HOME/skills/civil-materials-citation/mcp/academic_search/tests" -p "test_*.py" -v
```

## Smoke Test

```powershell
'{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}' | python "$CODEX_HOME/skills/civil-materials-citation/mcp/academic_search/server.py"
```

## Optional Environment Variables

- `OPENALEX_API_KEY`: enables OpenAlex searches.
- `SEMANTIC_SCHOLAR_API_KEY`: increases Semantic Scholar rate limits.
- `CIVIL_MATERIALS_CONTACT_EMAIL`: enables polite Crossref requests.

## Core Rule

Treat returned papers as candidates. Use `civil-materials-reader` for deep reading before making novelty, mechanism, or durability claims.

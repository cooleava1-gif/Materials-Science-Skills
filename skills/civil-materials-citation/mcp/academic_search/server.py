"""Minimal stdio MCP server for civil-materials academic search."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from academic_search.service import AcademicSearchService
else:
    from .service import AcademicSearchService


SERVER_NAME = "civil-materials-academic-search"
PROTOCOL_VERSION = "2025-06-18"


TOOL_DEFINITIONS: list[dict[str, Any]] = [
    {
        "name": "search_civil_materials",
        "description": "Search scholarly sources for civil engineering and construction-materials papers with journal and evidence-layer filters.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string"},
                "journal_family": {"oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]},
                "material_domain": {"type": "string", "default": "asphalt"},
                "evidence_layer": {"type": "string"},
                "year_range": {"type": "string", "description": "Example: 2020-2026"},
                "limit": {"type": "integer", "default": 10},
            },
            "required": ["topic"],
        },
    },
    {
        "name": "fetch_paper_metadata",
        "description": "Resolve DOI, title, year, journal, author, abstract, and source metadata for one paper.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "doi": {"type": "string"},
                "title": {"type": "string"},
                "external_id": {"type": "string"},
                "openalex_id": {"type": "string"},
                "semantic_scholar_id": {"type": "string"},
            },
        },
    },
    {
        "name": "suggest_search_queries",
        "description": "Generate CBM/CCC/JBE/RMPD/IJPE/JRE/CSCM-aware Boolean search queries.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string"},
                "journal_family": {"oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]},
                "material_domain": {"type": "string", "default": "asphalt"},
                "evidence_layer": {"type": "string"},
                "year_range": {"type": "string"},
                "limit": {"type": "integer", "default": 6},
            },
            "required": ["topic"],
        },
    },
    {
        "name": "build_claim_source_map",
        "description": "Map manuscript claims to evidence type, search query, candidate sources, and reviewer risk.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string"},
                "claims": {"type": "array", "items": {"type": "string"}},
                "text": {"type": "string"},
                "candidate_records": {"type": "array", "items": {"type": "object"}},
                "journal_family": {"oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]},
                "material_domain": {"type": "string", "default": "asphalt"},
                "year_range": {"type": "string"},
            },
        },
    },
    {
        "name": "audit_reference_gaps",
        "description": "Flag missing mechanism, performance, durability, and reviewer-safe source evidence.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "claims": {"type": "array", "items": {"type": "string"}},
                "text": {"type": "string"},
                "claim_source_map": {"type": "array", "items": {"type": "object"}},
                "candidate_records": {"type": "array", "items": {"type": "object"}},
            },
        },
    },
    {
        "name": "export_citation_matrix",
        "description": "Export rows compatible with the civil-materials citation matrix template.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string"},
                "claims": {"type": "array", "items": {"type": "string"}},
                "target_journals": {"oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]},
                "journal_family": {"oneOf": [{"type": "string"}, {"type": "array", "items": {"type": "string"}}]},
                "material_domain": {"type": "string", "default": "asphalt"},
                "year_range": {"type": "string"},
                "manuscript_location": {"type": "string"},
            },
        },
    },
]


def handle_message(message: dict[str, Any], *, service: AcademicSearchService | None = None) -> dict[str, Any] | None:
    """Handle one JSON-RPC message."""

    request_id = message.get("id")
    method = message.get("method")
    if request_id is None and method and method.startswith("notifications/"):
        return None
    service = service or AcademicSearchService()

    try:
        if method == "initialize":
            return _result(
                request_id,
                {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {"tools": {}},
                    "serverInfo": {"name": SERVER_NAME, "version": "0.1.0"},
                },
            )
        if method == "tools/list":
            return _result(request_id, {"tools": TOOL_DEFINITIONS})
        if method == "tools/call":
            params = message.get("params") or {}
            payload = _call_tool(service, params.get("name"), params.get("arguments") or {})
            return _result(
                request_id,
                {
                    "content": [{"type": "text", "text": json.dumps(payload, ensure_ascii=False, indent=2)}],
                    "structuredContent": payload,
                },
            )
        return _error(request_id, -32601, f"Unknown method: {method}")
    except MethodNotFound as exc:
        return _error(request_id, -32601, str(exc))
    except ValueError as exc:
        return _error(request_id, -32602, str(exc))
    except Exception as exc:  # MCP clients should get a machine-readable failure.
        return _error(request_id, -32603, str(exc))


def _call_tool(service: AcademicSearchService, name: str | None, args: dict[str, Any]) -> dict[str, Any]:
    if name == "search_civil_materials":
        return service.search_civil_materials(args)
    if name == "fetch_paper_metadata":
        return service.fetch_paper_metadata(args)
    if name == "suggest_search_queries":
        return service.suggest_search_queries(args)
    if name == "build_claim_source_map":
        return service.build_claim_source_map(args)
    if name == "audit_reference_gaps":
        return service.audit_reference_gaps(args)
    if name == "export_citation_matrix":
        return service.export_citation_matrix(args)
    raise MethodNotFound(f"Unknown tool: {name}")


class MethodNotFound(ValueError):
    pass


def _result(request_id: Any, result: dict[str, Any]) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "result": result}


def _error(request_id: Any, code: int, message: str) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": request_id, "error": {"code": code, "message": message}}


def main() -> int:
    service = AcademicSearchService()
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            message = json.loads(line)
            response = handle_message(message, service=service)
        except json.JSONDecodeError as exc:
            response = _error(None, -32700, f"Parse error: {exc}")
        if response is not None:
            print(json.dumps(response, ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

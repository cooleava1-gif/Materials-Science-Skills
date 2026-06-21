#!/usr/bin/env python3
"""Compatibility entrypoint for packaged MCP cwd resolution tests."""

from __future__ import annotations

import runpy
from pathlib import Path


REAL_SERVER = (
    Path(__file__).resolve().parents[6]
    / "skills"
    / "materials-citation"
    / "mcp"
    / "academic_search"
    / "server.py"
)

runpy.run_path(str(REAL_SERVER), run_name="__main__")

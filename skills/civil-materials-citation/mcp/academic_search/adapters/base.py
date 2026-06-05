"""Shared helpers for academic source adapters."""

from __future__ import annotations

import re
from typing import Any


class AdapterError(RuntimeError):
    """Raised when an upstream academic source fails unexpectedly."""


class AdapterDisabled(RuntimeError):
    """Raised when an optional upstream source is intentionally skipped."""


def normalize_doi(value: str | None) -> str:
    if not value:
        return ""
    doi = value.strip()
    doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", doi, flags=re.IGNORECASE)
    doi = re.sub(r"^doi:\s*", "", doi, flags=re.IGNORECASE)
    return doi.strip().lower()


def normalize_title(value: str | None) -> str:
    if not value:
        return ""
    text = re.sub(r"<[^>]+>", " ", value)
    text = re.sub(r"[^a-zA-Z0-9]+", " ", text.lower())
    return " ".join(text.split())


def first_value(value: Any) -> Any:
    if isinstance(value, list):
        return value[0] if value else None
    return value


def clean_abstract(value: str | None) -> str:
    if not value:
        return ""
    text = re.sub(r"<[^>]+>", " ", value)
    return " ".join(text.split())

"""Academic source adapters."""

from .base import AcademicSourceAdapter, AdapterDisabled, AdapterError, normalize_doi, normalize_title
from .crossref import CrossrefAdapter
from .openalex import OpenAlexAdapter
from .semantic_scholar import SemanticScholarAdapter

__all__ = [
    "AdapterDisabled",
    "AdapterError",
    "AcademicSourceAdapter",
    "CrossrefAdapter",
    "OpenAlexAdapter",
    "SemanticScholarAdapter",
    "normalize_doi",
    "normalize_title",
]

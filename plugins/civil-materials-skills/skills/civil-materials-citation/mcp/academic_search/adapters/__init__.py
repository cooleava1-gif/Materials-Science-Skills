"""Academic source adapters."""

from .base import AcademicSourceAdapter, AdapterDisabled, AdapterError, normalize_doi, normalize_title
from .crossref import CrossrefAdapter
from .openalex import OpenAlexAdapter
from .pubmed import PubMedAdapter
from .semantic_scholar import SemanticScholarAdapter

__all__ = [
    "AdapterDisabled",
    "AdapterError",
    "AcademicSourceAdapter",
    "CrossrefAdapter",
    "OpenAlexAdapter",
    "PubMedAdapter",
    "SemanticScholarAdapter",
    "normalize_doi",
    "normalize_title",
]

"""Shared helpers for academic source adapters."""

from __future__ import annotations

import re
import time
from collections.abc import Callable
from typing import Any, Protocol

import httpx


class AdapterError(RuntimeError):
    """Raised when an upstream academic source fails unexpectedly."""


class AdapterDisabled(RuntimeError):
    """Raised when an optional upstream source is intentionally skipped."""


class AcademicSourceAdapter(Protocol):
    """Contract for academic metadata/search providers."""

    name: str

    def search(
        self,
        query: str,
        *,
        journals: Any = None,
        year_range: str | None = None,
        limit: int = 10,
    ) -> list[dict[str, Any]]:
        ...

    def fetch(
        self,
        *,
        doi: str | None = None,
        title: str | None = None,
        external_id: str | None = None,
    ) -> dict[str, Any] | None:
        ...


RETRY_STATUS_CODES = {408, 429, 500, 502, 503, 504}
DEFAULT_BACKOFF_SECONDS = (1.0, 2.0, 4.0)


def get_response_with_retries(
    url: str,
    *,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 20.0,
    max_attempts: int = 3,
    backoff_seconds: tuple[float, ...] = DEFAULT_BACKOFF_SECONDS,
    client_factory: Callable[..., Any] = httpx.Client,
    sleep: Callable[[float], None] = time.sleep,
) -> Any:
    """GET a URL with bounded retry/backoff for transient upstream failures."""

    attempts = max(1, max_attempts)
    for attempt in range(attempts):
        try:
            client_kwargs: dict[str, Any] = {"timeout": timeout}
            if headers is not None:
                client_kwargs["headers"] = headers
            with client_factory(**client_kwargs) as client:
                response = client.get(url, params=params)
            if response.status_code in RETRY_STATUS_CODES and attempt < attempts - 1:
                sleep(_backoff_for_attempt(attempt, backoff_seconds))
                continue
            return response
        except httpx.HTTPError as exc:
            if _is_retryable_http_error(exc) and attempt < attempts - 1:
                sleep(_backoff_for_attempt(attempt, backoff_seconds))
                continue
            raise
    raise AdapterError("retry loop exited unexpectedly")


def get_json_with_retries(
    url: str,
    *,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 20.0,
    max_attempts: int = 3,
    backoff_seconds: tuple[float, ...] = DEFAULT_BACKOFF_SECONDS,
    client_factory: Callable[..., Any] = httpx.Client,
    sleep: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    response = get_response_with_retries(
        url,
        params=params,
        headers=headers,
        timeout=timeout,
        max_attempts=max_attempts,
        backoff_seconds=backoff_seconds,
        client_factory=client_factory,
        sleep=sleep,
    )
    response.raise_for_status()
    return response.json()


def _backoff_for_attempt(attempt: int, backoff_seconds: tuple[float, ...]) -> float:
    if attempt < len(backoff_seconds):
        return backoff_seconds[attempt]
    return backoff_seconds[-1] if backoff_seconds else 0.0


def _is_retryable_http_error(exc: httpx.HTTPError) -> bool:
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in RETRY_STATUS_CODES
    return isinstance(exc, (httpx.TimeoutException, httpx.NetworkError, httpx.TransportError))


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

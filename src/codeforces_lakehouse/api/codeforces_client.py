"""
Codeforces API client.

Provides a reusable wrapper around the Codeforces REST API.
"""

from __future__ import annotations

import logging
from typing import Any

import requests
from requests import Response
from requests.exceptions import RequestException

from codeforces_lakehouse.config.settings import get_settings


logger = logging.getLogger(__name__)


class CodeforcesAPIError(Exception):
    """Raised when the Codeforces API returns an error."""


class CodeforcesClient:
    """Client for interacting with the Codeforces REST API."""

    def __init__(
        self,
        base_url: str | None = None,
        timeout: int = 30,
    ) -> None:
        settings = get_settings()

        self.base_url = (
            base_url or settings.codeforces_api_base_url
        ).rstrip("/")

        self.timeout = timeout

        self.session = requests.Session()

        self.session.headers.update(
            {
                "User-Agent": "codeforces-data-lakehouse/1.0",
                "Accept": "application/json",
            }
        )

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """
        Execute an HTTP request against Codeforces.

        Raises:
            CodeforcesAPIError: If the request or API response fails.
        """

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        logger.info("Requesting Codeforces API: %s", url)

        try:
            response: Response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs,
            )

            response.raise_for_status()

        except RequestException as exc:
            logger.exception("HTTP request failed: %s", url)

            raise CodeforcesAPIError(
                f"Failed to request Codeforces API: {url}"
            ) from exc

        try:
            data = response.json()

        except ValueError as exc:
            raise CodeforcesAPIError(
                "Codeforces API returned invalid JSON."
            ) from exc

        if data.get("status") != "OK":
            comment = data.get(
                "comment",
                "Unknown Codeforces API error",
            )

            raise CodeforcesAPIError(
                f"Codeforces API error: {comment}"
            )

        return data

    def get_user_info(
        self,
        handles: list[str],
    ) -> list[dict[str, Any]]:
        """Retrieve information about Codeforces users."""

        if not handles:
            raise ValueError(
                "At least one Codeforces handle is required."
            )

        data = self._request(
            "GET",
            "/user.info",
            params={
                "handles": ";".join(handles),
            },
        )

        return data["result"]

    def get_problemset(self) -> dict[str, Any]:
        """
        Retrieve Codeforces problems and statistics.

        Returns:
            Dictionary containing:
                - problems
                - problemStatistics
        """

        data = self._request(
            "GET",
            "/problemset.problems",
        )

        return data["result"]
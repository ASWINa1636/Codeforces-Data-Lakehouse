"""
PostgreSQL database connection utilities.
"""

from __future__ import annotations

import logging

import psycopg

from codeforces_lakehouse.config.settings import (
    get_settings,
)


logger = logging.getLogger(__name__)


def get_connection() -> psycopg.Connection:
    """
    Create a PostgreSQL database connection.

    Returns:
        Active psycopg connection.
    """

    settings = get_settings()

    logger.info(
        "Connecting to PostgreSQL at %s:%s",
        settings.postgres_host,
        settings.postgres_port,
    )

    connection = psycopg.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.postgres_database,
        user=settings.postgres_user,
        password=settings.postgres_password,
    )

    return connection
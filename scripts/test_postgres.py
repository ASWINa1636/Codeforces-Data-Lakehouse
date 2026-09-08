"""
Test the Python to PostgreSQL connection.
"""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT / "src"),
)

from codeforces_lakehouse.database.postgres import (  # noqa: E402
    get_connection,
)


def main() -> None:
    """Test PostgreSQL connectivity."""

    with get_connection() as connection:

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT current_database(), current_user;"
            )

            database, user = cursor.fetchone()

    print(f"Database: {database}")
    print(f"User: {user}")


if __name__ == "__main__":
    main()
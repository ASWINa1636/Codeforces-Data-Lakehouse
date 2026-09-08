"""
Ingest Codeforces problemset data into the raw data layer.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Add src/ to Python's module search path.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))

from codeforces_lakehouse.api.codeforces_client import (  # noqa: E402
    CodeforcesAPIError,
    CodeforcesClient,
)
from codeforces_lakehouse.ingestion.raw_writer import (  # noqa: E402
    write_raw_json,
)


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)

logger = logging.getLogger(__name__)


def main() -> None:
    """Run the Codeforces problemset ingestion."""

    logger.info("Starting Codeforces problemset ingestion.")

    client = CodeforcesClient()

    try:
        problemset = client.get_problemset()

    except CodeforcesAPIError:
        logger.exception(
            "Problemset ingestion failed."
        )
        raise

    output_directory = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "codeforces"
        / "problemset"
    )

    output_file = write_raw_json(
        data=problemset,
        directory=output_directory,
        dataset_name="problemset",
    )

    problem_count = len(
        problemset.get("problems", [])
    )

    statistics_count = len(
        problemset.get("problemStatistics", [])
    )

    logger.info(
        "Problems extracted: %d",
        problem_count,
    )

    logger.info(
        "Statistics extracted: %d",
        statistics_count,
    )

    logger.info(
        "Raw data written to: %s",
        output_file,
    )


if __name__ == "__main__":
    main()
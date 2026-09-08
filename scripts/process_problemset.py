"""
Process the latest Codeforces problemset snapshot.
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(
    0,
    str(SRC_DIR),
)

from codeforces_lakehouse.ingestion.problemset_processor import (  # noqa: E402
    ProblemsetProcessor,
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


def get_latest_raw_file() -> Path:
    """Return the newest problemset JSON file."""

    directory = (
        PROJECT_ROOT
        / "data"
        / "raw"
        / "codeforces"
        / "problemset"
    )

    files = list(
        directory.glob("problemset_*.json")
    )

    if not files:
        raise FileNotFoundError(
            "No raw problemset files found."
        )

    return max(
        files,
        key=lambda file: file.stat().st_mtime,
    )


def main() -> None:
    """Run the problemset processing pipeline."""

    raw_file = get_latest_raw_file()

    output_directory = (
        PROJECT_ROOT
        / "data"
        / "processed"
        / "codeforces"
        / "problemset"
    )

    processor = ProblemsetProcessor(
        raw_file=raw_file,
        output_directory=output_directory,
    )

    processor.process()


if __name__ == "__main__":
    main()
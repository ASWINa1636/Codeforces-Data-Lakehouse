"""
Utilities for writing raw API responses to disk.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def write_raw_json(
    data: Any,
    directory: Path,
    dataset_name: str,
) -> Path:
    """
    Write data to a timestamped JSON file.

    Args:
        data: Data returned by the API.
        directory: Destination directory.
        dataset_name: Logical name of the dataset.

    Returns:
        Path to the created file.
    """

    directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = datetime.now(
        timezone.utc
    ).strftime("%Y%m%dT%H%M%SZ")

    file_path = directory / (
        f"{dataset_name}_{timestamp}.json"
    )

    with file_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2,
        )

    return file_path
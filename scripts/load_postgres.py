from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(
    0,
    str(PROJECT_ROOT / "src"),
)

from codeforces_lakehouse.ingestion.postgres_loader import (
    load_problemset,
)


if __name__ == "__main__":
    load_problemset()
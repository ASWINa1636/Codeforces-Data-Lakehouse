from pathlib import Path
import json
import sys

import duckdb
import psycopg

PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.insert(0, str(PROJECT_ROOT / "src"))

from codeforces_lakehouse.config.settings import get_settings


RAW_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "codeforces"
    / "problemset"
)

PROCESSED_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "codeforces"
    / "problemset"
)


def get_latest_raw_file() -> Path:
    files = sorted(RAW_DIR.glob("problemset_*.json"))

    if not files:
        raise FileNotFoundError(
            f"No raw problemset files found in {RAW_DIR}"
        )

    return files[-1]


def validate_raw_json() -> tuple[int, int]:
    raw_file = get_latest_raw_file()

    with raw_file.open("r", encoding="utf-8") as file:
        payload = json.load(file)

    if not isinstance(payload, dict):
        raise RuntimeError(
            f"Invalid raw JSON structure in {raw_file.name}"
        )

    if "problems" not in payload:
        raise RuntimeError(
            f"Raw file {raw_file.name} does not contain 'problems'"
        )

    if "problemStatistics" not in payload:
        raise RuntimeError(
            f"Raw file {raw_file.name} does not contain "
            "'problemStatistics'"
        )

    problems = payload["problems"]
    statistics = payload["problemStatistics"]

    if not isinstance(problems, list):
        raise RuntimeError(
            f"'problems' is not a list in {raw_file.name}"
        )

    if not isinstance(statistics, list):
        raise RuntimeError(
            f"'problemStatistics' is not a list in {raw_file.name}"
        )

    return len(problems), len(statistics)

def validate_parquet() -> tuple[int, int]:
    problems_file = PROCESSED_DIR / "problems.parquet"
    statistics_file = PROCESSED_DIR / "problem_statistics.parquet"

    connection = duckdb.connect()

    try:
        problems_count = connection.execute(
            f"""
            SELECT COUNT(*)
            FROM read_parquet('{problems_file.as_posix()}')
            """
        ).fetchone()[0]

        statistics_count = connection.execute(
            f"""
            SELECT COUNT(*)
            FROM read_parquet('{statistics_file.as_posix()}')
            """
        ).fetchone()[0]

    finally:
        connection.close()

    return problems_count, statistics_count


def validate_postgres() -> dict[str, int]:
    settings = get_settings()

    with psycopg.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.postgres_database,
        user=settings.postgres_user,
        password=settings.postgres_password,
    ) as connection:

        with connection.cursor() as cursor:

            queries = {
                "staging.problems": """
                    SELECT COUNT(*)
                    FROM staging.problems
                """,
                "staging.problem_statistics": """
                    SELECT COUNT(*)
                    FROM staging.problem_statistics
                """,
                "analytics.dim_problem": """
                    SELECT COUNT(*)
                    FROM analytics.dim_problem
                """,
                "analytics.fact_problem_statistics": """
                    SELECT COUNT(*)
                    FROM analytics.fact_problem_statistics
                """,
                "analytics.mart_problem_performance": """
                    SELECT COUNT(*)
                    FROM analytics.mart_problem_performance
                """,
            }

            results = {}

            for name, query in queries.items():
                cursor.execute(query)
                results[name] = cursor.fetchone()[0]

    return results


def assert_equal(name: str, expected: int, actual: int) -> None:
    if expected != actual:
        raise RuntimeError(
            f"{name} validation failed: "
            f"expected {expected:,}, got {actual:,}"
        )


def main() -> None:
    print("=" * 60)
    print("Codeforces Pipeline Validation")
    print("=" * 60)

    raw_problems, raw_statistics = validate_raw_json()

    print("\nRaw JSON")
    print(f"  problems:    {raw_problems:,}")
    print(f"  statistics:  {raw_statistics:,}")

    parquet_problems, parquet_statistics = validate_parquet()

    print("\nParquet")
    print(f"  problems:    {parquet_problems:,}")
    print(f"  statistics:  {parquet_statistics:,}")

    postgres = validate_postgres()

    print("\nPostgreSQL")

    for table, count in postgres.items():
        print(f"  {table}: {count:,}")

    print("\nValidation")

    assert_equal(
        "Raw problems → Parquet problems",
        raw_problems,
        parquet_problems,
    )

    assert_equal(
        "Raw statistics → Parquet statistics",
        raw_statistics,
        parquet_statistics,
    )

    assert_equal(
        "Parquet problems → staging problems",
        parquet_problems,
        postgres["staging.problems"],
    )

    assert_equal(
        "Parquet statistics → staging statistics",
        parquet_statistics,
        postgres["staging.problem_statistics"],
    )

    assert_equal(
        "Staging problems → dimension",
        postgres["staging.problems"],
        postgres["analytics.dim_problem"],
    )

    assert_equal(
        "Staging statistics → fact",
        postgres["staging.problem_statistics"],
        postgres["analytics.fact_problem_statistics"],
    )

    assert_equal(
        "Dimension → problem performance mart",
        postgres["analytics.dim_problem"],
        postgres["analytics.mart_problem_performance"],
    )

    print("\n" + "=" * 60)
    print("PIPELINE VALIDATION PASSED")
    print("=" * 60)


if __name__ == "__main__":
    main()
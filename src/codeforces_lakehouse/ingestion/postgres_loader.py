from pathlib import Path

import duckdb
import psycopg

from codeforces_lakehouse.config.settings import get_settings


PROJECT_ROOT = Path(__file__).resolve().parents[3]

PROCESSED_DIR = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "codeforces"
    / "problemset"
)


def get_parquet_connection():
    return duckdb.connect()


def load_parquet_to_postgres(
    parquet_file: Path,
    table_name: str,
) -> None:
    settings = get_settings()

    parquet_file = parquet_file.resolve()

    if not parquet_file.exists():
        raise FileNotFoundError(
            f"Parquet file not found: {parquet_file}"
        )

    duckdb_connection = get_parquet_connection()

    try:
        columns = duckdb_connection.execute(
            f"""
            DESCRIBE SELECT *
            FROM read_parquet('{parquet_file.as_posix()}')
            """
        ).fetchall()

        column_definitions = ", ".join(
            f'"{name}" {duckdb_type_to_postgres(data_type)}'
            for name, data_type, *_ in columns
        )

        rows = duckdb_connection.execute(
            f"""
            SELECT *
            FROM read_parquet('{parquet_file.as_posix()}')
            """
        ).fetchall()

    finally:
        duckdb_connection.close()

    with psycopg.connect(
        host=settings.postgres_host,
        port=settings.postgres_port,
        dbname=settings.postgres_database,
        user=settings.postgres_user,
        password=settings.postgres_password,
    ) as connection:

        with connection.cursor() as cursor:

            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS staging."{table_name}" (
                    {column_definitions}
                );
                """
            )

            cursor.execute(
                f'TRUNCATE TABLE staging."{table_name}";'
            )

            placeholders = ", ".join(["%s"] * len(columns))

            cursor.executemany(
                f"""
                INSERT INTO staging."{table_name}"
                VALUES ({placeholders});
                """,
                rows,
            )

        connection.commit()

    print(
        f"Loaded {len(rows):,} rows into "
        f"staging.{table_name}"
    )


def duckdb_type_to_postgres(data_type: str) -> str:
    data_type = data_type.upper()

    if "BIGINT" in data_type:
        return "BIGINT"

    if "INTEGER" in data_type or data_type == "INT":
        return "INTEGER"

    if "DOUBLE" in data_type or "FLOAT" in data_type:
        return "DOUBLE PRECISION"

    if "BOOLEAN" in data_type:
        return "BOOLEAN"

    if "TIMESTAMP" in data_type:
        return "TIMESTAMP"

    return "TEXT"


def load_problemset() -> None:
    problems_file = PROCESSED_DIR / "problems.parquet"
    statistics_file = PROCESSED_DIR / "problem_statistics.parquet"

    load_parquet_to_postgres(
        problems_file,
        "problems",
    )

    load_parquet_to_postgres(
        statistics_file,
        "problem_statistics",
    )
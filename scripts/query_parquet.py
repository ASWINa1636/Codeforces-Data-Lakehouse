"""
Query Codeforces Parquet data using DuckDB.
"""

from pathlib import Path

import duckdb


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "codeforces"
    / "problemset"
)


def main() -> None:
    """Run analytical queries against Parquet."""

    connection = duckdb.connect()

    problems_file = (
        DATA_DIRECTORY
        / "problems.parquet"
    )

    statistics_file = (
        DATA_DIRECTORY
        / "problem_statistics.parquet"
    )

    print("\nTop 10 hardest problems by rating:\n")

    result = connection.execute(
        """
        SELECT
            contest_id,
            problem_index,
            problem_name,
            rating
        FROM read_parquet(?)
        WHERE rating IS NOT NULL
        ORDER BY rating DESC
        LIMIT 10;
        """,
        [str(problems_file)],
    ).fetchall()

    for row in result:
        print(row)

    print(
        "\nTop 10 most solved problems:\n"
    )

    result = connection.execute(
        """
        SELECT
            p.contest_id,
            p.problem_index,
            p.problem_name,
            s.solved_count
        FROM read_parquet(?) p
        INNER JOIN read_parquet(?) s
            ON p.contest_id = s.contest_id
            AND p.problem_index = s.problem_index
        ORDER BY s.solved_count DESC
        LIMIT 10;
        """,
        [
            str(problems_file),
            str(statistics_file),
        ],
    ).fetchall()

    for row in result:
        print(row)

    connection.close()


if __name__ == "__main__":
    main()
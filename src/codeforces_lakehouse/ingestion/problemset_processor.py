"""
Transform Codeforces raw problemset JSON into analytical Parquet files.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

import duckdb


logger = logging.getLogger(__name__)


class ProblemsetProcessor:
    """Process raw Codeforces problemset data using DuckDB."""

    def __init__(
        self,
        raw_file: Path,
        output_directory: Path,
    ) -> None:
        self.raw_file = raw_file
        self.output_directory = output_directory

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def process(self) -> None:
        """Transform raw JSON into Parquet datasets."""

        logger.info(
            "Processing raw file: %s",
            self.raw_file,
        )

        with self.raw_file.open(
            "r",
            encoding="utf-8",
        ) as file:
            raw_data = json.load(file)

        problems = raw_data.get(
            "problems",
            [],
        )

        statistics = raw_data.get(
            "problemStatistics",
            [],
        )

        logger.info(
            "Loaded %d problems.",
            len(problems),
        )

        logger.info(
            "Loaded %d problem statistics.",
            len(statistics),
        )

        connection = duckdb.connect()

        try:
            self._write_problems(
                connection,
                problems,
            )

            self._write_statistics(
                connection,
                statistics,
            )

        finally:
            connection.close()

        logger.info(
            "Parquet processing completed."
        )

    def _write_problems(
        self,
        connection: duckdb.DuckDBPyConnection,
        problems: list[dict],
    ) -> None:
        """Write problem records to Parquet."""

        output_file = (
            self.output_directory
            / "problems.parquet"
        )

        connection.execute(
            """
            CREATE OR REPLACE TABLE problems AS
            SELECT
                CAST(problem->>'contestId' AS BIGINT)
                    AS contest_id,

                problem->>'index'
                    AS problem_index,

                problem->>'name'
                    AS problem_name,

                problem->>'type'
                    AS problem_type,

                TRY_CAST(
                    problem->>'rating'
                    AS INTEGER
                ) AS rating,

                problem->'tags'
                    AS tags

            FROM read_json(
                ?
            ) AS source,
            UNNEST(
                source.problems
            ) AS t(problem);
            """,
            [
                str(
                    self.raw_file
                )
            ],
        )

        connection.execute(
            """
            COPY problems
            TO ?
            (FORMAT PARQUET);
            """,
            [
                str(output_file)
            ],
        )

        logger.info(
            "Problems written to: %s",
            output_file,
        )

    def _write_statistics(
        self,
        connection: duckdb.DuckDBPyConnection,
        statistics: list[dict],
    ) -> None:
        """Write problem statistics to Parquet."""

        output_file = (
            self.output_directory
            / "problem_statistics.parquet"
        )

        connection.execute(
            """
            CREATE OR REPLACE TABLE problem_statistics AS
            SELECT
                CAST(stat->>'contestId' AS BIGINT)
                    AS contest_id,

                stat->>'index'
                    AS problem_index,

                CAST(
                    stat->>'solvedCount'
                    AS BIGINT
                ) AS solved_count

            FROM read_json(
                ?
            ) AS source,
            UNNEST(
                source.problemStatistics
            ) AS t(stat);
            """,
            [
                str(
                    self.raw_file
                )
            ],
        )

        connection.execute(
            """
            COPY problem_statistics
            TO ?
            (FORMAT PARQUET);
            """,
            [
                str(output_file)
            ],
        )

        logger.info(
            "Statistics written to: %s",
            output_file,
        )
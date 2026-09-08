"""Test the Codeforces problemset API."""

from codeforces_lakehouse.api.codeforces_client import CodeforcesClient


def main() -> None:
    client = CodeforcesClient()

    result = client.get_problemset()

    problems = result["problems"]
    statistics = result["problemStatistics"]

    print(f"Total problems: {len(problems)}")
    print(f"Total statistics: {len(statistics)}")

    print("\nFirst 5 problems:")

    for problem in problems[:5]:
        print(
            f"{problem.get('contestId')}"
            f"-{problem.get('index')}: "
            f"{problem.get('name')}"
        )


if __name__ == "__main__":
    main()
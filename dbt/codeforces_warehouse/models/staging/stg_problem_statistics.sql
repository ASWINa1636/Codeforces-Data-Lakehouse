SELECT
    contest_id,
    problem_index,
    solved_count
FROM {{ source('codeforces', 'problem_statistics') }}
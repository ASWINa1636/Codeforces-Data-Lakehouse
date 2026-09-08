SELECT
    contest_id,
    problem_index,
    solved_count
FROM {{ ref('stg_problem_statistics') }}
WHERE solved_count < 0
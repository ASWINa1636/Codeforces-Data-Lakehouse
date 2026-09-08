SELECT
    contest_id,
    problem_index,
    COUNT(*) AS problem_count
FROM {{ ref('stg_problems') }}
GROUP BY
    contest_id,
    problem_index
HAVING COUNT(*) > 1
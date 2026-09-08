SELECT
    f.problem_key,
    f.contest_id,
    f.problem_index
FROM {{ ref('fact_problem_statistics') }} AS f
LEFT JOIN {{ ref('dim_problem') }} AS p
    ON f.problem_key = p.problem_key
WHERE p.problem_key IS NULL
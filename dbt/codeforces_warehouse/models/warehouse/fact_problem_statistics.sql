{{ config(
    materialized='table'
) }}

SELECT
    p.problem_key,
    s.contest_id,
    s.problem_index,
    s.solved_count

FROM {{ ref('stg_problem_statistics') }} AS s

INNER JOIN {{ ref('dim_problem') }} AS p
    ON p.contest_id = s.contest_id
    AND p.problem_index = s.problem_index
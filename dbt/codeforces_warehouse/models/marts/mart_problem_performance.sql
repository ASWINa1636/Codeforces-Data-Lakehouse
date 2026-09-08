{{ config(
    materialized='table'
) }}

SELECT
    p.problem_key,
    p.contest_id,
    p.problem_index,
    p.problem_name,
    p.problem_type,
    p.rating,
    p.tags,
    f.solved_count

FROM {{ ref('dim_problem') }} AS p

INNER JOIN {{ ref('fact_problem_statistics') }} AS f
    ON p.problem_key = f.problem_key
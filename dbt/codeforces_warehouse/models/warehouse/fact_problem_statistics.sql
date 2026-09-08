{{ config(
    materialized='incremental',
    unique_key='problem_natural_key',
    incremental_strategy='merge'
) }}

SELECT
    p.problem_key,

    concat(
        s.contest_id,
        ':',
        s.problem_index
    ) AS problem_natural_key,

    s.contest_id,
    s.problem_index,
    s.solved_count

FROM {{ ref('stg_problem_statistics') }} AS s

INNER JOIN {{ ref('dim_problem') }} AS p
    ON p.problem_natural_key = concat(
        s.contest_id,
        ':',
        s.problem_index
    )
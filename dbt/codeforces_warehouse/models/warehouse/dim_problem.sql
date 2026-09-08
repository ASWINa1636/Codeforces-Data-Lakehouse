{{ config(
    materialized='table'
) }}

SELECT
    ROW_NUMBER() OVER (
        ORDER BY contest_id, problem_index
    ) AS problem_key,

    contest_id,
    problem_index,
    problem_name,
    problem_type,
    rating,
    tags

FROM {{ ref('stg_problems') }}
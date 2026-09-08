{{ config(
    materialized='incremental',
    unique_key='problem_natural_key',
    incremental_strategy='merge'
) }}

SELECT
    md5(
        concat(
            contest_id,
            ':',
            problem_index
        )
    ) AS problem_key,

    concat(
        contest_id,
        ':',
        problem_index
    ) AS problem_natural_key,

    contest_id,
    problem_index,
    problem_name,
    problem_type,
    rating,
    tags

FROM {{ ref('stg_problems') }}
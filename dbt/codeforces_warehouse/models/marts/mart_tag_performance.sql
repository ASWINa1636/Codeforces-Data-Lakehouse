{{ config(
    materialized='table'
) }}

WITH problem_tags AS (

    SELECT
        problem_key,
        problem_name,
        rating,
        solved_count,

        TRIM(
            BOTH '"' FROM
            TRIM(
                BOTH '[]' FROM
                TRIM(tag)
            )
        ) AS tag

    FROM {{ ref('mart_problem_performance') }},

    LATERAL unnest(
        string_to_array(tags, ',')
    ) AS tag

    WHERE tags IS NOT NULL
      AND tags <> ''

)

SELECT
    tag,
    COUNT(*) AS problem_count,
    SUM(solved_count) AS total_solves,
    AVG(solved_count) AS avg_solves,
    AVG(rating) AS avg_rating

FROM problem_tags

WHERE tag <> ''

GROUP BY tag
ORDER BY total_solves DESC
{{ config(
    materialized='table'
) }}

SELECT
    rating,
    COUNT(*) AS problem_count,
    SUM(solved_count) AS total_solves,
    AVG(solved_count) AS avg_solves,
    MIN(solved_count) AS min_solves,
    MAX(solved_count) AS max_solves

FROM {{ ref('mart_problem_performance') }}

WHERE rating IS NOT NULL

GROUP BY rating
ORDER BY rating
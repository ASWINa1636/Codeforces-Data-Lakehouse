SELECT
    'problem_statistics' AS table_name,
    source_count,
    staging_count
FROM (
    SELECT
        (SELECT COUNT(*) FROM {{ source('codeforces', 'problem_statistics') }}) AS source_count,
        (SELECT COUNT(*) FROM {{ ref('stg_problem_statistics') }}) AS staging_count
) counts
WHERE source_count != staging_count
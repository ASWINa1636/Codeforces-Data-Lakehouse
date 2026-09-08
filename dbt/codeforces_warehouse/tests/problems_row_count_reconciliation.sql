SELECT
    'problems' AS table_name,
    source_count,
    staging_count
FROM (
    SELECT
        (SELECT COUNT(*) FROM {{ source('codeforces', 'problems') }}) AS source_count,
        (SELECT COUNT(*) FROM {{ ref('stg_problems') }}) AS staging_count
) counts
WHERE source_count != staging_count
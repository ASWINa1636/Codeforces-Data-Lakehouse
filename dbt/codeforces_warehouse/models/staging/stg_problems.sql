SELECT
    contest_id,
    problem_index,
    problem_name,
    problem_type,
    rating,
    tags
FROM {{ source('codeforces', 'problems') }}
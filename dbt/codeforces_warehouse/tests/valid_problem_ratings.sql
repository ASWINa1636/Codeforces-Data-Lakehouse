SELECT
    contest_id,
    problem_index,
    rating
FROM {{ ref('stg_problems') }}
WHERE rating IS NOT NULL
  AND rating < 800
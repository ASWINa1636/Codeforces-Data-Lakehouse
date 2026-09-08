-- ============================================================
-- Load Warehouse from Staging
-- ============================================================

BEGIN;


-- ------------------------------------------------------------
-- 1. Load Problem Dimension
-- ------------------------------------------------------------

INSERT INTO warehouse.dim_problem (
    contest_id,
    problem_index,
    problem_name,
    problem_type,
    rating,
    tags
)
SELECT
    contest_id,
    problem_index,
    problem_name,
    problem_type,
    rating,
    tags
FROM staging.problems
ON CONFLICT (contest_id, problem_index)
DO UPDATE SET
    problem_name = EXCLUDED.problem_name,
    problem_type = EXCLUDED.problem_type,
    rating = EXCLUDED.rating,
    tags = EXCLUDED.tags;


-- ------------------------------------------------------------
-- 2. Load Problem Statistics Fact
-- ------------------------------------------------------------

INSERT INTO warehouse.fact_problem_statistics (
    problem_key,
    contest_id,
    problem_index,
    solved_count
)
SELECT
    p.problem_key,
    s.contest_id,
    s.problem_index,
    s.solved_count
FROM staging.problem_statistics s
INNER JOIN warehouse.dim_problem p
    ON p.contest_id = s.contest_id
    AND p.problem_index = s.problem_index
ON CONFLICT (contest_id, problem_index)
DO UPDATE SET
    problem_key = EXCLUDED.problem_key,
    solved_count = EXCLUDED.solved_count;


COMMIT;
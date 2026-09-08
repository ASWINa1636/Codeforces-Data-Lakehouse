-- ============================================================
-- Codeforces Data Lakehouse
-- Warehouse Layer
-- ============================================================

-- ------------------------------------------------------------
-- Dimension: Problems
-- ------------------------------------------------------------

DROP TABLE IF EXISTS warehouse.fact_problem_statistics;
DROP TABLE IF EXISTS warehouse.dim_problem;

CREATE TABLE warehouse.dim_problem (
    problem_key BIGSERIAL PRIMARY KEY,

    contest_id BIGINT NOT NULL,
    problem_index TEXT NOT NULL,
    problem_name TEXT,
    problem_type TEXT,
    rating INTEGER,
    tags TEXT,

    CONSTRAINT uq_dim_problem
        UNIQUE (contest_id, problem_index)
);


-- ------------------------------------------------------------
-- Fact: Problem Statistics
-- ------------------------------------------------------------

CREATE TABLE warehouse.fact_problem_statistics (
    problem_key BIGINT NOT NULL,

    contest_id BIGINT NOT NULL,
    problem_index TEXT NOT NULL,

    solved_count BIGINT NOT NULL,

    CONSTRAINT fk_fact_problem
        FOREIGN KEY (problem_key)
        REFERENCES warehouse.dim_problem(problem_key),

    CONSTRAINT uq_fact_problem
        UNIQUE (contest_id, problem_index)
);


-- ------------------------------------------------------------
-- Indexes
-- ------------------------------------------------------------

CREATE INDEX idx_fact_problem_key
    ON warehouse.fact_problem_statistics(problem_key);

CREATE INDEX idx_dim_problem_rating
    ON warehouse.dim_problem(rating);

CREATE INDEX idx_fact_solved_count
    ON warehouse.fact_problem_statistics(solved_count);

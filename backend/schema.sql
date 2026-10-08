CREATE TABLE IF NOT EXISTS poc_records (
    key text PRIMARY KEY,
    value text NOT NULL CHECK (length(value) BETWEEN 1 AND 200)
);

CREATE TABLE IF NOT EXISTS poc_job_runs (
    logical_key text PRIMARY KEY,
    scheduled_at timestamptz NOT NULL,
    executed_at timestamptz NOT NULL DEFAULT now(),
    status text NOT NULL CHECK (status IN ('completed'))
);

-- +goose Up
CREATE TABLE sessions (
    "id" UUID NOT NULL,
    "project_id" varchar(255) NOT NULL,

    "inited_at" timestamp NOT NULL,
    "created_at" timestamp NOT NULL,
    "started_at" timestamp,
    "ended_at" timestamp,
    "saved_at" timestamp NOT NULL,

    "discovered" integer,
    "scheduled" integer,
    "total" integer,
    "passed" integer,
    "failed" integer,
    "skipped" integer,

    "cmd" jsonb,
    "environment" jsonb,
    "interrupted" jsonb,

    PRIMARY KEY ("id")
);

-- +goose Down
DROP TABLE sessions;

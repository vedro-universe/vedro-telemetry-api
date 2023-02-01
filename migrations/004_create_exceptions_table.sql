-- +goose Up
CREATE TABLE exceptions (
    "session_id" UUID NOT NULL,
    "scenario_id" varchar(1024) NOT NULL,

    "type" varchar(255) NOT NULL,
    "message" text NOT NULL,
    "traceback" text NOT NULL,

    "raised_at" timestamp NOT NULL
);

-- +goose Down
DROP TABLE exceptions;

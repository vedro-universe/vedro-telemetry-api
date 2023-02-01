-- +goose Up
CREATE TABLE arguments (
    "session_id" UUID NOT NULL,
    "name" varchar(255) NOT NULL,
    "value" jsonb NOT NULL
);

-- +goose Down
DROP TABLE arguments;

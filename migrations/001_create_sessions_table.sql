-- +goose Up
CREATE TABLE sessions (
    "id" UUID NOT NULL,
    "created_at" timestamp NOT NULL,

    PRIMARY KEY ("id")
);

-- +goose Down
DROP TABLE sessions;

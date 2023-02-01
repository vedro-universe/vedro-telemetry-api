-- +goose Up
CREATE TABLE plugins (
    "session_id" UUID NOT NULL,
    "name" varchar(255) NOT NULL,
    "module" varchar(255) NOT NULL,
    "enabled" boolean NOT NULL
);

-- +goose Down
DROP TABLE plugins;

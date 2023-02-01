-- +goose Up
CREATE TABLE plugins (
    "session_id" UUID NOT NULL,
    "name" varchar(255) NOT NULL,
    "module" varchar(1024) NOT NULL,
    "enabled" boolean NOT NULL,
    "version" varchar(32) NOT NULL
);

-- +goose Down
DROP TABLE plugins;

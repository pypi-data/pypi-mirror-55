CREATE TABLE IF NOT EXISTS leases_v6 (
    uid TEXT NOT NULL UNIQUE,
    ip TEXT NOT NULL UNIQUE,
    last_connect INTEGER NOT NULL,
    last_disconnect INTEGER,
    PRIMARY KEY(uid)
);

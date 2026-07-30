"""Creates the tables used for statistics tracking."""

import sqlite3


_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id     INTEGER PRIMARY KEY,
    first_seen  DATETIME NOT NULL,
    last_seen   DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id    INTEGER NOT NULL,
    created_at DATETIME NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at);
CREATE INDEX IF NOT EXISTS idx_messages_user_id ON messages(user_id);
CREATE INDEX IF NOT EXISTS idx_users_last_seen ON users(last_seen);
"""


def create_schema(conn: sqlite3.Connection) -> None:
    """Creates the tables used for statistics tracking if they don't
    already exist.
    """
    conn.executescript(_SCHEMA)
    conn.commit()

"""Opens the shared SQLite handle used for statistics storage."""

from typing import Optional
import sqlite3

from stats.db_schema import create_schema


# DB_PATH is where the SQLite file lives. Railway's filesystem is ephemeral
# across deploys unless a volume is mounted at this path; mount a volume at
# /data in the Railway service settings to persist stats across deploys.
DB_PATH = "/data/stats.db"

# DB is the shared SQLite handle used for statistics storage. Set by
# init_db().
DB: Optional[sqlite3.Connection] = None


def init_db() -> sqlite3.Connection:
    """Opens the SQLite database and ensures the schema exists."""
    global DB
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA busy_timeout=5000")

    DB = conn
    create_schema(conn)
    return conn

"""Queries SQLite for a fresh Stats snapshot."""

from datetime import datetime, timedelta, timezone

from stats.stats import Stats
import stats.db as db


# ACTIVE_WINDOW is how recently a user must have been seen to count as
# "currently using the bot".
ACTIVE_WINDOW = timedelta(minutes=5)


def _scan_message_count(since: datetime) -> int:
    """Counts messages created at or after since."""
    row = db.DB.execute(
        "SELECT COUNT(*) FROM messages WHERE created_at >= ?", (since.isoformat(),)
    ).fetchone()
    return row[0]


def _minus_one_year(dt: datetime) -> datetime:
    """Subtracts exactly one year from dt, mirroring Go's time.AddDate(-1,
    0, 0): if dt is Feb 29 and the target year is not a leap year, it
    rolls over to Mar 1 rather than raising an error.
    """
    try:
        return dt.replace(year=dt.year - 1)
    except ValueError:
        # dt is Feb 29 and (dt.year - 1) is not a leap year.
        return dt.replace(month=3, day=1, year=dt.year - 1)


def load_stats() -> Stats:
    """Queries SQLite for a fresh Stats snapshot as of now."""
    s = Stats()
    now = datetime.now(timezone.utc)

    row = db.DB.execute(
        "SELECT COUNT(*) FROM users WHERE last_seen >= ?",
        ((now - ACTIVE_WINDOW).isoformat(),),
    ).fetchone()
    s.active_users = row[0]

    row = db.DB.execute("SELECT COUNT(*) FROM users").fetchone()
    s.unique_users = row[0]

    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    s.messages_today = _scan_message_count(midnight)
    s.messages_24h = _scan_message_count(now - timedelta(hours=24))
    s.messages_7d = _scan_message_count(now - timedelta(days=7))
    s.messages_30d = _scan_message_count(now - timedelta(days=30))
    s.messages_1y = _scan_message_count(_minus_one_year(now))

    row = db.DB.execute("SELECT COUNT(*) FROM messages").fetchone()
    s.messages_lifetime = row[0]

    return s

"""Unit tests for the stats package. Uses an in-memory SQLite database,
so these run with no network or filesystem dependency.
"""

import sqlite3
from datetime import datetime, timezone

import stats.db as db
from stats.db_schema import create_schema
from stats.track_message import track_message
from stats.load_stats import load_stats, _minus_one_year
from stats.stats import Stats
from stats.format_stats import format_stats


def _fresh_in_memory_db():
    conn = sqlite3.connect(":memory:")
    create_schema(conn)
    db.DB = conn
    return conn


def test_tracking_messages_updates_counts():
    _fresh_in_memory_db()

    track_message(111)
    track_message(111)
    track_message(222)

    s = load_stats()
    assert s.unique_users == 2
    assert s.messages_lifetime == 3
    assert s.active_users == 2
    assert s.messages_today == 3


def test_format_stats_includes_all_fields():
    s = Stats(
        active_users=2,
        unique_users=5,
        messages_today=10,
        messages_24h=12,
        messages_7d=50,
        messages_30d=200,
        messages_1y=1000,
        messages_lifetime=1500,
    )
    updated_at = datetime(2026, 7, 29, 14, 30, 0, tzinfo=timezone.utc)
    out = format_stats(s, updated_at)

    assert "<b>\U0001F4CA Statistics</b>" in out
    assert "<b>2</b>" in out
    assert "<b>1500</b>" in out
    assert "2026-07-29 14:30:00 UTC" in out


def test_minus_one_year_handles_leap_day():
    # Feb 29 2028 (leap year) minus one year should roll to Mar 1 2027
    # (not a leap year), matching Go's time.AddDate(-1, 0, 0) behavior,
    # rather than raising ValueError as a naive datetime.replace() would.
    leap_day = datetime(2028, 2, 29, 12, 0, 0, tzinfo=timezone.utc)
    result = _minus_one_year(leap_day)
    assert result == datetime(2027, 3, 1, 12, 0, 0, tzinfo=timezone.utc)


def test_minus_one_year_normal_case():
    normal = datetime(2026, 7, 29, 12, 0, 0, tzinfo=timezone.utc)
    result = _minus_one_year(normal)
    assert result == datetime(2025, 7, 29, 12, 0, 0, tzinfo=timezone.utc)

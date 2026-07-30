"""Renders a Stats snapshot as the text body of the Statistics message."""

from datetime import datetime, timezone

from stats.stats import Stats


def format_stats(s: Stats, updated_at: datetime) -> str:
    """Renders s as the text body of the Statistics message."""
    return (
        "<b>\U0001f4ca Statistics</b>\n\n"
        f"\U0001f7e2 Active users: <b>{s.active_users}</b>\n"
        f"\U0001f465 Unique users (all-time): <b>{s.unique_users}</b>\n\n"
        f"\U0001f4ac Messages today: <b>{s.messages_today}</b>\n"
        f"\U0001f4ac Last 24 hours: <b>{s.messages_24h}</b>\n"
        f"\U0001f4ac Last 7 days: <b>{s.messages_7d}</b>\n"
        f"\U0001f4ac Last 30 days: <b>{s.messages_30d}</b>\n"
        f"\U0001f4ac Last 1 year: <b>{s.messages_1y}</b>\n\n"
        f"\U0001f4c8 Lifetime total: <b>{s.messages_lifetime}</b>\n\n"
        f"<i>Updated {updated_at.astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC</i>"
    )

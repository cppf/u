"""Stats holds a snapshot of bot usage counts, as shown on the Statistics page."""

from dataclasses import dataclass


@dataclass
class Stats:
    """A snapshot of bot usage counts, as shown on the Statistics page."""

    active_users: int = 0  # distinct users seen in the last 5 minutes
    unique_users: int = 0  # distinct users, all-time
    messages_today: int = 0  # messages since local midnight UTC
    messages_24h: int = 0  # messages in the trailing 24 hours
    messages_7d: int = 0  # messages in the trailing 7 days
    messages_30d: int = 0  # messages in the trailing 30 days
    messages_1y: int = 0  # messages in the trailing 1 year
    messages_lifetime: int = 0  # all messages ever recorded

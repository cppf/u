"""Records one incoming Telegram update as a message event."""

from datetime import datetime, timezone
import logging

import stats.db as db


logger = logging.getLogger(__name__)


def track_message(user_id: int) -> None:
    """Records one incoming Telegram update as a message event for
    user_id, and upserts that user's first/last seen timestamps. Safe to
    call from every update handler (text, caption, media, sticker,
    document, etc.) — each call counts as exactly one message.
    """
    now = datetime.now(timezone.utc).isoformat()

    try:
        db.DB.execute(
            """
            INSERT INTO users (user_id, first_seen, last_seen) VALUES (?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET last_seen = excluded.last_seen
            """,
            (user_id, now, now),
        )
        db.DB.commit()
    except Exception as e:  # noqa: BLE001 - mirrors Go's log-and-continue
        logger.error("track_message: upsert user %s: %s", user_id, e)
        return

    try:
        db.DB.execute(
            "INSERT INTO messages (user_id, created_at) VALUES (?, ?)",
            (user_id, now),
        )
        db.DB.commit()
    except Exception as e:  # noqa: BLE001
        logger.error("track_message: insert message for user %s: %s", user_id, e)

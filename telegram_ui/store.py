"""Per-user mode storage, in memory."""

from typing import Dict
import asyncio

from core.mode import DEFAULT_MODE, Mode


class Store:
    """Holds each user's selected mode in memory, keyed by Telegram user ID.

    Safe for concurrent use from multiple asyncio tasks (PTB dispatches
    handlers as concurrent tasks on the same event loop).
    """

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._modes: Dict[int, Mode] = {}

    async def get(self, user_id: int) -> Mode:
        """Returns the mode for user_id, or DEFAULT_MODE if none has been set."""
        async with self._lock:
            return self._modes.get(user_id, DEFAULT_MODE)

    async def set(self, user_id: int, mode: Mode) -> None:
        """Stores the mode for user_id."""
        async with self._lock:
            self._modes[user_id] = mode


def new_store() -> Store:
    """Creates an empty store."""
    return Store()

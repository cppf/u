"""Splits rendered text into chunks that fit Telegram's message length limit."""

from rendering.best_split_point import best_split_point


def split_for_telegram(text: str, limit: int) -> list[str]:
    """Splits rendered text into chunks that each fit within limit
    characters, preferring to break at paragraph, then sentence, then
    word, then character boundaries so content is never truncated or lost.
    """
    if len(text) <= limit:
        return [text]

    chunks: list[str] = []
    remaining = text
    while len(remaining) > limit:
        cut = best_split_point(remaining, limit)
        if cut <= 0:
            cut = limit
        chunks.append(remaining[:cut])
        remaining = remaining[cut:]
    if len(remaining) > 0:
        chunks.append(remaining)
    return chunks

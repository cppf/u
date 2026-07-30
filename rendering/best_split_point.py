"""Picks the best boundary at which to split long text."""

from rendering.last_index_after import last_index_after
from rendering.last_sentence_break import last_sentence_break
from rendering.last_word_break import last_word_break


def best_split_point(remaining: str, limit: int) -> int:
    """Returns an index <= limit at which to cut remaining, preferring (in
    order) a paragraph break, a sentence break, a word break, falling back
    to a hard character cut at limit.
    """
    window = remaining[:limit]

    i = last_index_after(window, "\n\n")
    if i > 0:
        return i
    i = last_sentence_break(window)
    if i > 0:
        return i
    i = last_word_break(window)
    if i > 0:
        return i
    return limit

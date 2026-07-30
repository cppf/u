"""Finds the last sentence break within a string."""

from rendering.closing_mark import is_closing_mark


_TERMINATORS = (".", "!", "?")
_TRAILING_WHITESPACE = (" ", "\n", "\t")


def last_sentence_break(s: str) -> int:
    """Returns the index immediately after the last sentence-terminating
    punctuation (plus trailing closing marks and whitespace) within s, or
    -1 if none is found.
    """
    n = len(s)
    best = -1
    i = 0
    while i < n:
        r = s[i]
        if r in _TERMINATORS:
            j = i + 1
            while j < n and is_closing_mark(s[j]):
                j += 1
            while j < n and s[j] in _TRAILING_WHITESPACE:
                j += 1
            best = j
            i = j
            continue
        i += 1
    return best

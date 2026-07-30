"""Finds the last whitespace break within a string."""

_BREAK_CHARS = (" ", "\t", "\n")


def last_word_break(s: str) -> int:
    """Returns the index immediately after the last whitespace run within s,
    or -1 if none is found.
    """
    for i in range(len(s) - 1, -1, -1):
        if s[i] in _BREAK_CHARS:
            return i + 1
    return -1

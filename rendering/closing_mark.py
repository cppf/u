"""Recognizes trailing quote/bracket marks that follow sentence punctuation."""

_CLOSING_MARKS = {'"', "'", ")", "]", "}", "\u201d", "\u2019", "\u00bb"}


def is_closing_mark(r: str) -> bool:
    """Reports whether r is a closing quote or bracket that should stay
    attached to the sentence-terminating punctuation before it.
    """
    return r in _CLOSING_MARKS

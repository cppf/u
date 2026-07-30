"""Splits text into sentences."""

from typing import List

from rendering.closing_mark import is_closing_mark


_TERMINATORS = (".", "!", "?")


def split_sentences(text: str) -> List[str]:
    """Splits text into sentences, ending each unit after a
    sentence-terminating punctuation mark (. ! ?) plus any trailing quote
    or bracket, keeping following whitespace attached to the next sentence.
    """
    units: List[str] = []
    chars = text  # Python strings already index by code point
    start = 0
    i = 0
    n = len(chars)
    while i < n:
        r = chars[i]
        if r in _TERMINATORS:
            j = i + 1
            while j < n and is_closing_mark(chars[j]):
                j += 1
            units.append(chars[start:j])
            start = j
            i = j
            continue
        i += 1
    if start < n:
        units.append(chars[start:])
    return units

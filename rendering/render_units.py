"""Splits text into units, wraps each non-blank unit in its own code span,
and reassembles them preserving original separators.
"""

from typing import Callable, List

from rendering.split_surrounding_space import split_surrounding_space
from rendering.wrap_code import wrap_code


def render_units(text: str, splitter: Callable[[str], List[str]]) -> str:
    """Splits text into units with the given splitter, wraps each non-blank
    unit in its own code span, and reassembles them using the original
    separators so surrounding whitespace/newlines are preserved.
    """
    if text.strip() == "":
        return text

    units = splitter(text)
    parts: List[str] = []
    for u in units:
        if u.strip() == "":
            parts.append(u)
            continue
        lead, core, trail = split_surrounding_space(u)
        parts.append(lead)
        parts.append(wrap_code(core))
        parts.append(trail)
    return "".join(parts)

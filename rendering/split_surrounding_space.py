"""Separates leading/trailing whitespace from the core content of a unit."""

_WHITESPACE = " \t\r\n"


def split_surrounding_space(s: str) -> tuple[str, str, str]:
    """Separates leading/trailing whitespace from the core content of a unit.

    Returns (lead, core, trail) so wrapping only touches the visible text.
    """
    trimmed_left = s.lstrip(_WHITESPACE)
    lead = s[: len(s) - len(trimmed_left)]
    trimmed_both = trimmed_left.rstrip(_WHITESPACE)
    trail = trimmed_left[len(trimmed_both):]
    core = trimmed_both
    return lead, core, trail

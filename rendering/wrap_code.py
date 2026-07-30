"""Wraps a string in a Telegram monospace code span."""


def wrap_code(s: str) -> str:
    """Wraps s in a Telegram monospace code span.

    Backticks inside s are escaped so the span cannot be broken out of.
    """
    escaped = s.replace("`", "'")
    return f"`{escaped}`"

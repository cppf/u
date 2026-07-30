"""Finds the index just after the last occurrence of a substring."""


def last_index_after(s: str, sep: str) -> int:
    """Returns the index immediately after the last occurrence of sep in s,
    or -1 if not found.
    """
    idx = s.rfind(sep)
    if idx < 0:
        return -1
    return idx + len(sep)

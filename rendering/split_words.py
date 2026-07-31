"""Splits text into words, keeping whitespace attached for lossless reassembly."""


_SPACE_CHARS = (" ", "\t", "\n", "\r")


def split_words(text: str) -> list[str]:
    """Splits text into words, keeping the whitespace between them attached
    to the following word so reassembly is lossless.
    """
    units: list[str] = []
    cur: list[str] = []
    in_space = False
    started = False

    for r in text:
        is_space = r in _SPACE_CHARS
        if not started:
            cur.append(r)
            in_space = is_space
            started = True
            continue
        if is_space == in_space:
            cur.append(r)
            continue
        if in_space:
            # transition from space to word: keep space attached ahead
            cur.append(r)
            in_space = False
            continue
        # transition from word to space: flush word, start new unit with space
        units.append("".join(cur))
        cur = [r]
        in_space = True

    if cur:
        units.append("".join(cur))
    return units

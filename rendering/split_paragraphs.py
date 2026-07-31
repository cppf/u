"""Splits text on blank-line boundaries, preserving separators."""


def split_paragraphs(text: str) -> list[str]:
    """Splits text on blank-line boundaries (one or more blank lines),
    keeping the separating newlines attached so spacing is preserved.
    """
    units: list[str] = []
    cur: list[str] = []

    # Mirror Go's strings.SplitAfter(text, "\n"): every line keeps its
    # trailing "\n" attached, and a final fragment with no trailing
    # newline (possibly empty) is included too.
    lines: list[str] = []
    start = 0
    for idx, ch in enumerate(text):
        if ch == "\n":
            lines.append(text[start:idx + 1])
            start = idx + 1
    lines.append(text[start:])

    for line in lines:
        cur.append(line)
        if line.strip() == "":
            units.append("".join(cur))
            cur = []
    if cur:
        joined = "".join(cur)
        if joined:
            units.append(joined)
    return units

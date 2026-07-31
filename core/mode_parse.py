"""Maps a settings button label back to a Mode."""

from core.mode import Mode


_BY_LABEL = {
    "Word": Mode.WORD,
    "Sentence": Mode.SENTENCE,
    "Paragraph": Mode.PARAGRAPH,
    "Full": Mode.FULL,
}


def parse_mode(label: str) -> Mode | None:
    """Maps a settings button label back to a Mode.

    Returns None if label does not match a known mode.
    """
    return _BY_LABEL.get(label)

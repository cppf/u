"""Human-readable labels for each Mode, shown on settings buttons."""

from core.mode import Mode


_LABELS = {
    Mode.WORD: "Word",
    Mode.SENTENCE: "Sentence",
    Mode.PARAGRAPH: "Paragraph",
    Mode.FULL: "Full",
}


def mode_label(mode: Mode) -> str:
    """Returns the human-readable label shown on settings buttons."""
    return _LABELS.get(mode, str(mode.value))

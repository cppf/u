"""Converts text into Telegram monospace formatting according to Mode."""

from core.mode import Mode
from rendering.render_units import render_units
from rendering.split_paragraphs import split_paragraphs
from rendering.split_sentences import split_sentences
from rendering.split_words import split_words
from rendering.wrap_code import wrap_code


def render(mode: Mode, text: str) -> str:
    """Converts text into Telegram monospace formatting according to mode.

    Each unit (word, sentence, paragraph, or the whole text) is wrapped
    individually in its own code span, separated by the same whitespace
    that originally separated the units, so content and spacing are
    preserved.
    """
    if mode == Mode.WORD:
        return render_units(text, split_words)
    if mode == Mode.SENTENCE:
        return render_units(text, split_sentences)
    if mode == Mode.PARAGRAPH:
        return render_units(text, split_paragraphs)
    # Mode.FULL, and any unrecognized value, falls through to this default.
    if text.strip() == "":
        return text
    return wrap_code(text)

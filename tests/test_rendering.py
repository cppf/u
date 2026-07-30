"""Unit tests for the rendering package's pure text-transformation logic.
No network or Telegram dependency required.
"""

from core.mode import Mode
from core.limits import TELEGRAM_MESSAGE_LIMIT
from rendering.render import render
from rendering.split_for_telegram import split_for_telegram
from rendering.split_sentences import split_sentences
from rendering.split_words import split_words
from rendering.split_paragraphs import split_paragraphs


def test_full_mode_wraps_whole_text():
    assert render(Mode.FULL, "hello world") == "`hello world`"


def test_full_mode_passes_through_whitespace_only():
    assert render(Mode.FULL, "   ") == "   "


def test_full_mode_escapes_backticks():
    assert render(Mode.FULL, "code `here`") == "`code 'here'`"


def test_word_mode_wraps_each_word():
    assert render(Mode.WORD, "hello world foo") == "`hello` `world` `foo`"


def test_sentence_mode_wraps_each_sentence():
    result = render(Mode.SENTENCE, "Hi there. How are you? Fine!")
    assert result == "`Hi there.` `How are you?` `Fine!`"


def test_paragraph_mode_wraps_each_paragraph():
    result = render(Mode.PARAGRAPH, "para one\n\npara two")
    assert result == "`para one`\n\n`para two`"


def test_sentence_mode_keeps_closing_marks_attached():
    result = split_sentences('He said "Hello!" and left.')
    assert result[0] == 'He said "Hello!"'
    assert result[1] == " and left."


def test_split_words_keeps_whitespace_attached():
    result = split_words("  hello   world  ")
    assert result == ["  hello", "   world", "  "]


def test_split_paragraphs_empty_string():
    assert split_paragraphs("") == [""]


def test_split_paragraphs_multiple_blank_lines():
    result = split_paragraphs("a\n\n\nb")
    assert result == ["a\n\n", "\n", "b"]


def test_split_for_telegram_respects_limit():
    long_text = "word " * 1000
    rendered = render(Mode.FULL, long_text)
    chunks = split_for_telegram(rendered, TELEGRAM_MESSAGE_LIMIT)
    assert len(chunks) > 1
    for chunk in chunks:
        assert len(chunk) <= TELEGRAM_MESSAGE_LIMIT
    # No content should be lost across the split.
    assert sum(len(c) for c in chunks) == len(rendered)


def test_split_for_telegram_short_text_is_single_chunk():
    assert split_for_telegram("short text", TELEGRAM_MESSAGE_LIMIT) == ["short text"]


def test_split_for_telegram_handles_multibyte_unicode():
    # Emoji and other astral-plane characters are each a single Python
    # str element (codepoint), matching the rune/char semantics used
    # throughout this port. Guards against any byte-vs-codepoint bug.
    text = "a" * 4090 + "🎉" * 10
    chunks = split_for_telegram(text, 4096)
    assert sum(len(c) for c in chunks) == len(text)
    for chunk in chunks:
        assert len(chunk) <= 4096

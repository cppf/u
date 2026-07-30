"""Mode identifies how incoming text is chunked before being wrapped in
Telegram monospace formatting.
"""

from enum import Enum


class Mode(str, Enum):
    """How incoming text is chunked before being wrapped in monospace."""

    WORD = "word"
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
    FULL = "full"


# DEFAULT_MODE is used for users who have not chosen one yet.
DEFAULT_MODE = Mode.FULL

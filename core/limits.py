"""Telegram's hard caps on text message and caption length."""

# TELEGRAM_MESSAGE_LIMIT is Telegram's hard cap on text message length, in
# UTF-16 code units. We use it conservatively as a code-point count, which
# is always <= the UTF-16 length and therefore always safe.
TELEGRAM_MESSAGE_LIMIT = 4096

# TELEGRAM_CAPTION_LIMIT is Telegram's hard cap on media caption length.
TELEGRAM_CAPTION_LIMIT = 1024

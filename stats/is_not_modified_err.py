"""Detects Telegram's harmless "message is not modified" edit error."""


def is_not_modified_err(err: Exception) -> bool:
    """Reports whether err is Telegram's "message is not modified" error,
    raised when editing a message with identical content.
    """
    if err is None:
        return False
    return "message is not modified" in str(err).lower()

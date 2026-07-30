"""Constructs the PTB Application instance."""

from telegram.ext import Application


def new_bot(token: str) -> Application:
    """Creates a python-telegram-bot Application configured with the given
    token. The webhook listener itself is started separately via
    Application.run_webhook(...) in main.py, mirroring telebot.v3's
    separate Bot construction (newBot) and Start() call.
    """
    return Application.builder().token(token).build()

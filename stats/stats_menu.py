"""Builds the inline keyboard shown under the Statistics message."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


# STATS_REFRESH_CALLBACK_DATA is the callback_data of the inline button
# that reloads the Statistics message in place. register_stats_handlers.py
# binds a CallbackQueryHandler to this exact value, mirroring telebot's
# Unique-string button binding.
STATS_REFRESH_CALLBACK_DATA = "stats_refresh"


def stats_menu() -> InlineKeyboardMarkup:
    """Builds the inline keyboard shown under the Statistics message."""
    return InlineKeyboardMarkup(
        [[InlineKeyboardButton("\U0001f504 Refresh", callback_data=STATS_REFRESH_CALLBACK_DATA)]]
    )

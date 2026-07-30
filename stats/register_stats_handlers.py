"""Wires the Statistics button on the settings keyboard and the Refresh
inline button on the resulting message.
"""

from datetime import datetime
import logging

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram_ui.settings_menu import SettingsMenuButtons

from stats.format_stats import format_stats
from stats.is_not_modified_err import is_not_modified_err
from stats.load_stats import load_stats
from stats.stats_menu import STATS_REFRESH_CALLBACK_DATA, stats_menu


logger = logging.getLogger(__name__)


def register_stats_handlers(app: Application, settings_btns: SettingsMenuButtons) -> None:
    """Wires the Statistics button on the settings keyboard and the
    Refresh inline button on the resulting message.
    """

    async def on_stats_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        try:
            s = load_stats()
        except Exception as e:  # noqa: BLE001 - mirrors Go's log-and-fallback-message
            logger.error("stats: load: %s", e)
            await update.message.reply_text(
                "Couldn't load statistics right now — please try again."
            )
            return
        await update.message.reply_text(
            format_stats(s, datetime.now()),
            reply_markup=stats_menu(),
            parse_mode=ParseMode.HTML,
        )

    async def on_stats_refresh(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        try:
            s = load_stats()
        except Exception as e:  # noqa: BLE001
            logger.error("stats: refresh: %s", e)
            await query.answer("Couldn't refresh — try again.")
            return

        try:
            await query.edit_message_text(
                format_stats(s, datetime.now()),
                reply_markup=stats_menu(),
                parse_mode=ParseMode.HTML,
            )
        except Exception as e:  # noqa: BLE001
            # Telegram errors if the content is byte-for-byte identical to
            # the current message (e.g. two refreshes within the same
            # second). That's not a real failure, so just ack silently.
            if is_not_modified_err(e):
                await query.answer("Already up to date.")
                return
            logger.error("stats: edit: %s", e)
            await query.answer("Couldn't refresh — try again.")
            return

        await query.answer("Refreshed \u2705")

    app.add_handler(MessageHandler(filters.Text([settings_btns.stats]), on_stats_button))
    app.add_handler(
        CallbackQueryHandler(on_stats_refresh, pattern=f"^{STATS_REFRESH_CALLBACK_DATA}$")
    )

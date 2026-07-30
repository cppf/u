"""Wires up the Word/Sentence/Paragraph/Full buttons on the settings keyboard."""

from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters
from telegram_ui.mode_handler import mode_handler
from telegram_ui.settings_menu import SettingsMenuButtons
from telegram_ui.store import Store

from core.mode import Mode


def register_settings_handlers(
    app: Application,
    st: Store,
    settings_btns: SettingsMenuButtons,
    main_menu: ReplyKeyboardMarkup,
) -> None:
    """Wires up the Word/Sentence/Paragraph/Full buttons on the settings
    keyboard.
    """
    app.add_handler(
        MessageHandler(filters.Text([settings_btns.word]), mode_handler(st, main_menu, Mode.WORD))
    )
    app.add_handler(
        MessageHandler(
            filters.Text([settings_btns.sentence]), mode_handler(st, main_menu, Mode.SENTENCE)
        )
    )
    app.add_handler(
        MessageHandler(
            filters.Text([settings_btns.paragraph]), mode_handler(st, main_menu, Mode.PARAGRAPH)
        )
    )
    app.add_handler(
        MessageHandler(filters.Text([settings_btns.full]), mode_handler(st, main_menu, Mode.FULL))
    )

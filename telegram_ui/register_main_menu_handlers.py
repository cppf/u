"""Wires up /start plus the Start, Settings, and Back buttons."""

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram_ui.main_menu import MainMenuButtons
from telegram_ui.settings_menu import SettingsMenuButtons
from telegram_ui.store import Store
from telegram_ui.welcome_text import WELCOME_TEXT

from core.mode_label import mode_label


def register_main_menu_handlers(
    app: Application,
    st: Store,
    main_btns: MainMenuButtons,
    main_menu: ReplyKeyboardMarkup,
    settings_btns: SettingsMenuButtons,
    settings_menu: ReplyKeyboardMarkup,
) -> None:
    """Wires up /start plus the Start, Settings, and Back buttons."""

    async def on_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(WELCOME_TEXT, reply_markup=main_menu)

    async def on_start_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(WELCOME_TEXT, reply_markup=main_menu)

    async def on_settings_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        current = await st.get(update.effective_user.id)
        await update.message.reply_text(
            f"Current mode: {mode_label(current)}\n\nChoose a mode:",
            reply_markup=settings_menu,
        )

    async def on_back_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Back to main menu.", reply_markup=main_menu)

    app.add_handler(CommandHandler("start", on_start))
    app.add_handler(MessageHandler(filters.Text([main_btns.start]), on_start_button))
    app.add_handler(MessageHandler(filters.Text([main_btns.settings]), on_settings_button))
    app.add_handler(MessageHandler(filters.Text([settings_btns.back]), on_back_button))

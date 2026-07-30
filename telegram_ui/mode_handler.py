"""Handler factory for mode-select buttons."""

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram_ui.store import Store

from core.mode import Mode
from core.mode_label import mode_label


def mode_handler(store: Store, main_menu: ReplyKeyboardMarkup, mode: Mode):
    """Returns a handler that sets the sender's mode to mode and confirms
    the change, returning to the main menu.
    """

    async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await store.set(update.effective_user.id, mode)
        await update.message.reply_text(
            f"Mode set to {mode_label(mode)}.", reply_markup=main_menu
        )

    return handler

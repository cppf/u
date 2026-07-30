"""Wires up handling of incoming text messages and media."""

from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters
from telegram_ui.handle_media import handle_media
from telegram_ui.send_rendered import send_rendered
from telegram_ui.store import Store


# MEDIA_FILTER covers the same set of message types as telebot's OnMedia:
# photos, videos, animations, audio, voice, documents, stickers, and
# video notes.
MEDIA_FILTER = (
    filters.PHOTO
    | filters.VIDEO
    | filters.ANIMATION
    | filters.AUDIO
    | filters.VOICE
    | filters.Document.ALL
    | filters.Sticker.ALL
    | filters.VIDEO_NOTE
)


def register_content_handlers(app: Application, st: Store, main_menu: ReplyKeyboardMarkup) -> None:
    """Wires up handling of incoming text messages and media (photos,
    videos, voice notes, etc.).
    """

    async def on_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        mode = await st.get(update.effective_user.id)
        await send_rendered(update.message, mode, update.message.text, main_menu)

    async def on_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        mode = await st.get(update.effective_user.id)
        await handle_media(update.message, mode, main_menu)

    # ~filters.COMMAND excludes /start and other commands, which are
    # handled separately by CommandHandler.
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, on_text))
    app.add_handler(MessageHandler(MEDIA_FILTER, on_media))

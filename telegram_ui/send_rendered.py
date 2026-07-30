"""Renders text under a mode and sends it, splitting across messages if needed."""

from telegram import Message, ReplyKeyboardMarkup
from telegram.constants import ParseMode

from core.limits import TELEGRAM_MESSAGE_LIMIT
from core.mode import Mode
from rendering.render import render
from rendering.split_for_telegram import split_for_telegram


async def send_rendered(message: Message, mode: Mode, text: str, menu: ReplyKeyboardMarkup) -> None:
    """Renders text under mode and sends it, splitting across multiple
    messages if needed to respect Telegram's length limit.
    """
    rendered = render(mode, text)
    chunks = split_for_telegram(rendered, TELEGRAM_MESSAGE_LIMIT)
    for i, chunk in enumerate(chunks):
        reply_markup = menu if i == len(chunks) - 1 else None
        await message.chat.send_message(
            chunk, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup
        )

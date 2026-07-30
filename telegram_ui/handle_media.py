"""Re-sends received media with its caption rendered in the selected mode."""

from typing import List

from telegram import Message, ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram_ui.resend_media import resend_media

from core.limits import TELEGRAM_CAPTION_LIMIT
from core.mode import Mode
from rendering.render import render
from rendering.split_for_telegram import split_for_telegram


async def handle_media(message: Message, mode: Mode, menu: ReplyKeyboardMarkup) -> None:
    """Re-sends the received media with its caption rendered in the
    selected mode. If the rendered caption exceeds Telegram's caption
    limit, the media is sent with the first chunk as caption and any
    remaining chunks are sent as follow-up text messages so no content is
    lost.
    """
    chunks: List[str] = []
    if message.caption:
        rendered = render(mode, message.caption)
        chunks = split_for_telegram(rendered, TELEGRAM_CAPTION_LIMIT)

    first_caption = chunks[0] if chunks else ""
    media_reply_markup = menu if len(chunks) <= 1 else None

    await resend_media(message, first_caption, media_reply_markup)

    if len(chunks) <= 1:
        return

    rest = chunks[1:]
    for i, chunk in enumerate(rest):
        reply_markup = menu if i == len(rest) - 1 else None
        await message.chat.send_message(
            chunk, parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup
        )

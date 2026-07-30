"""Re-sends the same media file back to the chat, preserving its type."""

from typing import Optional

from telegram import Message, ReplyKeyboardMarkup
from telegram.constants import ParseMode


async def resend_media(
    message: Message,
    caption: str,
    reply_markup: Optional[ReplyKeyboardMarkup],
) -> None:
    """Sends the same media file back to the chat with the given caption,
    preserving the original media type. Uses Telegram's file_id so the
    file is re-sent without re-uploading it.
    """
    chat = message.chat
    kwargs = dict(parse_mode=ParseMode.MARKDOWN, reply_markup=reply_markup)

    if message.photo:
        # message.photo is a list of PhotoSize at increasing resolutions;
        # the last one is the highest resolution, mirroring what Telegram
        # itself considers "the" photo for re-send purposes.
        await chat.send_photo(photo=message.photo[-1].file_id, caption=caption, **kwargs)
    elif message.video:
        await chat.send_video(video=message.video.file_id, caption=caption, **kwargs)
    elif message.animation:
        await chat.send_animation(animation=message.animation.file_id, caption=caption, **kwargs)
    elif message.audio:
        await chat.send_audio(audio=message.audio.file_id, caption=caption, **kwargs)
    elif message.voice:
        await chat.send_voice(voice=message.voice.file_id, caption=caption, **kwargs)
    elif message.document:
        await chat.send_document(document=message.document.file_id, caption=caption, **kwargs)
    elif message.sticker:
        await chat.send_sticker(sticker=message.sticker.file_id, reply_markup=reply_markup)
    elif message.video_note:
        await chat.send_video_note(video_note=message.video_note.file_id, reply_markup=reply_markup)
    else:
        await chat.send_message("Unsupported media type.", reply_markup=reply_markup)

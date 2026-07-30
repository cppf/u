"""Cross-cutting handler that records every incoming update as a message.

python-telegram-bot has no direct equivalent to telebot's bot.Use(...)
middleware. The idiomatic PTB mechanism for "run this for every update,
regardless of which other handler also matches it" is a TypeHandler
registered in its own handler group — PTB processes groups in ascending
order and independently, so a handler in an earlier group does not stop
handlers in later groups from also running for the same update.
register_track_middleware wires this up in group -1, ahead of every
other handler (all registered in the default group 0).
"""

from telegram import Update
from telegram.ext import Application, ContextTypes, TypeHandler

from stats.track_message import track_message


# TRACK_MIDDLEWARE_GROUP runs before the default group (0) so every
# update is counted no matter which other handler(s) also process it.
TRACK_MIDDLEWARE_GROUP = -1


def register_track_middleware(app: Application) -> None:
    """Registers a handler that records every incoming update (text,
    caption, media, sticker, document, callback, etc.) as exactly one
    message for the sending user, then lets normal handler dispatch
    continue unaffected.
    """

    async def on_any_update(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        user = update.effective_user
        if user is not None:
            track_message(user.id)

    app.add_handler(TypeHandler(Update, on_any_update), group=TRACK_MIDDLEWARE_GROUP)

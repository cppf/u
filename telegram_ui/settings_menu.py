"""Builds the settings keyboard (Word/Sentence/Paragraph/Full/Stats/Back)."""

from dataclasses import dataclass

from telegram import KeyboardButton, ReplyKeyboardMarkup

from core.mode import Mode
from core.mode_label import mode_label


@dataclass(frozen=True)
class SettingsMenuButtons:
    """Groups the button labels on the settings keyboard so handlers can be
    registered against the same values used to build the menu.
    """

    word: str
    sentence: str
    paragraph: str
    full: str
    stats: str
    back: str


def new_settings_menu() -> tuple[ReplyKeyboardMarkup, SettingsMenuButtons]:
    """Builds the settings keyboard (one button per Mode, plus Statistics
    and Back) and returns it along with its button labels for handler
    registration.
    """
    btns = SettingsMenuButtons(
        word=mode_label(Mode.WORD),
        sentence=mode_label(Mode.SENTENCE),
        paragraph=mode_label(Mode.PARAGRAPH),
        full=mode_label(Mode.FULL),
        stats="\U0001f4ca Statistics",
        back="\u2b05\ufe0f Back",
    )
    menu = ReplyKeyboardMarkup(
        [
            [KeyboardButton(btns.word), KeyboardButton(btns.sentence)],
            [KeyboardButton(btns.paragraph), KeyboardButton(btns.full)],
            [KeyboardButton(btns.stats)],
            [KeyboardButton(btns.back)],
        ],
        resize_keyboard=True,
    )
    return menu, btns

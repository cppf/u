"""Builds the main persistent keyboard (Start, Settings)."""

from dataclasses import dataclass

from telegram import KeyboardButton, ReplyKeyboardMarkup


@dataclass(frozen=True)
class MainMenuButtons:
    """Groups the button labels on the main persistent keyboard so
    handlers can be registered against the same values used to build
    the menu.
    """

    start: str
    settings: str


def new_main_menu() -> tuple[ReplyKeyboardMarkup, MainMenuButtons]:
    """Builds the main persistent keyboard (Start, Settings) and returns it
    along with its button labels for handler registration.
    """
    btns = MainMenuButtons(start="\u25b6\ufe0f Start", settings="\u2699\ufe0f Settings")
    menu = ReplyKeyboardMarkup(
        [[KeyboardButton(btns.start), KeyboardButton(btns.settings)]],
        resize_keyboard=True,
    )
    return menu, btns

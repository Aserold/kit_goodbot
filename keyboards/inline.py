from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_buttons_inline(
        *,
        buttons: dict[str, ...],
        sizes: tuple[int, ...] = (2,)
):
    keyboard = InlineKeyboardBuilder()

    for text, value in buttons.items():
        if "://" in value:
            keyboard.add(InlineKeyboardButton(text=text, url=value))
        else:
            keyboard.add(InlineKeyboardButton(text=text, callback_data=value))

    return keyboard.adjust(*sizes).as_markup()

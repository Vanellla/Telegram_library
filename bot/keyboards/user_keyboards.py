from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_kb() -> InlineKeyboardMarkup:
    """Get kb for main menu
    """
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Мой id', callback_data='get_my_id')]
    ])

    return ikb
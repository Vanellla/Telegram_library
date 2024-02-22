from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_kb() -> InlineKeyboardMarkup:
    """Get kb for main menu
    """
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Справочники', callback_data='references')],
        [InlineKeyboardButton(text='Книги', callback_data='books_main')]
    ])

    return ikb


def return_to_main_menu_button():
    return InlineKeyboardButton(text='🔙 Вернуться в меню', callback_data='back_to_main_menu')


def main_references_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Авторы', callback_data='authors'))
    builder.row(InlineKeyboardButton(text='Жанры', callback_data='genres'))
    builder.row(InlineKeyboardButton(text='Параллели', callback_data='parallels'))
    builder.row(InlineKeyboardButton(text='Классы', callback_data='klasses'))
    builder.row(InlineKeyboardButton(text='Ученики', callback_data='students'))
    builder.row(return_to_main_menu_button())
    builder.adjust(2,2,1)
    return builder.as_markup()


def back_to_main_menu() -> InlineKeyboardMarkup:
    """Get kb for main menu
    """
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Вернуться в меню', callback_data='back_to_main_menu')]
    ])

    return ikb


def cancel_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='отмена', callback_data='back_to_main_menu')]
    ])

    return ikb


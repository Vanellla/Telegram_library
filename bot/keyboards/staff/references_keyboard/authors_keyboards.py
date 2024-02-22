from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional


class AuthorCallbackFactory(CallbackData, prefix="author"):
    action: str
    id: Optional[int] = None


def return_to_main_menu_button():
    return InlineKeyboardButton(text='🔙 Вернуться в меню', callback_data='back_to_main_menu')


def main_author_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Добавить автора', callback_data=AuthorCallbackFactory(action='add'))
    builder.button(text='Просмотреть список', callback_data=AuthorCallbackFactory(action='search'))
    builder.button(text='🔙 Назад', callback_data='references')
    builder.adjust(2)
    return builder.as_markup()


def author_cancel_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='отмена', callback_data='authors')]
    ])
    return ikb


def authors_list_kb(authors) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for author in authors:
        builder.button(text=author.fio, callback_data=AuthorCallbackFactory(action='open', id=author.id))
    builder.button(text='🔙 Назад', callback_data='authors')
    builder.adjust(1)
    return builder.as_markup()


def current_author_kb(author) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='✏️ редактировать', callback_data=AuthorCallbackFactory(action='edit', id=author.id))
    builder.button(text='❌ удалить', callback_data=AuthorCallbackFactory(action='delete', id=author.id))
    builder.button(text='🔙 Назад', callback_data='authors')
    builder.adjust(1)
    return builder.as_markup()

def author_delete_confirm(author_id):
    builder = InlineKeyboardBuilder()
    builder.button(text='Удалить', callback_data=AuthorCallbackFactory(action='delete_confirmed', id=author_id))
    builder.button(text='Отмена', callback_data=AuthorCallbackFactory(action='open', id=author_id))
    builder.adjust(1)
    return builder.as_markup()

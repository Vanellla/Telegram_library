from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional


class GenreCallbackFactory(CallbackData, prefix="genre"):
    action: str
    id: Optional[int] = None


def return_to_main_menu_button():
    return InlineKeyboardButton(text='🔙 Вернуться в меню', callback_data='back_to_main_menu')


def main_genres_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Добавить жанр', callback_data=GenreCallbackFactory(action='add'))
    builder.button(text='Поиск', callback_data=GenreCallbackFactory(action='search'))
    builder.button(text='Просмотреть весь список', callback_data=GenreCallbackFactory(action='genre_list'))
    builder.button(text='🔙 Назад', callback_data='references')
    builder.adjust(2,1)
    return builder.as_markup()


def genre_cancel_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='отмена', callback_data='genres')]
    ])
    return ikb


def genres_list_kb(genres) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for genre in genres:
        builder.button(text=genre.name, callback_data=GenreCallbackFactory(action='open', id=genre.id))
    builder.button(text='🔙 Назад', callback_data='genres')
    builder.adjust(1)
    return builder.as_markup()


def current_genre_kb(genre) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='✏️ редактировать', callback_data=GenreCallbackFactory(action='edit', id=genre.id))
    builder.button(text='❌ удалить', callback_data=GenreCallbackFactory(action='delete', id=genre.id))
    builder.button(text='🔙 Назад', callback_data='genres')
    builder.adjust(1)
    return builder.as_markup()


def genre_delete_confirm(genre_id):
    builder = InlineKeyboardBuilder()
    builder.button(text='Удалить', callback_data=GenreCallbackFactory(action='delete_confirmed', id=genre_id))
    builder.button(text='Отмена', callback_data=GenreCallbackFactory(action='open', id=genre_id))
    builder.adjust(1)
    return builder.as_markup()

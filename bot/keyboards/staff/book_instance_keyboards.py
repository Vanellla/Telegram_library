from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional


class BookInstanceCallbackFactory(CallbackData, prefix="book_instance"):
    action: str
    id: Optional[int] = None


# class BookInstanceSettingsCallbackFactory(CallbackData, prefix="settingsbook"):
#     action: str
#     config: Optional[str] = None
#     id: Optional[int] = None


# class BookSearchCallbackFactory(CallbackData, prefix="booksearch"):
#     action: Optional[str] = None
#     page: Optional[int] = 1
#     id: Optional[int] = None


def main_book_instance_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Добавить экземпляры', callback_data=BookInstanceCallbackFactory(action='add_instance'))
    # builder.button(text='Найти книгу', callback_data=BookInstanceCallbackFactory(action='search_book'))
    builder.button(text='🔙 Назад', callback_data='book_instance')
    builder.adjust(1)
    return builder.as_markup()


def parallel_choice_kb(parallels, action) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for p in parallels:
        builder.button(text=p.name, callback_data=BookCallbackFactory(action=action, id=p.id))
    builder.button(text='🔙 Назад', callback_data='books_main')
    builder.adjust(4, 5, 2, 1)
    return builder.as_markup()


def genre_choice_kb(genres, action) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for g in genres:
        builder.button(text=g.name, callback_data=BookCallbackFactory(action=action, id=g.id))
    builder.button(text='🔙 Назад', callback_data='books_main')
    builder.adjust(1)
    return builder.as_markup()


def author_choice_kb(authors, action) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for author in authors:
        builder.button(text=author.fio, callback_data=BookCallbackFactory(action=action, id=author.id))
    builder.button(text='🔙 Назад', callback_data='books_main')
    builder.adjust(1)
    return builder.as_markup()


def book_cancel_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='отмена', callback_data='books_main')]
    ])
    return ikb


def book_back_to_main_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Назад', callback_data='books_main')]
    ])
    return ikb


def book_search_settings_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='⚙️ жанр', callback_data=BookSettingsCallbackFactory(action='search_book', config='genre'))
    builder.button(text='⚙️ параллель',
                   callback_data=BookSettingsCallbackFactory(action='search_book', config='parallel'))
    builder.button(text='⚙️ автор',
                   callback_data=BookSettingsCallbackFactory(action='search_book_message', config='author'))
    builder.button(text='⚙️ название',
                   callback_data=BookSettingsCallbackFactory(action='search_book_message', config='book_name'))
    builder.button(text='🔍 начать поиск',
                   callback_data=BookSearchCallbackFactory(page=1))
    builder.button(text='🔙 отмена', callback_data='books_main')
    builder.adjust(2, 2, 1)
    return builder.as_markup()


def genre_config_kb(genres, action) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for g in genres:
        builder.button(text=g.name, callback_data=BookSettingsCallbackFactory(action=action, id=g.id, config='genre'))
    builder.button(text='🧹очистить',
                   callback_data=BookSettingsCallbackFactory(action=action, id=777, config='genre_clear'))
    builder.button(text='🔙 отмена', callback_data=BookSettingsCallbackFactory(action='search_book'))
    builder.adjust(2)
    return builder.as_markup()


def parallel_config_kb(parallels, action) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for p in parallels:
        builder.button(text=p.name,
                       callback_data=BookSettingsCallbackFactory(action=action, id=p.id, config='parallel'))
    builder.button(text='🧹очистить',
                   callback_data=BookSettingsCallbackFactory(action=action, id=777, config='parallel_clear'))
    builder.button(text='🔙 отмена', callback_data=BookSettingsCallbackFactory(action='search_book'))
    builder.adjust(4, 5, 2, 1)
    return builder.as_markup()


def back_to_search_settings(config):
    builder = InlineKeyboardBuilder()
    builder.button(text='отмена', callback_data=BookSettingsCallbackFactory(action='search_book'))
    if config != '':
        builder.button(text='🧹очистить',
                       callback_data=BookSettingsCallbackFactory(action='search_book', id=777, config=config))
    builder.adjust(2)
    return builder.as_markup()

def back_to_search_settings_from_book_info():
    builder = InlineKeyboardBuilder()
    builder.button(text='отмена', callback_data=BookSettingsCallbackFactory(action='search_book'))
    builder.adjust(1)
    return builder.as_markup()


def author_config_kb(authors, action, config) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for author in authors:
        builder.button(text=author.fio,
                       callback_data=BookSettingsCallbackFactory(action=action, id=author.id, config=config))
    builder.button(text='🔙 Назад', callback_data='search_book')
    builder.adjust(1)
    return builder.as_markup()


def book_search_result_kb(books, page=1, pagination=10) -> InlineKeyboardMarkup:
    l, r = page * pagination - pagination, page * pagination
    books_slice = books[l:r]
    arrow_buttons = 0
    builder = InlineKeyboardBuilder()
    for book in books_slice:
        builder.button(text=book.name,
                       callback_data=BookSearchCallbackFactory(id=book.id, action='book_info_open'))
    if l >= pagination:
        builder.button(text='предыдущие', callback_data=BookSearchCallbackFactory(page=page - 1))
        arrow_buttons += 1
    if len(books) > r:
        builder.button(text='следующие', callback_data=BookSearchCallbackFactory(page=page + 1))
        arrow_buttons += 1
    builder.button(text='🔙 к настройкам поиска', callback_data=BookSettingsCallbackFactory(action='search_book'))
    if len(books_slice) < pagination:
        pagination = len(books_slice)
    arrow_buttons = 1 if arrow_buttons == 0 else arrow_buttons
    builder.adjust(*[1 for _ in range(pagination)], arrow_buttons, 1)
    # builder.row(KeButton(text='🔙 к настройкам поиска', callback_data=BookSettingsCallbackFactory(action='search_book'))
    return builder.as_markup()

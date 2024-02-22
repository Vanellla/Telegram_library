from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional


class KlassCallbackFactory(CallbackData, prefix="klasses"):
    action: str
    id: Optional[int] = None


def main_klasses_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Добавить класс', callback_data=KlassCallbackFactory(action='add_klass'))
    builder.button(text='Просмотреть список', callback_data=KlassCallbackFactory(action='search_klass'))
    builder.button(text='🔙 Назад', callback_data='references')
    builder.adjust(2)
    return builder.as_markup()


def klass_parallel_choice_kb(parallels, action) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for p in parallels:
        builder.button(text=p.name, callback_data=KlassCallbackFactory(action=action, id=p.id))
    builder.button(text='🔙 Назад', callback_data='klasses')
    builder.adjust(4, 5, 2, 1)
    return builder.as_markup()


def klass_choice_kb(klasses) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for klass in klasses:
        builder.button(text=klass.name, callback_data=KlassCallbackFactory(action='open', id=klass.id))
    builder.adjust(8)
    builder.row(InlineKeyboardButton(text='🔙 Назад', callback_data='klasses'))
    return builder.as_markup()


def klass_cancel_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='отмена', callback_data='klasses')]
    ])
    return ikb


def current_klass_kb(klass_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='✏️ изменить название', callback_data=KlassCallbackFactory(action='edit_name', id=klass_id))
    builder.button(text='🏷️ изменить параллель',
                   callback_data=KlassCallbackFactory(action='edit_parallel', id=klass_id))
    builder.button(text='📋 скачать коды',
                   callback_data=KlassCallbackFactory(action='download_codes', id=klass_id))
    builder.button(text='❌ удалить', callback_data=KlassCallbackFactory(action='delete', id=klass_id))
    builder.button(text='🔙 Назад', callback_data='klasses')
    builder.adjust(1)
    return builder.as_markup()


def klass_delete_confirm(klass_id):
    builder = InlineKeyboardBuilder()
    builder.button(text='Удалить', callback_data=KlassCallbackFactory(action='delete_confirmed', id=klass_id))
    builder.button(text='Отмена', callback_data=KlassCallbackFactory(action='open', id=klass_id))
    builder.adjust(1)
    return builder.as_markup()

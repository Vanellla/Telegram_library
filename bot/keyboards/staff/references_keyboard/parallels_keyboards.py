from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional


class ParallelCallbackFactory(CallbackData, prefix="parallel"):
    action: str
    id: Optional[int] = None




def main_parallel_kb(parallels) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for p in parallels:
        builder.button(text=p.name, callback_data='#')
    builder.button(text='🔙 Назад', callback_data='references')
    builder.adjust(4,5,2,1)
    return builder.as_markup()



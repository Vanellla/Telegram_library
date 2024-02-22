from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Optional


class StudentCallbackFactory(CallbackData, prefix="students"):
    action: str
    id: Optional[int] = None
    page: Optional[int] = None


def main_students_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='Добавить ученика', callback_data=StudentCallbackFactory(action='add_student'))
    builder.button(text='Найти ученика', callback_data=StudentCallbackFactory(action='search_student'))
    builder.button(text='🔙 Назад', callback_data='references')
    builder.adjust(1)
    return builder.as_markup()


def student_parallel_choice_kb(parallels, action) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for p in parallels:
        builder.button(text=p.name, callback_data=StudentCallbackFactory(action=action, id=p.id))
    builder.button(text='🔙 Назад', callback_data='students')
    builder.adjust(4, 5, 2, 1)
    return builder.as_markup()


def student_klass_choice_kb(klasses, action) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for klass in klasses:
        builder.button(text=klass.name, callback_data=StudentCallbackFactory(action=action, id=klass.id))
    builder.adjust(8)
    builder.row(InlineKeyboardButton(text='🔙 Назад', callback_data='students'))
    return builder.as_markup()


def student_cancel_kb() -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='отмена', callback_data='students')]
    ])
    return ikb


def student_search_type_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='по фамилии', callback_data=StudentCallbackFactory(action='search_by_fio'))
    builder.button(text='по классу', callback_data=StudentCallbackFactory(action='search_by_klass'))
    builder.button(text='🔙 Назад', callback_data='students')
    builder.adjust(2)
    return builder.as_markup()


def student_search_result(students, action, parent_action, page=1, with_klass=False,
                          klass_id=None) -> InlineKeyboardMarkup:
    if page == None:
        page = 1
    builder = InlineKeyboardBuilder()
    l, r = page * 10 - 10, page * 10
    students_slice = list(students)[l:r]
    for i, student in enumerate(students_slice, start=l + 1):
        name = f'{i}) '
        name += f'{student.klass.name}) ' if with_klass == True else ''
        name += student.fio
        builder.button(text=name, callback_data=StudentCallbackFactory(action=action, id=student.id))
    if l > 9:
        builder.button(text='предыдущие',
                       callback_data=StudentCallbackFactory(action=parent_action, id=klass_id, page=page - 1))
    if len(students) > r:
        builder.button(text='следующие',
                       callback_data=StudentCallbackFactory(action=parent_action, id=klass_id, page=page + 1))

    builder.adjust(*[1 for i in range(len(students))], 2, 1)
    builder.row(InlineKeyboardButton(text='🔙 Назад', callback_data='students'))
    return builder.as_markup()


def student_search_result_by_fio_kb(students, action, with_klass=False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i, student in enumerate(students, start=1):
        name = f'{i}) '
        name += f'{student.klass.name}) ' if with_klass == True else ''
        name += student.fio
        builder.button(text=name, callback_data=StudentCallbackFactory(action=action, id=student.id))
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text='🔙 Назад', callback_data='students'))
    return builder.as_markup()


def current_student_kb(student_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(text='Выдать книгу', callback_data=StudentCallbackFactory(action='book_issuance', id=student_id))
    builder.button(text='Список уже выданных книг', callback_data=StudentCallbackFactory(action='books', id=student_id))
    builder.button(text='✏️ изменить ФИО', callback_data=StudentCallbackFactory(action='edit_name', id=student_id))
    builder.button(text='🏷️ изменить класс',
                   callback_data=StudentCallbackFactory(action='edit_klass', id=student_id))
    builder.button(text='❌ удалить', callback_data=StudentCallbackFactory(action='delete', id=student_id))
    builder.button(text='🔙 Назад', callback_data='students')
    builder.adjust(1)
    return builder.as_markup()


def student_delete_confirm(student_id):
    builder = InlineKeyboardBuilder()
    builder.button(text='Удалить', callback_data=StudentCallbackFactory(action='delete_confirmed', id=student_id))
    builder.button(text='Отмена', callback_data=StudentCallbackFactory(action='open', id=student_id))
    builder.adjust(1)
    return builder.as_markup()


def student_book_issuance(student_id):
    builder = InlineKeyboardBuilder()
    builder.button(text='Выдать', callback_data=StudentCallbackFactory(action='issuance_complete', id=student_id))
    builder.button(text='🔙 Отмена', callback_data='students')
    builder.adjust(1)
    return builder.as_markup()

def back_to_student(student_id):
    builder = InlineKeyboardBuilder()
    builder.button(text='🔙 Назад', callback_data=StudentCallbackFactory(action='open', id=student_id))
    builder.adjust(1)
    return builder.as_markup()
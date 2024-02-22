from aiogram import types, F, Router, Bot
from typing import Optional
from aiogram.filters.callback_data import CallbackData

from bot.keyboards.staff import main_author_kb, AuthorCallbackFactory, author_cancel_kb, authors_list_kb, \
    current_author_kb, author_delete_confirm
from aiogram.fsm.context import FSMContext

from bot.states.staff_states import Content_add
from db import Author

authors_router = Router()


@authors_router.callback_query(F.data == 'authors')
async def authors(clb: types.CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await state.clear()
    reply_text = 'Выберите действие:'
    await bot.edit_message_text(chat_id=clb.message.chat.id, message_id=clb.message.message_id, text=reply_text,
                                reply_markup=main_author_kb())


@authors_router.callback_query(AuthorCallbackFactory.filter(F.action == "add"))
async def callbacks_author_add_fab(callback: types.CallbackQuery, callback_data: AuthorCallbackFactory,
                                   state: FSMContext):
    await state.set_state(Content_add.author_add)
    await state.update_data(msg_id=callback.message.message_id)
    text = 'Введите Фамилию Имя Отчество автора'
    await callback.message.edit_text(text=text, reply_markup=author_cancel_kb())


@authors_router.message(Content_add.author_add)
async def author_add(msg: types.Message, state: FSMContext, bot: Bot):
    author_name = msg.text.title()
    author = Author.create(fio=author_name)
    contex_data = await state.get_data()
    msg_id = contex_data.get('msg_id')
    # await bot.delete_message(chat_id=msg.chat.id, message_id=msg_id)
    await msg.delete()
    await state.clear()
    text = f'Создан автор № {author.id}) {author.fio}'
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text, reply_markup=main_author_kb())


@authors_router.callback_query(AuthorCallbackFactory.filter(F.action == "search"))
async def callbacks_author_search(callback: types.CallbackQuery, callback_data: AuthorCallbackFactory,
                                  state: FSMContext):
    await state.set_state(Content_add.author_search)
    await state.update_data(msg_id=callback.message.message_id)
    text = 'Введите Фамилию Имя Отчество автора (можно хотябы фамилию)'
    await callback.message.edit_text(text=text, reply_markup=author_cancel_kb())


@authors_router.message(Content_add.author_search)
async def author_search(msg: types.Message, state: FSMContext, bot: Bot):
    author_name = msg.text.title()
    authors = Author.select().where(Author.fio.contains(author_name))
    contex_data = await state.get_data()
    msg_id = contex_data.get('msg_id')
    await msg.delete()
    await state.clear()
    if authors.count() > 0:
        text = f'Вот, что удалось найти в базе библиотеки:'
        await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text,
                                    reply_markup=authors_list_kb(authors))
    else:
        text = f'Не удалось найти подходящего автора.'
        await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text, reply_markup=author_cancel_kb())


@authors_router.callback_query(AuthorCallbackFactory.filter(F.action == "open"))
async def callbacks_author_open(callback: types.CallbackQuery, callback_data: AuthorCallbackFactory,
                                state: FSMContext):
    author_id = callback_data.id
    author = Author.get(id=author_id)
    text = author.fio
    await callback.message.edit_text(text=text, reply_markup=current_author_kb(author))


@authors_router.callback_query(AuthorCallbackFactory.filter(F.action == "edit"))
async def callbacks_author_edit1(callback: types.CallbackQuery, callback_data: AuthorCallbackFactory,
                                 state: FSMContext):
    author_id = callback_data.id
    await state.set_state(Content_add.author_edit)
    await state.update_data(msg_id=callback.message.message_id)
    await state.update_data(author_id=author_id)
    text = 'Введите новые Фамилию Имя Отчество автора'
    await callback.message.edit_text(text=text, reply_markup=author_cancel_kb())


@authors_router.message(Content_add.author_edit)
async def author_edit2(msg: types.Message, state: FSMContext, bot: Bot):
    new_author_name = msg.text.title()
    contex_data = await state.get_data()
    msg_id = contex_data.get('msg_id')
    author_id = contex_data.get('author_id')
    author = Author.get(id=author_id)
    author.fio = new_author_name
    author.save()
    await msg.delete()
    await state.clear()
    text = f'Имя автора изменено на {new_author_name}.'
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text, reply_markup=main_author_kb())


@authors_router.callback_query(AuthorCallbackFactory.filter(F.action == "delete"))
async def callbacks_author_delete(callback: types.CallbackQuery, callback_data: AuthorCallbackFactory,
                                  state: FSMContext):
    author_id = callback_data.id
    text = callback.message.text + '\nУверены, что хотите удалить автора?'
    await callback.message.edit_text(text=text, reply_markup=author_delete_confirm(author_id))


@authors_router.callback_query(AuthorCallbackFactory.filter(F.action == "delete_confirmed"))
async def callbacks_author_delete(callback: types.CallbackQuery, callback_data: AuthorCallbackFactory,
                                  state: FSMContext):
    author_id = callback_data.id
    author = Author.get(id=author_id)
    author_name = author.fio
    author.delete_instance()
    text = f'Автор {author_name} удалён.'
    await callback.message.edit_text(text=text, reply_markup=main_author_kb())

from aiogram import types, F, Router, Bot
from typing import Optional
from aiogram.filters.callback_data import CallbackData

from bot.keyboards.staff import main_genres_kb, GenreCallbackFactory, genre_cancel_kb, genres_list_kb, current_genre_kb, \
    genre_delete_confirm
from aiogram.fsm.context import FSMContext

from bot.states.staff_states import Content_add
from db import Genre

genre_router = Router()


@genre_router.callback_query(F.data == 'genres')
async def genres(clb: types.CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await state.clear()
    reply_text = 'Выберите действие:'
    await bot.edit_message_text(chat_id=clb.message.chat.id, message_id=clb.message.message_id, text=reply_text,
                                reply_markup=main_genres_kb())


@genre_router.callback_query(GenreCallbackFactory.filter(F.action == "add"))
async def callbacks_genre_add_fab(callback: types.CallbackQuery, callback_data: GenreCallbackFactory,
                                  state: FSMContext):
    await state.set_state(Content_add.genre_add)
    await state.update_data(msg_id=callback.message.message_id)
    text = 'Введите название жанра'
    await callback.message.edit_text(text=text, reply_markup=genre_cancel_kb())


@genre_router.message(Content_add.genre_add)
async def genre_add(msg: types.Message, state: FSMContext, bot: Bot):
    genre_name = msg.text.title()
    genre = Genre.create(name=genre_name)
    contex_data = await state.get_data()
    msg_id = contex_data.get('msg_id')
    await msg.delete()
    await state.clear()
    text = f'Создан жанр № {genre.id}) {genre.name}'
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text, reply_markup=main_genres_kb())


@genre_router.callback_query(GenreCallbackFactory.filter(F.action == "genre_list"))
async def callbacks_genre_search(callback: types.CallbackQuery, callback_data: GenreCallbackFactory,
                                 state: FSMContext):
    genres = Genre.select()
    text = 'Список жанров:'
    await callback.message.edit_text(text=text, reply_markup=genres_list_kb(genres))


@genre_router.callback_query(GenreCallbackFactory.filter(F.action == "search"))
async def callbacks_genre_search(callback: types.CallbackQuery, callback_data: GenreCallbackFactory,
                                 state: FSMContext):
    await state.set_state(Content_add.genre_search)
    await state.update_data(msg_id=callback.message.message_id)
    text = 'Введите название жанра'
    await callback.message.edit_text(text=text, reply_markup=genre_cancel_kb())


@genre_router.message(Content_add.genre_search)
async def genre_search(msg: types.Message, state: FSMContext, bot: Bot):
    genre_name = msg.text.title()
    genres = Genre.select().where(Genre.name.contains(genre_name))
    contex_data = await state.get_data()
    msg_id = contex_data.get('msg_id')
    await msg.delete()
    await state.clear()
    if genres.count() > 0:
        text = f'Вот, что удалось найти в базе библиотеки:'
        await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text,
                                    reply_markup=genres_list_kb(genres))
    else:
        text = f'Не удалось найти подходящего жанра.'
        await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text, reply_markup=genre_cancel_kb())


@genre_router.callback_query(GenreCallbackFactory.filter(F.action == "open"))
async def callbacks_genre_open(callback: types.CallbackQuery, callback_data: GenreCallbackFactory,
                               state: FSMContext):
    genre_id = callback_data.id
    genre = Genre.get(id=genre_id)
    text = genre.name
    await callback.message.edit_text(text=text, reply_markup=current_genre_kb(genre))


@genre_router.callback_query(GenreCallbackFactory.filter(F.action == "edit"))
async def callbacks_genre_edit1(callback: types.CallbackQuery, callback_data: GenreCallbackFactory,
                                state: FSMContext):
    genre_id = callback_data.id
    await state.set_state(Content_add.genre_edit)
    await state.update_data(msg_id=callback.message.message_id)
    await state.update_data(genre_id=genre_id)
    text = 'Введите новое название жанра'
    await callback.message.edit_text(text=text, reply_markup=genre_cancel_kb())


@genre_router.message(Content_add.genre_edit)
async def genre_edit2(msg: types.Message, state: FSMContext, bot: Bot):
    new_genre_name = msg.text.title()
    contex_data = await state.get_data()
    msg_id = contex_data.get('msg_id')
    genre_id = contex_data.get('genre_id')
    genre = Genre.get(id=genre_id)
    genre.name = new_genre_name
    genre.save()
    await msg.delete()
    await state.clear()
    text = f'Имя жанра изменено на {new_genre_name}.'
    await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text, reply_markup=main_genres_kb())


@genre_router.callback_query(GenreCallbackFactory.filter(F.action == "delete"))
async def callbacks_genre_delete(callback: types.CallbackQuery, callback_data: GenreCallbackFactory,
                                 state: FSMContext):
    genre_id = callback_data.id
    text = callback.message.text + '\nУверены, что хотите удалить жанр?'
    await callback.message.edit_text(text=text, reply_markup=genre_delete_confirm(genre_id))


@genre_router.callback_query(GenreCallbackFactory.filter(F.action == "delete_confirmed"))
async def callbacks_genre_delete(callback: types.CallbackQuery, callback_data: GenreCallbackFactory,
                                 state: FSMContext):
    genre_id = callback_data.id
    genre = Genre.get(id=genre_id)
    genre_name = genre.name
    genre.delete_instance()
    text = f'Жанр {genre_name} удалён.'
    await callback.message.edit_text(text=text, reply_markup=main_genres_kb())
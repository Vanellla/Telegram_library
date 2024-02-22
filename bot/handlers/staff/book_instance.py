import os

from aiogram import types, F, Router, Bot
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from aiogram.types import FSInputFile
from openpyxl import Workbook

from bot.dop_func import clean_tmp_files
from aiogram.fsm.context import FSMContext

from bot.keyboards.staff.book_instance_keyboards import main_book_instance_kb
from db import Parallel, Klass, Genre, Author, Book_info, Book
from settings import tmp_files

books_instance_router = Router()


@books_instance_router.callback_query(F.data == 'book_instance')
async def book_instance_main(clb: types.CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await state.clear()
    reply_text = 'Выберите действие:'
    await bot.edit_message_text(chat_id=clb.message.chat.id, message_id=clb.message.message_id, text=reply_text,
                                reply_markup=main_book_instance_kb())
#
#
# @books_main_router.callback_query(BookCallbackFactory.filter(F.action == "add_book"))
# async def callbacks_book_add1_fab(callback: types.CallbackQuery, callback_data: BookCallbackFactory,
#                                   state: FSMContext):
#     parallels = Parallel.select()
#     text = 'Выберите параллель:'
#     await callback.message.edit_text(text=text,
#                                      reply_markup=parallel_choice_kb(parallels, action='choice1_for_new_book'))
#
#
# @books_main_router.callback_query(BookCallbackFactory.filter(F.action == "choice1_for_new_book"))
# async def callbacks_book_add2_fab(callback: types.CallbackQuery, callback_data: BookCallbackFactory,
#                                   state: FSMContext):
#     parallel_id = callback_data.id
#     await state.set_state(Content_add.book_add)
#     await state.update_data(parallel_id=parallel_id)
#     genres = Genre.select()
#     text = 'Выберите жанр:'
#     await callback.message.edit_text(text=text,
#                                      reply_markup=genre_choice_kb(genres, action='choice2_for_new_book'))
#
#
# @books_main_router.callback_query(BookCallbackFactory.filter(F.action == "choice2_for_new_book"), Content_add.book_add)
# async def callbacks_book_add3_fab(callback: types.CallbackQuery, callback_data: BookCallbackFactory,
#                                   state: FSMContext):
#     genre_id = callback_data.id
#     await state.set_state(Content_add.book_add2)
#     await state.update_data(genre_id=genre_id)
#     await state.update_data(msg_id=callback.message.message_id)
#     # authors = Author.select()
#     text = 'Напишите фамилию автора:'
#     await callback.message.edit_text(text=text,
#                                      reply_markup=book_cancel_kb())
#
#
# @books_main_router.message(Content_add.book_add2)
# async def book_add4(msg: types.Message, state: FSMContext, bot: Bot):
#     author_name = msg.text.title()
#     authors = Author.select().where(Author.fio.contains(author_name))
#     contex_data = await state.get_data()
#     msg_id = contex_data.get('msg_id')
#     await msg.delete()
#     if authors.count() > 15:
#         text = f'По запросу "{author_name}" найдено слишком много записей.\n Введите более точный запрос еще раз или нажмите кнопку отмены.'
#         await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text, reply_markup=book_cancel_kb())
#     elif authors.count() > 0:
#         text = 'Вот что удалось найти:'
#         await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text,
#                                     reply_markup=author_choice_kb(authors, action='choice3_for_new_book'))
#     else:
#         text = f'По запросу "{author_name}" ничего не найдено.\n Введите запрос еще раз или нажмите кнопку отмены.:'
#         await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text,
#                                     reply_markup=book_cancel_kb())
#
#
# @books_main_router.callback_query(BookCallbackFactory.filter(F.action == "choice3_for_new_book"))
# async def callbacks_book_add5_fab(callback: types.CallbackQuery, callback_data: BookCallbackFactory,
#                                   state: FSMContext):
#     author_id = callback_data.id
#     await state.set_state(Content_add.book_add3)
#     await state.update_data(author_id=author_id)
#     await state.update_data(msg_id=callback.message.message_id)
#     text = 'Напишите название книги:'
#     await callback.message.edit_text(text=text,
#                                      reply_markup=book_cancel_kb())
#
#
# @books_main_router.message(Content_add.book_add3)
# async def book_add6(msg: types.Message, state: FSMContext, bot: Bot):
#     book_name = msg.text.title()
#     contex_data = await state.get_data()
#     msg_id = contex_data.get('msg_id')
#     author_id = contex_data.get('author_id')
#     genre_id = contex_data.get('genre_id')
#     parallel_id = contex_data.get('parallel_id')
#     author = Author.get(id=author_id)
#     genre = Genre.get(id=genre_id)
#     parallel = Parallel.get(id=parallel_id)
#     await msg.delete()
#     await state.clear()
#     book = Book_info.create(author=author, genre=genre, name=book_name, parallel=parallel)
#     text = f'Книга успешно добавлена.'
#     text += f'\nНазвание: {book.name}'
#     text += f'\nАвтор: {book.author.fio}'
#     text += f'\nЖанр: {book.genre.name}'
#     text += f'\nПараллель: {book.parallel.name}'
#     await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text, reply_markup=book_back_to_main_kb())
#
#
# @books_main_router.callback_query(BookSettingsCallbackFactory.filter(F.action == "search_book"))
# async def callbacks_book_search_main_fab(callback: types.CallbackQuery, callback_data: BookCallbackFactory,
#                                          state: FSMContext):
#     await state.set_state(Content_add.book_search)
#     limit = 1
#     if callback_data.id != None:
#         if callback_data.config == 'genre':
#             await state.update_data(genre_id=callback_data.id)
#             limit -= 1
#         elif callback_data.config == 'genre_clear':
#             await state.update_data(genre_id=None)
#             limit -= 1
#         elif callback_data.config == 'parallel':
#             await state.update_data(parallel_id=callback_data.id)
#             limit -= 1
#         elif callback_data.config == 'parallel_clear':
#             await state.update_data(parallel_id=None)
#             limit -= 1
#         elif callback_data.config == 'author':
#             await state.update_data(author_id=callback_data.id)
#             limit -= 1
#         elif callback_data.config == 'author_clear':
#             await state.update_data(author_id=None)
#             limit -= 1
#         elif callback_data.config == 'book_name_clear':
#             await state.update_data(book_name=None)
#             limit -= 1
#     contex_data = await state.get_data()
#     book_name = contex_data.get('book_name')
#     author_id = contex_data.get('author_id')
#     genre_id = contex_data.get('genre_id')
#     parallel_id = contex_data.get('parallel_id')
#     author = Author.get(id=author_id) if author_id != None else author_id
#     genre = Genre.get(id=genre_id) if genre_id != None else genre_id
#     parallel = Parallel.get(id=parallel_id) if parallel_id != None else parallel_id
#     text = f'Название: {"не указана" if book_name == None else f"{book_name}✅"}'
#     text += f'\nАвтор: {"не указан" if author == None else f"{author.fio}✅"}'
#     text += f'\nЖанр: {"не указан" if genre == None else f"{genre.name}✅"}'
#     text += f'\nПараллель: {"не указана" if parallel == None else f"{parallel.name}✅"}'
#     text += '\nНастройте параметры поиска:'
#     if callback_data.config == 'genre' and limit == 1:
#         genres = Genre.select()
#         await callback.message.edit_text(text=text, reply_markup=genre_config_kb(genres, action='search_book'))
#     elif callback_data.config == 'parallel' and limit == 1:
#         parallels = Parallel.select()
#         await callback.message.edit_text(text=text, reply_markup=parallel_config_kb(parallels, action='search_book'))
#     else:
#         await callback.message.edit_text(text=text, reply_markup=book_search_settings_kb())
#
#
# @books_main_router.callback_query(BookSettingsCallbackFactory.filter(F.action == "search_book_message"))
# async def callbacks_book_search_author_or_bookname_fab(callback: types.CallbackQuery,
#                                                        callback_data: BookCallbackFactory,
#                                                        state: FSMContext):
#     # limit = 1
#     if callback_data.config == 'book_name':
#         await state.set_state(Content_add.book_search_await_book_name)
#         await state.update_data(msg_id=callback.message.message_id)
#         text = 'Пришлите название книги'
#         await callback.message.edit_text(text=text, reply_markup=back_to_search_settings(config='book_name_clear'))
#     elif callback_data.config == 'author':
#         await state.set_state(Content_add.book_search_await_author)
#         await state.update_data(msg_id=callback.message.message_id)
#         text = 'Пришлите фамилию автора'
#         await callback.message.edit_text(text=text, reply_markup=back_to_search_settings(config='author_clear'))
#
#
# @books_main_router.message(Content_add.book_search_await_book_name)
# async def book_search_bookname(msg: types.Message, state: FSMContext, bot: Bot):
#     book_name = msg.text.title()
#     await msg.delete()
#     await state.set_state(Content_add.book_search)
#     await state.update_data(book_name=book_name)
#     contex_data = await state.get_data()
#     msg_id = contex_data.get('msg_id')
#     book_name = contex_data.get('book_name')
#     author_id = contex_data.get('author_id')
#     genre_id = contex_data.get('genre_id')
#     parallel_id = contex_data.get('parallel_id')
#     author = Author.get(id=author_id) if author_id != None else author_id
#     genre = Genre.get(id=genre_id) if genre_id != None else genre_id
#     parallel = Parallel.get(id=parallel_id) if parallel_id != None else parallel_id
#     text = f'Название: {"не указана" if book_name == None else f"{book_name}✅"}'
#     text += f'\nАвтор: {"не указан" if author == None else f"{author.fio}✅"}'
#     text += f'\nЖанр: {"не указан" if genre == None else f"{genre.name}✅"}'
#     text += f'\nПараллель: {"не указана" if parallel == None else f"{parallel.name}✅"}'
#     text += '\nНастройте параметры поиска:'
#     await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text,
#                                 reply_markup=book_search_settings_kb())
#
#
# # @books_main_router.message(Content_add.book_search_await_book_name)
# # async def book_search_bookname(msg: types.Message, state: FSMContext, bot: Bot):
# #     book_name = msg.text.title()
# #     await msg.delete()
# #     await state.set_state(Content_add.book_search)
# #     await state.update_data(book_name=book_name)
# #     contex_data = await state.get_data()
# #     msg_id = contex_data.get('msg_id')
# #     book_name = contex_data.get('book_name')
# #     author_id = contex_data.get('author_id')
# #     genre_id = contex_data.get('genre_id')
# #     parallel_id = contex_data.get('parallel_id')
# #     author = Author.get(id=author_id) if author_id != None else author_id
# #     genre = Genre.get(id=genre_id) if genre_id != None else genre_id
# #     parallel = Parallel.get(id=parallel_id) if parallel_id != None else parallel_id
# #     text = f'Название: {"не указана" if book_name == None else f"{book_name}✅"}'
# #     text += f'\nАвтор: {"не указан" if author == None else f"{author.fio}✅"}'
# #     text += f'\nЖанр: {"не указан" if genre == None else f"{genre.name}✅"}'
# #     text += f'\nПараллель: {"не указана" if parallel == None else f"{parallel.name}✅"}'
# #     text += '\nНастройте параметры поиска:'
# #     await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text,
# #                                 reply_markup=book_search_settings_kb())
#
#
# @books_main_router.message(Content_add.book_search_await_author)
# async def book_search_author(msg: types.Message, state: FSMContext, bot: Bot):
#     author_fio = msg.text.title()
#     await msg.delete()
#     contex_data = await state.get_data()
#     msg_id = contex_data.get('msg_id')
#     authors = Author.select().where(Author.fio.contains(author_fio))
#     if authors.count() > 15:
#         text = 'Результат запроса очень большой. Напишите более точный запрос.'
#         await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text,
#                                     reply_markup=back_to_search_settings())
#     elif authors.count() == 0:
#         text = 'По запросу ничего не найдено. Попробуйте уточнить запрос.'
#         await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text,
#                                     reply_markup=back_to_search_settings(config='author_clear'))
#     else:
#         await state.set_state(Content_add.book_search)
#         text = 'Вот что удалось найти по запросу:'
#         await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text,
#                                     reply_markup=author_config_kb(authors, action='search_book', config='author'))
#
# @books_main_router.callback_query(BookSearchCallbackFactory.filter(F.action == 'book_info_open'))
# async def callbacks_book_search_result_fab(callback: types.CallbackQuery, callback_data: BookCallbackFactory,
#                                            state: FSMContext):
#     book_id = callback_data.id
#     book = Book_info.get(id=book_id)
#     text = f'Информация о книге:'
#     text += f'\nНазвание: {book.name}'
#     text += f'\nАвтор: {book.author.fio}'
#     text += f'\nЖанр: {book.genre.name}'
#     text += f'\nПараллель: {book.parallel.name}'
#     await callback.message.edit_text(text=text, reply_markup=back_to_search_settings_from_book_info())
#
#
# @books_main_router.callback_query(BookSearchCallbackFactory.filter())
# async def callbacks_book_search_result_fab(callback: types.CallbackQuery, callback_data: BookCallbackFactory,
#                                            state: FSMContext):
#     await state.set_state(Content_add.book_search_result)
#     page = callback_data.page
#     contex_data = await state.get_data()
#     book_name = contex_data.get('book_name')
#     author_id = contex_data.get('author_id')
#     genre_id = contex_data.get('genre_id')
#     parallel_id = contex_data.get('parallel_id')
#     author = Author.get(id=author_id) if author_id != None else author_id
#     genre = Genre.get(id=genre_id) if genre_id != None else genre_id
#     parallel = Parallel.get(id=parallel_id) if parallel_id != None else parallel_id
#     text = f'Название: {"не указана" if book_name == None else f"{book_name}✅"}'
#     text += f'\nАвтор: {"не указан" if author == None else f"{author.fio}✅"}'
#     text += f'\nЖанр: {"не указан" if genre == None else f"{genre.name}✅"}'
#     text += f'\nПараллель: {"не указана" if parallel == None else f"{parallel.name}✅"}'
#     books = Book_info.select()
#     # print(list(books))
#     books = [book for book in books if book.author == author] if author else books
#     # print(list(books))
#     books = [book for book in books if book_name in book.name] if book_name else books
#     # print(list(books))
#     books = [book for book in books if book.genre == genre] if genre else books
#     # print(list(books))
#     books = [book for book in books if book.parallel == parallel] if parallel else books
#     # print(list(books))
#     if len(books) == 0:
#         text += '\nПо запросу ничего не найдено. Попробуйте изменить настройки поиска:'
#         await callback.message.edit_text(text=text, reply_markup=book_search_settings_kb())
#     else:
#         text += '\nВот что удалось найти по запросу:'
#         await callback.message.edit_text(text=text, reply_markup=book_search_result_kb(books, page))
#
#
#

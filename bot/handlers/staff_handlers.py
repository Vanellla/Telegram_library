# from aiogram.fsm.context import FSMContext
# from bot.states.staff_states import Content_add
# from db import Author
#
# # from main import Bot
#
# router = Router()
#
#
# @router.message(Command("start"), F.from_user.id.in_([646951760]))
# async def cmd_start(msg: types.Message) -> None:
#     reply_text = 'Привет, сотрудник?\n'
#     reply_text += f'Что делаем?'
#
#     await msg.answer(
#         text=reply_text,
#         reply_markup=get_main_kb()
#     )
#
#
# @router.callback_query(F.data == 'back_to_main_menu')
# async def cmd_start(clb: types.CallbackQuery,state: FSMContext, bot: Bot) -> None:
#     await state.clear()
#     reply_text = 'Привет, сотрудник?\n'
#     reply_text += f'Что делаем?'
#     await bot.edit_message_text(chat_id=clb.message.chat.id, message_id=clb.message.message_id, text=reply_text,
#                                 reply_markup=get_main_kb())
#
#
# @router.callback_query(F.data == 'author_add')
# async def get_id(clb: types.CallbackQuery, state: FSMContext, bot: Bot) -> None:
#     await state.set_state(Content_add.author_add)
#     await state.update_data(msg_id=clb.message.message_id)
#     text = f'Напишите Фамилию Имя Отчество автора (полностью)'
#     await bot.edit_message_text(chat_id=clb.message.chat.id, message_id=clb.message.message_id, text=text, reply_markup=cancel_kb())
#
#
# @router.message(Content_add.author_add)
# async def author_add(msg: types.Message, state: FSMContext, bot: Bot):
#     author_name = msg.text
#     author = Author.create(fio=author_name)
#     contex_data = await state.get_data()
#     msg_id = contex_data.get('msg_id')
#     # await bot.delete_message(chat_id=msg.chat.id, message_id=msg_id)
#     await msg.delete()
#     await state.clear()
#     text = f'Создан автор №{author.id}'
#     await bot.edit_message_text(chat_id=msg.chat.id, message_id=msg_id, text=text, reply_markup=get_main_kb())
#
#
# @router.callback_query(F.data == 'author_list')
# async def author_list(clb: types.CallbackQuery, state: FSMContext, bot: Bot) -> None:
#     await state.clear()
#     text = ''
#     for author in Author.select():
#         text += f'{author.id}) {author.fio}\n'
#     await bot.edit_message_text(chat_id=clb.message.chat.id, message_id=clb.message.message_id, text=text,
#                                 reply_markup=back_to_main_menu())


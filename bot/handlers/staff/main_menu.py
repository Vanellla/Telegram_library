from aiogram import types, F, Router, Bot
from aiogram.filters import Command
from bot.keyboards.staff.staff_keyboards import get_main_kb
from aiogram.fsm.context import FSMContext

from db import Staff
from settings import admins


staff_main_router = Router()


@staff_main_router.message(Command("start"), F.from_user.id.in_(admins))
async def cmd_start(msg: types.Message) -> None:
    reply_text = 'Привет, сотрудник?\n'
    reply_text += f'Что делаем?'
    if Staff.select().where(Staff.tg_id==msg.chat.id).count() == 0:
        Staff.create(fio=msg.from_user.username, tg_id=msg.chat.id)
    await msg.answer(
        text=reply_text,
        reply_markup=get_main_kb()
    )


@staff_main_router.callback_query(F.data == 'back_to_main_menu')
async def cmd_start(clb: types.CallbackQuery,state: FSMContext, bot: Bot) -> None:
    await state.clear()
    reply_text = 'Привет, сотрудник?\n'
    reply_text += f'Что делаем?'
    await bot.edit_message_text(chat_id=clb.message.chat.id, message_id=clb.message.message_id, text=reply_text,
                                reply_markup=get_main_kb())
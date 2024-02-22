from aiogram import types, F, Router, Bot
from typing import Optional
from aiogram.filters.callback_data import CallbackData

from bot.keyboards.staff import main_parallel_kb
from aiogram.fsm.context import FSMContext

from bot.states.staff_states import Content_add
from db import Parallel

parallel_router = Router()


@parallel_router.callback_query(F.data == 'parallels')
async def parallels_main(clb: types.CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await state.clear()
    reply_text = 'Выберите действие:'
    parallels = Parallel.select()
    await bot.edit_message_text(chat_id=clb.message.chat.id, message_id=clb.message.message_id, text=reply_text,
                                reply_markup=main_parallel_kb(parallels))


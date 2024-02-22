from aiogram import types, F, Router, Bot
from bot.keyboards.staff import main_references_kb
from aiogram.fsm.context import FSMContext

staff_main_references_router = Router()


@staff_main_references_router.callback_query(F.data == 'references')
async def cmd_start(clb: types.CallbackQuery, state: FSMContext, bot: Bot) -> None:
    await state.clear()
    reply_text = 'Выберите справочник:'
    await bot.edit_message_text(chat_id=clb.message.chat.id, message_id=clb.message.message_id, text=reply_text,
                                reply_markup=main_references_kb())

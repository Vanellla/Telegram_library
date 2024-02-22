from aiogram import types, F, Router
from aiogram.filters import Command
from bot.keyboards.user_keyboards import get_main_kb
from pprint import pprint


router = Router()


@router.message(Command("start"))
async def cmd_start(msg: types.Message) -> None:
    reply_text = 'Привет, как твои дела?\n'
    reply_text += f'Твое имя - {msg.from_user.first_name}!'

    await msg.answer(
        text=reply_text,
        reply_markup=get_main_kb()
    )


@router.callback_query(F.data == 'get_my_id')
async def get_id(clb: types.CallbackQuery) -> None:
    await clb.message.answer(text=f'Твой id {clb.from_user.id}')

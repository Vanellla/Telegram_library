import asyncio
import os
# import logging


from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import handlers_router
from bot.keyboards.staff import get_main_kb

from settings import admins
from db import db_init


async def on_startup(bot: Bot):
    db_init()
    for admin in admins:
        await bot.send_message(chat_id=admin, text='Бот запущен', reply_markup=get_main_kb())


async def main() -> None:
    """Entry point
    """
    
    token = ""
    bot = Bot(token)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(handlers_router)
    dp.startup.register(on_startup)


    try:
        await dp.start_polling(bot)
    except Exception as _ex:
        print(f'There is an exception - {_ex}')


if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from app import router
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
#переменные окружения
TOKEN = os.getenv('TOKEN')


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()  # Закрытие сессии бота

if __name__ == "__main__":
    asyncio.run(main())

# import asyncio
# import logging
#
# from aiogram import Bot, Dispatcher
# from aiogram.fsm.storage.memory import MemoryStorage
#
# import config
# from app import router
#
#
# async def main():
#     bot = Bot(token=config.TOKEN)
#     dp = Dispatcher(storage=MemoryStorage())
#     dp.include_router(router)
#
#     await bot.delete_webhook(drop_pending_updates=True)
#     await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
#
# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     asyncio.run(main())
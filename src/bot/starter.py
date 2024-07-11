import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher

from bot import config
from bot.routers import router as main_router
from db.models import async_main as run_db

bot = Bot(token=config.BOT_TOKEN)


async def main():
    await run_db()
    dp = Dispatcher()
    dp.include_router(main_router)

    logging.basicConfig(level=logging.INFO)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

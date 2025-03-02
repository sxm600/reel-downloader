import asyncio
import logging

from aiogram import Bot, Dispatcher
from src.config import TOKEN
from src.routes import router
from src.scraper import Scraper


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TOKEN)

    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    dispatcher["scraper"] = await Scraper().start()

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

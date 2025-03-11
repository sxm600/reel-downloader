import asyncio
import logging

from aiogram import Bot, Dispatcher
from src.config import TOKEN
from src.routes import router
from src.async_scraper import AsyncScraper


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TOKEN)

    dispatcher = Dispatcher()
    dispatcher.include_router(router)
    dispatcher["scraper"] = await AsyncScraper().start()

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

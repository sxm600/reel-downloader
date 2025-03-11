import logging

from aiogram.types import Message, ErrorEvent
from aiogram import Router, F
from src.async_scraper import AsyncScraper


router = Router()


@router.message(F.text.startswith("https://www.instagram.com/reel"))
async def reel(message: Message, scraper: AsyncScraper):
    source = await scraper.reel_source_url(message.text)
    logging.info(f"@{message.from_user.username} - {source}")
    await message.reply_video(source)


@router.error(F.update.message.as_("message"))
async def error(event: ErrorEvent, message: Message):
    logging.critical(event.exception, exc_info=True)
    await message.reply("Oops, something went wrong! Check if provided link is correct.")


@router.message(F.text)
async def default(message: Message):
    logging.info(f"@{message.from_user.username} - {message.text}")
    await message.reply("Only instagram reel links allowed.")

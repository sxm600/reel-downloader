import logging

from aiogram.types import Message, ErrorEvent
from aiogram import Router, F
from src.scraper import Scraper


router = Router()


@router.message(F.text.startswith("https://www.instagram.com/reel"))
async def reel(message: Message, scraper: Scraper):
    source = await scraper.reel_source_url(message.text)
    logging.info(f"@{message.from_user.username} - {source}")
    await message.answer_video(source)


@router.error(F.update.message.as_("message"))
async def error(event: ErrorEvent, message: Message):
    logging.critical(event.exception, exc_info=True)
    await message.answer("Oops, something went wrong!")


@router.message(F.text)
async def default(message: Message):
    logging.info(f"@{message.from_user.username} - {message.text}")
    await message.answer("Only instagram reel links allowed")
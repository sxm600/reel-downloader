import asyncio

from typing import Self
from playwright.async_api import async_playwright


class Scraper:
    def __init__(self):
        self.context = None


    async def start(self, headless: bool = True) -> Self:
        playwright = await async_playwright().start()
        browser = await playwright.chromium.launch(headless=headless)
        self.context = await browser.new_context()

        # warmup context
        page = await self.context.new_page()
        await page.goto("https://www.instagram.com/")
        await page.get_by_text("Decline optional cookies").click()
        await page.close()

        await asyncio.sleep(3)  # 3 just works to store cookies to context idk

        return self


    async def reel_source_url(self, url: str) -> str:
        page = await self.context.new_page()
        url = url.replace("/reels/", "/reel/")

        try:
            await page.goto(url)
            await page.get_by_role("button", name="Close").click()  # skip login

            async with page.expect_response("**/o1/v/t16/f2/**") as response:
                response = await response.value

            return response.url
        finally:
            await page.close()
import asyncio

from typing import Self
from playwright.async_api import async_playwright


class AsyncScraper:
    async def start(self, headless: bool = True) -> Self:
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.context = await self.browser.new_context()

        self.context.set_default_timeout(5000)

        # warmup context
        async with await self.context.new_page() as page:
            await page.goto("https://www.instagram.com/")
            await page.get_by_text("Decline optional cookies").click()
            await asyncio.sleep(3)  # 3 just works to store cookies to context idk

        return self

    async def reel_source_url(self, url: str) -> str:
        assert self.context, 'self.context is not instantiated, maybe you forgot self.start()'

        url = url.replace("/reels/", "/reel/")

        async with await self.context.new_page() as page:
            await page.goto(url)
            await page.get_by_role("button", name="Close").click()  # skip login

            async with page.expect_response("**/o1/v/t16/f2/**") as response:
                response = await response.value

            return response.url

import asyncio
from playwright.async_api import async_playwright

async def test():
    print("Starting Playwright test...")
    p = await async_playwright().start()
    print("Playwright started")
    b = await p.chromium.launch(headless=False)
    print("Browser launched")
    page = await b.new_page()
    print("Page created")
    await page.goto("https://www.google.com")
    print("Navigated to Google")
    await b.close()
    await p.stop()
    print("Test completed successfully")

if __name__ == "__main__":
    asyncio.run(test())

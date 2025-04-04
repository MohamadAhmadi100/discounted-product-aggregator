from playwright.async_api import async_playwright
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


async def scrape_zara() -> List[Dict]:
    logger.info("zara scrape")
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox']
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()

        try:
            await page.goto("https://www.zara.com/us/en/sale-man-l1310.html", timeout=2000)
            await page.wait_for_selector('.product-grid-product', timeout=2000)

        except Exception as e:
            logger.error(f"zara failed: {e}")
        finally:
            await context.close()
            await browser.close()

    return results

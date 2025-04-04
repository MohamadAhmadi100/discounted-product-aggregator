from playwright.async_api import async_playwright
import logging
import re
from typing import List, Dict
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


async def scrape_amazon() -> List[Dict]:
    logger.info("amazon scrape")
    results = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        try:
            await page.goto("https://www.amazon.com/s?i=fashion-mens&rh=n%3A7141123011&s=price-desc-rank&pd_rd_r=...",
                            timeout=60000)
            await page.wait_for_selector('.s-result-item')

            products = await page.query_selector_all('.s-result-item')

            for product in products:
                try:
                    name = await product.query_selector('h2')
                    name = await name.inner_text() if name else "No name"

                    price = await product.query_selector('.a-price .a-offscreen')
                    price = await price.inner_text() if price else None

                    original_price = await product.query_selector('.a-text-price .a-offscreen')
                    original_price = await original_price.inner_text() if original_price else price

                    if not original_price or not price:
                        continue

                    price_num = float(re.sub(r'[^\d.]', '', price))
                    original_num = float(re.sub(r'[^\d.]', '', original_price))
                    discount = ((original_num - price_num) / original_num) * 100

                    link = await product.query_selector('h2 a')
                    link = urljoin("https://www.amazon.com", await link.get_attribute('href')) if link else ""

                    image = await product.query_selector('img.s-image')
                    image = await image.get_attribute('src') if image else ""

                    results.append({
                        "name": name.strip(),
                        "original_price": f"${original_num:.2f}",
                        "discounted_price": f"${price_num:.2f}",
                        "discount_percent": round(discount, 2),
                        "purchase_url": link,
                        "image_url": image,
                        "store": "amazon",
                        "category": "clothing"
                    })
                except Exception as e:
                    logger.error(f"amazon product errror: {e}")
                    continue

        except Exception as e:
            logger.error(f"amazon fail: {e}")
        finally:
            await browser.close()

    return results

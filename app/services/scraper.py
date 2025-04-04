from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.product import Product
from app.utils.zara_scraper import scrape_zara
from app.utils.amazon_scraper import scrape_amazon
import logging
from datetime import datetime, timedelta
import asyncio

logger = logging.getLogger(__name__)


class ScraperService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def refresh_data(self):
        logger.info("refreshing")
        try:
            await self.db.execute(
                delete(Product).where(
                    Product.created_at < datetime.utcnow() - timedelta(minutes=10)
                )
            )

            zara, amazon = await asyncio.gather(
                scrape_zara(),
                scrape_amazon(),
                return_exceptions=True
            )
            print(zara)
            print(amazon)
            products = []
            if not isinstance(zara, Exception):
                products.extend(zara)
            else:
                logger.error(f"zara error: {zara}")

            if not isinstance(amazon, Exception):
                products.extend(amazon)
            else:
                logger.error(f"amazon error: {amazon}")
            print(products)
            if products:
                self.db.add_all([Product(**p) for p in products])
                await self.db.commit()
                logger.info(f"{len(products)} products")

        except Exception as e:
            await self.db.rollback()
            logger.error(f"error: {e}")
            raise
        finally:
            await self.db.close()

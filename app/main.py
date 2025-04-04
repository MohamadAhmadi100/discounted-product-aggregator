from fastapi import FastAPI
from app.routers import products
from app.database import engine, Base, async_session_maker
from app.services.scraper import ScraperService
from contextlib import asynccontextmanager
import asyncio
import logging

logging.basicConfig(level=logging.INFO)


async def continuous_scraping():
    while True:
        try:
            async with async_session_maker() as session:
                scraper_service = ScraperService(session)
                await scraper_service.refresh_data()
        except Exception as e:
            logging.error(f"scraping failed: {e}")
        await asyncio.sleep(1000)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    asyncio.create_task(continuous_scraping())
    yield


app = FastAPI(
    title="Discounted Product Aggregator",
    version="0.1.1",
    lifespan=lifespan
)

app.include_router(products.router, prefix="/api/v1")

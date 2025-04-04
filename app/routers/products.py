from fastapi import APIRouter, Query
from typing import List, Optional
from app.schemas.product import Product
from app.services.scraper import ScraperService
from app.database import get_db

router = APIRouter()


@router.get("/discounted-products", response_model=List[Product])
async def get_discounted_products(
        store: Optional[str] = Query(None, description="store (zara, amazon)"),
        category: Optional[str] = Query(None, description="category"),
        min_discount: Optional[float] = Query(None, description="min discount percentage")
):
    async with get_db() as db:
        scraper_service = ScraperService(db)
        return await scraper_service.get_products(store, category, min_discount)

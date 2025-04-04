from fastapi import APIRouter, Depends, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.product import Product
from app.services.scraper import ScraperService
from app.database import get_db

router = APIRouter()

@router.get("/discounted-products", response_model=List[Product])
async def get_discounted_products(
    store: Optional[str] = Query(None, description="Filter by store (zara, amazon)"),
    category: Optional[str] = Query(None, description="Filter by category"),
    min_discount: Optional[float] = Query(None, description="Minimum discount percentage"),
    db: AsyncSession = Depends(get_db)
):
    scraper_service = ScraperService(db)
    return await scraper_service.get_products(store, category, min_discount)
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    original_price: str
    discounted_price: str
    discount_percent: float
    purchase_url: str
    image_url: Optional[str]
    store: str
    category: str


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

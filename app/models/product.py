from sqlalchemy import Column, String, Float, DateTime, Integer
from datetime import datetime
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    original_price = Column(String)
    discounted_price = Column(String)
    discount_percent = Column(Float)
    purchase_url = Column(String)
    image_url = Column(String)
    store = Column(String)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

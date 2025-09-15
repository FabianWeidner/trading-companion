from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.db.base import Base


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    side = Column(String, index=True)
    strategy = Column(String, index=True)
    qty = Column(Float)
    price = Column(Float)
    screenshot_url = Column(String, nullable=True)
    opened_at = Column(DateTime, default=datetime.utcnow)

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    side = Column(String)
    strategy = Column(String)
    qty = Column(Float)
    price = Column(Float)
    opened_at = Column(DateTime(timezone=True), server_default=func.now())
    screenshot_url = Column(String, nullable=True)
    closed_at = Column(DateTime(timezone=True), nullable=True)
    exit_price = Column(Float, nullable=True)
    exit_reason = Column(String, nullable=True)

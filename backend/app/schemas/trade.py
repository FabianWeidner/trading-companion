from datetime import datetime
from pydantic import BaseModel


class TradeBase(BaseModel):
    symbol: str
    side: str
    strategy: str
    qty: float
    price: float
    screenshot_url: str | None = None


class TradeCreate(TradeBase):
    pass


class TradeRead(TradeBase):
    id: int
    opened_at: datetime

    class Config:
        from_attributes = True  # wichtig für SQLAlchemy -> Pydantic

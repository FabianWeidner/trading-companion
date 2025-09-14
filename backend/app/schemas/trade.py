from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class TradeBase(BaseModel):
    symbol: str
    side: str  # LONG / SHORT
    strategy: str
    qty: float
    price: float
    screenshot_url: Optional[str] = None


class TradeCreate(TradeBase):
    pass


class TradeUpdate(BaseModel):
    symbol: Optional[str] = None
    side: Optional[str] = None
    strategy: Optional[str] = None
    qty: Optional[float] = None
    price: Optional[float] = None
    screenshot_url: Optional[str] = None


class TradeRead(TradeBase):
    id: int
    opened_at: datetime

    # ⚠️ Neu für Pydantic V2
    model_config = ConfigDict(from_attributes=True)

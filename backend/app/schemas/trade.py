from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class TradeSide(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"


class TradeBase(BaseModel):
    symbol: str
    side: TradeSide
    strategy: str
    qty: float = Field(..., gt=0, description="Quantity must be positive")
    price: float = Field(..., gt=0, description="Price must be positive")
    screenshot_url: Optional[str] = None


class TradeCreate(TradeBase):
    pass


class TradeUpdate(BaseModel):
    symbol: Optional[str] = None
    side: Optional[TradeSide] = None
    strategy: Optional[str] = None
    qty: Optional[float] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)
    screenshot_url: Optional[str] = None


class TradeRead(TradeBase):
    id: int
    opened_at: datetime

    class Config:
        from_attributes = True

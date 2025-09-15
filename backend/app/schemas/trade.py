from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TradeBase(BaseModel):
    symbol: str
    side: str  # LONG / SHORT
    strategy: str
    qty: float = Field(..., gt=0, description="Quantity must be greater than 0")
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    screenshot_url: Optional[str] = None


class TradeCreate(TradeBase):
    pass


class TradeUpdate(BaseModel):
    symbol: Optional[str] = None
    side: Optional[str] = None
    strategy: Optional[str] = None
    qty: Optional[float] = Field(None, gt=0)
    price: Optional[float] = Field(None, gt=0)
    screenshot_url: Optional[str] = None


class TradeRead(TradeBase):
    id: int
    opened_at: datetime

    class Config:
        from_attributes = True

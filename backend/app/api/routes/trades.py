from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.trade import Trade
from app.schemas.trade import TradeCreate, TradeRead

router = APIRouter()


@router.post("/trades", response_model=TradeRead)
def create_trade(trade: TradeCreate, db: Session = Depends(get_db)):
    db_trade = Trade(**trade.dict())
    db.add(db_trade)
    db.commit()
    db.refresh(db_trade)
    return db_trade


@router.get("/trades", response_model=list[TradeRead])
def list_trades(db: Session = Depends(get_db)):
    return db.query(Trade).all()

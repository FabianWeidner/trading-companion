from sqlalchemy.orm import Session
from app.models.trade import Trade
from app.schemas.trade import TradeCreate, TradeUpdate


def get_trade(db: Session, trade_id: int) -> Trade | None:
    return db.query(Trade).filter(Trade.id == trade_id).first()


def get_trades(db: Session, skip: int = 0, limit: int = 100) -> list[Trade]:
    return db.query(Trade).offset(skip).limit(limit).all()


def create_trade(db: Session, trade_in: TradeCreate) -> Trade:
    db_obj = Trade(**trade_in.dict())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update_trade(db: Session, db_obj: Trade, trade_in: TradeUpdate) -> Trade:
    update_data = trade_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_obj, field, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_trade(db: Session, db_obj: Trade) -> None:
    db.delete(db_obj)
    db.commit()
